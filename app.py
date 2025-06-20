import streamlit as st
import pandas as pd
import yfinance as yf
import joblib
from datetime import datetime, timedelta

# Configuracion visual
st.set_page_config(page_title="Predicción Dow Jones", layout="wide")
st.title("📉 Predicción del cierre bursátil del Dow Jones")
st.markdown("Este sistema utiliza el último registro disponible por cada ticker para predecir si el precio de cierre **subirá** o **bajará** al día siguiente. Podés descargar datos recientes y lanzar la predicción.")

# Tickers principales (solo Dow Jones)
dow_tickers = [
    "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
    "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK",
    "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
]

# Inicializar variables de estado si no existen
if "df_recientes" not in st.session_state:
    st.session_state.df_recientes = None

st.markdown("### 📅 Paso 1: Descargar últimos precios de cierre")
if st.button("📅 Descargar datos recientes"):
    try:
        fin = datetime.today()
        inicio = fin - timedelta(days=5)

        datos = []
        for ticker in dow_tickers:
            df = yf.download(ticker, start=inicio.strftime("%Y-%m-%d"), end=fin.strftime("%Y-%m-%d"))
            if not df.empty:
                ultimo = df.iloc[-1]
                datos.append({
                    "Date": ultimo.name.date(),
                    "Ticker": ticker,
                    "Close": round(ultimo["Close"], 2)
                })

        df_recientes = pd.DataFrame(datos)
        st.session_state.df_recientes = df_recientes
        st.success("🚀 Datos descargados correctamente.")
        st.dataframe(df_recientes, use_container_width=True)

    except Exception as e:
        st.error(f"Error al descargar los datos: {e}")

st.markdown("### �udd2e Paso 2: Predecir movimiento de cierre")
if st.button("🌿 Predecir movimiento de cierre"):
    try:
        if st.session_state.df_recientes is None:
            st.warning("⚠️ Primero descargá los datos recientes.")
        else:
            modelo = joblib.load("final_time_series_model.pkl")
            feature_names = joblib.load("features_names_entrenamiento (9).pkl")

            df_pred = st.session_state.df_recientes.copy()
            for col in feature_names:
                if col not in df_pred.columns:
                    df_pred[col] = 0

            X_pred = df_pred[feature_names]
            predicciones = modelo.predict(X_pred)

            df_pred["Prediccion"] = predicciones
            df_pred["Prediccion"] = df_pred["Prediccion"].map({1: "📈 Sube", 0: "📉 Baja"})

            st.success("🚀 Predicción realizada correctamente.")
            st.dataframe(df_pred[["Date", "Ticker", "Close", "Prediccion"]].sort_values("Ticker"), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error durante la predicción: {e}")

st.markdown("""
---
st.caption("App creada por Sebas y equipo para el proyecto final - Dow Jones 2025")
""")
