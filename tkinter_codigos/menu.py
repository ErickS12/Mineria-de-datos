import tkinter as tk
import tkinter_codigos.binoPuntual as binoPuntual  # aquí está tu proceso
import tkinter_codigos.binomialInter as binomialInter   # cuando tengas otro, lo agregas
import tkinter_codigos.Multinomial as Multinomial
import tkinter_codigos.Multinomialc2 as Multinomialc2
import tkinter_codigos.Exponencial as Exponencial
import tkinter_codigos.Normal as Normal
import tkinter_codigos.NormalVARyMED as NormalVARyMED
import Gibbs

def salir():
    root.quit()

# ventana principal
root = tk.Tk()
root.title("Menú Principal")
root.geometry("450x550")

# Título
tk.Label(root, text="Selecciona una opción", font=("Arial", 14)).pack(pady=20)

# Botón que abre la ventana del proceso binomial puntual
tk.Button(root, text="Binomial puntual (Bernulli)", width=20, command=binoPuntual.abrir_ventana).pack(pady=10)
tk.Button(root, text="Binomial", width=20, command=binomialInter.abrir_ventana).pack(pady=10)
tk.Button(root, text="Multinomial", width=20, command=Multinomial.abrir_ventana).pack(pady=10)
tk.Button(root, text="Multinomial con repetición", width=20, command=Multinomialc2.abrir_ventana).pack(pady=10)
tk.Button(root, text="Exponencial", width=20, command=Exponencial.abrir_ventana).pack(pady=10)
tk.Button(root, text="Normal", width=20, command=Normal.abrir_ventana).pack(pady=10)
tk.Button(root, text="Normal con  media y varianza", width=20, command=NormalVARyMED.abrir_ventana).pack(pady=10)
tk.Button(root, text="Gibbs", width=20, command=Gibbs.abrir_gibbs).pack(pady=10)

tk.Button(root, text="Salir", width=20, command=salir).pack(pady=20)

root.mainloop()
