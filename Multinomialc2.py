import random
import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog

def abrir_ventana():
    ventana = tk.Toplevel()
    ventana.title("Simulación Multinomial")
    ventana.geometry("600x500")

    def ejecutar_simulacion():
        try:
            # Obtener datos de la interfaz
            repe = int(entry_repe.get())
            lanza = int(entry_lanza.get())
            opc = int(entry_opc.get())

            if repe <= 0 or lanza <= 0 or opc <= 0:
                messagebox.showerror("Error", "Todos los valores deben ser enteros positivos.")
                return
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese solo números enteros.")
            return

        # Inicialización
        res = np.zeros((repe, opc))
        proba = [(i + 1) / opc for i in range(opc)]

        # Simulación
        for j in range(repe):
            for i in range(lanza):
                num = random.random()
                for k in range(opc):
                    if num < proba[k]:
                        res[j][k] += 1
                        break

        # Mostrar resultados en la ventana
        resultado_text.delete("1.0", tk.END)
        resultado_text.insert(tk.END, "📊 Resultados de TODAS las repeticiones:\n\n")
        for j in range(repe):
            resultado_text.insert(tk.END, f"Repetición {j+1}: " +
                                  ", ".join(map(str, map(int, res[j]))) + "\n")

        resultado_text.insert(tk.END, "\n✅ Última repetición:\n")
        resultado_text.insert(tk.END, ", ".join(map(str, map(int, res[-1]))))

        # Guardar en archivo txt si el usuario quiere
        if var_guardar.get() == 1:
            archivo = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text files", "*.txt")])
            if archivo:
                with open(archivo, "w") as f:
                    f.write("📊 Resultados de TODAS las repeticiones:\n\n")
                    for j in range(repe):
                        f.write(f"Repetición {j+1}: " +
                                ", ".join(map(str, map(int, res[j]))) + "\n")

                    f.write("\n✅ Última repetición:\n")
                    f.write(", ".join(map(str, map(int, res[-1]))))

    # --- Interfaz Tkinter ---
    frame_inputs = tk.Frame(ventana, padx=10, pady=10)
    frame_inputs.pack()

    # Entradas
    tk.Label(frame_inputs, text="Repeticiones:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_repe = tk.Entry(frame_inputs)
    entry_repe.insert(0, "100")
    entry_repe.grid(row=0, column=1, padx=5)

    tk.Label(frame_inputs, text="Lanzamientos:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_lanza = tk.Entry(frame_inputs)
    entry_lanza.insert(0, "1000")
    entry_lanza.grid(row=1, column=1, padx=5)

    tk.Label(frame_inputs, text="Opciones:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entry_opc = tk.Entry(frame_inputs)
    entry_opc.insert(0, "6")
    entry_opc.grid(row=2, column=1, padx=5)

    # Checkbox para guardar en archivo
    var_guardar = tk.IntVar()
    check_guardar = tk.Checkbutton(ventana, text="Guardar resultado en archivo .txt", variable=var_guardar)
    check_guardar.pack(pady=5)

    # Botón de ejecutar
    btn_run = tk.Button(ventana, text="Ejecutar Simulación", command=ejecutar_simulacion)
    btn_run.pack(pady=10)

    # Cuadro de texto para mostrar resultados
    resultado_text = tk.Text(ventana, height=15, width=70)
    resultado_text.pack(pady=10)

    # Botón salir
    btn_exit = tk.Button(ventana, text="Salir", command=ventana.destroy)
    btn_exit.pack(pady=5)
