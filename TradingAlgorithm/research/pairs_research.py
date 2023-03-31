import argparse
from matplotlib.pyplot import figure
import pandas as pd
import numpy as np


def graph_pair(token1, token2):
    print(token1)
    print(token2)


def main(args):
    filename = args.filename

    df = pd.read_csv(
        f"TradingAlgorithm/data/{filename}")

    corr_matrix = df.corr()
    print(corr_matrix)

    highest_corr = sorted(corr_matrix.iloc[0].tolist())[-2]
    row, col = np.where(corr_matrix == highest_corr)
    token1 = corr_matrix.columns[col[0]].split(" ")[0]
    token2 = corr_matrix.columns[row[0]].split(" ")[0]

    graph_pair(token1, token2)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename",
                        help="folder and filename", required=True)
    args = parser.parse_args()
    main(args)
