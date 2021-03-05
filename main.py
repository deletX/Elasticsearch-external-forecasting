import logging
import logging.config
import numpy as np
import mxnet as mx
import utils.config as cfg
from utils.script import run_query

def setup():
    logging.config.dictConfig(cfg.log_config)
    # Define seed for results reproducibility
    mx.random.seed(0)
    np.random.seed(0)

def main():
    for query in cfg.queries:
        run_query(query)


if __name__ == "__main__":
    setup()
    main()
