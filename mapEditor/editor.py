from tkinter import *
from tkinter.ttk import *
from PIL import Image,ImageTk
from os import *
import xml.etree.cElementTree as ET
from xml.dom import minidom
import math

 # stałe
MS = 10
 # Funkcje do wykorzystania
class VisibleGround:
   z = 0
   def __init__(self, _x,_y,_width,_height, _type, sprite=None):
      VisibleGround.z+=1
      self.z = VisibleGround.z
      self.x = _x
      self.y = _y
      self.width = _width
      self.height = _height
      self.type = _type
      if sprite!=None and sprite!="None":
         spriteLocation = path.join(path.dirname(path.abspath(__file__)),"sprites",sprite)
         img = Image.open(spriteLocation)
         img = img.resize((self.width,self.height))
         img= ImageTk.PhotoImage(img)
         self.sprite = img
         self.spriteLoc =sprite
      else:
         self.sprite = None
   def resize(self,newWidth,newHeight, sprite=None):
      self.width = newWidth
      self.height = newHeight
      if self.sprite!=None and self.sprite!="None" or sprite!=None:
         if sprite!="Remove sprite":
            filename=sprite
            if sprite==None:
               filename = self.spriteLoc
            spriteLocation = path.join(path.dirname(path.abspath(__file__)),"sprites",filename)
            img = Image.open(spriteLocation)
            img = img.resize((self.width,self.height))
            img= ImageTk.PhotoImage(img)
            self.sprite = img
            self.spriteLoc = filename
         else:
            self.sprite=None
            self.spriteLoc="None"
timer = 0
mapSize = (1200,1200)
offset = (0,0)
windowOffset = (0,0)
loadedFilename = False
selected = False
grounds = []
map = ET.Element('map')
 # Flagi klawiszowe
keyFlags = {"Shift": False, "Ctrl": False}
def donothing():
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def reset():
   global grounds, selected
   grounds = []
   selected = False

def saveFile():
   global loadedFilename
   for ground in grounds:
      temp = ET.SubElement(map, ground.type)
      temp.set("x", str(ground.x))
      temp.set("y", str(ground.y))
      temp.set("width", str(ground.width))
      temp.set("height",str(ground.height))
      if ground.sprite!=None:
         temp.set("sprite",str(ground.spriteLoc))
      else:
         temp.set("sprite",str("None"))
   ET.dump(map)
   plik = ET.ElementTree(map)
   fileNum = len(listdir(path.dirname(path.abspath(__file__))))-1
   filename = path.join(path.dirname(path.abspath(__file__)), "mapa" + str(fileNum) +".xml")
   if loadedFilename!=False:
      filename = path.join(path.dirname(path.abspath(__file__)), loadedFilename)
   plik.write(filename)

def loadfile(_filename,filewin):
   filename = _filename.get(1.0, "end-1c")
   filenameLong = path.join(path.dirname(path.abspath(__file__)), filename)
   if path.isfile(filenameLong):
      global grounds, selected, loadedFilename
      grounds = []
      selected = False
      loadedFilename = filename
      plik = minidom.parse(filenameLong)
      mapa = plik.getElementsByTagName('map')[0]
      for child in mapa.childNodes:
         grounds.append(VisibleGround(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, sprite=child.getAttribute("sprite")))
      filewin.destroy()
   else:
      filewin = Toplevel(root)
      label = Label(filewin, text="ERROR: Wrong filename")
      label.pack()

def load():
   filewin = Toplevel(root)
   label = Label(filewin, text="Type in the filename")
   filename = Text(filewin, height = 1,  width = 20) 
   button = Button(filewin, text="Load", command= lambda: loadfile(filename,filewin))
   label.pack()
   filename.pack()
   button.pack()

def addTerrain(type):
      global windowOffsetoffset
      grounds.append(VisibleGround(windowOffset[0],windowOffset[1],120,80,type))

def keyBoardInput(event):
   global selected
   global keyFlags
   print(event.keysym)
   if event.keysym == "Shift_L":
      keyFlags["Shift"] = True
   if selected!=False:
      if event.keysym == "Delete":
         for i in grounds:
            if i == selected:
               grounds.remove(i)
               selected = False

def keyBoardInputRelease(event):
   global keyFlags
   print(event.keysym)
   if event.keysym == "Shift_L":
      keyFlags["Shift"] = False

def openSpriteEditWindow():
   global selected
   filewin = Toplevel(root)
   if selected!=False:
      if selected.sprite != None and selected.sprite != "None":
         label1 = Label(filewin, text="Current sprite: " + selected.spriteLoc)
      else:
         label1 = Label(filewin, text="Current sprite: None")
      sprites = Listbox(filewin)
      spriters = path.join(path.dirname(path.abspath(__file__)),"sprites")
      spriters = listdir(spriters)
      for i in range(len(spriters)):
         sprites.insert(i, spriters[i])
      sprites.insert(len(spriters),"Remove sprite")
      def updateFromSlider():
         selection = None
         for i in sprites.curselection():
            selection = sprites.get(i)
         selected.resize(selected.width, selected.height, sprite=selection)
         label1.config(text="Current sprite: " + selected.spriteLoc)
      button = Button(filewin, text="Load", command=updateFromSlider)
      label1.pack()
      sprites.pack()
      button.pack()
   else:
      label = Label(filewin, text="Nothing selected")
      label.pack()

def openSizeEditWindow():
   global selected
   filewin = Toplevel(root)
   if selected!=False:
      label1 = Label(filewin, text="Width (" + str(selected.width) + ")")
      label2 = Label(filewin, text="Height (" + str(selected.height) + ")")
      var1 = IntVar()
      var2 = IntVar()
      def updateFromSlider(cos):
         selected.resize(20*var1.get(),20*var2.get())
         label1.config(text="Width (" + str(selected.width) + ")")
         label2.config(text="Height (" + str(selected.height) + ")")
      width = Scale(filewin, from_=1, to=60, variable=var1,  command=updateFromSlider)
      height = Scale(filewin, from_=1, to=60, variable=var2, command=updateFromSlider)
      var1.set (int(selected.width/20)) 
      var2.set (int(selected.height/20)) 
      label1.pack()
      width.pack()
      label2.pack()
      height.pack()
   else:
      label = Label(filewin, text="Nothing selected")
      label.pack()

def canvasUpdate():
   global timer
   global img
   timer+=MS
   canvas.delete("all")
   for ground in grounds:
      width = 2
      if ground==selected:
         width=4
      if ground.sprite!=None:
         canvas.create_rectangle(ground.x, ground.y, ground.x + ground.width, ground.y + ground.height, fill='red',width=width)
         canvas.create_image(ground.x, ground.y, anchor=NW, image=ground.sprite)
      else:
         if ground.type == "mayo":
            canvas.create_rectangle(ground.x, ground.y, ground.x + ground.width, ground.y + ground.height, fill='yellow', width=width)
         if ground.type == "ketchup":
            canvas.create_rectangle(ground.x, ground.y, ground.x + ground.width, ground.y + ground.height, fill='red',width=width)
   # 40 to szerokosc gracza
   xLines = mapSize[0]//40 - 1
   yLines = mapSize[1]//40 - 1
   for i in range (xLines):
      canvas.create_line((i+1)*40,0,(i+1)*40,mapSize[1])
   for i in range (yLines):
      canvas.create_line(0,(i+1)*40,mapSize[1],(i+1)*40)
   canvas.after(MS, canvasUpdate)


 # Budowa aplikacji


root = Tk()
root.title("Edytor")
canvasFrame = Frame(root)
canvasFrame.grid(row = 1, column = 1)

 # Menu (pasek u gory)
menu = Menu(root)
 # zakladka file
fileMenu = Menu(menu, tearoff=0)
fileMenu.add_command(label="New", command=reset)
fileMenu.add_command(label="Open", command=load)
fileMenu.add_command(label="Save", command=saveFile)
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

canvas = Canvas (canvasFrame, bg="#FFFFFF",height=600,width=600, scrollregion=(0,0,mapSize[0],mapSize[1]), relief=SUNKEN, bd=3)
hbar = None
vbar = None
def changeOffsetH(a,b):
   canvas.xview(a,b)
   global windowOffset
   windowOffset = (canvas.winfo_width()/(hbar.get()[1]-hbar.get()[0])*hbar.get()[0],windowOffset[1])
def changeOffsetV(a,b):
   canvas.yview(a,b)
   global windowOffset
   windowOffset = (windowOffset[0],canvas.winfo_height()/(vbar.get()[1]-vbar.get()[0])*vbar.get()[0])
hbar=Scrollbar(canvasFrame,orient=HORIZONTAL, command=changeOffsetH)
hbar.pack(side=BOTTOM,fill=X)
vbar=Scrollbar(canvasFrame,orient=VERTICAL, command=changeOffsetV)
vbar.pack(side=RIGHT,fill=Y)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
# obsluga przyciskow myszy (musialem tutaj dac zeby wszystko bylo "swieze")
mouseTimer = False
def mouseSelect(event):
   global mouseTimer
   global selected
   global offset
   global windowOffset
   x = event.x + windowOffset[0]
   y = event.y + windowOffset[1]
   if len(grounds)>0:
      zs = {}
      for ground in grounds:
         if (x <= ground.x + ground.width and x >= ground.x) and (y <= ground.y + ground.height and y >= ground.y):
            zs[ground.z] = ground
      if len(zs)>0:
         mouseTimer=True
         selected = zs[max(zs.keys())]
         offset = [selected.x-x,selected.y-y]
      else:
         selected = False
         mouseTimer= False

def mouseMoveBlock(event):
   global mouseTimer
   global offset
   global keyFlags
   if mouseTimer:
      global selected
      x = event.x + canvas.winfo_width()/(hbar.get()[1]-hbar.get()[0])*hbar.get()[0]
      y = event.y + canvas.winfo_height()/(vbar.get()[1]-vbar.get()[0])*vbar.get()[0]
      if keyFlags["Shift"]:
         selected.x = round((x + offset[0])/40)*40
         selected.y = round((y + offset[1])/40)*40
      else:
         selected.x = int(x + offset[0])
         selected.y = int(y + offset[1])
def mouseRelease(event):
   global mouseTimer
   mouseTimer = False
canvas.bind("<Button-1>", mouseSelect)
canvas.bind("<B1-Motion>", mouseMoveBlock)
canvas.bind("<ButtonRelease-1>", mouseRelease)
canvas.bind("<Key>", keyBoardInput)
canvas.bind("<KeyRelease>", keyBoardInputRelease)
canvas.focus_set()
canvas.pack()

# Zakladka "Tereny" (po prawej)

Terrains= Menubutton (root, text="Terrains",width=30)
Terrains.grid(row = 0, column=2,sticky="nsew")
Terrains.menu = Menu ( Terrains, tearoff = 0 )
Terrains["menu"] = Terrains.menu
Terrains.menu.add_checkbutton (label="mayo", command=lambda: addTerrain("mayo"))
Terrains.menu.add_checkbutton (label="ketchup", command=lambda: addTerrain("ketchup"))

# Zakladka edycji terenow (po lewej)

Edit= Menubutton (root, text="Edit selected",width=30)
Edit.grid(row = 0, column=0,sticky="nsew")
Edit.menu = Menu ( Edit, tearoff = 0 )
Edit["menu"] = Edit.menu
Edit.menu.add_checkbutton (label="Sprites", command=openSpriteEditWindow)
Edit.menu.add_checkbutton (label="Size", command=openSizeEditWindow)

# Estetyka programu i odswiezanie okien

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)
root.geometry('1200x800')
canvas.after(MS, canvasUpdate)
root.mainloop()