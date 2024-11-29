import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import pandas as pd

#Diseño de la Ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry('500x400')
ventana_principal.config(background='#F5DEB3')
tk.Wm.wm_title(ventana_principal,"Sensor EsRes")

#Ventana de usuarios
def abrir_ventana_usuarios():
    # Crear una ventana secundaria
    ventana_secundaria1 = tk.Toplevel()
    ventana_secundaria1.title("Usuarios")
    ventana_secundaria1.config(width=400, height=300)
    
    def cursor():
        # Crear un Frame para contener el Listbox, Scrollbar y el botón
        frame = tk.Frame(ventana_secundaria1)
        frame.pack(pady=20)  # Agregar espacio superior e inferior al Frame
        
        # Scrollbar dentro del Frame
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox dentro del Frame
        mylist = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=10, width=40)
        for line in range(100):
            mylist.insert(tk.END, "This is line number " + str(line))
        
        mylist.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=mylist.yview)
        
        # Botón debajo del Listbox y Scrollbar
        boton_cerrar = ttk.Button(
            frame, 
            text="Cerrar", 
            command=ventana_secundaria1.destroy
        )  
        boton_cerrar.pack(pady=10, side=tk.BOTTOM)
    
    # Llamar a la función para crear el Listbox con Scrollbar y botón
    cursor()


#Labels
lname=tk.Label(ventana_principal,text='MEDIDOR DE FRECUENCIA RESPIRATORIA', bg='#F5DEB3',fg='black', font='Technic', anchor="center", padx=2, pady=2).pack()



#Boton1
boton1=tk.Button (ventana_principal,
                 text="usuario",
                 anchor="center", 
                 bd=3, 
                 bg="lightgray", 
                 cursor="hand2", 
                 disabledforeground="gray", 
                 fg="black", 
                 font=("Arial", 12), 
                 height=2, 
                 highlightbackground="black", 
                 highlightcolor="green", 
                 highlightthickness=2, 
                 justify="center", 
                 overrelief="raised", 
                 padx=10, 
                 pady=5, 
                 width=15, 
                 wraplength=100,
                 command=abrir_ventana_usuarios
                  )
boton1.pack(padx=20, pady=20)
#Boton2
boton2=tk.Button (ventana_principal,
                 text="Medición",
                 anchor="center", 
                 bd=3, 
                 bg="lightgray", 
                 cursor="hand2", 
                 disabledforeground="gray", 
                 fg="black", 
                 font=("Arial", 12), 
                 height=2, 
                 highlightbackground="black", 
                 highlightcolor="green", 
                 highlightthickness=2, 
                 justify="center", 
                 overrelief="raised", 
                 padx=10, 
                 pady=5, 
                 width=15, 
                 wraplength=100)
boton2.pack(padx=20, pady=20)

ventana_principal.mainloop()
