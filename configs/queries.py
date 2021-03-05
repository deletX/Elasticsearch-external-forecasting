# query definitions
# must have the following fields:
# example_query = {
#     'query': <elastic search request body dictionary here>,
#     'index': <elastic search index>,
#     'dest_index' : <elastic destination index>,
#     'interval' : <data interval, ex: 1d, 2d, 1h>,
#     'algorithm' : <algorithm from algorithms>,
#     'data_path': <path to data array in elastic response>,
#     'value_path_in_data' : <value path in element in the data array>,
#     'timestamp_path_in_data' : <timestamp path in element in the data array>,
#     'dest_field' : <destination value field>,
#     'forecast_size' : <size of forecast in interval numbers>,
#     'dest_timestamp' : <destination timestamp>,
#     'seasonality' : <seasonality in interval numbers'. Required for SARIMAX alg>,
#     }
# 
# A simple function has been created to help with the realization
from utils.utils import query_dict_helper
import algorithms.algorithms as alg

# Your queries here. You can use query_dict_helper to declare queries definitions
#
# For example with:
# quantity_query = query_dict_helper(
#     query = <body of query>,
#     index = <index>,
#     algorithm = alg.arima,
#     data_path = ('aggregations','2','buckets',),
#     value_path_in_data = ('3','value',),
#     timestamp_path_in_data = ('key_as_string',),
# )
