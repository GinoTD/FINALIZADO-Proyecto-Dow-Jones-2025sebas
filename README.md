# Predicción y Validación del Cierre Bursátil del Dow Jones

Este proyecto desarrolla una aplicación web con **Streamlit** que descarga datos bursátiles de los 30 componentes del índice Dow Jones para una fecha seleccionada, realiza predicciones sobre la dirección del cierre al día siguiente usando un modelo de `RandomForestClassifier` preentrenado, y valida la precisión de dichas predicciones con los precios reales.

---

## 📂 Estructura del proyecto

```text
├── app.py                          # Código principal de la aplicación Streamlit
├── final_time_series_model.pkl    # Modelo preentrenado (se descarga automáticamente)
├── requirements.txt                # Lista de dependencias
└── README.md                       # Este archivo de documentación
```

---

## ⚙️ Requisitos

* Python 3.8+
* Streamlit
* pandas
* yfinance
* joblib
* gdown

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

---

## 🚀 Uso

1. **Clonar el repositorio**

```bash
git clone [https://github.com/tu-usuario/dow-jones-prediction.git](https://github.com/tu-usuario/dow-jones-prediction.git)
cd dow-jones-prediction
 ```

2. **Instalar dependencias**
   
```bash
pip install -r requirements.txt
````

3. **Ejecutar la aplicación**

   ```bash
   streamlit run app.py
   ```

5. **Abrir visualización**

   ```bash
   Pulsar el botón verde de la ventana emergente en la parte inferior derecha de la pantalla
   ````
   
4. **Interacción**
   
   - Selecciona la fecha de análisis.  
   - Haz clic en **Ejecutar predicción y validación**.  
   - Consulta la tabla con tickers, predicción, cierre real y resultado.

---

## 🔍 Flujo de trabajo

1. **Selección de fecha**  
   El usuario elige un día hábil (2015–2025).
2. **Descarga de datos**  
   Se obtienen `Open`, `High`, `Low`, `Close`, `Volume`, etc, de Yahoo Finance.
3. **Extracción de características**  
   Se construye un vector con las variables anteriores.
4. **Predicción**  
   El modelo clasifica si el cierre subirá 📈 o bajará 📉 al día siguiente.
5. **Validación**  
   Se compara con el cierre real del siguiente día hábil y se marca “✅ Correcto” o “❌ Incorrecto”.

---

## 🧠 Modelo

El `RandomForestClassifier` está entrenado con datos históricos del Dow Jones (2015–2025) y validado para maximizar precisión. Se descarga automáticamente desde Google Drive en el primer arranque.

---

## 🤝 Contribuciones

- Pablo Morena
- Pablo Rodado
- Gino Tomas
- Sebastian López

---

## ✍️ Autores

Equipo Proyecto Dow Jones 2025

---
```bash
*¡Gracias por todo lo aprendido!*

```
