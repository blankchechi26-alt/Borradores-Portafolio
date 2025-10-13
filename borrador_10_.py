# -*- coding: utf-8 -*-
"""Aplicación interactiva de análisis de portafolio con Streamlit y Yahoo Finance"""

import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# TÍTULO E INTRODUCCIÓN
# -----------------------------------------------------------
st.set_page_config(page_title="Análisis de Portafolio", page_icon="📈", layout="centered")

st.title("📈 ANÁLISIS DE PORTAFOLIO DE INVERSIÓN")
st.markdown("""
Explora cómo la **diversificación** reduce el riesgo al combinar activos de distintos sectores.  
Selecciona dos acciones, visualiza su comportamiento y analiza la relación entre riesgo y rentabilidad.
""")

# -----------------------------------------------------------
# MENÚ LATERAL
# -----------------------------------------------------------
st.sidebar.header("⚙️ Controles de análisis")

# Selección de acciones (puedes elegir cualquiera de Yahoo Finance)
ticker1 = st.sidebar.text_input("Primera acción (ejemplo: AAPL)", value="AAPL")
ticker2 = st.sidebar.text_input("Segunda acción (ejemplo: KO)", value="KO")

# Fechas de análisis
fecha_inicio = st.sidebar.date_input("Fecha de inicio", pd.to_datetime("2022-01-01"))
fecha_fin = st.sidebar.date_input("Fecha final", pd.to_datetime("2025-01-01"))

# -----------------------------------------------------------
# BOTÓN PRINCIPAL
# -----------------------------------------------------------
if st.sidebar.button("🔍 Ejecutar análisis"):

    tickers = [ticker1.upper(), ticker2.upper()]
    st.subheader(f"📊 Acciones seleccionadas: {tickers}")

    # -----------------------------------------------------------
    # DESCARGA DE DATOS
    # -----------------------------------------------------------
    with st.spinner("Descargando datos desde Yahoo Finance..."):
        try:
            data = yf.download(tickers, start=fecha_inicio, end=fecha_fin)["Adj Close"]
            st.success("Datos descargados correctamente ✅")
        except Exception as e:
            st.error(f"Error al descargar los datos: {e}")
            st.stop()

    # Mostrar los últimos datos
    st.subheader("📊 Precios históricos ajustados")
    st.dataframe(data.tail())

    # -----------------------------------------------------------
    # CÁLCULO DE RENDIMIENTOS
    # -----------------------------------------------------------
    returns = data.pct_change().dropna()
    st.subheader("📈 Estadísticas de rentabilidad diaria")
    st.write(returns.describe())

    # -----------------------------------------------------------
    # MENÚ DE VISUALIZACIÓN
    # -----------------------------------------------------------
    opcion_vista = st.selectbox(
        "Selecciona el tipo de gráfico que deseas visualizar:",
        ("Evolución de precios", "Relación de rendimientos", "Matriz de correlación")
    )

    # -----------------------------------------------------------
    # GRÁFICOS
    # -----------------------------------------------------------
    if opcion_vista == "Evolución de precios":
        st.subheader("📉 Evolución del precio de las acciones")
        fig, ax = plt.subplots(figsize=(8, 4))
        data.plot(ax=ax)
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio ajustado (USD)")
        ax.legend(tickers)
        st.pyplot(fig)

    elif opcion_vista == "Relación de rendimientos":
        st.subheader("🔗 Relación entre los rendimientos (correlación)")
        fig2, ax2 = plt.subplots(figsize=(5, 5))
        ax2.scatter(returns[tickers[0]], returns[tickers[1]], alpha=0.6, color="teal")
        ax2.set_xlabel(f"Rendimiento diario de {tickers[0]}")
        ax2.set_ylabel(f"Rendimiento diario de {tickers[1]}")
        ax2.set_title(f"Diversificación: {tickers[0]} vs {tickers[1]}")
        st.pyplot(fig2)

    elif opcion_vista == "Matriz de correlación":
        st.subheader("📊 Matriz de correlación")
        correlacion = returns.corr()
        st.write(correlacion.style.background_gradient(cmap="coolwarm").format("{:.2f}"))

    # -----------------------------------------------------------
    # INTERPRETACIÓN FINAL
    # -----------------------------------------------------------
    st.markdown("""
    ---
    ### 💡 Interpretación
    - Si la **correlación** entre las dos acciones es **baja o negativa**, significa que no se mueven igual:
      cuando una baja, la otra puede subir o mantenerse estable.  
    - Esto **reduce el riesgo total del portafolio** y demuestra la utilidad de la **diversificación**.

    **Conclusión:**  
    Combinar activos de sectores distintos genera un portafolio más estable frente a la volatilidad del mercado.
    """)

else:
    st.info("👈 Completa los campos y presiona **Ejecutar análisis** para comenzar.")

