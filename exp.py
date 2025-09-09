import numpy as np
import matplotlib.pyplot as plt
import streamlit as st 

def main():
    st.title("Distribución Exponencial")

    # --- Controles en la interfaz ---
    lmbda = st.slider("Valor de λ (lambda)", min_value=1, max_value=200, value=1, step=1)
    n = st.number_input("Número de pruebas", min_value=1, max_value=50000, value=10000, step=1000)

    # --- Generar datos ---
    U = np.random.rand(n)
    X = -np.log(1 - U) / lmbda

    # --- Graficar ---
    plt.figure(figsize=(8,5))
    plt.hist(X, bins=50, density=True, alpha=0.6, color="blue", label="Simulación", rwidth=0.7)

    x_vals = np.linspace(0, max(X), 200)
    f_x = lmbda * np.exp(-lmbda * x_vals)
    plt.plot(x_vals, f_x, 'r-', linewidth=2, label="Teórica")

    plt.title(f"Distribución Exponencial (λ = {lmbda})")
    plt.xlabel("x")
    plt.ylabel("Densidad")
    plt.legend()

    st.pyplot(plt)

    # --- Mostrar muestra ---
    st.subheader("Muestra generada")
    st.write("Aquí están los primeros 20 valores de la muestra simulada:")
    st.write(X[:20])  # solo mostramos 20 para no saturar

    # Opción: tabla completa (con scroll si es grande)
    if st.checkbox("Mostrar toda la muestra"):
        st.dataframe(X)

if __name__ == "__main__":
    main()

