# from Strategy import Strategy

class MMR:
    def __init__(self, df, **kwargs):
        self.df = df.astype({'Close': float})
        self.momentum_window = kwargs.get('momentum_window', 5)
        self.mean_reversion_threshold = kwargs.get('mean_reversion_threshold', 0.05)

    def next(self) -> str:
        # Calculate momentum
        returns = self.df['Close'].pct_change()
        momentum = returns[-self.momentum_window:].mean()

        # Check momentum
        if momentum > 0:
            # Positive momentum indicates an uptrend, so we check for mean reversion
            current_price = self.df['Close'].iloc[-1]
            mean_price = self.df['Close'].mean()
            
            price_diff = current_price - mean_price
            z_score = price_diff / self.df['Close'].std()

            # Check mean reversion
            if z_score > self.mean_reversion_threshold:
                return 'sell'  # Sell signal
        else:
            # Negative or zero momentum indicates a downtrend, so we check for mean reversion
            current_price = self.df['Close'].iloc[-1]
            mean_price = self.df['Close'].mean()
            price_diff = current_price - mean_price
            z_score = price_diff / self.df['Close'].std()

            # Check mean reversion
            if z_score < -self.mean_reversion_threshold:
                return 'buy'  # Buy signal

        return 'hold'  # No signal
