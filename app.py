import os
import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
import gdown
from datetime import datetime, timedelta

st.set_page_config(page_title="Predicción Dow Jones", layout="wide")
st.title("📉 Predicción del cierre bursátil de las empresas del Dow Jones 📉")

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
    "Seleccione la fecha para descargar datos ***(este modelo ha sido entrenado con datos entre 2015 y 2025)***", 
    datetime.today().date()
)

st.markdown("""
Aqui se extraen, para la fecha que selecciones, los datos bursátiles (apertura, máximo, mínimo, cierre, volumen, etc...) de cada componente del Dow Jones. A continuación, un modelo de machine learning preentrenado analiza estas series temporales para determinar si el precio de cierre subirá o bajará al día siguiente, basándose en patrones históricos aprendidos.

1. **Selección de fecha**  
   Se indica la fecha para realizar la predicción
2. **Recopilación de datos**  
   Se descargan, mediante la API de Yahoo Finance.  
3. **Extracción de características**  
   A partir de los datos recuperados, se construye un vector de atributos que sirve de entrada al modelo.
4. **Predicción**  
   El modelo, entrenado previamente sobre datos históricos y validado para maximizar la precisión, procesa el vector de atributos y genera una etiqueta binaria: “sube” o “baja” para el cierre del día siguiente.  
5. **Presentación de resultados**  
   Se muestra en pantalla, de forma ordenada, el ticker y la predicción asociada, facilitando la interpretación y la toma de decisiones.
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
            st.warning("El mercado está cerrado durante esta fecha, por favor, prueba con otra")
        else:
            feature_names = ['Open', 'High', 'Low', 'Close', 'Volume']
            X = df_pred[feature_names]

            df_pred["Predicción"] = modelo.predict(X)
            df_pred["Predicción"] = df_pred["Predicción"].map({1: "📈 Sube", 0: "📉 Baja"})

            st.success("✅ Predicción realizada correctamente")
            st.dataframe(
                df_pred[                 
                    ["Ticker", "Close", "Predicción"]
                ].sort_values("Ticker"),
                use_container_width=True
            )

    except Exception as e:
        st.error(f"❌ Error durante la predicción: {e}")

st.markdown("---")
st.caption("App desarrollada  – Equipo Proyecto Dow Jones 2025")