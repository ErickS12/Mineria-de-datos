import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.stats import beta
import pandas as pd



def show_beta():
    st.header("Simulación Metropolis-Hastings para Distribución Beta")
    st.write(
        "Genera muestras de la distribución Beta utilizando el algoritmo Metropolis-Hastings para el caso continuo con propuesta independiente uniforme."
    )

    # Caja de texto informativa y Ecuación
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Muestreo</h4>
            <p>
            La distribución Beta es una distribución continua definida en el intervalo (0, 1).
            Es especialmente útil para modelar probabilidades, proporciones y variables acotadas en ese rango.
            Depende de dos parámetros positivos, α₁ y α₀, que controlan la forma de la distribución:
            Si ambos son mayores que 1, la Beta tiene forma de “campana”.
            Si α₁ < 1 y α₀ < 1, la distribución se concentra en los extremos (0 y 1).
            Si α₁ > α₀, la distribución se sesga hacia valores grandes.
            Si α₁ < α₀, se sesga hacia valores pequeños.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Función de Densidad de la Distribución Beta")
    st.image("images/Imag_Beta.png", use_container_width=True)

    st.markdown("---")
    st.subheader("Parámetros de la Simulación")

    # Controles de Usuario
    col1, col2 = st.columns(2)
    with col1:
        alpha1 = st.number_input("Parámetro α₁", min_value=0.1, value=2.0, step=0.1)
        alpha0 = st.number_input("Parámetro α₀", min_value=0.1, value=5.0, step=0.1)
    with col2:
        N_iteraciones = st.number_input("Total de Iteraciones (N)", min_value=500, value=10000, step=500)
        cortar = st.number_input("Muestras a descartar)", min_value=0, value=500, step=100)

    # Estado inicial
    estado_inicial = st.slider("Estado inicial x₀", min_value=0.0, max_value=1.0, value=0.5)

    # Función objetivo π(x)
    def pi(x):
        if 0 < x < 1:
            return (x**(alpha1 - 1)) * ((1 - x)**(alpha0 - 1))
        return 0.0

    # Ejecución
    if st.button("Ejecutar Simulación M-H"):

        # INICIALIZACIÓN
        cadMarkov = []
        x_i = estado_inicial
        cadMarkov.append(x_i)

        with st.spinner(f"Generando {N_iteraciones} muestras..."):

            for _ in range(N_iteraciones + cortar):

                # Propuesta independiente: Y ~ Uniforme(0,1)
                y = random.random()

                # Aceptación α = min(1, π(y) / π(x))
                num = pi(y)
                den = pi(x_i)
                alpha = min(1.0, num / den if den > 0 else 1.0)

                # Segunda uniforme para aceptar
                if random.random() <= alpha:
                    x_i = y  # Aceptado

                cadMarkov.append(x_i)

        st.success("¡Simulación M-H finalizada con éxito!")

        # --- PROCESAMIENTO ---
        muestras_validas = cadMarkov[cortar:]


        # -----------------------------------------------------
        # TASA DE ACEPTACIÓN
        # -----------------------------------------------------
        tasa_aceptación = (
            np.sum(np.diff(cadMarkov) != 0) / len(cadMarkov)
            if len(cadMarkov) > 1 else 0
        )

        st.subheader("Tasa de Aceptación del Algoritmo")
        st.metric("Aceptación", f"{tasa_aceptación*100:.2f}%")

        # -----------------------------------------------------
        # HISTOGRAMA
        # -----------------------------------------------------
        fig, ax = plt.subplots(figsize=(10, 6))

        # Histograma
        ax.hist(
            muestras_validas,
            bins=40,
            density=True,
            color='lightgreen',
            edgecolor='black',
            alpha=0.7,
            label='Muestras M-H'
        )

        # Densidad real
        x = np.linspace(0, 1, 300)
        ax.plot(x, beta.pdf(x, alpha1, alpha0), 'r-', linewidth=2, label='Beta real')

        ax.set_title(f"Histograma de Muestras vs Beta({alpha1}, {alpha0})")
        ax.set_xlabel("x")
        ax.set_ylabel("Densidad")
        ax.grid(alpha=0.4)
        ax.legend()

        st.pyplot(fig)

        # --- Graficar la traza de la cadena ---
        st.subheader("Traza de la Cadena de Markov")

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(muestras_validas, linewidth=1)
        ax2.set_title("Evolución de la cadena después del burn-in")
        ax2.set_xlabel("Iteración")
        ax2.set_ylabel("Valor (x)")
        ax2.grid(alpha=0.3)

        st.pyplot(fig2)


        # -----------------------------------------------------
        # TABLA 1: Primeras 50 muestras
        # -----------------------------------------------------
        # --- Mostrar la muestra ---
        with st.expander("¿Quieres ver la muestra?"):
            st.write("Primeros 50 valores de la muestra:")

            df = pd.DataFrame(
                muestras_validas,     # <-- cambia este nombre si tus muestras se llaman distinto
                columns=["Resultado"],
                index=range(1, len(muestras_validas) + 1)
            )
            df.index.name = "Iteración"

            # Mostrar los primeros 50 valores
            st.dataframe(df.head(50))




        # -----------------------------------------------------
        # TABLA 2: Estadísticos descriptivos
        # -----------------------------------------------------
        st.subheader("Estadísticos Descriptivos")
        st.table({
            "Estadístico": ["Media", "Varianza", "Mínimo", "Máximo"],
            "Valor": [
                np.mean(muestras_validas),
                np.var(muestras_validas),
                np.min(muestras_validas),
                np.max(muestras_validas)
            ]
        })