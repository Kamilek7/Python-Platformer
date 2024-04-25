from tkinter import *
from tkinter.ttk import *
import xml.etree.cElementTree as ET

 # Funkcje do wykorzystania
timer = 0
map = ET.Element('map')
def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def addTerrain(type):
   temp = ET.SubElement(map, type)
   temp.set("x", "0")
   temp.set("y", "0")
   temp.set("width", "120")
   temp.set("height", "80")
   ET.dump(map)

def canvasUpdate():
   global timer
   timer+=10
   canvas.delete("all")
   for child in map:
      attribs = child.attrib
      if child.tag == "mayo":
         canvas.create_rectangle(attribs["x"], attribs["y"], attribs["x"] + attribs["width"], attribs["y"] + attribs["height"], fill='yellow')
      if child.tag == "ketchup":
         canvas.create_rectangle(attribs["x"], attribs["y"], attribs["x"] + attribs["width"], attribs["y"] + attribs["height"], fill='red')
   canvas.after(50, canvasUpdate)
   

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
def motion(event):
   _x = hbar.get()[0]*canvas.winfo_width()
   _y = vbar.get()[0]*canvas.winfo_height()
   print("Mouse position: (%s %s)" % (event.x + _x,event.y + _y ))
canvas.bind('<Motion>',motion)
canvas.pack()

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

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.geometry('800x600')
canvas.after(50, canvasUpdate)
root.mainloop()