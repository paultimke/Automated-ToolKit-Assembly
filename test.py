import tkinter as tk
from tkinter import *
from tkinter import ttk

root = tk.Tk()

def hola():
    print("Hola")

def deact(btn):
    btn.grid_forget()

def act(btn):
    btn.grid(column=0,row = 0)

btn = ttk.Button(text = 'Hola', command = hola)
btn.grid(column=0, row = 0)

btn_deact = ttk.Button(text = 'deactivate', command = lambda : deact(btn))
btn_deact.grid(column=1, row = 0)

btn_act = ttk.Button(text = "act", command = lambda: act(btn))
btn_act.grid(column=2, row = 0)

root.mainloop()