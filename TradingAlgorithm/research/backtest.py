import sys
import os

# Add the parent directory to the sys.path list
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(parent_dir)

import pandas as pd
from TradingAlgorithm.strategies.MMR import MMR


# Obtain historical price data (e.g., from a CSV file)
historical_data = pd.read_csv('/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/separate/1DAY_ETHUSDT.csv')

# Instantiate the MMR strategy with desired parameters
mmr_strategy = MMR(historical_data, momentum_window=5, mean_reversion_threshold=0.05)

# Initialize variables
positions = []  # To track trading positions
signals = []  # To track trading signals

# Iterate over historical data
for index, row in historical_data.iterrows():
    # Generate trading signal
    signal = mmr_strategy.next()
    signals.append(signal)
    
    # Execute trading action based on the signal
    if signal == 'buy':
        positions.append(1)  # Buy position
    elif signal == 'sell':
        positions.append(-1)  # Sell position
    else:
        positions.append(0)  # No position (hold)
        
# Calculate portfolio returns based on positions and price changes
price_changes = historical_data['Close'].pct_change()
portfolio_returns = positions[:-1] * price_changes[1:]

# Calculate cumulative returns
cumulative_returns = (1 + portfolio_returns).cumprod()

print(cumulative_returns)

# Evaluate performance metrics (e.g., cumulative returns, portfolio value, etc.)
# ...

# Plot results or perform further analysis
import matplotlib.pyplot as plt

# Assuming cumulative_returns is a pandas Series containing the cumulative returns

# Plot cumulative returns
plt.plot(cumulative_returns.index, cumulative_returns)
plt.title('Cumulative Returns Over Time')
plt.xlabel('Time Step')
plt.ylabel('Cumulative Returns')
plt.grid(True)
plt.show()

