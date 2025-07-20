import streamlit as st
import random
import time
from PIL import Image
import base64

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

# ---- ESTILOS PERSONALIZADOS ----
st.markdown("""
    <style>
  .block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

    .pregunta {
        font-size: 28px;
        font-weight: bold;
        color: white;
        margin: 1em 0 1em 0;
    }

    div[data-baseweb="radio"] > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    button[kind="primary"] {
        display: block;
        margin: 0.5em auto;
    }

/* Imagen del insecto más grande y centrada dentro de su contenedor */
div.stImage > img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-width: 260px;
    border-radius: 12px;
    box-shadow: 0px 0px 15px rgba(255, 255, 255, 0.2);
}

    </style>
""", unsafe_allow_html=True)

# ---- TÍTULO PRINCIPAL ----
st.markdown("""
<h1 style='
    text-align: center;
    color: #ffffff;
    font-size: 3rem;
    font-family: "Comic Sans MS", cursive;
    text-shadow: 2px 2px 4px #000000;
    margin-bottom: 2rem;
'>
    🐞 Adivina el insecto 🦋
</h1>
""", unsafe_allow_html=True)

def mostrar_imagen_actual():
    ruta = st.session_state.insecto_actual["imagen"]
    if not os.path.exists(ruta):
        st.error(f"❌ Imagen no encontrada: {ruta}")
        return
    img = Image.open(ruta)
    imagen_placeholder.image(img, width=260)


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

ordenes = ["Blattodea", "Coleoptera", "Diptera", "Hemiptera", "Hymenoptera", "Lepidoptera", "Mantodea", "Odonata", "Orthoptera"]


# ---- ESTADO ----
if "girando" not in st.session_state:
    st.session_state.girando = False
if "insecto_actual" not in st.session_state:
    st.session_state.insecto_actual = random.choice(insectos)

# ---- CONTENEDOR DE IMAGEN ----
# ---- Contenedor de imagen ----
imagen_placeholder = st.empty()

# ---- Función para mostrar imagen actual ----
def mostrar_imagen_actual():
    img = Image.open(st.session_state.insecto_actual["imagen"])
    imagen_placeholder.image(img, width=260)

# ---- Mostrar imagen si no está girando ----
if not st.session_state.girando:
    mostrar_imagen_actual()

# ---- BOTONES DE RUEDA ----
col1, col2 = st.columns(2, gap="large")
with col1:
    if not st.session_state.girando:
        if st.button("🎯 Girar Ruleta"):
            st.session_state.girando = True
            
with col2:
    if st.session_state.girando:
        if st.button("🛑 Detener"):
            st.session_state.girando = False
            st.rerun()

# ---- EFECTO RULETA ----
if st.session_state.girando:
    for _ in range(30):
        st.session_state.insecto_actual = random.choice(insectos)
        img = Image.open(st.session_state.insecto_actual["imagen"])
        imagen_placeholder.image(img, width=250)
        time.sleep(0.06)
    st.rerun()

# ---- PREGUNTA ----
st.markdown('<div class="pregunta">¿A qué orden pertenece este insecto?</div>', unsafe_allow_html=True)

# ---- OPCIONES ----
orden_seleccionado = st.radio("", ordenes, key="orden_radio", horizontal=False)

# ---- COMPROBAR ----
if st.button("Comprobar"):
    actual = st.session_state.insecto_actual
    if orden_seleccionado == actual["orden"]:
        st.success(f"✅ ¡Correcto! Es un {actual['nombre']} ({actual['orden']})")
    else:
        st.error(f"❌ Incorrecto. Era un {actual['nombre']} ({actual['orden']})")

# ---- REINICIAR ----
if st.button("🔄 Reiniciar"):
    st.session_state.insecto_actual = random.choice(insectos)
    st.session_state.girando = False
    st.rerun()
