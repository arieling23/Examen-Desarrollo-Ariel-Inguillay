import streamlit as st # type: ignore
import requests # type: ignore

# URL del backend Flask
BACKEND_URL = "http://127.0.0.1:8008"

st.title("Clasificador de Textos")

# Input para código y texto
code = st.number_input("Código", min_value=0, step=1)
text = st.text_input("Texto")

if st.button("Clasificar"):
    if text and code:
        # Enviar datos al backend Flask
        response = requests.post(f"{BACKEND_URL}/classify", json={"code": code, "value": text})
        if response.status_code == 200:
            data = response.json()
            st.write(f"Código: {data['code']}, Respuesta: {data['label']}")
        else:
            st.error("Error al clasificar el texto")

# Mostrar historial
if st.button("Mostrar Historial"):
    history_response = requests.get(f"{BACKEND_URL}/history")
    if history_response.status_code == 200:
        history = history_response.json()
        for item in history:
            st.write(f"Código: {item['code']}, Respuesta: {item['label']}")
    else:
        st.error("Error al obtener el historial")
