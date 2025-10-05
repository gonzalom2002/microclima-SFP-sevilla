try:
    response = requests.get(url, timeout=10)  # Añade timeout para evitar bloqueos largos
    response.raise_for_status()  # Lanza excepción si el código de estado no es 200

    data = response.json()

    # Verifica que los datos esperados estén presentes
    if "properties" in data and "parameter" in data["properties"]:
        records = data["properties"]["parameter"]
        dates = list(records["T2M"].keys())

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
        st.warning("La respuesta de la API no contiene los datos esperados. Intenta más tarde o revisa los parámetros.")

except requests.exceptions.Timeout:
    st.error("⏱️ La solicitud a la API tardó demasiado. Verifica tu conexión o intenta más tarde.")

except requests.exceptions.HTTPError as err:
    st.error(f"❌ Error HTTP al consultar la API: {err}")

except requests.exceptions.RequestException as err:
    st.error(f"⚠️ Error de conexión con la API: {err}")

except Exception as e:
    st.error(f"🚨 Ocurrió un error inesperado: {e}")
