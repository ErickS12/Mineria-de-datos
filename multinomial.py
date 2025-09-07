import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
from PIL import Image

st.title("Simulación Multinomial")

# Elegir número de categorías
k = st.number_input("Número de categorías", min_value=2, value=6, step=1, key="k_input")

# Parámetros del experimento
n = st.number_input("Tamaño de la muestra (n)", min_value=1, value=10, step=1, key="n_input")
size = st.number_input("Número de simulaciones", min_value=1, value=5, step=1, key="size_input")

# Inicializar en session_state
if "muestras" not in st.session_state:
    st.session_state.muestras = None
if "k_state" not in st.session_state:
    st.session_state.k_state = k
if "size_state" not in st.session_state:
    st.session_state.size_state = size

# Botón para simular
if st.button("Simular", key="multi_button"):
    # Guardamos los valores actuales para que no cambien
    st.session_state.k_state = k
    st.session_state.size_state = size
    
    # Crear inputs dinámicos según k
    pvals = [1/k for i in range(k)]
    
    # Verificar que las probabilidades sumen 1
    if np.isclose(sum(pvals), 1.0):
        st.session_state.muestras = np.random.multinomial(n, pvals, size=size)
    else:
        st.error("⚠️ La suma de las probabilidades debe ser 1.")

# Si ya hay muestras guardadas, mostrarlas
# Y solo si los parámetros no han cambiado desde la última simulación
if st.session_state.muestras is not None and st.session_state.k_state == k and st.session_state.size_state == size:
    muestras = st.session_state.muestras
    
    st.write("Resultados (cada fila es una simulación):")

    # Crear un DataFrame con el arreglo de NumPy
    df_muestras = pd.DataFrame(
        muestras,
        index=np.arange(1, st.session_state.size_state + 1),  # El índice de la fila empieza en 1
        columns=[f"Categoria. {i+1}" for i in range(st.session_state.k_state)] # Nombres de columna
    )
    
    # Mostrar el DataFrame, que ya incluye el índice
    st.dataframe(df_muestras)
    
    # Selector de fila 
    fila = st.number_input(
        "Elige el número de simulación para graficar",
        min_value=1, max_value=st.session_state.size_state, value=1, step=1
    )
    
    # Histograma de la simulación seleccionada
    seleccion = df_muestras.iloc[fila-1]

    fig, ax = plt.subplots()

    # Generar colores diferentes para cada categoría
    colors = plt.cm.tab10.colors  # paleta de 10 colores (puedes cambiarla)
    colores = [colors[i % len(colors)] for i in range(st.session_state.k_state)]

    # Dibujar barras
    bars = ax.bar(
        np.arange(1, st.session_state.k_state+1),   # posiciones
        seleccion,           # alturas (frecuencia de cada categoría)
        color=colores,       # colores distintos
        edgecolor='black',
        width=0.6
    )

    # Agregar el valor encima de cada barra
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,  # centro de la barra
            height + 0.005,                     # un poco arriba del borde
            str(height),                      # texto = conteo
            ha='center', va='bottom', fontsize=10, fontweight='bold'
        )

    # Configuración del gráfico
    ax.set_xticks(range(1, st.session_state.k_state+1))
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Frecuencia")
    ax.set_title(f"Histograma de la simulación #{fila}")

    st.pyplot(fig)