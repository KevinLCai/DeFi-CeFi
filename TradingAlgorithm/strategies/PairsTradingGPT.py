import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

class PairsTrading:
    
    def __init__(self, hist_btc, hist_eth):
        # hist_btc and hist_eth are dataframes containing historical data for 4-hour candlesticks for Bitcoin and Ether
        self.hist_btc = hist_btc
        self.hist_eth = hist_eth
        self.position = (0, 0)
    
    def calculate_spread(self):
        # Combine the historical data for Bitcoin and Ether into a single dataframe
        df = pd.concat([self.hist_btc['close'], self.hist_eth['close']], axis=1)
        df.columns = ['btc', 'eth']

        # Calculate the spread between the two tokens
        spread = df['btc'] - df['eth']
        return spread
    
    def check_for_signal(self):  
        # Calculate the z-score of the spread
        spread = self.calculate_spread()
        zscore = (spread - np.mean(spread)) / np.std(spread)

        # If there is no open position, determine whether to enter a long or short position
        if not self.position[0] and not self.position[1]:
            # If the z-score is greater than 1, enter a short position (sell btc, buy eth)
            if zscore > 1:
                self.position = (-1, 1)
        
            # If the z-score is less than -1, enter a long position (buy btc, sell eth)
            elif zscore < -1:
                self.position = (1, -1)
        
        # If there is an open position, determine whether to close it out for a profit
        else:
            # Calculate the current position based on the sign of the positions for btc and eth
            btc_pos = np.sign(self.position[0])
            eth_pos = np.sign(self.position[1])
        
            # If the current position is long on btc and short on eth, check if it's time to close out
            if btc_pos == 1 and eth_pos == -1:
                # If the z-score is less than 0.5, close out the position for a profit
                if zscore < 0.5:
                    self.position = (0, 0)
            
            # If the current position is short on btc and long on eth, check if it's time to close out
            elif btc_pos == -1 and eth_pos == 1:
                # If the z-score is greater than -0.5, close out the position for a profit
                if zscore > -0.5:
                    self.position = (0, 0)
    
    def get_signal(self):
        self.check_for_signal()
        return self.position
    
    def update_hist_data(self, hist_btc, hist_eth):
        # Update the historical data for Bitcoin and Ether
        self.hist_btc = hist_btc
        self.hist_eth = hist_eth
        # Reset the position to 0,0
        self.position = (0, 0)






# use the class 

# Load the historical data for Bitcoin and Ether
hist_btc = pd.read_csv('btc_data.csv')
hist_eth = pd.read_csv('eth_data.csv')

# Create an instance of the PairsTrading class
pt = PairsTrading(hist_btc, hist_eth)

# Get the initial position
initial_position = pt.get_signal()

# Loop through new historical data and get signals from the pairs trading strategy
for i in range(len(new_hist_btc)):
    # Update the historical data for Bitcoin and Ether
    new_hist_btc = pd.read_csv('new_btc_data.csv')
    new_hist_eth = pd.read_csv('new_eth_data.csv')
    pt.update_hist_data(new_hist_btc, new_hist_eth)
    
    # Get the signal from the pairs trading strategy
    signal = pt.get_signal()
    
    # If the signal has changed, take action
    if signal != pt.position:
        # If the new signal is to enter a position, execute the trade
        if signal[0] != 0 and signal[1] != 0:
            # Buy/sell btc/eth according to the signal
            # ...
            
            # Update the position
            pt.position = signal
        
        # If the new signal is to exit a position, execute the trade
        else:
            # Buy/sell btc/eth to close out the position
            # ...
            
            # Update the position
            pt.position = signal
