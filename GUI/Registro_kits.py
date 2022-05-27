import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd

df = pd.read_csv("../Kits_DataBase.csv")
cantidad_de_renglones = len(df.index)
#lista = [None] * cantidad_de_renglones

def printValues():
	#for renglon in range(0,cantidad_de_renglones):
	#	dict_valores = {}
	#for x in len(lista):
	#	lista(x)=(globals()[f'varname{x}'] = x)
	print(lista)

root = tk.Tk()
frm1 = ttk.Frame(root, padding=20)
frm1.grid()
contador = 4

ttk.Label(frm1, text="Nombre del kit:").grid(column=0, row=0)
textbox = ttk.Entry(frm1,).grid(column=0, row=1) 

for x in range(0,cantidad_de_renglones):
	globals()[f'test{x}'] = tk.IntVar()

#test0 = IntVar()
#lista = []
#lista = [test1, test2, test3, test4]
#lista.append()
#lista.append(test1)
#lista.append(test2)
#lista.append(test3)

for renglon in range(0,cantidad_de_renglones):

	ttk.Label(frm1, text="").grid(column=0, row=contador-1)
	ttk.Label(frm1, text=f"Tornillo tipo #{renglon+1}:").grid(column=0, row=contador)
	ttk.Label(frm1, width=3).grid(column=1, row=contador)
	spinbox = ttk.Spinbox(frm1, width=6, from_=0, to=9999,).grid(column=2, row=contador)

	contador += 2

frm2 = ttk.Frame(root, padding=20)
frm2.grid()

ttk.Button(frm2, text="Registrar kit", command=printValues).grid(column=0, row=0)

root.mainloop()