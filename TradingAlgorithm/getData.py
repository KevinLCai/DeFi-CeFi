from binance.client import Client
import argparse
import csv
import config
import datetime
import logging
import pandas as pd


def set_interval(timeframe):
    if timeframe == "1MINUTE":
        interval = Client.KLINE_INTERVAL_1DAY
    elif timeframe == "3MINUTE":
        interval = Client.KLINE_INTERVAL_3MINUTE
    elif timeframe == "15MINUTE":
        interval = Client.KLINE_INTERVAL_15MINUTE
    elif timeframe == "30MINUTE":
        interval = Client.KLINE_INTERVAL_30MINUTE
    elif timeframe == "1HOUR":
        interval = Client.KLINE_INTERVAL_1HOUR
    elif timeframe == "2HOUR":
        interval = Client.KLINE_INTERVAL_2HOUR
    elif timeframe == "4HOUR":
        interval = Client.KLINE_INTERVAL_4HOUR
    elif timeframe == "12HOUR":
        interval = Client.KLINE_INTERVAL_12HOUR
    elif timeframe == "1DAY":
        interval = Client.KLINE_INTERVAL_1DAY
    elif timeframe == "3DAY":
        interval = Client.KLINE_INTERVAL_3DAY
    elif timeframe == "1WEEK":
        interval = Client.KLINE_INTERVAL_1WEEK
    elif timeframe == "1MONTH":
        interval = Client.KLINE_INTERVAL_1MONTH
    return interval


def main(args):
    # prices = client.get_all_tickers()
    # for price in prices:
    #     print(price)

    timeframe = args.timeframe
    pairs = args.pairs
    filetype = args.filetype
    interval = set_interval(timeframe)
    if not args.from_date:
        args.from_date = "010122"
    from_date = datetime.datetime.strptime(
        args.from_date, "%d%m%y").strftime("%-d %b, %Y")

    client = Client(config.API_KEY, config.API_SECRET)

    if filetype == "combined":
        candlestick_data = {}
        for symbol in pairs:
            candles = client.get_klines(symbol=symbol, interval=interval)
            candlesticks = client.get_historical_klines(
                symbol, interval, from_date)
            print(candles)
            print(candlesticks)

            for candlestick in candlesticks:
                # Convert timestamp to date
                candlestick[0] = candlestick[0] / 1000
                t = datetime.datetime.fromtimestamp(candlestick[0])
                day = t.strftime('%Y-%m-%d')

                # Create a new list for the pair and date if it doesn't exist
                if symbol not in candlestick_data:
                    candlestick_data[symbol] = {}
                if day not in candlestick_data[symbol]:
                    candlestick_data[symbol][day] = []

                # Add the candlestick data to the list
                candlestick_data[symbol][day].append(candlestick[4])

        # Write the data to a CSV file
        with open(f'TradingAlgorithm/data/combined/{timeframe}_{"".join([pair + "_" for pair in pairs])}_combined.csv', 'w', newline='') as csvfile:
            candlestick_writer = csv.writer(csvfile, delimiter=',')

            # Write header row
            header = ['Date']
            for symbol in pairs:
                header.append(f'{symbol} Close')
            candlestick_writer.writerow(header)

            # Write data rows
            for date in candlestick_data[pairs[0]]:
                row = [date]
                for symbol in pairs:
                    if date in candlestick_data[symbol]:
                        row.append(candlestick_data[symbol][date][0])
                    else:
                        row.append('')
                candlestick_writer.writerow(row)

        csvfile.close()

    elif filetype == "separate":
        for symbol in pairs:

            candles = client.get_klines(
                symbol=symbol, interval=interval)

            csvfile = open(
                f'TradingAlgorithm/data/separate/{timeframe}_{symbol}.csv', 'w', newline='')
            candlestick_writer = csv.writer(csvfile, delimiter=',')

            # for candlestick in candles:
            #     candlestick_writer.writerow(candlestick)

            candlesticks = client.get_historical_klines(
                symbol, interval, "1 Jan, 2022")

            csvfile.write('Date,Open,High,Low,Close,Volume,OpenInterest\n')
            for candlestick in candlesticks:
                candlestick[0] = candlestick[0] / 1000
                t = datetime.datetime.fromtimestamp(candlestick[0])
                day = t.strftime('%Y-%m-%d')
                candlestick[0] = day
                candlestick[6] = 0.0
                candlestick_writer.writerow(candlestick[:7])

            csvfile.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeframe", choices=["1MINUTE", "3MINUTE", "15MINUTE", "30MINUTE", "1HOUR", "2HOUR",
                                                "4HOUR", "12HOUR", "1DAY", "3DAY", "1WEEK", "1MONTH"], help="Candlestick timeframe", required=True)
    parser.add_argument("--pairs", nargs='+',
                        help="Token pairs", required=True)
    parser.add_argument(
        "--filetype", choices=["combined", "separate"], help="Output CSV Format", required=True)
    parser.add_argument(
        "--from-date", help="Data starting date, format DDMMYY"
    )

    args = parser.parse_args()

    main(args)
