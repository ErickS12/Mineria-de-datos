# Gibbs.py
import streamlit as st
import sympy as sp
from sympy import integrate, N
import random
import numpy as np
import plotly.graph_objects as go


# --- Lógica de Cálculo y Gráfica ---
def ejecutar_simulacion(f_str, lim_inf_str, lim_sup_str, x_inicial_str, y_inicial_str, muestra_str):
    """
    Función que se ejecuta al presionar el botón de Streamlit.
    """
    st.write("Calculando... Esto puede tardar unos segundos.")
    chart_container = st.empty()

    try:
        # --- 1. OBTENER Y VALIDAR DATOS DE LA INTERFAZ ---
        x, y, u = sp.symbols('x y u')
        f = sp.sympify(f_str)
        lim_inf = float(lim_inf_str)
        lim_sup = float(lim_sup_str)
        x_inicial = float(x_inicial_str)
        y_inicial = float(y_inicial_str)
        muestra = int(muestra_str)

        if lim_sup <= lim_inf:
            st.error("El límite superior debe ser mayor que el inferior.")
            return

        # --- 2. CÁLCULOS DEL MUESTREADOR DE GIBBS ---
        # Se usa el punto inicial proporcionado, sin importar si está dentro de los límites.
        puntos = [[x_inicial, y_inicial]]

        # CÁLCULO DE LA CDF INVERSA PARA X
        marginal_y = integrate(f, (x, lim_inf, lim_sup))
        condicional_x_dado_y = integrate(sp.cancel(f / marginal_y), (x, lim_inf, x))
        soluciones_x = sp.solve(sp.Eq(condicional_x_dado_y, u), x)

        solucion_x = None
        test_mid_point = (lim_sup + lim_inf) / 2
        for sol in soluciones_x:
            try:
                eval_sol = N(sol.subs({u: 0.5, y: test_mid_point}))
                if lim_inf <= eval_sol <= lim_sup:
                    solucion_x = sol
                    break
            except (TypeError, sp.SympifyError):
                continue
        if solucion_x is None:
            st.error("No se encontró una solución válida para la CDF inversa de X.")
            return

        # CÁLCULO DE LA CDF INVERSA PARA Y
        marginal_x = integrate(f, (y, lim_inf, lim_sup))
        condicional_y_dado_x = integrate(sp.cancel(f / marginal_x), (y, lim_inf, y))
        soluciones_y = sp.solve(sp.Eq(condicional_y_dado_x, u), y)

        solucion_y = None
        for sol in soluciones_y:
            try:
                eval_sol = N(sol.subs({u: 0.5, x: test_mid_point}))
                if lim_inf <= eval_sol <= lim_sup:
                    solucion_y = sol
                    break
            except (TypeError, sp.SympifyError):
                continue
        if solucion_y is None:
            st.error("No se encontró una solución válida para la CDF inversa de Y.")
            return

        burn_in = 200
        progress_bar = st.progress(0)

        for i in range(1, muestra + burn_in):
            u_n_x = random.random()
            x_n = solucion_x.subs({y: puntos[i - 1][1], u: u_n_x}).evalf()

            u_n_y = random.random()
            y_n = solucion_y.subs({x: x_n, u: u_n_y}).evalf()

            puntos.append([x_n, y_n])
            progress_bar.progress(i / (muestra + burn_in))

        puntos_finales = puntos[burn_in:]

        # --- 3. PREPARAR DATOS PARA LA GRÁFICA 3D ---
        puntos_np = np.array(puntos_finales, dtype=float)
        px, py = puntos_np[:, 0], puntos_np[:, 1]
        f_numerica = sp.lambdify((x, y), f, 'numpy')
        pz = f_numerica(px, py)

        grid_x = np.linspace(lim_inf, lim_sup, 40)
        grid_y = np.linspace(lim_inf, lim_sup, 40)
        X, Y = np.meshgrid(grid_x, grid_y)
        Z = f_numerica(X, Y)

        # Calcular el valor de f(x,y) en el punto inicial
        pz_inicial = f_numerica(np.array([x_inicial]), np.array([y_inicial]))

        # --- 4. DIBUJAR LA GRÁFICA CON PLOTLY ---
        fig = go.Figure()

        # Superficie
        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale="Viridis",
            opacity=0.6,
            showscale=False
        ))

        # Puntos de Gibbs
        fig.add_trace(go.Scatter3d(
            x=px, y=py, z=pz,
            mode="markers",
            marker=dict(size=3, color="red"),
            name=f"{muestra} Puntos"
        ))

        # MODIFICACIÓN: Punto inicial
        fig.add_trace(go.Scatter3d(
            x=[x_inicial], y=[y_inicial], z=pz_inicial,
            mode="markers",
            marker=dict(size=8, color="green", symbol='circle'),  # Marcador más grande y verde
            name="Punto Inicial"
        ))

        fig.update_layout(
            scene=dict(
                xaxis_title="Eje X",
                yaxis_title="Eje Y",
                zaxis_title="f(x,y)"
            ),
            title="Muestras de Gibbs sobre f(x,y) y Punto Inicial",  # Título actualizado
            paper_bgcolor='white',
            plot_bgcolor='black',
            font=dict(color='black')
        )

        with chart_container.container():
            st.plotly_chart(fig, use_container_width=True)
            st.success("Simulación finalizada. Resultados mostrados a continuación.")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
        st.warning("Revisa la función y los límites. Asegúrate de que las soluciones de la CDF inversa sean válidas.")
        chart_container.empty()


# --- Interfaz de Usuario para Streamlit ---
def show_gibbs():
    st.header("Muestreador de Gibbs")
    st.write("Genera muestras de una distribución de probabilidad conjunta f(x,y) usando el algoritmo de Gibbs.")
    st.markdown("""
        <div class="caja-info">
            <h4>Concepto del Muestreador de Gibbs</h4>
            <p>El Muestreador de Gibbs es un algoritmo utilizado en estadística para generar muestras de una distribución de probabilidad multivariada compleja, especialmente cuando el muestreo directo es difícil. Funciona extrayendo muestras repetidamente de cada variable, condicionando a los valores más recientes de las otras.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("Parámetros de Entrada", expanded=True):
        f_str = st.text_input("Función f(x, y):", value="(1/28)*(2*x+3*y+2)")

        col1, col2 = st.columns(2)
        with col1:
            lim_inf_str = st.text_input("Límite inferior:", value="0")
            x_inicial_str = st.text_input("X inicial:", value="1")
        with col2:
            lim_sup_str = st.text_input("Límite superior:", value="2")
            y_inicial_str = st.text_input("Y inicial:", value="1")

        muestra_str = st.text_input("Tamaño de muestra:", value="250")

    if st.button("Ejecutar Simulación"):
        ejecutar_simulacion(f_str, lim_inf_str, lim_sup_str, x_inicial_str, y_inicial_str, muestra_str)