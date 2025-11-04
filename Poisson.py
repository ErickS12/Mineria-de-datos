import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def show_poisson():
    st.header("Simulación Metropolis-Hastings para Poisson")
    st.write(
        "Genera muestras de la distribución de Poisson utilizando el algoritmo M-H con una Cadena de Markov.")

    # Caja de texto informativa y Ecuación
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Muestreo</h4>
            <p>El algoritmo de Metropolis-Hastings construye una cadena de Markov cuya distribución estacionaria es la distribución objetivo (Poisson). Se propone un movimiento a un estado vecino que se acepta o rechaza con una probabilidad que asegura la convergencia a la distribución deseada.</p>
        </div>
    """, unsafe_allow_html=True)
    st.subheader("Ecuación de Poisson")
    st.image("images/poisson.png", use_container_width=True)

    st.markdown("---")
    st.subheader("Parámetros de la Simulación")

    # Controles de Usuario
    col1, col2 = st.columns(2)
    with col1:
        # 1. Lambda (λ)
        lambdaa = st.slider("Parámetro Lambda (λ)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
        # 2. Estado Inicial (i)
        estado_inicial = st.number_input("Estado Inicial (i)", min_value=0, value=int(lambdaa), step=1)
    with col2:
        # 3. Número de Iteraciones
        N_iteraciones = st.number_input("Total de Iteraciones (N)", min_value=1000, value=50000, step=1000)
        # 4. muestras a descartar
        cortar = st.number_input("Muestras a descartar", min_value=0, value=1000, step=100)


    # Condición para ejecutar la simulación
    if st.button("Ejecutar Simulación M-H"):

        # INICIALIZACIÓN DE LA CADENA
        cadMarkov = []
        estado_i = estado_inicial
        k = 0
        cadMarkov.append(estado_i)

        # BUCLE PRINCIPAL DE METROPOLIS-HASTINGS
        with st.spinner(f"Generando {N_iteraciones} muestras..."):

            for b in range(N_iteraciones + cortar):
                # PASO DE PROPUESTA
                u_1 = random.random()

                # Definición del candidato k (i-1 o i+1)
                if u_1 <= 0.5:
                    if estado_i == 0:
                        k = 0  # No puede ir a negativo
                    else:
                        k = estado_i - 1
                else:
                    k = estado_i + 1

                # PASO DE ACEPTACIÓN (Cálculo de alphaa = min(1, pi_k / pi_i))

                if k == estado_i and estado_i == 0:
                    ratio_pi = 1.0
                elif k == (estado_i - 1):  # Movimiento a la izquierda
                    ratio_pi = estado_i / lambdaa
                elif k == (estado_i + 1):  # Movimiento a la derecha
                    ratio_pi = lambdaa / (estado_i + 1)
                else:
                    ratio_pi = 0.0

                alphaa = min(1.0, ratio_pi)

                # PASO DE DECISIÓN (Transición de estado)
                u_2 = random.random()

                if u_2 <= alphaa:
                    # Aceptado: el estado se actualiza
                    estado_i = k
                # else: Rechazado: el estado_i se mantiene.

                # Guardamos el estado resultante
                cadMarkov.append(estado_i)

        st.success("¡Simulación M-H finalizada con éxito!")

        # PROCESAMIENTO Y VISUALIZACIÓN DE RESULTADOS
        muestras_validas = cadMarkov[cortar:]

        # Definir el rango del histograma
        max_val = max(muestras_validas) if muestras_validas else int(lambdaa) + 5
        x_max = max(max_val, int(lambdaa) + 5)

        fig, ax = plt.subplots(figsize=(10, 6))

        # HISTOGRAMA (Muestras de MH)
        ax.hist(
            muestras_validas,
            bins=np.arange(0, x_max + 2) - 0.5,
            rwidth=0.8,
            density=True,
            color='skyblue',
            edgecolor='black',
            label='Muestras Metropolis-Hastings'
        )

        # Títulos y Etiquetas
        ax.set_title(f'Histograma de Muestras de Poisson (λ={lambdaa}) por M-H')
        ax.set_xlabel('Valor del Estado (k)')
        ax.set_ylabel('Frecuencia Normalizada')
        # Establecer ticks en los enteros
        ax.set_xticks(np.arange(0, x_max + 1))
        ax.set_xlim(-0.5, x_max + 0.5)
        ax.legend()
        ax.grid(axis='y', alpha=0.5)

        st.pyplot(fig)

        # Mostrar las primeras muestras
        with st.expander("Ver Muestras (Después del descarte)"):
            st.write(f"Se generaron {N_iteraciones} muestras y se descartaron {cortar} (descarte).")
            st.write("Primeros 100 valores de la cadena válida:")
            st.write(muestras_validas[:100])