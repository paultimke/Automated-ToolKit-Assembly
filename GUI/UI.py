import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd

class Registro_kits(tk.Toplevel):#***************** VENTANA DE REGISTRO DE KITS ********************

	def __init__(self,parent):
		super().__init__(parent)

		#Caracteristicas de la ventana
		self.title("Registro de kits (Nombre temporal)")

		#Frames de trabajo
		self.frm1 = ttk.Frame(self, padding=20)
		self.frm1.grid()

		self.frm2 = ttk.Frame(self)
		self.frm2.grid()

		self.frm3 = ttk.Frame(self, padding=20)
		self.frm3.grid()

		#Constantes necesarias
		self.dict_variables = {}
		self.dict_valores = {}
		self.dict_fin = {}
		self.contador = 4
		self.df = pd.read_csv("../Kits_DataBase.csv")
		self.cantidad_de_renglones = len(self.df.index)
		self.kit_titulo = tk.StringVar()

		#FRAME 1
		ttk.Label(self.frm1, text="Nombre del kit:").grid(column=0, row=0)
		ttk.Label(self.frm1, width=3).grid(column=1, row=0)
		self.textbox = ttk.Entry(self.frm1, textvariable=self.kit_titulo).grid(column=2, row=0)

		#FRAME 2
		for self.renglon in range(0,self.cantidad_de_renglones):
			self.dict_variables[self.renglon] = globals()[f'tornillo_tipo{self.renglon}+1'] = tk.IntVar()

			ttk.Label(self.frm2, text="").grid(column=0, row=self.contador-1)
			ttk.Label(self.frm2, text=f"Tornillo tipo #{self.renglon+1}:").grid(column=0, row=self.contador)
			ttk.Label(self.frm2, width=3).grid(column=1, row=self.contador)

			self.spinbox = ttk.Spinbox(self.frm2, width=6, from_=0, to=9999, textvariable=self.dict_variables[self.renglon]).grid(column=2, row=self.contador)

			self.contador += 2

		#FRAME 3
		ttk.Button(self.frm3, text='Guardar kit', command=self.printValues).grid(column=0, row=0)
		ttk.Label(self.frm3, width=3).grid(column=1, row=0)
		ttk.Button(self.frm3, text='Cerrar ventana', command=self.destroy).grid(column=2, row=0)
	#FIN DE LA FUNCION __init__()

	def printValues(self):
		for self.renglon in range(0,self.cantidad_de_renglones):
			self.dict_valores[f'T{self.renglon+1}'] = self.dict_variables[self.renglon].get()
		self.dict_fin = {self.kit_titulo.get():self.dict_valores}

		print(self.dict_fin)
	#FIN DE LA FUNCION printValues()

class root(tk.Tk):#******************************* VENTANA PRINCIPAL ******************************

	def __init__(self):
		super().__init__()

		#Caracteristicas de la ventana
		self.title("Selector de kits (Nombre temporal)")

		#Frames de trabajo
		self.frm1 = ttk.Frame(self, padding=20)
		self.frm1.grid()

		#FRAME 1
		ttk.Button(self.frm1, text="Registrar kit nuevo", command=self.open_Registro).grid(column=0, row=0)
		ttk.Button(self.frm1, text="Test").grid(column=1, row=0)
	#FIN DE LA FUNCION __init__()

	#Registro de kits - ventana
	def open_Registro(self):
		Registro = Registro_kits(self)
		Registro.grab_set()
	#FIN DE LA FUNCION open_registro()

#Iniciar codigo
if __name__ == "__main__":
	root = root()
	root.mainloop()