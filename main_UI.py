import tkinter as tk
from tkinter import *
from tkinter import ttk
from turtle import bgcolor
import pandas as pd
import csv 

import helper
import main
import Global_vars as global_vars


class Registro_kits(tk.Toplevel):#***************** VENTANA DE REGISTRO DE KITS ********************

	def __init__(self,parent):
		"""La estructura y el comportamiento de cada elemento en la ventana de registro de kits"""
		super().__init__(parent)

		#Caracteristicas de la ventana
		self.title("Registro de kits (Nombre temporal)")
		self.configure(bg = global_vars.UI_BACKGROUND_COLOR)

		#Frames de trabajo
		self.frm1 = ttk.Frame(self, padding=20)
		self.frm1.grid()

		self.frm2 = ttk.Frame(self)
		self.frm2.grid()

		self.frm3 = ttk.Frame(self, padding=20)
		self.frm3.grid()

		#Constantes necesarias
		self.dict_variables = {}
		self.contador = 4
		self.df = pd.read_csv("Kits_DataBase.csv")
		self.cantidad_de_renglones = len(self.df.index)
		self.kit_titulo = tk.StringVar()

		#FRAME 1
		ttk.Label(self.frm1, text="Nombre del kit:").grid(column=0, row=0)
		ttk.Label(self.frm1, width=3).grid(column=1, row=0)
		self.textbox = ttk.Entry(self.frm1, textvariable=self.kit_titulo).grid(column=2, row=0)

		#FRAME 2
		for renglon in range(0,self.cantidad_de_renglones):
			self.dict_variables[renglon] = globals()[f'tornillo_tipo{self.df.iloc[renglon][0]}+1'] = tk.IntVar()

			ttk.Label(self.frm2, text="").grid(column=0, row=self.contador-1)
			ttk.Label(self.frm2, text=f"Tipo {self.df.iloc[renglon][0]}:").grid(column=0, row=self.contador)
			ttk.Label(self.frm2, width=1).grid(column=1, row=self.contador)

			self.spinbox = ttk.Spinbox(self.frm2, width=6, from_=0, to=9999, textvariable=self.dict_variables[renglon]).grid(column=2, row=self.contador)

			self.contador += 2

		#FRAME 3
		ttk.Button(self.frm3, text='Guardar kit', command=self.register_csv_Values).grid(column=0, row=0)
		ttk.Label(self.frm3, width=3).grid(column=1, row=0)
		ttk.Button(self.frm3, text='Cerrar ventana', command=self.destroy).grid(column=2, row=0)
	#FIN DE LA FUNCION __init__()

	def register_csv_Values(self):
		"""Imprime los valores en el csv al seleccionar el boton 'guardar kit'"""
		with open ('GUI/DB_Selector.csv', 'r') as r:
			csv_reader = csv.reader(r)
			self.bigdata = list(csv_reader)

		#Constantes necesarias
		#self.fixcsv = [['','T1','T2','T3','T4'],['test','1','2','3','4']] <- esto es para arreglar la base de datos en caso de perdida durante los cambios al codigo
		self.header = ['']
		self.data = []
		self.flag = True
		self.data.append(self.kit_titulo.get())

		for renglon in range(0,self.cantidad_de_renglones):
			self.header.append(f'T{renglon+1}') #Se reconstruye el header debido a la calidad variable de los T_Tornillo
			self.data.append(self.dict_variables[renglon].get()) #Se construye un renglon nuevo para el nuevo kit

		self.bigdata[0] = (self.header) #Se reemplaza el viejo header con el nuevo, en caso de haber nuevos T_tornillos

		for element in range(0,len(self.bigdata)): #Se hace un for para comprobar si ya existe el nombre del kit dentro de la base de datos
			if self.bigdata[element][0] != self.data[0]:
				continue
			elif self.bigdata[element][0] == self.data[0]:
				self.bigdata[element] = self.data
				self.flag = False

		if self.flag == True: #si la bandera se queda activa durante todo el for pasado, eso significa que como minimo el nombre es nuevo
			self.bigdata.append(self.data) 

		with open('GUI/DB_Selector.csv', 'w', newline='') as f: #Se escribe el nuevo bigdata renglon por renglon en el csv
			writer = csv.writer(f)
			for x in range(0,len(self.bigdata)):
				writer.writerow(self.bigdata[x])
	#FIN DE LA FUNCION register_csv_values()
#END OF CLASS Registro_kits

class root(tk.Tk):#******************************* VENTANA PRINCIPAL ******************************

	def __init__(self):
		"""La estructura y el comportamiento de cada elemento en la ventana principal"""
		super().__init__()

		#Caracteristicas de la ventana
		self.title("Selector de kits (Nombre temporal)")
		self.configure(bg = global_vars.UI_BACKGROUND_COLOR)

		#Frames de trabajo
		self.frm1 = ttk.Frame(self, padding=20)
		self.frm1.grid()
		self.frm2 = ttk.Frame(self, padding=20)
		self.frm2.grid()

		#Constantes necesarias
		self.cantidad_seleccion = tk.IntVar()
		self.seleccion = tk.StringVar()
		self.lista_kits = []
		self.send_list = []

		with open ('GUI/DB_Selector.csv', 'r') as r: #Esto es para adquirir los nombres de los kits para desplegar en el Combobox
			csv_reader = csv.reader(r)
			self.bigdata = list(csv_reader)
		for x in range(1,len(self.bigdata)):
			self.lista_kits.append(self.bigdata[x][0]) 


		#FRAME 1
		ttk.Label(self.frm1, text="Seleccionar kit:").grid(column=0, row=0)
		ttk.Label(self.frm1, text="Cantidad de kits a realizar:").grid(column=2, row=0)

		self.cbox = ttk.Combobox(self.frm1, state = 'readonly',
								values = self.lista_kits, 
								textvariable = self.seleccion, 
								postcommand = self.updt_Combobox)
		self.cbox.grid(column=0, row=1) #NOTA: esta linea tiene que estar aparte, de lo contrario, nunca se actualizara el combobox
		ttk.Label(self.frm1, width=6).grid(column=1, row=1)
		ttk.Spinbox(self.frm1, from_=0, to=9999, textvariable=self.cantidad_seleccion).grid(column=2, row=1)
		ttk.Label(self.frm1, width=3).grid(column=3, row=1)
		global_vars.StartProcess_Btn = ttk.Button(self.frm1, text="Enviar Instrucción", command=self.Start_Main_Process)
		global_vars.StartProcess_Btn.grid(column=4, row=1) #el text es temporal

		#FRAME 2
		ttk.Label(self.frm2, width=3).grid(column=1, row=0)
		Reg_button = ttk.Button(self.frm2, text="Registrar kit nuevo", command=self.Open_Registro)
		Reg_button.grid(column=2, row=0)
	#FIN DE LA FUNCION __init__()

	#Registro de kits - ventana
	def Open_Registro(self):
		"""La unica funcion es abrir la ventana de registro de kits al presionar el boton correspondiente en la UI"""
		Registro = Registro_kits(self)
		Registro.grab_set()
	#FIN DE LA FUNCION open_registro()

	def Start_Main_Process(self):
		""" 1. - Se encarga de juntar los datos y de enviarlos
			2. - Luego Empieza todo el proceso, desde crear los kits de referncia,
				mandar la informacion al PLC del conveyor y el Robot para armar los kits
				en fisico. Y finalmente, tomar la imagen y clasificar para ver si el kit
				se armo de forma correcta."""

		# Disable Button during Process to avoid multiple requests until process is done
		global_vars.StartProcess_Btn.grid_forget()

		# Collect the kit information from the User Interface
		for x in range(0,len(self.bigdata)):
			if self.bigdata[x][0] == self.seleccion.get():
				self.send_list = self.bigdata[x][1:]
			else:
				continue

		self.lista_fin = [self.seleccion.get(), self.cantidad_seleccion.get()]
		self.lista_fin.append(self.send_list)

		# ---- Start The Process ---- #

		# Create kit with the apropiate format needed for classification
		ref_kit = helper.create_Kit(self.lista_fin)

		# Send Commands to Robot and Conveyor PLC to start Assembly
		DESIRED_KIT_NAME   : str = self.lista_fin[0]
		DESIRED_ITERATIONS : int = self.lista_fin[1]
		main.Start_Assembly(DESIRED_KIT_NAME, DESIRED_ITERATIONS)

		# Takes an image of the assembled kit and verifies it for correctness
		main.Verify_Kit(ref_kit)

		print(self.lista_fin)

		# Process is done, now we can enable the Button again
		global_vars.StartProcess_Btn.grid(column=4, row=1)
	#FIN DE LA FUNCION Start_Main_Process()

	def updt_Combobox(self):
		"""Se encarga de actualizar la lista del combobox cada vez que es desplegada"""
		self.lista_kits = []
		with open ('GUI/DB_Selector.csv', 'r') as r:
			csv_reader = csv.reader(r)
			self.bigdata = list(csv_reader)
		for x in range(1,len(self.bigdata)):
			self.lista_kits.append(self.bigdata[x][0])
		self.cbox['values'] = self.lista_kits
	#FIN DE LA FUNCION updt_Combobox()
#END OF CLASS root()