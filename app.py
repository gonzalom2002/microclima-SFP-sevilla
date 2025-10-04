import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go

st.set_page_config(page_title="Microclima en Sevilla", layout="wide")

# Título y bienvenida
st.title("🌱 Simulación de Microclima para Invernadero Escolar")
st.markdown("""
Bienvenidos a esta aplicación interactiva desarrollada por estudiantes del colegio como parte del proyecto de sostenibilidad y tecnología aplicada.  
Aquí simulamos las condiciones climáticas de **Sevilla en septiembre de 2025** para entender cómo afectan al cultivo de vegetales esenciales para la supervivencia humana.  
Este entorno virtual nos permite visualizar datos como **temperatura**, **humedad relativa** y **radiación solar**, y aprender cómo controlar un microclima en un invernadero escolar.
""")

# Función para cargar y mostrar gráficos
def mostrar_grafico(nombre_archivo, titulo):
    fig = pio.read_json(nombre_archivo)
    fig.update_layout(title=titulo)
    st.plotly_chart(fig, use_container_width=True)

# Mostrar los gráficos
mostrar_grafico("grafico_temperatura.json", "🌡️ Temperatura diaria en Sevilla (Septiembre 2025)")
mostrar_grafico("grafico_humedad.json", "💧 Humedad relativa diaria en Sevilla (Septiembre 2025)")
mostrar_grafico("grafico_radiacion.json", "☀️ Radiación solar diaria en Sevilla (Septiembre 2025)")

# Sección final del proyecto
st.markdown("""
---

### 🔧 Próximo paso del proyecto escolar

En la siguiente fase, adaptaremos estos datos simulados al control físico de un **invernadero escolar** mediante prototipos construidos con:

- **Arduino** como unidad de control
- **Sensores de humedad ambiental y del suelo**
- **Sensores de temperatura**
- **Servomotores** para abrir o cerrar ventilaciones
- **Ventiladores y calefactores** para regular el clima interno

El objetivo es crear un sistema automatizado que mantenga las condiciones óptimas para cultivar vegetales como tomates, espinacas, patatas y legumbres, suficientes para alimentar a 10 personas.

Este proyecto combina ciencia, tecnología y sostenibilidad, y nos prepara para desafíos reales como el diseño de hábitats autosuficientes en la Tierra o en futuras misiones espaciales 🚀🌍
""")
