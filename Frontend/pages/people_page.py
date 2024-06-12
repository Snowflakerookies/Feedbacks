import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
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

#Recuperamos el correo del usuario introducido en el main y se lo enviamos a la API para obtener el nombre asociado a ese correo.
rating_user = st.session_state.ratingUser
request_name_by_mail = requests.get(f"{API_CALL}/trabajadores/" + rating_user).json()
rating_user_name = f"{request_name_by_mail[0]} {request_name_by_mail[1]}"

st.title('PEOPLE')
st.header('Buenas ' + rating_user_name)

actions = ["Añadir trabajador", "Eliminar trabajador","Actualizar datos de un trabajador"]

action = st.selectbox(
    "¿Que accion deseas realizar",
    actions,
    index=None,
    placeholder="Seleccione la acción...",
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
    key="people_action",
)

