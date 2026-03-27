import pandas as pd
import numpy as np

def run_backtest(df, spread, positions, cost=0.0002):
    """
    Calculates strategy returns, applies transaction costs, and computes Sharpe ratio.
    """
    # Build a dedicated backtest dataframe
    bt_df = pd.DataFrame(index=df.index)
    bt_df["spread"] = spread
    bt_df["position"] = positions
    bt_df["spread_ret"] = bt_df["spread"].diff()
    
    # Calculate trades for transaction cost deduction
    bt_df["trades"] = bt_df["position"].diff().abs().fillna(0)
    
    bt_df["strategy_ret"] = (
        bt_df["position"].shift(1).fillna(0) * bt_df["spread_ret"].fillna(0)
    -   bt_df["trades"] * cost
    )
    # Performance metrics
    total_ret = bt_df["strategy_ret"].sum()
    mean_ret = bt_df["strategy_ret"].mean()
    std_ret = bt_df["strategy_ret"].std()

    # Annualize Sharpe based on 1-minute data (252 days * 390 minutes)
    annualization_factor = np.sqrt(252 * 390)

    sharpe = annualization_factor * (mean_ret / std_ret) if std_ret > 0 else 0.0
    
    # Detect entries and exits
    bt_df["prev_position"] = bt_df["position"].shift(1)

    entries = (bt_df["position"] != 0) & (bt_df["prev_position"] == 0)
    exits = (bt_df["position"] == 0) & (bt_df["prev_position"] != 0)

    entry_times = bt_df.index[entries]
    exit_times = bt_df.index[exits]

    # Ensure matching entry-exit pairs
    num_trades = min(len(entry_times), len(exit_times))

    holding_times = []

    entry_time = None

    for i in range(len(bt_df)):

        pos = bt_df["position"].iloc[i]
        prev_pos = bt_df["position"].iloc[i-1] if i > 0 else 0

        # Entry
        if prev_pos == 0 and pos != 0:
            entry_time = bt_df.index[i]

        # Exit
        elif prev_pos != 0 and pos == 0 and entry_time is not None:
            exit_time = bt_df.index[i]

            hold = (exit_time - entry_time).total_seconds() / 60
            holding_times.append(hold)

            entry_time = None

    avg_holding_time = np.mean(holding_times) if holding_times else 0
    total_trades = len(holding_times)
    
    # Annualize Sharpe based on 1-minute data (252 days * 390 minutes)
    
    
    results = {
    "Total Return": total_ret,
    "Sharpe Ratio": sharpe,
    "Total Trades": int(total_trades),
    "Average Holding Time (minutes)": avg_holding_time
}
    
    return bt_df, results