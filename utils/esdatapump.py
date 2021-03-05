from elasticsearch.helpers import parallel_bulk
from elasticsearch import Elasticsearch
from datetime import datetime
from dateutil.parser import isoparse
import pandas as pd
import configs.config as cfg
import logging
logger = logging.getLogger(__name__)

def run_query(query,index,data_path,timestamp_path_in_data,value_path_in_data):
    """
        Execute a query using given query. A dictionary that must comply with
        the defition in queries.py
    """
    # Get the data and travel the result dictionary as per in the data_path conf.
    logger.debug(f"Getting data from es index {index}")
    data = get_es_data(query, index=index)
    
    logger.debug(f"Navigating throught to reach data array. path: {data_path}")
    for path_part in data_path:
        data = data[path_part]

    # initialize data array
    values = []

    logger.debug("Extracting data")
    for datum in data:
        # extract timestamp
        timestamp = datum[timestamp_path_in_data[0]]
        for i in range(1,len(timestamp_path_in_data)):
            timestamp = timestamp[timestamp_path_in_data[i]]

        # extract value
        value = datum[value_path_in_data[0]]
        for i in range(1,len(value_path_in_data)):
            value = value[value_path_in_data[i]]
        
        element = {
            "timestamp" : str(isoparse(timestamp))[:-6], # parse datetime string. milliseconds and microseconds are removed
            "value": value
        }

        values.append(element)
    logger.debug(f"Got a total of {len(values)} elements")
    
    # transform data to a pandas data frame
    logger.debug(f"Creating data frame")

    df = pd.DataFrame(data=values)

    # timestamp is set as index
    df = df.set_index('timestamp')

    return df

def get_es_data(query_body, index):
    """
        Run the elasticsearch query. Max result size is bound to elastic cluster configuration.
        Default is 10000.
    """
    # Using elasticsearch helper library for python
    logger.debug("Instantiating elasticsearch helper")
    es = Elasticsearch(cfg.es_host)

    # Running query on index
    logger.debug(f"Running {query_body} on index{index}")
    
    data = es.search(body=query_body, index=index)
    
    logger.debug(f"Got {len(data)} values")

    logger.debug(f"Closing connection")
    es.close()
    return data

def bulk_generator(data,index,dest_field,dest_timestamp):
    """
        This generator is meant to generate elasticsearch events with the data from the forecasting algorithms
    """
    # We prepare the data by transforming the dataframe into a dictionary for each row
    logger.debug("Transforming data frame to dictionary")
    data_dict = data.reset_index().to_dict(orient='records')

    for element in data_dict:

        # tranform the source
        source = {
            dest_timestamp : element['timestamp'].isoformat(),
            f'{dest_field}_lower' : element['0.1'],
            dest_field : element['values'],
            f'{dest_field}_upper' : element['0.9']
        }
        logger.debug(f"Created elasticsearch event: {source}")

        # unique id has been given in case of multiple uploads. This means only a single forecast per index is supported.
        yield {
            "_id" : f"forecast-{index}-{source[dest_timestamp]}"
            "_index":index,
            "_source": source
        }

def push_data(source,index,dest_field,dest_timestamp):
    """
        Use a bulk generator to send data throught the elasticsearch bulk helper
    """
    # Open es connection using python helper
    es = Elasticsearch(cfg.es_host)

    # using helper function that enables multi threading and uses a generator
    for success, info in parallel_bulk(es, bulk_generator(source,index,dest_field,dest_timestamp)):
        if not success:
            logger.warn(f"An event failed to be indexed. Info: {info}")
        else:
            logger.debug(f"Successfully indexed an event in index {index}")

    # closing es connection
    es.close()
