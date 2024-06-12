from components.inputEvents import *
from components.applicationBuild import *

def addTerrain(type):
      ratio = TILE_SIZE/EditorComponents.tileViewSize
      if type=="block":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="plat":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],120,40,type, sprite="donica3.png"))
      elif type=="decor":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],120,40,type, sprite="lawka.png"))
      elif type=="key":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="key_red.png"))
      elif type=="door":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],20,80,type, sprite="door_side_red.png"))
      elif type=="ladder":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="ladder.png"))
      elif type=="spawn":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,80,type, sprite="player_left0.png"))
      elif type=="background":
         EditorComponents.grounds.append(Background(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],80,80))
      elif type=="trigger":
         EditorComponents.grounds.append(Trigger(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40))
      elif type=="enemy":
         EditorComponents.grounds.append(EnemyPlaceholder(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1]))

def openMapEditWindow():
   filewin = Toplevel(App.root)
   label1 = Label(filewin, text="Map properties")
   label2 = Label(filewin, text="Map size: " + str(EditorComponents.mapSize))
   label3 = Label(filewin, text="Width:")
   label4 = Label(filewin, text="Height:")
   tempX = EditorComponents.mapSize[0]
   tempY = EditorComponents.mapSize[1]
   def showX(a):
      global tempX
      tempX = int(float(a))
      label2.config(text="Map size: (" + str(tempX) + ", " + str(tempY) + ")")
   def showY(a):
      global tempY
      tempY = int(float(a))
      label2.config(text="Map size: (" + str(tempX) + ", " + str(tempY) + ")")
   width = Scale(filewin, from_=10, to=200, command=showX)
   height = Scale(filewin, from_=10, to=200, command=showY)
   width.set(EditorComponents.mapSize[0])
   height.set(EditorComponents.mapSize[1])
   def updateFromSlider():
      EditorComponents.mapSize= (int(width.get()), int(height.get()))
      App.canvas.config(scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize))
   button = Button(filewin, text="Save changes", command=updateFromSlider)
   label1.pack()
   label2.pack()
   label3.pack()
   width.pack()
   label4.pack()
   height.pack()
   button.pack()

def openSpriteEditWindow():
   filewin = Toplevel(App.root)
   if EditorComponents.selected==False:
      label = Label(filewin, text="Nothing selected")
      label.pack()
   else:
      EditorComponents.selected.spriteWindow(filewin)

def openSizeEditWindow():
   filewin = Toplevel(App.root)
   if EditorComponents.selected==False:
      label = Label(filewin, text="Nothing selected")
      label.pack()
   else:
      EditorComponents.selected.sizeWindow(filewin)

def openSpecialEditWindow():
   filewin = Toplevel(App.root)
   if EditorComponents.selected==False:
      label = Label(filewin, text="Nothing selected")
      label.pack()
   else:
      EditorComponents.selected.specialWindow(filewin)


 # Budowa aplikacji

 # Menu (pasek u gory)

menu = Menu(App.root)

 # zakladka file

fileMenu = Menu(menu, tearoff=0)
fileMenu.add_command(label="New", command=MenuFuncs.reset)
fileMenu.add_command(label="Open", command=lambda: MenuFuncs.load(canvas=App.canvas))
fileMenu.add_command(label="Save", command=MenuFuncs.saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=App.root.quit)
menu.add_cascade(label="File", menu=fileMenu)

 # zakladka edit

editMenu = Menu(menu, tearoff=0)
editMenu.add_command(label="Undo", command=MenuFuncs.donothing)
editMenu.add_separator()
editMenu.add_command(label="Cut", command=MenuFuncs.cut)
editMenu.add_command(label="Copy", command=MenuFuncs.copy)
editMenu.add_command(label="Paste", command=MenuFuncs.paste)
editMenu.add_command(label="Delete", command=MenuFuncs.delete)
editMenu.add_separator()
editMenu.add_command(label="Map properties", command=openMapEditWindow)
menu.add_cascade(label="Edit", menu=editMenu)

App.root.config(menu=menu)
App.hbar.config(command=App.changeOffsetH)
App.hbar.pack(side=BOTTOM,fill=X)
App.vbar.config(command=App.changeOffsetV)
App.vbar.pack(side=RIGHT,fill=Y)
App.canvas.config(xscrollcommand=App.hbar.set, yscrollcommand=App.vbar.set)

App.canvas.bind("<Button-1>", App.mouseSelect)
App.canvas.bind("<B1-Motion>", App.mouseMoveBlock)
App.canvas.bind("<ButtonRelease-1>", App.mouseRelease)
App.canvas.bind("<Key>", InputEvents.keyBoardInput)
App.canvas.bind("<KeyRelease>", InputEvents.keyBoardInputRelease)
App.canvas.bind("<MouseWheel>", InputEvents.mouseWheelEvents)
App.canvas.focus_set()
App.canvas.pack()

# Zakladka "Tereny" (po prawej)

Terrains= Menubutton (App.root, text="Terrains",width=30)
Terrains.grid(row = 0, column=2,sticky="nsew")
Terrains.menu = Menu ( Terrains, tearoff = 0 )
Terrains["menu"] = Terrains.menu
Terrains.menu.add_checkbutton (label="Solid block", command=lambda: addTerrain("block"))
Terrains.menu.add_checkbutton (label="Platform", command=lambda: addTerrain("plat"))
Terrains.menu.add_checkbutton (label="Decoration", command=lambda: addTerrain("decor"))
Terrains.menu.add_checkbutton (label="Key", command=lambda: addTerrain("key"))
Terrains.menu.add_checkbutton (label="Door", command=lambda: addTerrain("door"))
Terrains.menu.add_checkbutton (label="Ladder", command=lambda: addTerrain("ladder"))
Terrains.menu.add_checkbutton (label="Enemy", command=lambda: addTerrain("enemy"))
Terrains.menu.add_checkbutton (label="Player spawn", command=lambda: addTerrain("spawn"))
Terrains.menu.add_checkbutton (label="Background", command=lambda: addTerrain("background"))
Terrains.menu.add_checkbutton (label="Trigger", command=lambda: addTerrain("trigger"))

# Zakladka edycji terenow (po lewej)

Edit= Menubutton (App.root, text="Selected",width=30)
Edit.grid(row = 0, column=0,sticky="nsew")
Edit.menu = Menu ( Edit, tearoff = 0 )
Edit["menu"] = Edit.menu
Edit.menu.add_checkbutton (label="Ground sprites", command=openSpriteEditWindow)
Edit.menu.add_checkbutton (label="Ground size", command=openSizeEditWindow)
Edit.menu.add_checkbutton (label="Special settings", command=openSpecialEditWindow)

# Estetyka programu i odswiezanie okien

App.root.columnconfigure(0, weight=1)
App.root.columnconfigure(1, weight=1)
App.root.columnconfigure(2, weight=1)
App.root.rowconfigure(1, weight=1)
App.root.geometry('1200x800')
App.canvas.after(MS, App.canvasUpdate)
App.root.mainloop()