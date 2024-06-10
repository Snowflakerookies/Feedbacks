import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import os

rating_user = st.session_state.ratingUser
request_name_by_mail = requests.get("http://localhost:8000/trabajadores/" + rating_user).json()
rating_user_name = f"{request_name_by_mail[0]} {request_name_by_mail[1]} {request_name_by_mail[2]}"

request_users_names = requests.get("http://localhost:8000/trabajadores/name").json()
users_names = list(map(lambda name: ' '.join(filter(None, name)), request_users_names))


current_date = datetime.now().strftime("%d-%m-%y")
current_directory = os.getcwd()

if "feedback_df" not in st.session_state:
    st.session_state.feedback_df = pd.DataFrame(columns=["Usuario",
                                                        "Usuario valorado",
                                                        "Skills",
                                                        "Descripción skills",
                                                        "Teamwork",
                                                        "Descripción teamwork",
                                                        "Empathy",
                                                        "Descripción empathy",
                                                        "Motivation",
                                                        "Descripción motivation"])

st.image('stemdoLOGO.png', caption=None, use_column_width='always')

st.title('FEEDBACK')
st.header('Buenas ' + rating_user_name)


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True

if st.session_state.ratingUser:
    st.session_state.disabled = False
    
    ratedUser = st.selectbox(
        "Usuario a valorar:",
        [user for user in users_names if user != rating_user_name],
        index=None,
        placeholder="Seleccione su nombre...",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        key="ratedUser",
    )

    #get_rated_user_mail = lambda username: requests.get(f"http://localhost:8000/trabajadores/{'/'.join(username.lower().split())}").json()
    #rated_user_mail = get_rated_user_mail(ratedUser)
    #st.write(rated_user_mail)
    
    if st.session_state.ratedUser:
        
        st.subheader('Skills')
        rateSkills = st.slider("Valoración skills", 1, 5)
        descriptionSkills = st.text_area(
            "¿En qué te basas para dar esa puntuación de Skills?:",
            None,
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Argumenta tu respuesta...",
            )
        
        st.subheader('Teamwork')
        rateTeamwork = st.slider("Valoración teamwork", 1, 5)
        descriptionTeamWork = st.text_area(
            "¿En qué te basas para dar esa puntuación de teamwork?:",
            "",
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Argumenta tu respuesta...",
            )

        st.subheader('Empathy')
        rateEmpathy = st.slider("Valoración empathy", 1, 5)
        descriptionEmpathy = st.text_area(
            "¿En qué te basas para dar esa puntuación de empathy?:",
            "",
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Argumenta tu respuesta...",
            )

        st.subheader('Motivation')
        rateMotivation = st.slider("Valoración motivation", 1, 5)
        descriptionMotivation = st.text_area(
            "¿En qué te basas para dar esa puntuación de motivation?:",
            "",
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                placeholder="Argumenta tu respuesta...",
            )
            
        if st.button('Enviar'):
            # Crear un nuevo DataFrame con los datos ingresados
            if descriptionSkills != '' and descriptionTeamWork != '' and descriptionEmpathy != '' and descriptionMotivation != '':
                feedback_df = pd.DataFrame({
                "Fecha": current_date,
                "Usuario": [st.session_state.ratingUser],
                "Usuario valorado": [st.session_state.ratedUser],
                "Skills": [rateSkills],
                "Descripción skills": [descriptionSkills],
                "Teamwork": [rateTeamwork],
                "Descripción teamwork": [descriptionTeamWork],
                "Empathy": [rateEmpathy],
                "Descripción empathy": [descriptionEmpathy],
                "Motivation": [rateMotivation],
                "Descripción motivation": [descriptionMotivation]
            })
                st.write(feedback_df.to_json())
                send_feedback = requests.post("http://localhost:8000/feedback/", json=feedback_df.to_json())
                
                if send_feedback.status_code == 200:
                    st.success("Feedback enviado exitosamente!")
                else:
                    st.error("Error al enviar el feedback")
                
            else:
                st.error("Por favor, rellene todos los campos")


if not st.session_state.ratingUser:
    st.session_state.disabled = True

