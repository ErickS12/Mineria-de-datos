import streamlit as st
from bernoulli import show_bernoulli
from binomial import show_binomial
from multi import show_multinomial
from exp import show_exponencial
from normalConVyM import show_normalConVyM

# --- INYECTAR EL CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- Contenido principal de la página ---
st.title("Simuladores de Distribuciones")
st.write("Selecciona una de las simulaciones para empezar.")

st.set_page_config(page_title="Simuladores de Probabilidad", layout="centered")


# --- Lógica de la navegación ---
# Inicializar el estado de la página
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# --- 1. Botón de Inicio Centrado ---
# Se crea una fila con 3 columnas para centrar el botón de Inicio
col_izq, col_centro, col_der = st.columns([1, 2, 1])

with col_centro:
    if st.button('Inicio', use_container_width=True):
        st.session_state.current_page = 'home'

# --- 2. Espaciador ---
# Un simple espacio para separar las filas de botones
st.markdown("---")

# --- 3. Fila de Botones de Distribuciones ---
# Se crea una nueva fila con 3 columnas para los otros botones
col_dist1, col_dist2, col_dist3 = st.columns(3)

with col_dist1:
    if st.button('Bernoulli', use_container_width=True):
        st.session_state.current_page = 'bernoulli'

with col_dist2:
    if st.button('Binomial', use_container_width=True):
        st.session_state.current_page = 'binomial'

with col_dist3:
    if st.button('Multinomial', use_container_width=True):
        st.session_state.current_page = 'multinomial'

col_dist4, col_dist5, col_dist6 = st.columns(3)

with col_dist4:
    if st.button('Exponencial', use_container_width=True):
        st.session_state.current_page = 'Exponencial'

with col_dist5:
    if st.button('Normal Varianza y Media', use_container_width=True):
        st.session_state.current_page = 'Normal Varianza y Media'

with col_dist6:
    if st.button('Gibbs', use_container_width=True):
        st.session_state.current_page = 'Gibbs'

# --- Mostrar la página actual según el estado de sesión ---
if st.session_state.current_page == 'home':
    st.header("Bienvenido")
    
elif st.session_state.current_page == 'bernoulli':
    show_bernoulli()

elif st.session_state.current_page == 'binomial':
    show_binomial()

elif st.session_state.current_page == 'multinomial':
    show_multinomial()    

elif st.session_state.current_page == 'Exponencial':
    show_exponencial()

elif st.session_state.current_page == 'Normal Varianza y Media':
    show_normalConVyM()

elif st.session_state.current_page == 'Gibbs':
    st.write("Funcionalidad de Gibbs en desarrollo.")
    # show_gibbs()  
    