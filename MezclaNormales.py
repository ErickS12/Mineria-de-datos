import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import math

def show_MezclaNormales():
    st.header("Simulación Metropolis-Hastings para Mezcal de Normales")
    st.write(
        "Genera muestras de una distribución compuesta por una mezcla de normales utilizando el algoritmo M-H con una Cadena de Markov.")

    # Caja de texto informativa y Ecuación
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Muestreo</h4>
            <p>El algoritmo de Metropolis-Hastings construye una cadena de Markov cuya distribución estacionaria es la distribución objetivo (Mezcla de normales). Se propone un movimiento a un estado vecino que se acepta o rechaza con una probabilidad que asegura la convergencia a la distribución deseada.</p>
            <p>La mezcla de normales es una distribución de probabilidad que es una combinación ponderada de dos o más distribuciones normales individuales. </p>
            <p>Se usa para modelar datos que no se ajustan a una sola distribución normal y que pueden ser bimodales (con dos picos), multimodales (con más de dos picos) o tener un exceso de curtosis (un pico más pronunciado y colas más pesadas). </p>
        </div>
    """, unsafe_allow_html=True)
    #st.subheader("Ecuación de Poisson")
    #st.image("img/poisson.png", use_container_width=False)

    st.markdown("---")
    st.subheader("Parámetros de la Simulación")

    # Controles de Usuario
    col1, col2 = st.columns(2)
    with col1:#parametros de la primer normal
        # escalar para la primera normal
        esc_1 = st.slider("Escalar para la primer normal", min_value=0.0, max_value=1.0, value=0.7, step=0.1, key="slider_1")
        mu_1 = st.slider("Media (μ) de la primera normal", min_value=-20.0, max_value=20.0, value=7.0, step=0.1, key="slider_2")
        sigma_1 = st.slider("Desviación estandar (𝜎) de la primera normal", min_value=0.0, max_value=20.0, value=0.5, step=0.1, key="slider_3")
        # Número de Iteraciones
        muestra = st.number_input("Total de Iteraciones (N)", min_value=1000, value=50000, step=1000)
    with col2:
        esc_2 = 1-esc_1
        st.text(" ")
        st.text(f"Escalar para la segunda normal: {esc_2:.1f}")
        st.text(" ")
        st.text(" ")
        mu_2 = st.slider("Media (μ) de la primera normal", min_value=-20.0, max_value=20.0, value=10.0, step=0.1)
        sigma_2 = st.slider("Desviación estandar (𝜎) de la primera normal", min_value=0.0, max_value=20.0, value=0.5,step=0.1)
        descarte = st.number_input("Muestras a descartar", min_value=0, value=5000, step=100)


    # Condición para ejecutar la simulación
    if st.button("Ejecutar Simulación M-H"):
        Z = 2
        y = 0
        cadMarkov = []
        cadMarkov.append(Z)

        # if (esc_1 + esc_2) !=1 and (esc_1 > 0 & esc_2) > 0:
        for i in range(0, muestra + descarte):
            y = random.gauss(Z, 0.1)  # numero aleatorio para Y que se encuentra en una normal
            pi_x1 = esc_1 * (
                        1 / math.sqrt(2 * math.pi * sigma_1 ** 2) * math.exp(-(Z - mu_1) ** 2 / (2 * sigma_1 ** 2)))
            pi_x2 = esc_2 * (
                        1 / math.sqrt(2 * math.pi * sigma_2 ** 2) * math.exp(-(Z - mu_2) ** 2 / (2 * sigma_2 ** 2)))
            pi_x = pi_x1 + pi_x2
            pi_y1 = esc_1 * (
                        1 / math.sqrt(2 * math.pi * sigma_1 ** 2) * math.exp(-(y - mu_1) ** 2 / (2 * sigma_1 ** 2)))
            pi_y2 = esc_2 * (
                        1 / math.sqrt(2 * math.pi * sigma_2 ** 2) * math.exp(-(y - mu_2) ** 2 / (2 * sigma_2 ** 2)))
            pi_y = pi_y1 + pi_y2

            alpha = min(1, pi_y / pi_x)
            u = random.random()
            if u <= alpha:
                Z = y
            cadMarkov.append(Z)
        cad_final = cadMarkov[descarte:]
        # print(cadMarkov)
        st.success("¡Simulación M-H finalizada con éxito!")

        # Histograma para Mostrar la Distribución (Mezcla de Normales)
        fig = plt.figure(figsize=(10, 6))

        # Dibujar el Histograma de las muestras
        # density=True normaliza el histograma para que el área total sea 1 (PDF)
        plt.hist(cad_final, bins=50, density=True, color='skyblue', edgecolor='black', alpha=0.7, label='Muestras MCMC')

        # Superponer la Densidad Teórica (Opcional, pero esencial para verificación)
        # Definir el rango de valores para graficar la función teórica
        x_vals = np.linspace(min(cad_final), max(cad_final), 500)

        # Calcular la densidad teórica de la Mezcla de Normales para cada punto en x_vals
        # Utilizamos los mismos parámetros que definiste al inicio del script
        def pi_teorica(x):
            # PDF de la Normal 1
            pdf1 = (1 / (math.sqrt(2 * math.pi) * sigma_1)) * np.exp(-0.5 * ((x - mu_1) / sigma_1) ** 2)
            # PDF de la Normal 2
            pdf2 = (1 / (math.sqrt(2 * math.pi) * sigma_2)) * np.exp(-0.5 * ((x - mu_2) / sigma_2) ** 2)
            # Mezcla: w1*PDF1 + w2*PDF2
            return esc_1 * pdf1 + esc_2 * pdf2

        y_teorico = pi_teorica(x_vals)

        # Dibujar la curva teórica
        plt.plot(x_vals, y_teorico, color='red', linewidth=2, label='Densidad Teórica $\pi(x)$')

        # Configuración final del gráfico
        plt.title('Simulación de la Mezcla de Normales (Histograma MCMC vs. PDF Teórica)')
        plt.xlabel('Valor de la Variable')
        plt.ylabel('Densidad de Probabilidad')
        plt.legend()
        plt.grid(axis='y', alpha=0.5)

        st.pyplot(fig)

        # Mostrar las primeras muestras
        with st.expander("Ver Muestras (Después del descarte)"):
            st.write(f"Se generaron {muestra} muestras y se descartaron {descarte} (descarte).")
            st.write("Primeros 100 valores de la cadena válida:")
            st.write(cad_final[:100])
