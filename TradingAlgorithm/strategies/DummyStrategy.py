import math
import pandas as pd
import random

class DummyStrategy():
    def __init__(self, df):
        self.df = df

    def next(self):
        close_price = float(self.df["Close"].iloc[-1])
        possible_decisions = ["buy", "sell", "hold"]
        decision = random.choice(possible_decisions)
        print(f"Close price: {close_price}; Decision: {decision}")
        return f"{decision}"