import numpy as np
import matplotlib.pyplot as plt
import streamlit as st 
import pandas as pd

def show_exponencial():
    st.title("Distribución Exponencial")
    st.write("Explora la distribución Exponencial y su comportamiento.")
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Distribución Exponencial</h4>
            <p>La distribución Exponencial modela el tiempo transcurrido entre eventos en un proceso continuo e independiente. Es utilizada para predecir la vida útil de un componente, el tiempo entre clientes que entran a una tienda o el intervalo entre terremotos.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- Sección para la Imagen ---
    st.subheader("Ecuación")
    st.image("Imag_Exponencial.png", caption="Diagrama de un ensayo una Exponencial", use_container_width=True)
        

    # --- Controles en la interfaz ---
    lmbda = st.slider("Valor de λ (lambda)", min_value=1, max_value=200, value=1, step=1)
    n = st.number_input("Número de simulaciones (n)", min_value=1, max_value=50000, value=10000, step=1000)

    if st.button("Simular"):
    # --- Simulación ---
        # --- Generar datos ---
        U = np.random.rand(n)
        X = -np.log(1 - U) / lmbda
        st.session_state["muestra_exp"] = X
    
    if "muestra_exp" in st.session_state:
        X = st.session_state["muestra_exp"]

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

        # --- Mostrar la muestra ---
        with st.expander("¿Quieres ver la muestra?"):
            st.write("Primeros 50 valores de la muestra:")
            df = pd.DataFrame(X, columns=["Resultado"], index=range(1, len(X) + 1))
            df.index.name = "Lanzamiento"

            # Mostrar los primeros 50 valores
            st.dataframe(df.head(50))

            # Checkbox para mostrar toda la muestra
            if st.checkbox("Mostrar toda la muestra"):
                st.dataframe(df)

