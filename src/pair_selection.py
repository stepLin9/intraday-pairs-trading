from statsmodels.tsa.stattools import coint

def check_pair_validity(df, p_value_threshold=0.05):
    corr = df["A_close"].corr(df["B_close"])
    score, pvalue, _ = coint(
        df["A_close"],
        df["B_close"],
        maxlag=1,
        autolag=None
    )

    is_valid = pvalue < p_value_threshold

    print(f"Correlation: {corr:.4f}")
    print(f"Cointegration p-value: {pvalue:.4f}")
    print(f"Pair is {'VALID (Cointegrated)' if is_valid else 'INVALID (Not Cointegrated)'}")

    return is_valid, pvalue, corr