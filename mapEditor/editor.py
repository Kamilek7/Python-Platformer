from tkinter import *
from tkinter.ttk import *
from os import *
import xml.etree.cElementTree as ET

 # Funkcje do wykorzystania
class VisibleGround:
   z = 0
   def __init__(self, _x,_y,_width,_height, _type):
      VisibleGround.z+=1
      self.z = VisibleGround.z
      self.x = _x
      self.y = _y
      self.width = _width
      self.height = _height
      self.type = _type
timer = 0
selected = False
grounds = []
map = ET.Element('map')
def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def saveFile():
   for ground in grounds:
      temp = ET.SubElement(map, ground.type)
      temp.set("x", str(ground.x))
      temp.set("y", str(ground.y))
      temp.set("width", str(ground.width))
      temp.set("height",str(ground.height))
   ET.dump(map)
   plik = ET.ElementTree(map)
   filename = path.join(path.dirname(path.abspath(__file__)), "mapa.xml")
   plik.write(filename)
def addTerrain(type):
   grounds.append(VisibleGround(0,0,120,80,type))

def moveBlocks(event):
   if selected!=False:
      if event.keysym == "a" or event.keysym == "Left":
         selected.x -=1
      if event.keysym == "d" or event.keysym == "Right":
         selected.x +=1
      if event.keysym == "w" or event.keysym == "Up":
         selected.y -=1
      if event.keysym == "s" or event.keysym == "Down":
         selected.y +=1
def canvasUpdate():
   global timer
   timer+=10
   canvas.delete("all")
   for ground in grounds:
      if ground.type == "mayo":
         canvas.create_rectangle(ground.x, ground.y, ground.x + ground.width, ground.y + ground.height, fill='yellow')
      if ground.type == "ketchup":
         canvas.create_rectangle(ground.x, ground.y, ground.x + ground.width, ground.y + ground.height, fill='red')
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
fileMenu.add_command(label="Save", command=saveFile)
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
   global selected
   x = event.x + hbar.get()[0]*canvas.winfo_width()
   y = event.y + vbar.get()[0]*canvas.winfo_height()
   if len(grounds)>0:
      zs = {}
      for ground in grounds:
         if (x <= ground.x + ground.width and x >= ground.x) and (y <= ground.y + ground.height and y >= ground.y):
            zs[ground.z] = ground
      if len(zs)>0:
         selected = zs[max(zs.keys())]
      else:
         selected = False
canvas.bind("<Button-1>", motion)
canvas.bind("<Key>", moveBlocks)
canvas.focus_set()
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