import streamlit as st
import random
import time
from PIL import Image
import base64
import os

# ---- CONFIGURACIÓN INICIAL ----
st.set_page_config(page_title="Adivina el insecto", layout="centered")

# ---- ESTADOS INICIALES ----
if "insecto_actual" not in st.session_state:
    st.session_state.insecto_actual = {}
if "girando" not in st.session_state:
    st.session_state.girando = False
if "stop" not in st.session_state:
    st.session_state.stop = False
if "puntos" not in st.session_state:
    st.session_state.puntos = 0
if "aciertos" not in st.session_state:
    st.session_state.aciertos = 0
if "historial" not in st.session_state:
    st.session_state.historial = []

# ---- FONDO PERSONALIZADO ----
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

# ---- CSS PERSONALIZADO ----
st.markdown("""
<style>
/* Image sizing */
div.stImage > img {
    display: block;
    margin: 0 auto;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
    width: 200px;
}

    /* Title styling */
    h1 {
        text-align: center;
        color: white;
        font-size: 2.2rem;
        font-family: "Comic Sans MS", cursive;
        text-shadow: 2px 2px 4px black;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }

    /* Image container styling */
div.stImage > img {
    display: block;
    margin: 0 auto;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
}

/* On very small screens */
@media screen and (max-width: 480px) {
    div.stImage > img {
        width: 160px;
    }
}

/* On large screens (desktops) */
@media screen and (min-width: 768px) {
    div.stImage > img {
        width: 180px;
    }
}

/* Container with image + buttons */
.image-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    margin-bottom: 1rem;
}

/* Button container below image */
.button-row {
    display: flex;
    justify-content: space-between;
    width: 220px;
    margin-top: 10px;
}

/* Adjust buttons for small screens */
@media screen and (max-width: 480px) {
    .button-row {
        width: 180px;
    }
}

    /* Question text */
    .pregunta {
        font-size: 22px;
        font-weight: bold;
        color: white;
        margin: 1em 0;
        text-align: center;
    }

    /* Radio options in white */
    div[data-baseweb="radio"] label {
        color: white !important;
        font-size: 16px;
    }

    /* Responsive label size */
    @media screen and (max-width: 480px) {
        .pregunta {
            font-size: 18px;
        }

        div[data-baseweb="radio"] label {
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>
    🐞 Adivina el insecto 🦋
</h1>
""", unsafe_allow_html=True)

# ---- DATOS ----
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

ordenes = ["Blattodea", "Coleoptera", "Diptera", "Hemiptera", "Hymenoptera", "Lepidoptera", "Mantodea", "Odonata", "Orthoptera"]

# ---- FUNCIONES ----
def mostrar_imagen():
    ruta = st.session_state.insecto_actual.get("imagen")
    if ruta and os.path.exists(ruta):
        img = Image.open(ruta)
        st.image(img, width=220)
    else:
        st.warning("⚠️ Imagen no encontrada")

def seleccionar_insecto():
    st.session_state.insecto_actual = random.choice(insectos)

# ---- INTERFAZ PRINCIPAL ----
if not st.session_state.girando:
    if not st.session_state.insecto_actual:
        seleccionar_insecto()
    mostrar_imagen()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎯 Girar Ruleta"):
            st.session_state.girando = True
            st.session_state.stop = False
            st.rerun()

    with col2:
        st.button("🛑 Detener", disabled=True)
else:
    imagen_placeholder = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        st.button("🎯 Girando...", disabled=True)
    with col2:
        if st.button("🛑 Detener"):
            st.session_state.stop = True

    for _ in range(40):
        if st.session_state.stop:
            break
        st.session_state.insecto_actual = random.choice(insectos)
        ruta = st.session_state.insecto_actual["imagen"]
        if os.path.exists(ruta):
            img = Image.open(ruta)
            imagen_placeholder.image(img, width=220)
        time.sleep(0.07)
    st.session_state.girando = False
    st.rerun()

# ---- PREGUNTA Y RESPUESTA ----
st.markdown('<div class="pregunta">¿A qué orden pertenece este insecto?</div>', unsafe_allow_html=True)
orden_seleccionado = st.radio("", ordenes, key="orden_radio")

if st.button("Comprobar"):
    actual = st.session_state.insecto_actual
    if orden_seleccionado == actual["orden"]:
        st.success(f"✅ ¡Correcto! Es una {actual['nombre']} ({actual['orden']})")
        st.session_state.puntos += 10
        st.session_state.aciertos += 1
    else:
        st.error(f"❌ Incorrecto. Era una {actual['nombre']} ({actual['orden']})")
    st.session_state.historial.append((actual['nombre'], orden_seleccionado))

# ---- RESULTADOS ----
st.markdown("""
---
### 🏆 Puntos acumulados: {0}
### ✅ Aciertos: {1}
""".format(st.session_state.puntos, st.session_state.aciertos))

if st.session_state.historial:
    st.markdown("### Historial de respuestas:")
    for i, (nombre, respuesta) in enumerate(reversed(st.session_state.historial[-5:]), 1):
        st.markdown(f"{i}. Dijiste *{respuesta}*, era *{nombre}*.")

if st.button("🔄 Reiniciar"):
    seleccionar_insecto()
    st.session_state.girando = False
    st.session_state.stop = False
    st.rerun()
