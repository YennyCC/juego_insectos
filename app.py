import streamlit as st
import random
import time
from PIL import Image
import base64
import os

# ---- CONFIGURACIÓN INICIAL ----
st.set_page_config(page_title="Adivina el insecto", layout="centered")

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
    width: 260px;
    max-width: 100%;
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
        width: 260px;
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

    /* Texto de opciones del radio en blanco */
    div[data-baseweb="radio"] label {
        color: white;
        font-size: 16px;
        padding: 4px 0;
    }

    /* Alineación centrada */
    div[data-baseweb="radio"] {
        display: flex;
        flex-direction: column;
        align-items: center;
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

    /* Centrar todo el contenido */
.block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Imagen más grande y centrada */
div.stImage {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
}
div.stImage img {
    max-width: 260px;
    width: 100%;
    height: auto;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(255,255,255,0.3);
}

/* Centrar botones debajo de la imagen */
.boton-container {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
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
    {"nombre": "mariposa", "orden": "Lepidoptera", "imagen": "siluetas/mariposa.png"},
    {"nombre": "escarabajo", "orden": "Coleoptera", "imagen": "siluetas/escarabajo.png"},
    {"nombre": "abeja", "orden": "Hymenoptera", "imagen": "siluetas/abeja.png"},
    {"nombre": "libélula", "orden": "Odonata", "imagen": "siluetas/libelula.png"},
    {"nombre": "chinche", "orden": "Hemiptera", "imagen": "siluetas/chinche.png"},
    {"nombre": "mosquito", "orden": "Diptera", "imagen": "siluetas/mosquito.png"},
    {"nombre": "saltamontes", "orden": "Orthoptera", "imagen": "siluetas/saltamontes.png"},
    {"nombre": "cucaracha", "orden": "Blattodea", "imagen": "siluetas/cucaracha.png"},
    {"nombre": "mantis", "orden": "Mantodea", "imagen": "siluetas/mantis.png"}
]

ordenes = ["Blattodea", "Coleoptera", "Diptera", "Hemiptera", "Hymenoptera", "Lepidoptera", "Mantodea", "Odonata", "Orthoptera"]


# ---- ESTADOS ----
if "insecto_actual" not in st.session_state:
    st.session_state.insecto_actual = random.choice(insectos)

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

# ---- MOSTRAR IMAGEN ----
def mostrar_imagen_actual():
    ruta = st.session_state.insecto_actual["imagen"]
    if os.path.exists(ruta):
        img = Image.open(ruta)
        st.image(img, width=220)
    else:
        st.warning(f"⚠️ Imagen no encontrada: {ruta}")

# ---- INTERFAZ ----
col1, col2 = st.columns(2)
with col1:
    if st.button("🎯 Girar Ruleta"):
        st.session_state.girando = True
        st.session_state.stop = False
        st.rerun()

with col2:
    if st.session_state.girando:
        if st.button("🛑 Detener"):
            st.session_state.stop = True

# ---- EFECTO RULETA ----
if st.session_state.girando:
    for _ in range(40):  # Gira un poco antes de verificar si se detiene
        if st.session_state.stop:
            break
        st.session_state.insecto_actual = random.choice(insectos)
        mostrar_imagen_actual()
        time.sleep(0.07)
    st.session_state.girando = False
    st.session_state.stop = False
    st.rerun()
else:
    mostrar_imagen_actual()

# ---- PREGUNTA ----
st.markdown("### ¿A qué orden pertenece este insecto?")
orden_seleccionado = st.radio("", ordenes, key="orden_radio")

# ---- COMPROBAR ----
if st.button("Comprobar"):
    actual = st.session_state.insecto_actual
    femenino = ["cucaracha", "abeja", "mariposa", "mantis", "libélula"]
    articulo = "una" if actual["nombre"].lower() in femenino else "un"

    if orden_seleccionado == actual["orden"]:
        st.success(f"✅ ¡Correcto! Es {articulo} {actual['nombre']} ({actual['orden']})")
        st.session_state.aciertos += 1
        st.session_state.puntos += 10
    else:
        st.error(f"❌ Incorrecto. Era {articulo} {actual['nombre']} ({actual['orden']})")

    st.session_state.historial.append((actual["orden"], orden_seleccionado))

# ---- RESULTADOS ----
st.markdown(f"""
---
### 🏆 Puntos acumulados: {st.session_state.puntos}
### ✅ Aciertos: {st.session_state.aciertos}
""")

if st.session_state.historial:
    st.markdown("### Historial de respuestas:")
    for i, (orden, respuesta) in enumerate(reversed(st.session_state.historial[-5:]), 1):
        st.markdown(f"{i}. Dijiste *{respuesta}*, era *{orden}*.")

# ---- REINICIAR ----
if st.button("🔄 Reiniciar"):
    st.session_state.insecto_actual = random.choice(insectos)
    st.session_state.girando = False
    st.session_state.stop = False
    st.session_state.puntos = 0
    st.session_state.aciertos = 0
    st.session_state.historial = []
    st.rerun()
