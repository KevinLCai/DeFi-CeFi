import requests
import pandas as pd
import csv

class Historical():
    def __init__(self, filepath):
        self.api_url = "http://127.0.0.1:5000/cefi_historical"
        self.filepath = filepath

    def format_data(self):
        data = []
        with open(self.filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row
            for row in reader:
                date = row[0]
                close_price = float(row[4])
                obj = {'time': date, 'value': int(close_price)}
                data.append(obj)
        return data
    
    def extract_data(self):
        self.data_to_send = self.format_data()

    def send_data(self):
        self.extract_data()
        response = requests.post(self.api_url, json=self.data_to_send)

class Deal():
    def __init__(self, strategy, tradeID, tokenID, timestamp, price, size, fees):
        # Might need to include which tokens are being traded - more data
        self.api_url = "http://127.0.0.1:5000/deal"
        self.data_to_send = {"strategy": strategy, "tradeID": tradeID, "tokenID": tokenID,
                             "timestamp": timestamp, "price": price, "size": size, "fees": fees}

    def send_data(self):
        response = requests.post(self.api_url, json=self.data_to_send)
