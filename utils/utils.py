from algorithms import algorithms as alg
import logging
logger = logging.getLogger(__name__)

def query_dict_helper(query,index,data_path,value_path_in_data,timestamp_path_in_data,interval="1d",dest_index=None,algorithm=alg.arima,forecast_size=7,dest_field="predValue",dest_timestamp="@timestamp",seasonality=1):
    """
        Helper function to create a query dictionary. Comes with some defaults.

        Args:
            query (dict): body of the es query
            index (str):  index to which send the query
            data_path (tuple): path to get to the data array inside the es response
            value_path_in_data (tuple): path to get to the desired value on which perform the forecast operation inside the dictionary inside the data array
            timestamp_path_in_data (tuple) same as value_path_in_data, but for the timestamp
            interval (str): interval of the query. MUST MATCH THE ONE IN THE QUERY. no check done as of now. Defaults to "1d"
            dest_index (str): destination index of the forecast values. If not indicated will be the same as the source index. Defaults to None
            algorithm (str): must be one of those found in algorithms.py. Defaults to arima
            forecast_size (int): Forecast size in interval windows. Defaults to 7
            dest_field (str): field of the elasticsearch event that will contain the predicted value. Defaults to "predValue"
            dest_timestamp (str): field of the elasticsearch event that will contain the predicted timestamp. Defaults to "@timestamp"
            
    """
    if dest_index is None:
        dest_index = index
    query_dict = {
        'query': query,
        'interval' : interval,
        'index' : index,
        'dest_index': dest_index,
        'algorithm': algorithm,
        'data_path' : data_path,
        'value_path_in_data' : value_path_in_data,
        'timestamp_path_in_data' : timestamp_path_in_data,
        'dest_field' : dest_field,
        'forecast_size': 7,
        'dest_timestamp' : dest_timestamp,
        'seasonality': 1
    }
    logger.debug(f"Created a query dictionary: {query_dict}")
    return query_dict