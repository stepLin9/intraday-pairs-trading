import statsmodels.api as sm
import numpy as np

def construct_spread(df, use_log=False):
    """
    Calculates the hedge ratio (beta) using OLS regression and constructs the spread.
    """
    if use_log:
        y = np.log(df["A_close"])
        x = np.log(df["B_close"])
    else:
        y = df["A_close"]
        x = df["B_close"]
        
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    beta = model.params.iloc[1]
    
    # Construct the spread matching the price type
    spread = y - beta * x
    
    return beta, spread