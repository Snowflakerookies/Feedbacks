import requests
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import streamlit as st

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

#Componente de Streamlit para mostrar el logo, situado en la carpeta del proyectro y siendo referenciado mediante su nombre.
st.image("stemdoLOGO.png", caption=None, use_column_width="always")

st.title("FEEDBACK")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True

#Pedimos al usuario que introduzca su correo y comprobamos que exista en la lista de emails obtenidos de la API. 
# Si existe nos redirige a la pagina para dar feedback. En caso de no encontrarlo se muestra al usuario un aviso por pantalla.
st.session_state.ratingUser = st.text_input("Introduzca su email de Stemdo", "")

if st.button("Dar Feedback"):
    if st.session_state.ratingUser:
        if st.session_state.ratingUser in users_mails:
            st.switch_page("pages/feedback_page.py")
        else:
            st.error("Error, no se ha encontrado un usuario con ese email, reviselo y vuelva a intentarlo")
    else:
        st.error("Por favor, introduzca su email corporativo")
