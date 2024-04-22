from tkinter import *
from tkinter.ttk import *
import xml.etree.cElementTree as ET

 # Funkcje do wykorzystania

def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()


 # Budowa aplikacji


root = Tk()
root.title("Edytor")
canvasFrame = Frame(root)
canvasFrame.pack()

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

 # grupa na "anonimowe" elementy
elements = []
elements.append(Label(root, text ="Tutaj cos bedzie."))

 # canvas

canvas = Canvas (canvasFrame, bg="#FFFFFF",height=500,width=500, scrollregion=(0,0,600,600), relief=SUNKEN, bd=3)
hbar=Scrollbar(canvasFrame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(canvasFrame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

for element in elements:
    element.pack()
canvas.pack()
line = canvas.create_line(150,200,300,100)

root.geometry('800x600')
root.mainloop()