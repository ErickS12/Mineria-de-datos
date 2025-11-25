import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import math
import pandas as pd

def show_MezclaNormales():
    st.header("Simulación Metropolis-Hastings para Mezcal de Normales")
    st.write(
        "Genera muestras de una distribución compuesta por una mezcla de normales utilizando el algoritmo M-H con una Cadena de Markov.")

    # Caja de texto informativa
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Muestreo</h4>
            <p>El algoritmo de Metropolis-Hastings construye una cadena de Markov cuya distribución estacionaria es la distribución objetivo (Mezcla de normales).</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Ecuación de Mezcla de Normales")
    st.image("images/Imag_MezclaNormales.png", use_container_width=False)

    st.markdown("---")
    st.subheader("Parámetros de la Simulación")

    # Controles de Usuario
    col1, col2 = st.columns(2)
    with col1:
        esc_1 = st.slider("Escalar para la primer normal", 0.0, 1.0, 0.7, 0.1)
        mu_1 = st.slider("Media (μ) de la primera normal", -20.0, 20.0, 7.0, 0.1)
        sigma_1 = st.slider("Desviación estándar (σ) de la primera normal", 0.1, 20.0, 0.5, 0.1)
        muestra = st.number_input("Total de Iteraciones (N)", min_value=1000, value=50000, step=1000)

    with col2:
        esc_2 = 1 - esc_1
        st.text(f"Escalar para la segunda normal: {esc_2:.1f}")
        mu_2 = st.slider("Media (μ) de la segunda normal", -20.0, 20.0, 10.0, 0.1)
        sigma_2 = st.slider("Desviación estándar (σ) de la segunda normal", 0.1, 20.0, 0.5, 0.1)
        descarte = st.number_input("Muestras a descartar (burn-in)", min_value=0, value=5000, step=100)

    # Botón de ejecución
    if st.button("Ejecutar Simulación M-H"):

        Z = 2
        cadMarkov = [Z]

        # --- Contador de aceptación ---
        aceptaciones = 0

        for i in range(muestra + descarte):
            y = random.gauss(Z, 10)

            # densidad objetivo en X
            pi_x = (
                esc_1 * (1 / (math.sqrt(2 * math.pi) * sigma_1)) * math.exp(-0.5 * ((Z - mu_1) / sigma_1) ** 2) +
                esc_2 * (1 / (math.sqrt(2 * math.pi) * sigma_2)) * math.exp(-0.5 * ((Z - mu_2) / sigma_2) ** 2)
            )

            # densidad objetivo en Y
            pi_y = (
                esc_1 * (1 / (math.sqrt(2 * math.pi) * sigma_1)) * math.exp(-0.5 * ((y - mu_1) / sigma_1) ** 2) +
                esc_2 * (1 / (math.sqrt(2 * math.pi) * sigma_2)) * math.exp(-0.5 * ((y - mu_2) / sigma_2) ** 2)
            )

            alpha = min(1, pi_y / pi_x)

            if random.random() <= alpha:
                Z = y
                aceptaciones += 1

            cadMarkov.append(Z)

        # Quitar burn-in
        cad_final = cadMarkov[descarte:]

        st.success("¡Simulación M-H finalizada con éxito!")

        # --- Tasa de aceptación ---
        tasa = aceptaciones / (muestra + descarte)
        st.subheader("Tasa de Aceptación")
        st.write(f"**Tasa de aceptación:** `{tasa:.4f}`")

        # Histograma
        fig = plt.figure(figsize=(10, 6))
        plt.hist(cad_final, bins=50, density=True, color='skyblue',
                 edgecolor='black', alpha=0.7, label='Muestras MCMC')

        x_vals = np.linspace(min(cad_final), max(cad_final), 500)

        def pi_teorica(x):
            pdf1 = (1 / (math.sqrt(2 * math.pi) * sigma_1)) * np.exp(-0.5 * ((x - mu_1) / sigma_1) ** 2)
            pdf2 = (1 / (math.sqrt(2 * math.pi) * sigma_2)) * np.exp(-0.5 * ((x - mu_2) / sigma_2) ** 2)
            return esc_1 * pdf1 + esc_2 * pdf2

        plt.plot(x_vals, pi_teorica(x_vals), color='red', linewidth=2,
                 label='Densidad Teórica $\pi(x)$')

        plt.title('Simulación de la Mezcla de Normales (Histograma MCMC vs PDF Teórica)')
        plt.xlabel('Valor de la Variable')
        plt.ylabel('Densidad de Probabilidad')
        plt.legend()
        plt.grid(axis='y', alpha=0.5)
        st.pyplot(fig)

        # --- Traza de la cadena completa ---
        st.subheader("Traza de la Cadena de Markov")
        fig_trace, ax_trace = plt.subplots(figsize=(10, 4))
        ax_trace.plot(cad_final, linewidth=1)
        ax_trace.set_title("Evolución de la cadena después del burn-in")
        ax_trace.set_xlabel("Iteración")
        ax_trace.set_ylabel("Valor")
        ax_trace.grid(alpha=0.3)
        st.pyplot(fig_trace)

        # Mostrar primeras 100 muestras + traza resumida
        with st.expander("Ver muestras y traza (Después del descarte)"):

            st.write(f"Se generaron {muestra} muestras y se descartaron {descarte}.")
            st.write("Primeros **50 valores** de la cadena válida:")

            df = pd.DataFrame(cad_final[:50], columns=["Resultado"])
            df.index = np.arange(1, len(df) + 1)
            df.index.name = "Iteración"
            st.dataframe(df, use_container_width=True)
