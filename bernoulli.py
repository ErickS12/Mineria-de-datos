import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from PIL import Image

def show_bernoulli():
    
    st.title("Distribución de Bernoulli")
    st.write("Explora la probabilidad de éxito y fracaso en un solo intento.")

    # --- Caja de texto informativa usando la clase CSS ---
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Bernoulli</h4>
            <p>La distribución de Bernoulli es un modelo de probabilidad para experimentos con solo dos resultados posibles: <b>éxito</b> o <b>fracaso</b>. Por ejemplo, lanzar una moneda y obtener cara (éxito) o cruz (fracaso).</p>
        </div>
    """, unsafe_allow_html=True)
    # --- Fin de la caja de texto informativa ---
    
    # --- Sección para la Imagen ---
    st.subheader("Ecuación")
    st.image("images/Imag_DistribucionBernoulli.png", use_container_width=True)
    
    
    
    # Entradas con sliders y cajas numéricas
    n = 1
    p = st.slider("Probabilidad de éxito (θ)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="b_slider")
    k = st.number_input("Número de simulaciones (n)", min_value=1, value=100, step=1000, key="b_input")

    # Botón para ejecutar simulación
    if st.button("Simular"):
        # Generar datos
        resultados = np.random.binomial(n, p, k)
        
    # Recuadros de éxito y fracaso 
        col1, col2 = st.columns(2)
        with col1: st.markdown(
            "<div style='background-color: #FF4C4C; color:white; padding: 10px; border-radius: 8px; text-align:center; font-weight:bold;'>Fracaso</div>", 
            unsafe_allow_html=True ) 
        
        with col2: st.markdown(
            "<div style='background-color: #4C6BFF; color: white; padding: 10px; border-radius: 8px; text-align:center; font-weight:bold;'>Éxito</div>", 
            unsafe_allow_html=True )

        # Crear figura
        fig, ax = plt.subplots()
        counts, bins, patches = ax.hist(resultados, bins=range(n+2), edgecolor='black', rwidth=0.7)


        colors = ['salmon', 'skyblue']  # tantos colores como barras
        for patch, color in zip(patches, colors):
            patch.set_facecolor(color)
        

        # Mostrar conteo adentro de cada barra
        for count, bin_edge in zip(counts, bins[:-1]):
            if count > 0:  # Solo si hay barras
                ax.text(
                    bin_edge + 0.5,          # centrado en x
                    count / 2,               # mitad de la altura de la barra
                    str(int(count)),         # el número
                    ha='center', va='center',
                    fontsize=9, fontweight='bold', color="black"
                )

        ax.set_xlabel("Comparacion")
        ax.set_ylabel("Número de éxitos y fracasos")
        ax.set_title(f"Distribución de Bernoulli")
        ax.set_xticks([0.5, 1.5])
        ax.set_xticklabels(["Fracaso", "Éxito"])
        
        

        st.pyplot(fig)
        
        muestra = ['🟩E' if x == 1 else '🟥F' for x in resultados]
        
        if k <= 200:
            with st.expander("¿Quieres ver la muestra?"):
                st.write("Muestra:")
                st.write(", ".join(muestra))


        # Mensaje informativo
        st.success(f"El experimento se ha realizado {k} veces con una probabilidad de éxito de {p}.")
        