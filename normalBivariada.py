import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def show_normalBivariada():
    st.header("Distribución Normal Bivariada")
    st.write(
        "Genera y visualiza una distribución normal en dos variables, calculando la función de densidad manualmente.")
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto de Distribución Normal Bivariada</h4>
            <p>La distribución Normal Bivariada es una extensión de la Normal a dos variables aleatorias. Es ideal para modelar la relación entre dos variables correlacionadas, como la altura y el peso de una persona, y se representa como una campana tridimensional.</p>
        </div>
    """, unsafe_allow_html=True)
    # --- Sección para la Imagen ---
    st.subheader("Ecuación")
    st.image("images/Imag_NormalBivariada1.png", use_container_width=True)

    # --- Widgets para los Parámetros ---
    st.markdown("---")
    st.subheader("Parámetros de la Distribución")

    col1, col2 = st.columns(2)
    with col1:
        mu_x = st.slider("Media de X ($\mu_x$)", -5.0, 5.0, 0.0, 0.1)
        sigma_x = st.slider("Desviación estándar de X ($\sigma_x$)", 0.1, 5.0, 1.0, 0.1)

    with col2:
        mu_y = st.slider("Media de Y ($\mu_y$)", -5.0, 5.0, 0.0, 0.1)
        sigma_y = st.slider("Desviación estándar de Y ($\sigma_y$)", 0.1, 5.0, 1.0, 0.1)

    rho = st.slider("Coeficiente de Correlación (𝜌)", 0.0, 1.0, 0.0, 0.05, help="La correlación entre X y Y.")

    # --- Botón para Generar Gráfica ---
    if st.button("Generar Gráfica"):
        with st.spinner("Realizando cálculos y generando gráfica..."):

            # --- 1. DEFINICIÓN DE LA FUNCIÓN DE DENSIDAD DE PROBABILIDAD (PDF) ---
            def normal_bivariada_pdf(x, y, mu_x, mu_y, sigma_x, sigma_y, rho):
                """
                Calcula la PDF de una distribución normal bivariada.
                """
                # Matriz de covarianza
                cov = np.array([
                    [sigma_x ** 2, rho * sigma_x * sigma_y],
                    [rho * sigma_x * sigma_y, sigma_y ** 2]
                ])

                # Determinante de la matriz de covarianza
                det_cov = np.linalg.det(cov)

                # Inversa de la matriz de covarianza
                inv_cov = np.linalg.inv(cov)

                # Factor de normalización
                norm_factor = 1 / (2 * np.pi * np.sqrt(det_cov))

                # Vector de la variable (x,y)
                xy = np.array([x, y])

                # Vector de la media
                mu = np.array([mu_x, mu_y])

                # Exponente de la fórmula
                exponent = -0.5 * np.dot(np.dot((xy - mu).T, inv_cov), (xy - mu))

                return norm_factor * np.exp(exponent)

            # --- 2. PREPARACIÓN DE LA MALLA DE PUNTOS ---
            x = np.linspace(-10, 10, 200)
            y = np.linspace(-10, 10, 200)
            X, Y = np.meshgrid(x, y)

            # --- 3. CÁLCULO DEL VALOR DE LA PDF PARA CADA PUNTO ---
            Z = np.zeros(X.shape)
            for i in range(X.shape[0]):
                for j in range(X.shape[1]):
                    Z[i, j] = normal_bivariada_pdf(X[i, j], Y[i, j], mu_x, mu_y, sigma_x, sigma_y, rho)

            # --- 4. VISUALIZACIÓN ---
            fig = plt.figure(figsize=(12, 6))

            # Gráfica de Contorno
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.set_title("Gráfica de Contorno")
            ax1.contourf(X, Y, Z, levels=15, cmap='viridis')
            ax1.set_xlabel("X")
            ax1.set_ylabel("Y")
            ax1.set_aspect('equal')

            # Gráfica 3D
            ax2 = fig.add_subplot(1, 2, 2, projection='3d')
            ax2.set_title("Gráfica 3D de la Densidad")
            ax2.plot_surface(X, Y, Z, cmap='viridis')
            ax2.set_xlabel("X")
            ax2.set_ylabel("Y")
            ax2.set_zlabel("f(x,y)")
            ax2.view_init(elev=20, azim=45)

            st.pyplot(fig)

        st.success("¡Gráfica generada con éxito!")