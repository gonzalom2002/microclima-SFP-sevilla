import streamlit as st
import plotly.graph_objects as go
import requests
import time
import pandas as pd

st.set_page_config(page_title="Microclima en Sevilla", layout="wide")

st.title("🌿 v3 Microclima de invernadero automatizado. NASA Space Apps (4 octubre 2025)")
st.markdown("Con datos en tiempo real de la NASA POWER API, mostramos la simulación meteorológica de Sevilla. Los gráficos se actualizan cada segundo.")

API_URL = "https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,WS2M,RH2M&community=AG&longitude=-5.9845&latitude=37.3891&start=20251004&end=20251004&format=JSON"
REFRESH_INTERVAL = 1  # seconds

def fetch_nasa_power():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        # Parse the hourly data
        hours = list(data["properties"]["parameter"]["T2M"].keys())
        temp = list(data["properties"]["parameter"]["T2M"].values())
        wind = list(data["properties"]["parameter"]["WS2M"].values())
        hum = list(data["properties"]["parameter"]["RH2M"].values())
        df = pd.DataFrame({
            "Hora": hours,
            "Temperatura (°C)": temp,
            "Viento (m/s)": wind,
            "Humedad (%)": hum,
        })
        return df
    except Exception as e:
        st.error(f"Error obteniendo datos de NASA POWER: {e}")
        return pd.DataFrame({"Hora": [], "Temperatura (°C)": [], "Viento (m/s)": [], "Humedad (%)": []})

# Real-time simulation: update every second
if "last_run" not in st.session_state or time.time() - st.session_state["last_run"] > REFRESH_INTERVAL:
    st.session_state["df"] = fetch_nasa_power()
    st.session_state["last_run"] = time.time()
    st.experimental_rerun()

df = st.session_state.get("df", pd.DataFrame({"Hora": [], "Temperatura (°C)": [], "Viento (m/s)": [], "Humedad (%)": []}))

if not df.empty:
    # Find the value with the fastest change in one hour
    df["ΔTemp"] = df["Temperatura (°C)"].diff().abs()
    df["ΔViento"] = df["Viento (m/s)"].diff().abs()
    df["ΔHumedad"] = df["Humedad (%)"].diff().abs()
    fastest_var = max(df["ΔTemp"].max(), df["ΔViento"].max(), df["ΔHumedad"].max())
    if fastest_var == df["ΔViento"].max():
        var_name = "Viento (m/s)"
    elif fastest_var == df["ΔTemp"].max():
        var_name = "Temperatura (°C)"
    else:
        var_name = "Humedad (%)"
    st.info(f"La variable meteorológica que cambia más rápido durante la hora es: **{var_name}**, con una variación máxima de {fastest_var:.2f} unidades.")

    # Plotting
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x=df["Hora"], y=df["Temperatura (°C)"], mode="lines+markers", name="Temperatura", line=dict(color="red")))
    fig_temp.update_layout(title="🌡️ Temperatura horaria", xaxis_title="Hora", yaxis_title="°C")
    st.plotly_chart(fig_temp, use_container_width=True)

    fig_wind = go.Figure()
    fig_wind.add_trace(go.Scatter(x=df["Hora"], y=df["Viento (m/s)"], mode="lines+markers", name="Viento", line=dict(color="blue")))
    fig_wind.update_layout(title="💨 Viento horario", xaxis_title="Hora", yaxis_title="m/s")
    st.plotly_chart(fig_wind, use_container_width=True)

    fig_hum = go.Figure()
    fig_hum.add_trace(go.Scatter(x=df["Hora"], y=df["Humedad (%)"], mode="lines+markers", name="Humedad", line=dict(color="green")))
    fig_hum.update_layout(title="💧 Humedad horaria", xaxis_title="Hora", yaxis_title="%")
    st.plotly_chart(fig_hum, use_container_width=True)

    st.markdown("✅ Esta simulación en tiempo real te ayuda a ajustar ventilación, riego y luz artificial en el invernadero, según los datos meteorológicos más cambiantes.")
else:
    st.warning("No se pudieron obtener datos de NASA POWER para la visualización.")
