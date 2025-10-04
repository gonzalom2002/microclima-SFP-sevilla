import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Microclima en Sevilla en Tiempo Real", layout="wide")

# Título y bienvenida
st.title("🌱 Microclima en Sevilla - Datos en Tiempo Real desde NASA POWER")
st.markdown("""
Bienvenidos a esta aplicación interactiva desarrollada por estudiantes del colegio como parte del proyecto de sostenibilidad y tecnología aplicada.  
Aquí consultamos datos meteorológicos reales desde la API de **NASA POWER** para visualizar las condiciones actuales en **Sevilla, España**, y entender cómo afectan al cultivo de vegetales esenciales para la supervivencia humana.  
""")

# Coordenadas de Sevilla
lat, lon = 37.3886, -5.9953

# Fechas para el rango de datos (últimos 7 días)
end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=6)

# Parámetros meteorológicos: temperatura, humedad, radiación solar
parameters = "T2M,RH2M,ALLSKY_SFC_SW_DWN"

# URL de la API de NASA POWER
url = (
    f"https://power.larc.nasa.gov/api/temporal/daily/point?"
    f"start={start_date.strftime('%Y%m%d')}&end={end_date.strftime('%Y%m%d')}"
    f"&latitude={lat}&longitude={lon}"
    f"&parameters={parameters}&community=AG&format=JSON"
)

# Solicitud a la API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    records = data["properties"]["parameter"]
    dates = list(records["T2M"].keys())

    # Crear DataFrame
    df = pd.DataFrame({
        "Fecha": pd.to_datetime(dates),
        "🌡️ Temperatura (°C)": list(records["T2M"].values()),
        "💧 Humedad relativa (%)": list(records["RH2M"].values()),
        "☀️ Radiación solar (W/m²)": list(records["ALLSKY_SFC_SW_DWN"].values())
    })

    # Mostrar gráficos
    st.subheader("🌡️ Temperatura diaria")
    fig_temp = px.line(df, x="Fecha", y="🌡️ Temperatura (°C)", markers=True)
    st.plotly_chart(fig_temp, use_container_width=True)

    st.subheader("💧 Humedad relativa diaria")
    fig_hum = px.line(df, x="Fecha", y="💧 Humedad relativa (%)", markers=True)
    st.plotly_chart(fig_hum, use_container_width=True)

    st.subheader("☀️ Radiación solar diaria")
    fig_rad = px.line(df, x="Fecha", y="☀️ Radiación solar (W/m²)", markers=True)
    st.plotly_chart(fig_rad, use_container_width=True)

else:
    st.error("No se pudo obtener datos en tiempo real desde la API de NASA POWER.")

# Sección final del proyecto
st.markdown("""
---

### 🔧 Próximo paso del proyecto escolar

En la siguiente fase, adaptaremos estos datos reales al control físico de un **invernadero escolar** mediante prototipos construidos con:

- **Arduino** como unidad de control
- **Sensores de humedad ambiental y del suelo**
- **Sensores de temperatura**
- **Servomotores** para abrir o cerrar ventilaciones
- **Ventiladores y calefactores** para regular el clima interno

El objetivo es crear un sistema automatizado que mantenga las condiciones óptimas para cultivar vegetales como tomates, espinacas, patatas y legumbres, suficientes para alimentar a 10 personas.

Este proyecto combina ciencia, tecnología y sostenibilidad, y nos prepara para desafíos reales como el diseño de hábitats autosuficientes en la Tierra o en futuras misiones espaciales 🚀🌍
""")
