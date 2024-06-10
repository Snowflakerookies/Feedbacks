import streamlit as st
import pandas as pd
from datetime import datetime
import os

ratingUser = st.session_state.ratingUser
users_names = ("Adrian", "Miguel", "Juanma", "Gonzalo", "Mariana", "Bella", "Diego", "Enrique", "Alejandro", "Juan", "Raul", "Angel")
current_date = datetime.now().strftime("%d-%m-%y")
csv_file_name = f"feedback_semanal_{current_date}.csv"
current_directory = os.getcwd()
csv_path = os.path.join(current_directory, csv_file_name)


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
st.header('Buenas ' + ratingUser)


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True

if st.session_state.ratingUser:
    st.session_state.disabled = False
    
    ratedUser = st.selectbox(
        "Usuario a valorar:",
        [user for user in users_names if user != st.session_state.ratingUser],
        index=None,
        placeholder="Seleccione su nombre...",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        key="ratedUser",
    )
    
    if st.session_state.ratedUser:
        
        st.subheader('Skills')
        rateSkills = st.slider("Valoración skills", 1, 5)
        descriptionSkills = st.text_area(
            "Descripción skills:",
            None,
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
                key="descriptionSkills",
            )
        
        st.subheader('Teamwork')
        rateTeamwork = st.slider("Valoración teamwork", 1, 5)
        descriptionTeamWork = st.text_area(
            "Descripción teamwork:",
            "",
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )

        st.subheader('Empathy')
        rateEmpathy = st.slider("Valoración empathy", 1, 5)
        descriptionEmpathy = st.text_area(
            "Descripción empathy:",
            "",
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )

        st.subheader('Motivation')
        rateMotivation = st.slider("Valoración motivation", 1, 5)
        descriptionMotivation = st.text_area(
            "Descripción motivation:",
            "",
            label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )

            
        if st.button('Submit'):
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
                st.success("Feedback enviado exitosamente!")
                st.write(feedback_df)
                feedback_df.to_csv(csv_path, index=False, mode='a', header=False)
                
                # Exportado a json para hacer la llamada a la url correspondiente de la API
                feedback_df.to_json()
                
            else:
                st.error("Por favor, rellene todos los campos")


if not st.session_state.ratingUser:
    st.session_state.disabled = True

