import random
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def abrir_ventana():
    ventana = tk.Toplevel()  # ventana hija
    ventana.title("Simulador Binomial")
    ventana.geometry("1150x700")

    # --- Frame para inputs ---
    input_frame = tk.Frame(ventana, padx=10, pady=10)
    input_frame.pack()

    tk.Label(input_frame, text="Repeticiones:").pack(side=tk.LEFT, padx=5)
    entry_repe = tk.Entry(input_frame)
    entry_repe.insert(0, "1000")
    entry_repe.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Lanzamientos:").pack(side=tk.LEFT, padx=5)
    entry_lanza = tk.Entry(input_frame)
    entry_lanza.insert(0, "1000")
    entry_lanza.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Probabilidad de éxito:").pack(side=tk.LEFT, padx=5)
    entry_exito = tk.Entry(input_frame)
    entry_exito.insert(0, "0.5")
    entry_exito.pack(side=tk.LEFT, padx=5)

    label_status = tk.Label(ventana, text="", fg="black")
    label_status.pack()

    graph_frame = tk.Frame(ventana)
    graph_frame.pack(pady=10)

    # --- Función de simulación ---
    def ejecutar_simulacion():
        try:
            repe = int(entry_repe.get())
            lanza = int(entry_lanza.get())
            prob_exito = float(entry_exito.get())

            if not (0 <= prob_exito <= 1):
                messagebox.showerror("Error de entrada", "La probabilidad debe estar entre 0 y 1.")
                return

            label_status.config(text="Simulación en curso...", fg="blue")
            ventana.update_idletasks()

            numExitos = []
            for _ in range(repe):
                exitos = sum(1 for _ in range(lanza) if random.random() < prob_exito)
                numExitos.append(exitos)

            # Limpiar gráfico previo
            for widget in graph_frame.winfo_children():
                widget.destroy()

            # Crear histograma
            fig = plt.Figure(figsize=(6, 5), dpi=100)
            ax = fig.add_subplot(111)

            N, bins, patches = ax.hist(numExitos, bins=30, color='skyblue', edgecolor='black')

            # Añadir texto con frecuencias
            for i in range(len(patches)):
                altura = patches[i].get_height()
                x_posicion = patches[i].get_x() + patches[i].get_width() / 2
                ax.text(x_posicion, altura, str(int(altura)), ha='center', va='bottom')

            ax.set_title('Histograma de Número de Éxitos')
            ax.set_xlabel('Número de Éxitos')
            ax.set_ylabel('Frecuencia')
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            # Integrar gráfico en Tkinter
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            canvas.draw()

            label_status.config(text="Simulación completada.", fg="green")

        except ValueError:
            messagebox.showerror("Error de entrada", "Introduce solo números válidos.")
            label_status.config(text="Error en la simulación.", fg="red")

    # Botón ejecutar
    button_run = tk.Button(input_frame, text="Ejecutar Simulación", command=ejecutar_simulacion)
    button_run.pack(side=tk.LEFT, padx=5)
    button_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    button_salir.pack(pady=10)
