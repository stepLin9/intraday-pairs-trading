import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import pandas as pd

def calculate_half_life(spread):
    adf_result = adfuller(spread.dropna())
    print(f"ADF Statistic: {adf_result[0]:.4f}, p-value: {adf_result[1]:.4f}")

    spread_lag = spread.shift(1)
    spread_ret = spread - spread_lag

    reg_df = pd.DataFrame({
        "spread_ret": spread_ret,
        "spread_lag": spread_lag
    }).dropna()

    X = sm.add_constant(reg_df["spread_lag"])
    model = sm.OLS(reg_df["spread_ret"], X).fit()

    gamma = model.params.iloc[1]

    if gamma >= 0:
        print("Warning: gamma >= 0, spread does not appear mean-reverting.")
        return np.nan

    halflife = -np.log(2) / gamma
    print(f"Estimated Half-Life: {halflife:.2f} periods")

    return halflife