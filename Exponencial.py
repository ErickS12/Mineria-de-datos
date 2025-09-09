import random
import matplotlib.pyplot as plt
import math
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

def abrir_ventana():
    ventana = tk.Toplevel()
    ventana.title("Simulador Exponencial")
    ventana.geometry("800x700")

    # Frame para los inputs
    input_frame = tk.Frame(ventana, padx=10, pady=10)
    input_frame.pack()

    tk.Label(input_frame, text="Muestra:").pack(side=tk.LEFT, padx=5)
    entry_repe = tk.Entry(input_frame)
    entry_repe.insert(0, "1000")
    entry_repe.pack(side=tk.LEFT, padx=5)

    tk.Label(input_frame, text="Lambda:").pack(side=tk.LEFT, padx=5)
    entry_lamb = tk.Entry(input_frame)
    entry_lamb.insert(0, "20")
    entry_lamb.pack(side=tk.LEFT, padx=5)

    label_status = tk.Label(ventana, text="", fg="black")
    label_status.pack()

    graph_frame = tk.Frame(ventana)
    graph_frame.pack(pady=10)

    # --- Función de simulación ---
    def simu():
        try:
            repe = int(entry_repe.get())
            lambdaa = float(entry_lamb.get())

            if repe <= 0 or lambdaa <= 0:
                messagebox.showerror("Error de entrada", "Los valores deben ser enteros positivos.")
                return
        except ValueError:
            messagebox.showerror("Error de entrada", "Por favor, ingrese números enteros válidos.")
            return

        label_status.config(text="Simulación en curso...", fg="blue")
        ventana.update_idletasks()

        mu = []
        x = []
        for i in range(repe):
            mu.append(random.random())
            x.append(math.log(1 - mu[i]) / (-lambdaa))

        # Limpiar gráfico anterior
        for widget in graph_frame.winfo_children():
            widget.destroy()

        # Crear histograma
        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)

        N, bins, patches = ax.hist(x, bins=30, color='skyblue', edgecolor='black')

        # Añadir frecuencias encima de las barras
        for i in range(len(patches)):
            altura = patches[i].get_height()
            x_pos = patches[i].get_x() + patches[i].get_width() / 2
            ax.text(x_pos, altura, str(int(altura)), ha='center', va='bottom')

        ax.set_title('Histograma de una exponencial')
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