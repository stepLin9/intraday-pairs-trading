import os
import numpy as np

from data_prep import load_and_clean_data
from pair_selection import check_pair_validity
from spread_construction import construct_spread
from spread_diagnostics import calculate_half_life
from trading_signals import generate_signals
from backtest import run_backtest


def main():

    print("--- Starting Pairs Trading Backtest ---")

    # 1. Dynamically resolve file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_A = os.path.join(current_dir, "..", "data", "AAPL.csv")
    file_B = os.path.join(current_dir, "..", "data", "MSFT.csv")

    # 2. Load and Clean Data
    print("Loading data...")
    df = load_and_clean_data(file_A, file_B)

    # 3. Pair Selection Diagnostics
    print("\nRunning Diagnostics...")
    is_valid, pvalue, corr = check_pair_validity(df)

    # Early exit if pair is not cointegrated
    if not is_valid:
        print("\n[STOP] The pair failed the cointegration test.")
        print("Since the spread is not statistically mean-reverting, the backtest is aborted.")
        return

    # 4. Spread Construction & Diagnostics
    print("\nConstructing Spread and Calculating Half-Life...")
    beta, spread = construct_spread(df)
    hl = calculate_half_life(spread)

    # 5. Sensitivity Analysis
    print("\n--- Running Sensitivity Analysis ---")

    best_sharpe = -np.inf
    best_params = {}
    best_results = None

    # Loop through different entry thresholds and transaction costs
    for entry_threshold in [1.5, 2.0, 2.5]:
        for cost in [0.0, 0.0001, 0.0002]:

            # Generate trading signals
            positions = generate_signals(
                spread,
                hl,
                entry_z=entry_threshold
            )

            # Run backtest
            bt_df, results = run_backtest(
                df,
                spread,
                positions,
                cost=cost
            )

            current_sharpe = results["Sharpe Ratio"]

            print(
                f"Tested Entry: {entry_threshold}, Cost: {cost} "
                f"-> Sharpe: {current_sharpe:.4f}"
            )

            # Store best configuration
            if current_sharpe > best_sharpe:
                best_sharpe = current_sharpe
                best_params = {
                    "entry_z": entry_threshold,
                    "cost": cost
                }
                best_results = results

    # 6. Print Optimization Results
    print("\n--- Optimization Results ---")
    print(f"Best Sharpe Ratio: {best_sharpe:.4f}")
    print(f"Best Parameters: {best_params}")

    # 7. Print Statistics from Best Run
    print("\n--- Strategy Statistics (Best Run) ---")
    for k, v in best_results.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()