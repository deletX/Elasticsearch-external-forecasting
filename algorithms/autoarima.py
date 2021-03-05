import logging
import pandas as pd
import pmdarima as pm
from datetime import datetime

logger = logging.getLogger(__name__)


def arima_to_df(forecast,conf,forecast_begin_date,interval):
    """
        Convert forecast and confidence arrays into a dataframe with timestamp, 0.1, 0.9 columns
    """
    # create date index for dataframe
    logger.debug(f"Creating date range for dataframe with first date {forecast_begin_date}, interval {interval}, periods {len(forecast)}")
    dates = pd.date_range(forecast_begin_date, freq=interval, periods=len(forecast), closed='right')

    forecast_dict = {'values':forecast,'0.1':conf[:,0],'0.9':conf[:,1]}

    logger.debug("Creating dataframe and giving the correct name to the index column")
    df = pd.DataFrame(forecast_dict,index=dates)
    df.index.name = 'timestamp'
    return df

# data,query['interval'],query['forecast_size'],query['seasonality']>1,query['seasonality']
def ARIMA(data,interval,forecast_size,seasonal,seasonality):
    """
        Run Auto Arima model from pyramid arima if seasonal a SARIMAX will be trained.
        Execute prediction and return a pandas dataframe
    """
    logger.info("Executing ARIMA algorithm")
    # Define train ds
    train = data.value[:]

    # Train the model
    logger.debug(f"Running pm.auto_arima, seasonality is {seasonal}, m is {seasonality}, data_size is {len(train)}")
    start = datetime.now()

    model = pm.auto_arima(train, start_p=1, start_q=1,
                    test='adf',       # use adftest to find optimal 'd'
                    max_p=10, max_q=10, # maximum p and q
                    m=seasonality,              # frequency of series, non-seasonal. no frequency
                    d=None,           # let model determine 'd'
                    seasonal=seasonal,   # No Seasonality
                    start_P=0, 
                    D=0, 
                    trace=True,
                    error_action='warn',  
                    suppress_warnings=True, 
                    stepwise=True)

    end = datetime.now()
    if seasonal:
        logger.debug(f"Trained an ARIMAX model in {end-start}")
    else:
        logger.debug(f"Trained an SARIMAX model in {end-start}")

    # Compute predictions on the model
    logger.debug(f"Predicting {forecast_size} {interval} windows")
    start = datetime.now()

    forecast, conf = model.predict(n_periods=forecast_size, return_conf_int=True,alpha=0.1)

    end = datetime.now()
    logger.debug(f"Prediction took {end-start}")

    # return pandas dataframe
    return arima_to_df(forecast,conf,data.index[-1],interval)