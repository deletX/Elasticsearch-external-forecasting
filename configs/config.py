import configs.queries as qry
import os

# Elasticsearch host No support yet for multiple hosts
es_host = "http://localhost:9200"

# Queries on which execute prediction
queries = [] #example [qry.sample_query1, qry.sample_query2]

# DeepAR training epochs
gluon_epochs = 35

# Log configuration
log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'file_handler': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'filename': 'application.log',
                'encoding': 'utf8'
            },
            'stream_handler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file_handler','stream_handler'],
                'level': 'DEBUG',
                'propagate': False
            }
        }
    }

