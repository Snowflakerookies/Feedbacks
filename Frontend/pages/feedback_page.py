import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json

import streamlit as st

with open(".streamlit/styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

rating_user = st.session_state.ratingUser
request_name_by_mail = requests.get("http://localhost:8000/trabajadores/" + rating_user).json()
rating_user_name = f"{request_name_by_mail[0]} {request_name_by_mail[1]} {request_name_by_mail[2]}"
request_users_names = requests.get("http://localhost:8000/trabajadores/name").json()
users_names = list(map(lambda name: ' '.join(filter(None, name)), request_users_names))
current_date = datetime.now().strftime("%Y-%m-%d")
current_directory = os.getcwd()

parse_rated_user_link = lambda data: "/".join([parte.replace(" ", "%20") if parte is not None else "" for parte in data[:2]]) + "?TRABAJADOR_APELLIDO2=" + (data[2].replace(" ", "%20") if data[2] is not None else "")

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
    
    if st.session_state.ratedUser:
        
        def buscar_registro(data, nombre_completo):
            # Dividir el nombre completo en partes
            partes_nombre = nombre_completo.split()
            
            # Inicializar una variable para almacenar la coincidencia encontrada
            coincidencia_encontrada = None
            
            # Contar el número de coincidencias
            numero_de_coincidencias = 0
            
            # Recorrer la lista de registros y buscar la coincidencia
            for registro in data:
                # Verificar si el registro es None o contiene valores None
                if registro is None:
                    continue
                
                # Crear una lista plana del registro, reemplazando None con una cadena vacía
                registro_flat = [parte if parte is not None else "" for parte in registro]
                
                # Unir las partes del registro en una sola cadena para comparar
                registro_completo = ' '.join(registro_flat)
                
                # Verificar si todas las partes del nombre completo están en el registro
                if all(parte in registro_completo for parte in partes_nombre):
                    numero_de_coincidencias += 1
                    coincidencia_encontrada = registro
                    
                    # Si se ha encontrado más de una coincidencia, continuar buscando
                    if numero_de_coincidencias > 1:
                        break
            
            # Si se encontró exactamente una coincidencia, devolverla
            if numero_de_coincidencias == 1:
                return coincidencia_encontrada
            else:
                # Si no se encontró ninguna coincidencia o se encontraron múltiples coincidencias
                return None
        
        #limitar la busqueda al registro que encuentr primero (1), si hay varios entonces que busque ahí
        rated_user_reg = buscar_registro(request_users_names, ratedUser)
        
        if rated_user_reg:
            rated_user_json = json.dumps(rated_user_reg)
            data = json.loads(rated_user_json)
            rated_user_link = parse_rated_user_link(data)
            request_rated_user_mail = requests.get("http://localhost:8000/trabajadores/" + rated_user_link).json()
            rated_user_mail = request_rated_user_mail['email'][0]
        else:
            st.error("Registro no encontrado")
        
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
                "FECHA": [current_date],
                "PUNT_SKILLS": [int(rateSkills)],
                "DESC_SKILLS": [str(descriptionSkills)],
                "PUNT_TEAMWORK": [int(rateTeamwork)],
                "DESC_TEAMWORK": [str(descriptionTeamWork)],
                "PUNT_EMPATHY": [int(rateEmpathy)],
                "DESC_EMPATHY": [str(descriptionEmpathy)],
                "PUNT_MOTIVATION": [int(rateMotivation)],
                "DESC_MOTIVATION": [str(descriptionMotivation)],
                "EMAIL_EVALUADOR": [str(rating_user)],
                "EMAIL_EVALUADO": [str(rated_user_mail)]
            })

                feedback_json = feedback_df.to_json(orient='records').strip("[]")
                send_feedback = requests.post("http://localhost:8000/feedback/", data=feedback_json)
                
                if send_feedback.status_code == 200:
                    st.success("Feedback enviado exitosamente!")
                else:
                    st.error("Error al enviar el feedback")
                
            else:
                st.error("Por favor, rellene todos los campos")


if not st.session_state.ratingUser:
    st.session_state.disabled = True

