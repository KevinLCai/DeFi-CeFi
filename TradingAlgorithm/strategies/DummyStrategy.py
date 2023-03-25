import math
import pandas as pd

class DummyStrategy():
    def __init__(self, df):
        self.df = df

    def next(self):
        close_price = float(self.df["Close"].iloc[-1])
        if close_price % 2 == 0:
            print(close_price)
            return "BUY======="
        elif close_price % 2 == 1:
            print(close_price)
            return "SELL========"
        else:
            return "HOLD======="
