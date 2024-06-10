import streamlit as st
import pandas as pd
from datetime import datetime
import os

users_mails = "peticion a la api"


st.image('stemdoLOGO.png', caption=None, use_column_width='always')

st.title('FEEDBACK')


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True
    


st.session_state.ratingUser = st.text_input("Introduzca su email de Stemdo", "")

if st.button("Dar Feedback"):
    if st.session_state.ratingUser:
        if st.session_state.ratingUser not in users_mails:
            st.switch_page("pages/feedback_page.py")
        else:
            st.error("Error, no se ha encontrado un usuario con ese email, reviselo y vuelva a intentarlo")
    else:
        st.error("Por favor, introduzca su email corporativo")


