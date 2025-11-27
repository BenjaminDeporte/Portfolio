# Portfolio
Projects Portfolio

UTILITIES:

1- /src/Exttract.py : Python script to extract crypto data (BTC here) from the Binance API
2- /notebooks/Log_returns_stationarity_checks.ipynb : NB to perform ADF test on BTC log returns and check stationarity

LEGACY MODELS:

1- LSTM : /notebooks/Forecast_Baseline_LSTM.ipynb
    LSTM model to try and forecast BTC time series (prices, log prices, log returns).
    Unsurprisingly, the model fails to produce good predictions on either family of time series.
    The model is basically learning values over the training dataset, failing to capture dynamics.

2- ARIMA : 
