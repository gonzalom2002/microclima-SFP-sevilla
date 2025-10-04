import requests
import pandas as pd
import json
import time
from datetime import datetime

# Coordenadas de Sevilla
lat, lon = 37.3886, -5.9953

# Parámetros meteorológicos: temperatura, humedad, radiación solar
parameters = "T2M,RH2M,ALLSKY_SFC_SW_DWN"

# Función para consultar la API de NASA POWER y guardar los datos
def actualizar_datos():
    fecha_actual = datetime.utcnow().date()

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"start={fecha_actual.strftime('%Y%m%d')}&end={fecha_actual.strftime('%Y%m%d')}"
        f"&latitude={lat}&longitude={lon}"
        f"&parameters={parameters}&community=AG&format=JSON"
    )

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        registros = data["properties"]["parameter"]
        fechas = list(registros["T2M"].keys())

        df = pd.DataFrame({
            "Fecha": pd.to_datetime(fechas),
            "Temperatura (°C)": list(registros["T2M"].values()),
            "Humedad relativa (%)": list(registros["RH2M"].values()),
            "Radiación solar (W/m²)": list(registros["ALLSKY_SFC_SW_DWN"].values())
        })

        # Guardar como CSV y JSON sobrescribiendo los anteriores
        df.to_csv("datos_climaticos_sevilla.csv", index=False)
        df.to_json("datos_climaticos_sevilla.json", orient="records", date_format="iso")

        print(f"✅ Datos actualizados correctamente a las {datetime.now().strftime('%H:%M:%S')}")
    else:
        print("❌ Error al consultar la API de NASA POWER.")

# Ejecutar la actualización cada minuto
while True:
    actualizar_datos()
    time.sleep(60)
