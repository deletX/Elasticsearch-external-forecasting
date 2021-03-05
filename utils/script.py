import logging
import utils.esdatapump as esdatapump
import algorithms.algorithms as alg
from algorithms.autoarima import ARIMA
from algorithms.deepar import DeepAR

logger = logging.getLogger(__name__)

def run_query(query):
    # 1 Take data
    logger.info(f"Retrieving data from index {query['index']}")
    data = esdatapump.run_query(query['query'],query['index'],query['data_path'],query['timestamp_path_in_data'],query['value_path_in_data'])

    # 2 Run algorithm
    algorithm = query['algorithm']
    logger.info(f"Trying to execute algorithm {algorithm}")
    if algorithm == alg.arima or algorithm == alg.sarimax:
        results = ARIMA(data, query['interval'], query['forecast_size'], query['seasonality']>1, query['seasonality'])
    elif algorithm == alg.deepar:
        results = DeepAR(data,query['interval'],query['forecast_size'])
    else:
        logger.error(f"Algorithm {algorithm} is not implemented")
        logger.error(f"Aborting")
        exit(1)
    
    # 3 Push results to es
    logger.info(f"Sending data to index")
    esdatapump.push_data(results,query['index'],query['dest_field'],query['dest_timestamp'])

