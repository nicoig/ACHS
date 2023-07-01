

# Para crear el requirements.txt ejecutamos 
# pipreqs --encoding=utf8 --force

# Primera Carga a Github
# git init
# git add .
# git commit -m "primer commit"
# git remote add origin https://github.com/nicoig/ACHS.git
# git push -u origin master

# Actualizar Repo de Github
# git add .
# git commit -m "Se actualizan las variables de entorno"
# git push origin master

# Para eliminar un repo cargado
# git remote remove origin

# En Render
# agregar en variables de entorno
# PYTHON_VERSION = 3.9.12

###############################################################





import streamlit as st
from streamlit_chat import message
import os
from dotenv import load_dotenv
from judini.agent import Agent
load_dotenv()

# Configuración del título y el encabezado de la página
st.set_page_config(
    page_title="Asistente ACHS", 
    page_icon=":robot_face:")

# Estableciendo el logo de ACHS
st.image("img/logo_mundo.png", width=300)

# Título y descripción
st.subheader("Asistente Virtual ACHS")
st.markdown("""
<p style='font-size: 15px;'>
Este es un asistente virtual diseñado para responder a todas tus consultas relacionadas con la Asociación Chilena de Seguridad (ACHS). 
Puedo ayudarte con temas como: Seguridad laboral, Procesos de la ACHS, Normativas y reglamentos, 
Servicios que ofrece la ACHS, y cualquier otra pregunta que puedas tener acerca de la ACHS.
Por favor, escribe tu pregunta y me pondré a trabajar para darte la mejor respuesta posible.
</p>
""", unsafe_allow_html=True)

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "Eres un experto en la Asociación Chilena de Seguridad (ACHS), con un profundo entendimiento y conocimiento exhaustivo de todos los aspectos relacionados con esta institución. Tienes la capacidad para analizar y explicar en detalle las leyes laborales, políticas de seguridad, procedimientos de prevención, y todo lo que abarque la salud ocupacional en Chile. Tu objetivo es recibir consultas del usuario, analizar la información proporcionada y generar un resumen conciso y claro que pueda ser comprendido en un lapso de dos minutos. Este resumen debe incluir los puntos más importantes, explicando cualquier concepto complejo de manera simple y directa. Tu contenido será transformado en un video por otra IA, por lo que tu redacción debe ser clara, directa y visualmente descriptiva para facilitar este proceso Se amable y basa todo tu conocimiento en el contexto entregado"}
    ]

# generar una respuesta
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    api_key= os.getenv("JUDINI_API_KEY")
    agent_id= os.getenv("JUDINI_AGENT_ID_CHAT")

    agent = Agent(api_key, agent_id)

    response = agent.completion(prompt)  # Aquí cambiamos para que el prompt sea la entrada del usuario
    st.session_state['messages'].append({"role": "assistant", "content": response})

    total_tokens = 0
    prompt_tokens = 0
    completion_tokens = 0
    return response, total_tokens, prompt_tokens, completion_tokens

# contenedor para el historial de chat
response_container = st.container()

# contenedor para cuadro de texto
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Escribe tu solicitud:", key='input', height=100)
        submit_button = st.form_submit_button(label='Enviar')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

# Estableciendo la franja superior
st.image("img/franja_inferior.png")
