# External forecasting for elasticsearch
This is a python program made to execute several univariated time series forcasting.
There are several algorithms available:
- **DeepAR** algorithm using GluonTS toolkit
- **ARIMA** and **SARIMA** using pyramid auto arima

This is ment to be executed periodically with cron jobs.  

Depending on your implementation, in production should be kept on a different machine since computing requirements especially for *DeepAR* are high, and have a direct proportion with data size and forecast size.

## Requirements
This was made with **python 3.7** and **elasticsearch 7.6**.

Python required packages are found in the `requirements.txt` I created with pip freeze.

## Configuration
This program has two configuration files both located in `\configs`:
- `config.py`: that contains main configuration values. In here there are the variables to define
  - **Elasticsearch address**. No support for multiple elasticsearch addresses yet
  - **Queries** to evaluate. This enables you to define multiple queries and test only a subset
  - Gluon toolkit **training epochs**
  - **logging configuration**
- `queries.py`: that contains the various queries and configuration parameters for each query. Each query must be defined throught a dictionary with the configuration parameters. For simplicity an helper function has been provided with some default values. Each query is defined by
  - `query`: the body of the elasticsearch query
  - `index`: the source elasticserch index
  - `dest_index`: the destination index. If `None` in the helper function it will be set to the source index
  - `interval`: time interval between data. Examples: `"1h"`, `"1d"`, `"7d"`. This **must** match the interval of the `query`. *No check has been implemented*. Defaults to `"1d"` in helper function
  - `algorithm`: algorithm to use for the query. Has to be one in `\algorithms\algorithms.py` otherwise a `NotImlpementedError` will be raised. Defaults to `alg.arima` in helper functon
  - `data_path`: tuple that indicates the path to reach the array containing the required elements inside the elasticsearch response. For instance, consider the elastic example below. The data array is `"buckets"` inside `"2"` inside `"aggregations"`. In this example `data_path : ("aggregations","2","buckets",)`
  - `value_path_in_data` same as `data_path` but inside the element inside the data array for the desired data. Looking at the example if we want to forecast on the value `"4"`, `value_path_in_data` will be `value_path_in_data : ("4","value,)`
  - `timestamp_path_in_data` I guess you can figure it out yourself by now. Bear in mind we want the string datetime.
  - `dest_field`: the field inside the elasticsearch document that will be sent with the forecacst. Upper and lower limit will be in the form of: `f"{dest_field}_upper"` and `f"{dest_field}_lower"`. Defaults to `"predValue"` in helper functon
  - `dest_timestamp`: same as `dest_field` but for the timestamp. Defaults to `"@timestamp"` in helper functyion
  - `forecast_size`: the number of `interval` windows to forecast in the future. Defaults to `7` in helper function
  - `seasonality`: required for SARIMAX algorithm to compute seasonality. Must be the seasonality of data in `interval` measure. Defaults to `1` in helper function

### Elastic response example
```
  {
	"took": 7,
	"timed_out": false,
	"_shards": {
		"total": 1,
		"successful": 1,
		"skipped": 0,
		"failed": 0
	},
	"hits": {
		"total": 979446,
		"max_score": null,
		"hits": []
	},
	"aggregations": {
		"2": {
			"buckets": [
				{
					"3": {
						"value": 51954
					},
					"4": {
						"value": 51954
					},
					"5": {
						"value": null
					},
					"key_as_string": "2020-11-18T00:00:00.000+01:00",
					"key": 1605654000000,
					"doc_count": 18291,
					"3-metric": {
						"value": 51954
					}
				},
				{
					"3": {
						"value": 130868
					},
					"4": {
						"value": 78914
					},
					"5": {
						"value": 51954
					},
					"key_as_string": "2020-11-19T00:00:00.000+01:00",
					"key": 1605740400000,
					"doc_count": 19313,
					"3-metric": {
						"value": 78914
					}
				},
                ...
            ]
        }
    }
}
```