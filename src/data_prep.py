import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

def load_and_clean_data(file_path_A, file_path_B):
    """
    Loads CSVs, standardizes timestamps, merges on close prices, 
    and filters out intraday market open/close noise.
    """
    df_A = pd.read_csv(file_path_A)
    df_B = pd.read_csv(file_path_B)
    
    # Standardize column names
    df_A.columns = ["datetime", "open", "high", "low", "close", "volume"]
    df_B.columns = ["datetime", "open", "high", "low", "close", "volume"]
    
    # Convert datetime and set as index
    df_A["datetime"] = pd.to_datetime(df_A["datetime"])
    df_B["datetime"] = pd.to_datetime(df_B["datetime"])
    df_A.set_index("datetime", inplace=True)
    df_B.set_index("datetime", inplace=True)
    
    df_A = df_A.sort_index()
    df_B = df_B.sort_index()
    
    # Merge on close prices and drop any missing overlaps
    df = pd.DataFrame({
        "A_close": df_A["close"],
        "B_close": df_B["close"]
    }).dropna()
    
    # Filter intraday noise (9:45 AM - 3:45 PM)
    df = df.between_time("09:45", "15:45")
    
    return df