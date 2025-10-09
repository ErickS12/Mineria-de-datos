import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def show_normalConVyM():
    st.title("Simulación de una función de densidad normal estándar")
    st.write("Genera una distribución normal estándar y ajusta con media y varianza.")
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Distribución Normal</h4>
            <p>La distribución Normal o de Gauss es una distribución continua que describe datos que tienden a agruparse alrededor de un valor central. Es la "curva de campana" clásica, fundamental en la estadística para modelar fenómenos naturales como la altura de las personas o las puntuaciones en un examen.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- Sección para la Imagen ---
    st.subheader("Ecuación de la Función de Densidad Normal Estándar")   
    st.image("images/Imag_FuncionDensidadNormalEstandar.png", use_container_width=True)

    st.subheader("Ecuación de la Función de Densidad Normal con Media y Varianza")   
    st.image("images/Imag_FuncionDensidadNormalConMediaVarianza.png", use_container_width=True)

    # Número de simulaciones
    n3 = st.number_input("Número de simulaciones (n)", min_value=1, value=1000, step=100, key="n3_input")
    # Inputs de media y varianza
    media = st.number_input("Media (μ)", value=0.0, step=0.1, key="media_input")
    varianza = st.number_input("Varianza (σ²)", min_value=0.1, value=1.0, step=0.1, key="varianza_input")


    if st.button("Simular"):
        # Generar números aleatorios uniformes
        u = np.random.rand(n3)
        v = np.random.rand(n3)

        # Transformación Box-Muller para distribución normal estándar
        x = np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * v)  # Nota: log natural para correcta normal estándar

        # Graficar histograma de la distribución estándar
        fig, ax = plt.subplots()
        ax.hist(x, bins=30, color='skyblue', edgecolor='black', alpha=0.7, label="Normal estándar")
        ax.set_title("Distribución normal estándar vs ajustada(con media y varianza)")
        ax.set_xlabel("Valor") 
        ax.set_ylabel("Frecuencia")
        ax.grid(True)


        # Ajuste correcto con media y desviación estándar
        y = media + np.sqrt(varianza) * x

        # Graficar histograma de la distribución ajustada
        ax.hist(y, bins=30, color='salmon', edgecolor='black', alpha=0.7, label="Normal ajustada")
        ax.legend()

        st.pyplot(fig)

        # Mostrar muestras si son pocas
        if n3 <= 200:
            with st.expander("¿Quieres ver las muestras?"):
                st.write("Normal estándar:")
                st.write(", ".join([f"{num:.4f}" for num in x]))
                st.write("Normal ajustada (con media y varianza):")
                st.write(", ".join([f"{num:.4f}" for num in y]))

        st.success(f"El experimento se ha realizado {n3} veces.")
