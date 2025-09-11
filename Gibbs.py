# Gibbs.py
import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
from sympy import integrate, N
import random
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# --- Lógica de Cálculo y Gráfica ---
def ejecutar_simulacion(f_var, lim_inf_var, lim_sup_var, muestra_var, fig, canvas):
    """
    Función que se ejecuta al presionar el botón.
    Realiza los cálculos y actualiza la gráfica en el canvas.
    """
    # Limpiamos la figura para poder graficar de nuevo
    fig.clear()

    x, y, u = sp.symbols('x y u')

    try:
        # --- 1. OBTENER Y VALIDAR DATOS DE LA INTERFAZ ---
        f = sp.sympify(f_var.get())
        lim_inf = float(lim_inf_var.get())
        lim_sup = float(lim_sup_var.get())
        muestra = int(muestra_var.get())

        if lim_sup <= lim_inf:
            raise ValueError("El límite superior debe ser mayor que el inferior.")

        # --- 2. CÁLCULOS DEL MUESTREADOR DE GIBBS ---
        puntos = [[random.uniform(lim_inf, lim_sup), random.uniform(lim_inf, lim_sup)]]

        # --- CÁLCULO DE LA CDF INVERSA PARA X ---
        marginal_y = integrate(f, (x, lim_inf, lim_sup))
        condicional_x_dado_y = integrate(sp.cancel(f / marginal_y), (x, lim_inf, x))
        soluciones_x = sp.solve(sp.Eq(condicional_x_dado_y, u), x)

        # Filtramos las soluciones para encontrar la correcta en lugar de tomar la primera [0]
        solucion_x = None
        test_mid_point = (lim_sup + lim_inf) / 2
        for sol in soluciones_x:
            # N() evalúa numéricamente la expresión para probarla
            if lim_inf <= N(sol.subs({u: 0.5, y: test_mid_point})) <= lim_sup:
                solucion_x = sol
                break
        if solucion_x is None:
            raise ValueError("No se encontró una solución válida para la CDF inversa de X.")

        # --- CÁLCULO DE LA CDF INVERSA PARA Y ---
        marginal_x = integrate(f, (y, lim_inf, lim_sup))
        condicional_y_dado_x = integrate(sp.cancel(f / marginal_x), (y, lim_inf, y))
        soluciones_y = sp.solve(sp.Eq(condicional_y_dado_x, u), y)

        # Repetimos la misma lógica de filtrado para 'y'
        solucion_y = None
        for sol in soluciones_y:
            if lim_inf <= N(sol.subs({u: 0.5, x: test_mid_point})) <= lim_sup:
                solucion_y = sol
                break
        if solucion_y is None:
            raise ValueError("No se encontró una solución válida para la CDF inversa de Y.")

        burn_in = 1000

        for i in range(1, muestra + burn_in):
            u_n_x = random.random()
            x_n = solucion_x.subs({y: puntos[i - 1][1], u: u_n_x}).evalf()

            u_n_y = random.random()
            y_n = solucion_y.subs({x: x_n, u: u_n_y}).evalf()

            puntos.append([x_n, y_n])

        # Se descartan las primeras 'burn_in' muestras
        puntos_finales = puntos[burn_in:]

        # --- 3. PREPARAR DATOS PARA LA GRÁFICA 3D ---
        puntos_np = np.array(puntos_finales, dtype=float)
        px, py = puntos_np[:, 0], puntos_np[:, 1]
        f_numerica = sp.lambdify((x, y), f, 'numpy')
        pz = f_numerica(px, py)

        grid_x = np.linspace(lim_inf, lim_sup, 30)
        grid_y = np.linspace(lim_inf, lim_sup, 30)
        X, Y = np.meshgrid(grid_x, grid_y)
        Z = f_numerica(X, Y)

        # --- 4. DIBUJAR LA GRÁFICA EN EL CANVAS ---
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z, alpha=0.6, cmap='viridis', rstride=1, cstride=1, edgecolor='none')
        ax.scatter(px, py, pz, color='red', s=15, label=f'{muestra} Puntos', depthshade=True)
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_zlabel('f(x,y)')
        ax.legend()
        ax.set_title("Muestras de Gibbs sobre f(x,y)")

        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error",
                             f"Ocurrió un error: {e}\n\nRevisa la función y los límites. Asegúrate de que las soluciones de la CDF inversa sean válidas.")


# --- Interfaz Gráfica ---
def abrir_gibbs():
    """
    Función principal que crea y configura la ventana de la interfaz.
    Esta función es la que se llama desde el menú principal.
    """
    # Crear la ventana secundaria (Toplevel)
    window = tk.Toplevel()
    window.title("Muestreador de Gibbs (Versión Funciones)")
    window.geometry("450x600")
    window.minsize(600, 800)

    main_frame = ttk.Frame(window, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Variables para almacenar el contenido de los Entry
    f_var = tk.StringVar(value="(1/28)*(2*x+3*y+2)")
    lim_inf_var = tk.StringVar(value="0")
    lim_sup_var = tk.StringVar(value="2")
    muestra_var = tk.StringVar(value="250")

    # --- Creación de Widgets ---
    # Frame para las entradas del usuario
    input_frame = ttk.LabelFrame(main_frame, text="Parámetros de Entrada", padding="10")
    input_frame.pack(fill=tk.X, pady=5)

    ttk.Label(input_frame, text="Función f(x, y):").pack(anchor="w")
    ttk.Entry(input_frame, textvariable=f_var).pack(fill=tk.X, pady=(0, 5))

    ttk.Label(input_frame, text="Límite inferior:").pack(anchor="w")
    ttk.Entry(input_frame, textvariable=lim_inf_var).pack(fill=tk.X, pady=(0, 5))

    ttk.Label(input_frame, text="Límite superior:").pack(anchor="w")
    ttk.Entry(input_frame, textvariable=lim_sup_var).pack(fill=tk.X, pady=(0, 5))

    ttk.Label(input_frame, text="Tamaño de muestra:").pack(anchor="w")
    ttk.Entry(input_frame, textvariable=muestra_var).pack(fill=tk.X)

    # Canvas para la gráfica de Matplotlib
    graph_frame = ttk.Frame(main_frame)
    graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    fig = Figure(figsize=(5, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Frame para los botones
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X)

    # Botón para ejecutar
    ttk.Button(
        button_frame,
        text="Ejecutar Simulación",
        command=lambda: ejecutar_simulacion(f_var, lim_inf_var, lim_sup_var, muestra_var, fig, canvas)
    ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

    # Botón para salir
    ttk.Button(
        button_frame,
        text="Salir",
        command=window.destroy
    ).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))
