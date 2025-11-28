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

2- ARIMA : /notebooks/Forecast_Baseline_ARIMA.ipynb
    Legacy ARIMA modeling. We use log prices. One differenciation leads to a wide-senses stationary process
    (checked with ADF test) so d=1. Looking at the Partial Auto Correlation plot of the original series, we
    infer p=1 (AR(1) process). The innovation coefficient is chosen at random (q=0 or 1). Residuals are checked.
    Overall, the forecasting power of the model is poor.

STOCHASTIC MODELS:

1- GEOMETRIC BROWNIAN MOTION (GBM)
Black, F. & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. J. Political Economy.
Bjork, T. (2009). Arbitrage Theory in Continuous Time. Chapter 7.

2- MERTON JUMP-DIFFUSION
Merton, R. (1976). Option Pricing When Underlying Stock Returns Are Discontinuous. J. Financial Economics.

3- HESTON
Heston, S. (1993). A Closed-Form Solution for Options with Stochastic Volatility. Review of Financial Studies.

4- HULL-WHITE LOG NORMAL
Hull, J. & White, A. (1987). The Pricing of Options with Stochastic Volatilities. J. Finance.

5- LEVY AND GENERAL JUMP MODELS
Madan, D. B., Carr, P., & Chang, E. (1998). The Variance Gamma Process and Option Pricing. European Finance Review.
Carr, P., Geman, H., Madan, D., & Yor, M. (2002). The Fine Structure of Asset Returns. J. Business.

6- ROUGH VOLATILITY
Gatheral, J., Jaisson, T., & Rosenbaum, M. (2018). Volatility Is Rough. Quantitative Finance.