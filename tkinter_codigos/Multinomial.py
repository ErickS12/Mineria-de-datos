import random
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def abrir_ventana():
    ventana = tk.Toplevel()
    ventana.title("Simulador Multinomial")
    ventana.geometry("800x700")

    # Frame para los inputs
    input_frame = tk.Frame(ventana, padx=10, pady=10)
    input_frame.pack()

    tk.Label(input_frame, text="Lanzamientos:").pack(side=tk.LEFT, padx=5)
    entry_lanza = tk.Entry(input_frame)
    entry_lanza.insert(0, "1000")
    entry_lanza.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Opciones:").pack(side=tk.LEFT, padx=5)
    entry_opc = tk.Entry(input_frame)
    entry_opc.insert(0, "20")
    entry_opc.pack(side=tk.LEFT, padx=5)

    label_status = tk.Label(ventana, text="", fg="black")
    label_status.pack()

    graph_frame = tk.Frame(ventana)
    graph_frame.pack(pady=10)

    # --- Función de simulación ---
    def simu():
        try:
            lanza = int(entry_lanza.get())
            opc = int(entry_opc.get())

            if lanza <= 0 or opc <= 0:
                messagebox.showerror("Error de entrada", "Los valores deben ser enteros positivos.")
                return
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingrese números enteros válidos.")
            return

        label_status.config(text="Simulación en curso...", fg="blue")
        ventana.update_idletasks()
        # Simulación multinomial: randint entre 1 y opc
        numExitos = [random.randint(1, opc) for _ in range(lanza)]

        # Limpiar gráfico anterior
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Crear histograma
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)

        N, bins, patches = ax.hist(numExitos, bins=opc, range=(0.5, opc + 0.5),color='skyblue', edgecolor='black')

        # Añadir frecuencias encima de las barras
        for i in range(len(patches)):
            altura = patches[i].get_height()
            x_pos = patches[i].get_x() + patches[i].get_width() / 2
            ax.text(x_pos, altura, str(int(altura)), ha='center', va='bottom')

        ax.set_title('Histograma de número de repeticiones')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()

        label_status.config(text="Simulación completada.", fg="green")

    # Botón ejecutar
    button_run = tk.Button(input_frame, text="Ejecutar Simulación", command=simu)
    button_run.pack(side=tk.LEFT, padx=5)

    # Botón salir (cierra solo esta ventana)
    button_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    button_salir.pack(pady=10)
