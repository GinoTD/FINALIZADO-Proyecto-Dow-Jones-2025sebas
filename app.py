import os
import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
import gdown
from datetime import datetime, timedelta

st.set_page_config(page_title="Predicción Dow Jones", layout="wide")
st.title("📉 Predicción del cierre bursátil de las empresas del Dow Jones")

# --- Model download & load ---
@st.cache_resource
def load_model_from_drive():
    url = "https://drive.google.com/uc?id=1nPYvsXTFaErWuLoiyYTrGA4NbwLz615J"
    output_path = "final_time_series_model.pkl"
    if not os.path.exists(output_path):
        gdown.download(url, output_path, quiet=False)
    return joblib.load(output_path)

modelo = load_model_from_drive()

# --- User date selection ---
selected_date = st.date_input(
    "Seleccione la fecha para descargar datos", 
    datetime.today().date()
)

st.markdown("""
Este sistema descarga los datos de cada empresa del Dow Jones para la fecha seleccionada y predice si el precio de cierre **subirá o bajará** al día siguiente, usando un modelo previamente entrenado.

1. Seleccione una fecha.  
2. Descarga los datos de esa fecha.  
3. Aplica el modelo y muestra la predicción.
""")

# --- Dow Jones tickers ---
dow_tickers = [
    "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK",
    "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]

# --- Fetch, predict and display ---
if st.button("📥 Descargar datos y predecir"):
    try:
        # Use selected_date as the target day
        fin = datetime(
            year=selected_date.year, 
            month=selected_date.month, 
            day=selected_date.day
        )
        inicio = fin
        fin_plus = fin + timedelta(days=1)

        datos = []
        for ticker in dow_tickers:
            df = yf.download(
                ticker,
                start=inicio.strftime("%Y-%m-%d"),
                end=fin_plus.strftime("%Y-%m-%d")
            )
            if not df.empty:
                ultimo = df.iloc[-1]
                datos.append({
                    "Ticker": ticker,
                    "Open": ultimo["Open"],
                    "High": ultimo["High"],
                    "Low": ultimo["Low"],
                    "Close": ultimo["Close"],
                    "Volume": ultimo["Volume"]
                })

        df_pred = pd.DataFrame(datos)

        if df_pred.empty:
            st.warning("No se encontraron datos para la fecha seleccionada.")
        else:
            feature_names = ['Open', 'High', 'Low', 'Close', 'Volume']
            X = df_pred[feature_names]

            df_pred["Predicción"] = modelo.predict(X)
            df_pred["Predicción"] = df_pred["Predicción"].map({1: "📈 Sube", 0: "📉 Baja"})

            st.success("✅ Predicción realizada correctamente para la fecha:", selected_date)
            st.dataframe(
                df_pred[                 
                    ["Ticker", "Close", "Predicción"]
                ].sort_values("Ticker"),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"❌ Error durante la predicción: {e}")

st.markdown("---")
st.caption("App desarrollada  – Proyecto Dow Jones 2025")