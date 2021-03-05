from gluonts.dataset.common import ListDataset
from gluonts.model.deepar import DeepAREstimator
from gluonts.mx.trainer import Trainer
import pandas as pd
import numpy as np
import mxnet as mx
import logging
from configs.config import gluon_epochs
from datetime import datetime

logger = logging.getLogger(__name__)

def DeepAR(data,interval,forecast_size):
    """
        Execute DeepAR estimator using the gluonTS framework.
        Returns a pandas dataframe with columns: timestamp, value, 0.1, 0.9
    """
    
    logger.info("Executing DeepAR algorithm")

    # Define training data
    logger.debug(f"Defining training ds. start {data.index[0]}, data size {len(data.value)}, interval {interval}")
    training_data = ListDataset([{"start": data.index[0], "target": data.value[:]}], freq = interval)

    # Define estimator with given frequency, prediction length and trainer with config epochs
    logger.debug(f"Defining estimator with prediction length {forecast_size} and {gluon_epochs} epochs")
    estimator = DeepAREstimator(freq = interval, prediction_length = forecast_size, trainer=Trainer(epochs=gluon_epochs))

    # Train the estimator
    logger.debug(f"Training on training data of size {len(training_data)}")
    start = datetime.now()

    predictor = estimator.train(training_data=training_data)

    end = datetime.now()
    logger.debug(f"Training took {end-start}")

    # Run the predictions using helper function (truncates the test dataset and does extra stuff)
    logger.debug(f"Predicting {forecast_size} {interval} samples")
    start = datetime.now()

    forecast = predictor.predict(training_data,num_samples=forecast_size)

    end = datetime.now()
    logger.debug(f"Prediction took {end-start}")

    # Transform forecast iterator to pandas dataframe with columns value, 0.1, 0.9
    from gluonts.model.forecast import Config
    logger.debug("Transforming the results into a dataframe")
    # Since we have only a single time serie we take the first (and only) value from forecast list
    forecast_entry = list(forecast)[0]
    
    # we transform the forecast to a dictionary
    logger.debug("Tranforming the forecast entry to a json dictionary with default configuration")
    forecast_dict = forecast_entry.as_json_dict(Config())

    # The values from the inner dictionary quantiles are brought at the top level
    logger.debug("Moving subdictionary qantiles sub values to top level")
    forecast_dict['0.1'] = forecast_dict['quantiles']['0.1']
    forecast_dict['0.9'] = forecast_dict['quantiles']['0.9']
    del forecast_dict['quantiles']

    # A Dataframe is created with index a data range
    ns, h = forecast_entry.samples.shape
    logger.debug("Creating dataframe and giving the correct name to the index and value column")
    dates = pd.date_range(forecast_entry.start_date, freq=forecast_entry.freq, periods=h)
    df = pd.DataFrame(forecast_dict,index=dates)
    df.index.name = 'timestamp'
    df = df.rename(columns={'mean':'values'})

    return df
    


