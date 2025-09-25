import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from PIL import Image



def show_binomial():
    st.set_page_config(page_title="Simulador Binomial y Multinomial", layout="centered")
    st.title("Binomial")
    st.write("Explora la distribución Binomial con múltiples lanzamientos.")
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Distribución Binomial</h4>
            <p>La distribución Binomial modela el número de éxitos en una secuencia de <b>n</b> ensayos independientes. Es perfecta para situaciones como el número de caras en 10 lanzamientos de una moneda o el número de productos defectuosos en un lote de 100.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- Sección para la Imagen ---
    #st.subheader("Ecuación")
    #st.image("Imag_Binomial.png", caption="Diagrama de un ensayo de Binomial", use_container_width=True)
    

    n1 = st.number_input("Número de lanzamientos (n)", min_value=1, value=10, step=1, key="m_n_input")
    p1 = st.slider("Probabilidad de éxito (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key="m_slider")
    k1 = st.number_input("Número de simulaciones (k)", min_value=1, value=100, step=1000, key="m_input")

    if st.button("Simular Binomial", key="b_button"):
        resultados1 = np.random.binomial(n1, p1, k1)

        
        fig1, ax1 = plt.subplots()
        counts1, bins1, patches1 = ax1.hist(resultados1, bins=range(n1+2), edgecolor='black', rwidth=0.7)

        # Colorear barras
        colors = plt.cm.viridis(np.linspace(0, 1, len(patches1)))
        for patch, color in zip(patches1, colors):
            patch.set_facecolor(color)
        
        for count, bin_edge in zip(counts1, bins1[:-1]):
            ax1.text(bin_edge + 0.5, count + (max(counts1)*0.01), str(int(count)),
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax1.set_xlabel("Comparacion")
        ax1.set_ylabel("Frecuencia")
        ax1.set_title(f"Distribución Binomial")

        st.pyplot(fig1)
        
        if k1 <= 200:
            with st.expander("¿Quieres ver la muestra?"):
                st.write("Muestra:")
                df = pd.DataFrame(resultados1, columns=["Resultado"], index=range(1, len(resultados1) + 1))
                df.index.name = "Lanzamiento"
                st.dataframe(df)



        st.success(f"El experimento se ha realizado {k1} veces con una probabilidad de éxito de {p1} y con {n1} lanzamientos.")

