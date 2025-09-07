import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulador Normal Estandar", layout="centered")
st.title("Simulación de una función de densidad normal estándar")

# Número de simulaciones
n3 = st.number_input("Número de simulaciones (n)", min_value=1, value=1000, step=100, key="n3_input")

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

# Inputs de media y varianza
media = st.number_input("Media (μ)", value=0.0, step=0.1, key="media_input")
varianza = st.number_input("Varianza (σ²)", min_value=0.1, value=1.0, step=0.1, key="varianza_input")

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
