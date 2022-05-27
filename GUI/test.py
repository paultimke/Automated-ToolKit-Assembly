import tkinter as tk
from tkinter import *
from tkinter import ttk


root = tk.Tk()
#^Necesario para iniciar la interfaz
root.title("Configuracion de kits")
#^Ponerle titulo en el margen de la interfaz

def sendValues():
	"""Las acciones que se ejecutaran al momento de presionar el boton dentro y durante la interfaz grafica"""

	dict_cantidades1 = {"Tipo_1": kit1_tornillo1.get(), "Tipo_2": kit1_tornillo2.get(), "Tipo_3": kit1_tornillo3.get(), "Tipo_4":kit1_tornillo4.get()}
	#^Aqui estamos haciendo un diccionario, donde la llave es "tipo_#" y el valor de cada llave seria la cantidad de tornillos que se quieren dentro del kit

	dict_fin = {f"{kit1.get()}": dict_cantidades1}
	#^Aqui estamos metiendo el diccionario anterior dentro de un diccinario "externo", el cual liga las cantidades de tornillos a cada kit respectivamente
	#Idealmente seria mejor tener un nombre que no cambie, pero solo para que se vea bonito en el prototipo, utilice lo que sea que este escrito en el Entry

	print(dict_fin)
	#Este print es temporal, es solo para comprobar que funciona

#FRAME 1
frm1 = ttk.Frame(root, padding=20)
#^ Definimos el area de trabajo sobre el nombre frm1 (que viene de frame 1)

frm1.grid()
#^ Definimos una estructura de "grid" al area de trabajo

ttk.Label(frm1, text="Kit #1:").grid(column=0, row=0)
#^ Le ponemos un texto para decorar, en la posicion (0, 0) del grid 

ttk.Label(frm1, width=10).grid(column=1, row=0)
ttk.Label(frm1, width=3).grid(column=3, row=0)
ttk.Label(frm1, width=3).grid(column=5, row=0)
ttk.Label(frm1, width=3).grid(column=7, row=0)
#^ Añadimos espacios usando labels vacios de forma practica

ttk.Label(frm1, text="Cantidad de Tornillo 1:").grid(column=2, row=0)
ttk.Label(frm1, text="Cantidad de Tornillo 2:").grid(column=4, row=0)
ttk.Label(frm1, text="Cantidad de Tornillo 3:").grid(column=6, row=0)
ttk.Label(frm1, text="Cantidad de Tornillo 4:").grid(column=8, row=0)
#^ Estos labels solo son decoracion

kit1 = tk.StringVar()
#^ Creamos una variable, que utilizaremos dentro de poco, definida como tipo string y bajo el nombre de "kit1"
kit1_tornillo1 = tk.IntVar()
kit1_tornillo2 = tk.IntVar()
kit1_tornillo3 = tk.IntVar()
kit1_tornillo4 = tk.IntVar()
#^ Mismo paso que el anterior solo que con int

textbox = ttk.Entry(frm1, textvariable=kit1).grid(column=0, row=1)
textbox = ttk.Entry(frm1, textvariable=kit1_tornillo1).grid(column=2, row=1)
textbox = ttk.Entry(frm1, textvariable=kit1_tornillo2).grid(column=4, row=1)
textbox = ttk.Entry(frm1, textvariable=kit1_tornillo3).grid(column=6, row=1)
textbox = ttk.Entry(frm1, textvariable=kit1_tornillo4).grid(column=8, row=1)
#Y utilizamos la variables anteriores para definir que comportamientos van a tener lo que sea que se escriba dentro de los espacios en blanco

#FRAME 2
frm2 = ttk.Frame(root, padding=20)
frm2.grid()

ttk.Button(frm2, text='Registrar kits', command=sendValues).grid(column=2, row=0)
#Todo esto es solo para el boton, lo mas importante ^ es el command, es para definir que funcion va a realizar el boton

root.mainloop()
#es como un while, que nos va a estar mostrando constantemente la interfaz