import yfinance as yf
from trading.models import Security, Exchange
from djmoney.money import Money  # Importă Money din djmoney

def run():
    print("Fetching NASDAQ tickers...")

    ftp_url = "ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt"

    try:
        import pandas as pd
        df = pd.read_csv(ftp_url, sep='|')

        if 'File Creation Time' in df.columns[-1]:
            df = df.iloc[:-1]

        nasdaq_tickers = df['Symbol'].tolist()

    except Exception as e:
        print(f"Error reading FTP file: {e}")
        return

    exchange, _ = Exchange.objects.get_or_create(
        name="NASDAQ",
        defaults={'url': 'http://www.nasdaq.com'}  
    )

    for ticker_symbol in nasdaq_tickers:
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            Security.objects.update_or_create(
                symbol=info['symbol'],
                exchange=exchange,
                defaults={
                    'name': info.get('shortName', 'N/A'),
                    'price': Money(info.get('regularMarketPrice', 0), 'USD'),
                }
            )
            print(f"Processed ticker: {info['symbol']}")
        except Exception as e:
            print(f"Error processing {ticker_symbol}: {e}")

    print("Stocks imported successfully!")
