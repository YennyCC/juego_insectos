import streamlit as st
import random
import time
from PIL import Image
import base64
import os

# -------- FONDO PERSONALIZADO --------
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("fondo.jpg")

# ---- ESTILOS PERSONALIZADOS Y RESPONSIVOS ----
st.markdown("""
    <style>
    html, body, .stApp {
        max-width: 100%;
        overflow-x: hidden;
        padding: 0;
        margin: 0;
        color: white !important;
    }

    /* Contenedor principal */
    .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }

    /* Título */
    h1 {
        font-size: 2.5rem;
        text-align: center;
        color: white;
        text-shadow: 2px 2px 4px black;
    }

    /* Texto de pregunta */
    .pregunta {
        font-size: 22px;
        font-weight: bold;
        color: white;
        margin: 1em 0;
        text-align: center;
    }

    /* Imagen del insecto */
    div.stImage > img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        max-width: 100%;
        width: 220px;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
    }

    /* Botones */
    button[kind="primary"] {
        display: block;
        margin: 0.5em auto;
    }

    /* Opciones radio centradas y en blanco */
    div[data-baseweb="radio"] {
        color: white;
    }
    div[data-baseweb="radio"] label {
        color: white !important;
        font-size: 16px;
        padding: 4px 0;
    }

    /* Responsive en móviles */
    @media screen and (max-width: 480px) {
        h1 {
            font-size: 2rem;
        }

        .pregunta {
            font-size: 18px;
        }

        div.stImage > img {
            width: 180px;
        }

        label {
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)


# -------- TÍTULO --------
st.markdown("""
<h1 style='
    text-align: center;
    color: #ffffff;
    font-size: 3rem;
    font-family: "Comic Sans MS", cursive;
    text-shadow: 2px 2px 4px #000000;
    margin-bottom: 2rem;
'>
    🐞 Adivina el insecto 
</h1>
""", unsafe_allow_html=True)

# Datos
# Lista de insectos con sus rutas de imagen y órdenes
insectos = [
    {"nombre": "Mariposa", "orden": "Lepidoptera", "imagen": "siluetas/mariposa.png"},
    {"nombre": "Escarabajo", "orden": "Coleoptera", "imagen": "siluetas/escarabajo.png"},
    {"nombre": "Abeja", "orden": "Hymenoptera", "imagen": "siluetas/abeja.png"},
    {"nombre": "Libélula", "orden": "Odonata", "imagen": "siluetas/libelula.png"},
    {"nombre": "Chinche", "orden": "Hemiptera", "imagen": "siluetas/chinche.png"},
    {"nombre": "Mosquito", "orden": "Diptera", "imagen": "siluetas/mosquito.png"},
    {"nombre": "Saltamontes", "orden": "Orthoptera", "imagen": "siluetas/saltamontes.png"},
    {"nombre": "Cucaracha", "orden": "Blattodea", "imagen": "siluetas/cucaracha.png"},
    {"nombre": "Mantis", "orden": "Mantodea", "imagen": "siluetas/mantis.png"}

]

ordenes = sorted(list(set(i["orden"] for i in insectos)))

# ---- INICIALIZAR ESTADOS NECESARIOS ----
if "insecto_actual" not in st.session_state:
    st.session_state.insecto_actual = random.choice(insectos)

if "girando" not in st.session_state:
    st.session_state.girando = False

if "stop" not in st.session_state:
    st.session_state.stop = False

# ---- CONTENEDOR DE IMAGEN ----
imagen_placeholder = st.empty()

# ---- FUNCIÓN PARA MOSTRAR IMAGEN ACTUAL ----
def mostrar_imagen_actual():
    ruta = st.session_state.insecto_actual["imagen"]
    if os.path.exists(ruta):
        img = Image.open(ruta)
        imagen_placeholder.image(img, use_container_width=False)
    else:
        st.warning(f"⚠️ Imagen no encontrada: {ruta}")

# ---- BOTONES SIEMPRE PRESENTES ----
col1, col2 = st.columns(2, gap="large")
with col1:
    if st.button("🎯 Girar Ruleta") and not st.session_state.girando:
        st.session_state.girando = True
        st.session_state.stop = False
        st.rerun()  # rerun to enter the spinning loop

with col2:
    if st.button("🛑 Detener") and st.session_state.girando:
        st.session_state.stop = True

# ---- RULETA SPINNING ----
if st.session_state.girando:
    while not st.session_state.stop:
        st.session_state.insecto_actual = random.choice(insectos)
        mostrar_imagen_actual()
        time.sleep(0.07)  # adjust speed
    st.session_state.girando = False
    st.session_state.stop = False
    st.rerun()  # refresh to exit spinning loop

# ---- MOSTRAR IMAGEN FINAL SI NO ESTÁ GIRANDO ----
if not st.session_state.girando:
    mostrar_imagen_actual()


# -------- PREGUNTA --------
st.markdown('<div class="pregunta">¿A qué orden pertenece este insecto?</div>', unsafe_allow_html=True)

# -------- OPCIONES --------
orden_seleccionado = st.radio("", ordenes, key="orden_radio", horizontal=False)

# -------- COMPROBAR --------
if st.button("Comprobar"):
    actual = st.session_state.insecto_actual
    if orden_seleccionado == actual["orden"]:
        st.success(f"✅ ¡Correcto! Es un {actual['nombre']} ({actual['orden']})")
    else:
        st.error(f"❌ Incorrecto. Era un {actual['nombre']} ({actual['orden']})")

# -------- REINICIAR --------
if st.button("🔄 Reiniciar"):
    st.session_state.insecto_actual = random.choice(insectos)
    st.session_state.girando = False
    st.session_state.stop = False
    mostrar_imagen_actual()

