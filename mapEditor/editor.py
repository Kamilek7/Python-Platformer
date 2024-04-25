from tkinter import *
from tkinter.ttk import *
import xml.etree.cElementTree as ET

 # Funkcje do wykorzystania

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def addTerrain(type):
   print(type)
 # Budowa aplikacji


root = Tk()
root.title("Edytor")
canvasFrame = Frame(root)
canvasFrame.grid(row = 1, column = 1)

 # Menu (pasek u gory)
menu = Menu(root)
 # zakladka file
fileMenu = Menu(menu, tearoff=0)
fileMenu.add_command(label="New", command=donothing)
fileMenu.add_command(label="Open", command=donothing)
fileMenu.add_command(label="Save", command=donothing)
fileMenu.add_command(label="Save as...", command=donothing)
fileMenu.add_command(label="Close", command=donothing)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=fileMenu)
 # zakladka edit
editMenu = Menu(menu, tearoff=0)
editMenu.add_command(label="Undo", command=donothing)
editMenu.add_separator()
editMenu.add_command(label="Cut", command=donothing)
editMenu.add_command(label="Copy", command=donothing)
editMenu.add_command(label="Paste", command=donothing)
editMenu.add_command(label="Delete", command=donothing)
editMenu.add_command(label="Select All", command=donothing)
menu.add_cascade(label="Edit", menu=editMenu)
 # zakladka help
helpMenu = Menu(menu, tearoff=0)
helpMenu.add_command(label="Help Index", command=donothing)
helpMenu.add_command(label="About...", command=donothing)
menu.add_cascade(label="Help", menu=helpMenu)
root.config(menu=menu)

 # canvas

canvas = Canvas (canvasFrame, bg="#FFFFFF",height=500,width=500, scrollregion=(0,0,600,600), relief=SUNKEN, bd=3)
hbar=Scrollbar(canvasFrame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(canvasFrame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

Terrains= Menubutton (root, text="Terrains",width=30)
Terrains.grid(row = 0, column=2,sticky="nsew")
Terrains.menu = Menu ( Terrains, tearoff = 0 )
Terrains["menu"] = Terrains.menu
mayoVar = IntVar()
ketchVar = IntVar()
Terrains.menu.add_checkbutton (label="mayo", command=lambda: addTerrain("mayo"))
Terrains.menu.add_checkbutton (label="ketchup", command=lambda: addTerrain("ketchup"))

Edit= Menubutton (root, text="Edit",width=30)
Edit.grid(row = 0, column=0,sticky="nsew")
Edit.menu = Menu ( Edit, tearoff = 0 )
Edit["menu"] = Edit.menu
mayoVar = IntVar()
ketchVar = IntVar()
Edit.menu.add_checkbutton (label="mayo", variable=mayoVar)
Edit.menu.add_checkbutton (label="ketchup", variable=ketchVar)

canvas.pack()

line = canvas.create_line(150,200,300,100)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=0) # not needed, this is the default behavior
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.geometry('800x600')
root.mainloop()