# -*- coding: utf-8 -*-
"""Aplicación Streamlit: Análisis de Portafolio con dos acciones (diversificación)"""

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# --------------------------------------------
# ENCABEZADO
# --------------------------------------------
st.title('ANÁLISIS DE PORTAFOLIO DE INVERSIÓN')
st.subheader('Ejemplo de diversificación con dos acciones')

st.markdown("""
Este ejemplo muestra cómo la **diversificación** reduce el riesgo al combinar activos de diferentes sectores.  
Usaremos las acciones de **Apple (AAPL)** y **Coca-Cola (KO)**.
""")

# --------------------------------------------
# SELECCIÓN DE ACCIONES
# --------------------------------------------
tickers = ['AAPL', 'KO']
st.write("**Acciones seleccionadas:**", tickers)

# --------------------------------------------
# DESCARGA DE DATOS
# --------------------------------------------
try:
    data = yf.download(tickers, start='2022-01-01', end='2025-01-01')['Adj Close']
except Exception as e:
    st.error(f"Error al descargar los datos: {e}")
    st.stop()

# Mostrar datos
st.subheader("📊 Precios históricos ajustados")
st.dataframe(data.tail())

# --------------------------------------------
# CÁLCULO DE RENDIMIENTOS
# --------------------------------------------
returns = data.pct_change().dropna()
st.subheader("📈 Estadísticas de rentabilidad diaria")
st.write(returns.describe())

# --------------------------------------------
# GRÁFICO DE EVOLUCIÓN DE PRECIOS
# --------------------------------------------
st.subheader("📉 Evolución del precio de las acciones")
fig, ax = plt.subplots()
data.plot(ax=ax)
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio ajustado (USD)")
ax.set_title("Evolución histórica de precios")
st.pyplot(fig)

# --------------------------------------------
# GRÁFICO DE CORRELACIÓN (DISPERSIÓN)
# --------------------------------------------
st.subheader("🔗 Relación entre rendimientos (correlación)")
fig2, ax2 = plt.subplots()
ax2.scatter(returns['AAPL'], returns['KO'], alpha=0.6)
ax2.set_xlabel('Rendimiento diario AAPL')
ax2.set_ylabel('Rendimiento diario KO')
ax2.set_title('Diversificación: Apple vs Coca-Cola')
st.pyplot(fig2)

# --------------------------------------------
# MATRIZ DE CORRELACIÓN
# --------------------------------------------
st.subheader("📊 Matriz de correlación")
correlacion = returns.corr()
st.write(correlacion)

# --------------------------------------------
# INTERPRETACIÓN
# --------------------------------------------
st.markdown("""
### 💡 Interpretación:
- Si la **correlación** entre AAPL y KO es **baja o negativa**, significa que las acciones no se mueven igual.  
  Cuando una baja, la otra puede subir o mantenerse estable.  
- Esto **reduce el riesgo total del portafolio** y demuestra la utilidad de la **diversificación**.

**Conclusión:**  
Combinar activos de sectores distintos (tecnología y consumo) genera un portafolio más estable frente a la volatilidad del mercado.
""")

