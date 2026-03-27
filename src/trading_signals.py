import numpy as np
import pandas as pd

def generate_signals(spread, half_life, entry_z=2.0, exit_z=0.0):
    """
    Calculates rolling Z-scores using half-life and generates position signals.
    """
    # Ensure window is at least 1 to prevent rolling errors
    window = max(int(half_life), 1)
    
    spread_mean = spread.rolling(window=window).mean()
    spread_std = spread.rolling(window=window).std()
    z_score = (spread - spread_mean) / spread_std
    
    z_scores = z_score.values
    positions = np.zeros(len(z_scores))
    curr_pos = 0
    
    for i in range(len(z_scores)):
        z = z_scores[i]
        
        # Keep position flat during the initial rolling window buildup
        if np.isnan(z):
            positions[i] = 0
            continue
            
        # Entry/Exit Logic
        if curr_pos == 0:
            if z > entry_z:
                curr_pos = -1  # Short the spread
            elif z < -entry_z:
                curr_pos = 1   # Long the spread
        elif curr_pos == 1:
            if z > -exit_z:
                curr_pos = 0   # Exit long
        elif curr_pos == -1:
            if z < exit_z:
                curr_pos = 0   # Exit short
                
        positions[i] = curr_pos
        
    return pd.Series(positions, index=spread.index, name="position")

