import random
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def abrir_ventana():
    # Usamos Toplevel, no Tk()
    ventana = tk.Toplevel()
    ventana.title("Simulador de Moneda")

    # --- Frame de entradas ---
    input_frame = tk.Frame(ventana, padx=10, pady=10)
    input_frame.pack()

    label_lanza = tk.Label(input_frame, text="Número de lanzamientos:")
    label_lanza.pack(side=tk.LEFT, padx=5)

    entry_lanza = tk.Entry(input_frame)
    entry_lanza.insert(0, "100000")
    entry_lanza.pack(side=tk.LEFT, padx=5)

    label_exito = tk.Label(input_frame, text="Probabilidad de éxito:")
    label_exito.pack(side=tk.LEFT, padx=5)

    entry_exito = tk.Entry(input_frame)
    entry_exito.insert(0, "0.5")
    entry_exito.pack(side=tk.LEFT, padx=5)

    label_status = tk.Label(ventana, text="", fg="black")
    label_status.pack()

    graph_frame = tk.Frame(ventana)
    graph_frame.pack(pady=10)

    # --- Función del proceso ---
    def bin():
        lanza = int(entry_lanza.get())
        exito = float(entry_exito.get())
        conteo = np.array([0, 0])  # fracasos y éxitos
        for i in range(lanza):
            num = random.random()
            if num < exito:
                conteo[0] += 1
            else:
                conteo[1] += 1

        # Limpiar el frame anterior (si hay un gráfico viejo)
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Crear gráfico
        posiciones_x = np.arange(1)
        ancho_barra = 0.35
        fig, ax = plt.subplots()

        barra1 = ax.bar(posiciones_x - ancho_barra / 2, conteo[0], ancho_barra, label='Fracaso', color='royalblue')
        barra2 = ax.bar(posiciones_x + ancho_barra / 2, conteo[1], ancho_barra, label='Éxito', color='coral')

        ax.set_ylabel('Número de éxitos y fracasos')
        ax.set_title('Fracaso vs Éxitos')
        ax.set_xticks(posiciones_x)
        ax.set_xticklabels(['Comparación'])
        ax.legend()
        ax.set_ylim(0, 100000)

        ax.bar_label(barra1, padding=3, fmt='%.0f')
        ax.bar_label(barra2, padding=3, fmt='%.0f')

        # Integrar gráfico en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

        label_status.config(text="Simulación completada.", fg="green")

    # Botón de ejecutar
    button_run = tk.Button(input_frame, text="Ejecutar Simulación", command=bin)
    button_run.pack(side=tk.LEFT, padx=5)
    button_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    button_salir.pack(pady=10)