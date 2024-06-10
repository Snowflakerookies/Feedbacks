import requests
import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# URL del endpoint de FastAPI
url_mail = 'http://127.0.0.1:8000/trabajadores/email'

# Enviar solicitud POST al backend de FastAPI
response = requests.get(url_mail)

# Mostrar error si lo hubiera en Streamlit
if response.status_code != 200:
    st.error('Error en la solicitud')


users_mails = [email[0] for email in response.json()]

st.write(users_mails)

st.image('stemdoLOGO.png', caption=None, use_column_width='always')

st.title('FEEDBACK')


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True


st.session_state.ratingUser = st.text_input("Introduzca su email de Stemdo", "")

if st.button("Dar Feedback"):
    if st.session_state.ratingUser:
        if st.session_state.ratingUser in users_mails:
            st.switch_page("pages/feedback_page.py")
        else:
            st.error("Error, no se ha encontrado un usuario con ese email, reviselo y vuelva a intentarlo")
    else:
        st.error("Por favor, introduzca su email corporativo")

