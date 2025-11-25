import streamlit as st
import os

from bernoulli import show_bernoulli
from binomial import show_binomial
from multi import show_multinomial
from exp import show_exponencial
from normalConVyM import show_normalConVyM
from Gibbs import show_gibbs
from normalBivariada import show_normalBivariada
from Poisson import show_poisson
from MezclaNormales import show_MezclaNormales
from metropolis_beta import show_beta


# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Simuladores de Probabilidad ",
    layout="wide"
)

# --- INYECTAR CSS ---
def local_css(file_name):
    current_dir = os.path.dirname(__file__)
    css_file_path = os.path.join(current_dir, file_name)
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        st.error(f"Error: No se pudo encontrar el archivo CSS: {css_file_path}")

local_css("style.css")

# --- ESTADO DE LA PÁGINA ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# --- SIDEBAR CON BOTONES ---
st.sidebar.title(" Simulaciones")

if st.sidebar.button("Inicio"):
    st.session_state.current_page = 'home'
if st.sidebar.button("Bernoulli"):
    st.session_state.current_page = 'bernoulli'
if st.sidebar.button("Binomial"):
    st.session_state.current_page = 'binomial'
if st.sidebar.button("Multinomial"):
    st.session_state.current_page = 'multinomial'
if st.sidebar.button("Exponencial"):
    st.session_state.current_page = 'exponencial'
if st.sidebar.button("Normal V&M"):
    st.session_state.current_page = 'normalVYM'
if st.sidebar.button("Gibbs"):
    st.session_state.current_page = 'gibbs'
if st.sidebar.button("Normal Bivariada"):
    st.session_state.current_page = 'normalBivariada'
if st.sidebar.button("Poisson"):
    st.session_state.current_page = 'poisson'
if st.sidebar.button("Mezcla de Normales"):
    st.session_state.current_page = 'MezclaNormales'
if st.sidebar.button("Beta"):
    st.session_state.current_page = 'beta'

# --- PÁGINA PRINCIPAL ---
if st.session_state.current_page == 'home':
    st.title(" Bienvenido a Simuladores de Distribuciones")
    st.write("Selecciona una simulación desde la barra lateral para empezar.")
    
    st.markdown("### Descripción de los simuladores:")
    
    st.markdown("""
    -  **Bernoulli**: Experimentos de éxito o fracaso, con una sola prueba.
    -  **Binomial**: Repite varios experimentos de Bernoulli y analiza la distribución de resultados.
    -  **Multinomial**: Extensión de la binomial para más de dos resultados posibles.
    -  **Exponencial**: Modela tiempos entre eventos en procesos aleatorios.
    -  **Normal V&M**: Distribución normal con media y varianza personalizables.
    -  **Gibbs**: Método de muestreo para generar muestras de distribuciones complejas.
    -  **Normal Bivariada**: Distribución normal para dos variables correlacionadas.
    -  **Beta**: Modela proporciones o probabilidades, útil en contextos de incertidumbre entre 0 y 1.
    -  **Mezcla de Normales**: Combina varias distribuciones normales para modelar datos con múltiples grupos.
    -  **Poisson**: Modela el número de eventos que ocurren en un intervalo dado cuando los sucesos son independientes.
    """)


elif st.session_state.current_page == 'bernoulli':
    show_bernoulli()
elif st.session_state.current_page == 'binomial':
    show_binomial()
elif st.session_state.current_page == 'multinomial':
    show_multinomial()
elif st.session_state.current_page == 'exponencial':
    show_exponencial()
elif st.session_state.current_page == 'normalVYM':
    show_normalConVyM()
elif st.session_state.current_page == 'gibbs':
    show_gibbs()
elif st.session_state.current_page == 'normalBivariada':
    show_normalBivariada()
elif st.session_state.current_page == 'poisson': # Debes añadir el botón y la condición
    show_poisson()
elif st.session_state.current_page == 'MezclaNormales': # Debes añadir el botón y la condición
    show_MezclaNormales()
elif st.session_state.current_page == 'beta':
    show_beta() 