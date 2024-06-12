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

#Obtenemos de la API una lista de todos los nombres de los usuarios en la DB para mostrarlos en el desplegable 
# en el cual se va a elegir a que usuario damos el feedback.
request_users_names = requests.get(f"{API_CALL}/trabajadores/name").json()
users_names = list(map(lambda name: ' '.join(filter(None, name)), request_users_names))

#Obtenemos la fecha actual del sistema y la formateamos para añadirla al feedback que enviamos.
current_date = datetime.now().strftime("%Y-%m-%d")

#Componente de Streamlit para mostrar el logo a través de un HTML
st.markdown(html_code_image, unsafe_allow_html=True)

st.title('FEEDBACK')
st.header('Buenas ' + rating_user_name)


if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True

#Comprobamos que hay un usuario que va a mandar un feedback, en caso de no haberlo no se visualiza el formulario y 
# se muestra un error al usuario indicandole que vuelva a la pantalla principal. 
#De esta manera controlamos que haya un usuario valorador y que no se haya accedido al formulario de feedback 
# directamente desde su URL.
if st.session_state.ratingUser:
    st.session_state.disabled = False
    
    ratedUser = st.selectbox(
        "Usuario a valorar:",
        [user for user in users_names if user != rating_user_name],
        index=None,
        placeholder="Seleccione el usuario al que quiere dar feedback...",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        key="ratedUser",
    )
    
    #Una vez seleccionado el usuario a valorar, se muestra el formulario.
    if st.session_state.ratedUser:
        with st.form("my_form"):
            
            st.subheader('Skills 🛠️')
            rateSkills = st.slider("Valoración skills", 1, 5)
            descriptionSkills = st.text_area(
                "¿En qué te basas para dar esa puntuación de Skills?:",
                None,
                label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    placeholder="Argumenta tu respuesta...",
                )
            
            st.subheader('Teamwork 🤝')
            rateTeamwork = st.slider("Valoración teamwork", 1, 5)
            descriptionTeamWork = st.text_area(
                "¿En qué te basas para dar esa puntuación de teamwork?:",
                "",
                label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    placeholder="Argumenta tu respuesta...",
                )

            st.subheader('Empathy ❤️')
            rateEmpathy = st.slider("Valoración empathy", 1, 5)
            descriptionEmpathy = st.text_area(
                "¿En qué te basas para dar esa puntuación de empathy?:",
                "",
                label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    placeholder="Argumenta tu respuesta...",
                )

            st.subheader('Motivation 💪')
            rateMotivation = st.slider("Valoración motivation", 1, 5)
            descriptionMotivation = st.text_area(
                "¿En qué te basas para dar esa puntuación de motivation?:",
                "",
                label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                    placeholder="Argumenta tu respuesta...",
                )
            
            
            #En la BD se contempla el email del usuario valorado, no su nombre. Para obtenerlo realizamos una llamada
            # a la API la cual nos devuelve el email asociado a un nombre completo, el cual enviamos sin espacios 
            # parseandolo previamente mediante un .replace().
            parse_rated_user_link = lambda data: data.replace(" ", "")
            rated_user_link = parse_rated_user_link(ratedUser)
            request_rated_user_mail = requests.get(f"{API_CALL}/trabajadores/json/email/" + rated_user_link).json()
            rated_user_mail = request_rated_user_mail['email']

            #Cuando creamos un formulario obligatoriamente debe haber un boton de submit
            submitted = st.form_submit_button("Enviar")
            
            #Creamos un nuevo DataFrame con los datos ingresados a partir del cual obtendremos un JSON. Los datos de  
            # este JSON los enviamos a la BD mediante una llamada POST a la API.
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
                
                if submitted:
                    feedback_json = feedback_df.to_json(orient='records').strip("[]")
                    send_feedback = requests.post(f"{API_CALL}/feedback/", data=feedback_json)
                    
                    #Se notifica al usuario si se ha enviado el feedback a la BD correctamente o no.
                    if send_feedback.status_code == 200:
                        st.success("Feedback enviado exitosamente!")
                    else:
                        st.error("Error al enviar el feedback")
            else:
                #Si queda algun campo por rellenar, se le indica al usuario ya que es obligatorio.
                if submitted:
                    st.error("Por favor, rellene todos los campos")
else:
    st.session_state.disabled = True
    st.error("Error, por favor vuelva a la página de inicio.")
