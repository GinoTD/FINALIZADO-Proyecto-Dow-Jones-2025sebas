import yfinance as yf
import pandas as pd
from datetime import date, timedelta

# Lista de tickers del Dow Jones
tickers_dow = [
    "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
    "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]

# Fechas para evitar fines de semana
hoy = date.today()
ayer = hoy - timedelta(days=3)

print(f"Descargando datos desde {ayer} hasta {hoy}...")

try:
    data = yf.download(tickers_dow, start=ayer, end=hoy)
    df_close = data["Close"].copy()

    df_list = []
    for ticker in df_close.columns:
        last_valid = df_close[ticker].dropna().iloc[-1]
        last_date = df_close[ticker].dropna().index[-1]
        df_list.append({
            "Date": last_date.strftime("%Y-%m-%d"),
            "Ticker": ticker,
            "Close": round(last_valid, 2)
        })

    df_resultado = pd.DataFrame(df_list)
    print("\n✅ Datos descargados correctamente:")
    print(df_resultado)

except Exception as e:
    print(f"\n❌ Error al descargar datos: {e}")
