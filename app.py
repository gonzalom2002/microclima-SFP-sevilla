
import streamlit as st
import plotly.graph_objects as go
import json

st.set_page_config(page_title="Microclima en Sevilla", layout="wide")

st.title("🌿 Simulación de Microclima para Invernadero en Sevilla (Septiembre 2025)")
st.markdown("Esta aplicación muestra cómo los datos meteorológicos simulados pueden ayudar a controlar un microclima para cultivar vegetales esenciales para 10 personas.")

def cargar_datos(nombre_archivo):
    with open(nombre_archivo, "r") as f:
        return json.load(f)

def graficar_temperatura(datos):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=datos["fecha"], y=datos["temperatura_max"], mode="lines+markers", name="Máxima", line=dict(color="red")))
    fig.add_trace(go.Scatter(x=datos["fecha"], y=datos["temperatura_min"], mode="lines+markers", name="Mínima", line=dict(color="blue")))
    fig.update_layout(title="🌡️ Temperatura diaria", xaxis_title="Fecha", yaxis_title="°C")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("Las temperaturas afectan el crecimiento de tomates, espinacas y legumbres. Se recomienda mantener el invernadero entre 18°C y 28°C.")

def graficar_humedad(datos):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=datos["fecha"], y=datos["humedad"], name="Humedad", marker_color="skyblue"))
    fig.update_layout(title="💧 Humedad relativa diaria", xaxis_title="Fecha", yaxis_title="%")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("La humedad es clave para evitar enfermedades en cultivos de hoja como espinacas. Se recomienda mantenerla entre 60% y 80%.")

def graficar_radiacion(datos):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=datos["fecha"], y=datos["radiacion"], name="Radiación solar", marker_color="orange"))
    fig.update_layout(title="☀️ Radiación solar diaria", xaxis_title="Fecha", yaxis_title="W/m²")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("La radiación solar influye en la fotosíntesis. Para cultivos como tomates y pimientos, se recomienda al menos 200 W/m² diarios.")

# Cargar y mostrar los gráficos
graficar_temperatura(cargar_datos("grafico_temperatura.json"))
graficar_humedad(cargar_datos("grafico_humedad.json"))
graficar_radiacion(cargar_datos("grafico_radiacion.json"))

st.markdown("✅ Ajusta el microclima del invernadero con ventilación, riego y luz artificial según estos datos.")
