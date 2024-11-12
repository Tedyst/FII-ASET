import requests
import io
import csv
import yfinance as yf


class Ticker:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price

    def __str__(self):
        return f"{self.symbol} at price {self.price}"


def get_ticker_symbols():
    url = "http://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
    response = requests.get(url)
    response.raise_for_status()

    data = io.StringIO(response.text)
    reader = csv.reader(data, delimiter="|")
    tickers_list = []

    next(reader)

    for row in reader:
        if row:
            ticker_symbol = row[0]
            tickers_list.append(ticker_symbol)

    return tickers_list


def save_valid_tickers(tickers_list, output_file):
    count = 0

    with open(output_file, "w") as output:
        for ticker_symbol in tickers_list:
            try:
                _ = yf.Ticker(ticker_symbol).history(period="1d")["Close"].iloc[-1]

                output.write(f"{ticker_symbol}\n")
                count += 1
            except (ValueError, IndexError, KeyError) as e:
                print(f"Skipping ticker {ticker_symbol} due to error: {e}")
                print(f"List currently at size: {count}")


def get_valid_tickers(input_file):
    tickers_list = []

    with open(input_file) as tickers:
        tickers_list = [line.strip() for line in tickers.readlines()]

    return tickers_list


# probabil de facut pe chunk uri
def get_ticker_prices(ticker_symbols):
    tickers_list = []

    for ticker_symbol in ticker_symbols:
        try:
            ticker = yf.Ticker(ticker_symbol)

            last_price = ticker.history(period="1d")["Close"].iloc[-1]

            tickers_list.append(Ticker(symbol=ticker_symbol, price=last_price))
        except (ValueError, IndexError, KeyError) as e:
            print(f"Skipping ticker {ticker_symbol} due to error: {e}")

    return tickers_list


def flow():
    ticker_symbols = get_ticker_symbols()
    save_valid_tickers(ticker_symbols, "./valid.txt")
    valid_tickers = get_valid_tickers("./valid.txt")
    tickers = get_ticker_prices(valid_tickers)

    for ticker in tickers:
        print(ticker)


flow()
