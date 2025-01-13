from unidecode import unidecode
import yfinance as yf
from trading.models import Security

def run():
    print("Populare descrieri pentru securities...")

    securities = Security.objects.filter(description__isnull=True)

    if not securities.exists():
        print(unidecode("Nu exista securities fara descriere."))
        return

    for security in securities:
        try:
            ticker = yf.Ticker(security.symbol)
            description = ticker.info.get("longBusinessSummary", None)

            if description:
                security.description = unidecode(description) 
                security.save()
                print(unidecode(f"Descriere adaugata pentru {security.name} ({security.symbol})"))
            else:
                print(unidecode(f"Descriere indisponibila pentru {security.name} ({security.symbol})"))

        except Exception as e:
            print(unidecode(f"Eroare pentru {security.name} ({security.symbol}): {e}"))

    print(unidecode("Popularea descrierilor a fost finalizata!"))
