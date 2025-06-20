import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
from datetime import datetime, timedelta

st.set_page_config(page_title="Predicción Dow Jones", layout="wide")
st.title("📉 Predicción del cierre bursátil del Dow Jones")

st.markdown("""
Este sistema descarga los últimos datos disponibles de cada empresa del Dow Jones y predice si el precio de cierre **subirá o bajará** al día siguiente, usando un modelo previamente entrenado.

1. Descarga los datos de los últimos días.  
2. Aplica el modelo y muestra la predicción.
""")

dow_tickers = [
    "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK",
    "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]

if st.button("📥 Descargar datos y predecir"):
    try:
        fin = datetime.today()
        inicio = fin - timedelta(days=7)

        datos = []
        for ticker in dow_tickers:
            df = yf.download(ticker, start=inicio.strftime("%Y-%m-%d"), end=fin.strftime("%Y-%m-%d"))
            if not df.empty:
                ultimo = df.iloc[-1]
                datos.append({
                    "Ticker": ticker,
                    "Date": df.index[-1].date(),
                    "Open": ultimo["Open"],
                    "High": ultimo["High"],
                    "Low": ultimo["Low"],
                    "Close": ultimo["Close"],
                    "Volume": ultimo["Volume"]
                })

        df_pred = pd.DataFrame(datos)

        if df_pred.empty:
            st.warning("No se encontraron datos.")
        else:
            # Cargar modelo y features
            modelo = joblib.load("final_time_series_model.pkl")
            feature_names = ['Open', 'High', 'Low', 'Close', 'Volume']
            X = df_pred[feature_names]

            df_pred["Predicción"] = modelo.predict(X)
            df_pred["Predicción"] = df_pred["Predicción"].map({1: "📈 Sube", 0: "📉 Baja"})

            st.success("✅ Predicción realizada correctamente")
            st.dataframe(df_pred[["Ticker", "Date", "Close", "Predicción"]].sort_values("Ticker"), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error durante la predicción: {e}")

st.markdown("---")
st.caption("App desarrollada por Sebas – Proyecto Dow Jones 2025")
