import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd

dict_variables = {}
dict_valores = {}
contador = 4
#^Aqui solo se establecen dos diccionarios y un contador que seran de ayuda luego
#El contador empieza desde este numero en particular debido a la estructura que tendra la interfaz

def printValues():
	"""Esta funcion ahora mismo solo esta encargada de construir un diccionario con los valores dentro de los spinbox dinamicos"""
	for renglon in range(0,cantidad_de_renglones):
		dict_valores[f'Tipo{renglon+1}'] = dict_variables[renglon].get()
		#En este for, se le pide a python que busque las variables (las cuales estan definidas mas adelante) y consiga el valor que esta dentro
		#una vez con ese valor, se construye el segundo diccionario definido al principio del codigo

	print(dict_valores)  
	#Este print ^ es temporal y es solo para confirmar que si funciona esta parte del codigo

df = pd.read_csv("../Kits_DataBase.csv")
cantidad_de_renglones = len(df.index)
#^Aqui el codigo abre y lee cuantos tipos de tornillos hay registrados en el excel

root = tk.Tk()
#Aqui solo establecemos la variable que estaremos utilizando para la interfaz

#Frame 1
frm1 = ttk.Frame(root, padding=20)
frm1.grid()
#establecemos el area de trabajo y la estructura que tendra

ttk.Label(frm1, text="Nombre del kit:").grid(column=0, row=0)
textbox = ttk.Entry(frm1,).grid(column=0, row=1)
#Tanto la etiqueta como el espacio en blanco son correspondientes a las dos primeras unidades de la variable contador

for renglon in range(0,cantidad_de_renglones):
	dict_variables[renglon] = globals()[f'tornillo_tipo{renglon}+1'] = tk.IntVar()
	#Aqui estamos creando variables y agregandolas al diccionario de variables (definido al inicio del codigo) de forma dinamica

	ttk.Label(frm1, text="").grid(column=0, row=contador-1)
	ttk.Label(frm1, text=f"Tornillo tipo #{renglon+1}:").grid(column=0, row=contador)
	ttk.Label(frm1, width=3).grid(column=1, row=contador)
	#Aqui establecemos un espacio horizontal, una etiqueta con texto, y un espacio vertical respectivamente

	spinbox = ttk.Spinbox(frm1, width=6, from_=0, to=9999, textvariable=dict_variables[renglon]).grid(column=2, row=contador)
	#Aqui definimos el spinbox, los cuales van a ser los espacios en blanco donde estaran las cantidades de los tipos de tornillo, y los ligamos
	#A las variables dinamicas creadas al principio del for

	contador += 2
	#Aqui aumentamos el valor del contador a dos, pues es el que determina en que posicion van a estar los siguientes elementos
	#como nota, la cantidad de elementos depende de la cantidad de tipo de tornillos dentro del excel, es por eso que se utiliza un for
	#y se crean y agregan las variables a un diccionario de forma dinamica

frm2 = ttk.Frame(root, padding=20)
frm2.grid()
#Se crea una segunda area de trabajo dentro del root, y se le define con una estructura en forma de matriz

ttk.Button(frm2, text="Registrar kit", command=printValues).grid(column=0, row=0)
#Se agrega un boton al segundo frame el cual es el que se encarga de realizar la funcion establecida al principio del codigo

root.mainloop()
#Esta es la instrucion para que comience a realizar la interfaz como tal.