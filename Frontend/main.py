import requests
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import streamlit as st
import base64

# Función para cargar y codificar la imagen en base64
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

# Ruta a la imagen
image_path = "stemdoLOGO.png"

# Cargar y codificar la imagen
encoded_image = load_image(image_path)

# HTML con la imagen en base64
html_code_image = f"""
<div style="display: flex; justify-content: center;">
    <img src="data:image/png;base64,{encoded_image}" style="max-width: 100%; height: auto;">
</div>
"""

with open(".streamlit/styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#Direccion de la API
API_CALL = "http://localhost:8000"

# URL del endpoint de FastAPI.
url_mail = (f"{API_CALL}/trabajadores/email")

# Enviar solicitud al backend de FastAPI.
response = requests.get(url_mail)

# Mostrar error si lo hubiera en Streamlit.
if response.status_code != 200:
    st.error("Error en la solicitud")

#Creamos una lista con todos los emails obtenidos de la API.
users_mails = [email[0] for email in response.json()]

#Componente de Streamlit para mostrar el logo a través de un HTML
st.markdown(html_code_image, unsafe_allow_html=True)

st.title("FEEDBACK")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True

#Pedimos al usuario que introduzca su correo y comprobamos que exista en la lista de emails obtenidos de la API. 
# Si existe nos redirige a la pagina para dar feedback. En caso de no encontrarlo se muestra al usuario un aviso por pantalla.
st.session_state.ratingUser = st.text_input("Introduzca su email de Stemdo", "").lower()

if st.button("Dar Feedback"):
    if st.session_state.ratingUser:
        if st.session_state.ratingUser in users_mails:
            st.switch_page("pages/feedback_page.py")
        else:
            st.error("Error, no se ha encontrado un usuario con ese email, reviselo y vuelva a intentarlo")
    else:
        st.error("Por favor, introduzca su email corporativo")
