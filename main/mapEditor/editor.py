from components.editorComponents import *
from components.trigger import *
from components.background import *
from components.grounds import *
from components.enemy import *
from components.menuOptions import *

def addTerrain(type):
      ratio = TILE_SIZE/EditorComponents.tileViewSize
      if type=="block":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="plat":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="decor":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],120,40,type, sprite="lawka.png"))
      elif type=="key":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="key_red.png"))
      elif type=="door":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],20,80,type, sprite="door_side_red.png"))
      elif type=="ladder":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40,type, sprite="ladder.png"))
      elif type=="spawn":
         EditorComponents.grounds.append(Grounds(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,80,type))
      elif type=="background":
         EditorComponents.grounds.append(Background(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],80,80))
      elif type=="trigger":
         EditorComponents.grounds.append(Trigger(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1],40,40))
      elif type=="enemy":
         EditorComponents.grounds.append(EnemyPlaceholder(ratio*EditorComponents.windowOffset[0],ratio*EditorComponents.windowOffset[1]))

def scaleMap(how):
   if how =="bigger" and EditorComponents.tileViewSize<250:
      EditorComponents.tileViewSize +=5
   elif how =="smaller" and EditorComponents.tileViewSize>10:
      EditorComponents.tileViewSize -=5
   canvas.config(scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize))

def openMapEditWindow():
   filewin = Toplevel(EditorComponents.root)
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
      canvas.config(scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize))
   button = Button(filewin, text="Save changes", command=updateFromSlider)
   label1.pack()
   label2.pack()
   label3.pack()
   width.pack()
   label4.pack()
   height.pack()
   button.pack()

def mouseWheelEvents(event):
    if event.num == 5 or event.delta <= -10:
        scaleMap("smaller")
    if event.num == 4 or event.delta >= 10:
        scaleMap("bigger")

def keyBoardInput(event):
   if event.keysym == "Shift_L":
      EditorComponents.keyFlags["Shift"] = True
   if event.keysym == "Control_L":
      EditorComponents.keyFlags["Ctrl"] = True
   if EditorComponents.selected!=False:
      if event.keysym == "Delete":
         MenuFuncs.delete()
      if event.keysym == "x" and EditorComponents.keyFlags["Ctrl"]:
         MenuFuncs.cut()
      if event.keysym == "c" and EditorComponents.keyFlags["Ctrl"]:
         MenuFuncs.copy()

   if event.keysym == "v" and EditorComponents.keyFlags["Ctrl"] and EditorComponents.copyboard!=None:
      MenuFuncs.paste()
   if event.keysym == "s" and EditorComponents.keyFlags["Ctrl"]:
      MenuFuncs.saveFile()
def keyBoardInputRelease(event):
   if event.keysym == "Shift_L":
      EditorComponents.keyFlags["Shift"] = False
   if event.keysym == "Control_L":
      EditorComponents.keyFlags["Ctrl"] = False

def openSpriteEditWindow():
   filewin = Toplevel(EditorComponents.root)
   if EditorComponents.selected==False:
      label = Label(filewin, text="Nothing EditorComponents.selected")
      label.pack()
   else:
      EditorComponents.selected.spriteWindow(filewin)

def openSizeEditWindow():
   filewin = Toplevel(EditorComponents.root)
   if EditorComponents.selected==False:
      label = Label(filewin, text="Nothing EditorComponents.selected")
      label.pack()
   else:
      EditorComponents.selected.sizeWindow(filewin)


def openSpecialEditWindow():
   filewin = Toplevel(EditorComponents.root)
   if EditorComponents.selected==False:
      label = Label(filewin, text="Nothing EditorComponents.selected")
      label.pack()
   else:
      EditorComponents.selected.specialWindow(filewin)

def canvasUpdate():
   canvas.delete("all")
   radio = EditorComponents.tileViewSize/TILE_SIZE
   for ground in EditorComponents.grounds:
      width = 2
      if ground==EditorComponents.selected:
         width=4
      bounds = (EditorComponents.windowOffset[0]-ground.width*radio, EditorComponents.windowOffset[1]-ground.height*radio, radio+EditorComponents.windowOffset[0]+ canvas.winfo_width(),EditorComponents.windowOffset[1]+ canvas.winfo_height())
      if (int(ground.x*radio)>=bounds[0] and int(ground.y*radio)>=bounds[1] and int(ground.x*radio)<=bounds[2] and int(ground.y*radio)<=bounds[3]):
         if ground.sprite!=None:
            ground.resize(ground.width, ground.height)
            canvas.create_rectangle(int(ground.x*radio), int(ground.y*radio), int(ground.x*radio) + int(ground.width*radio), int(ground.y*radio + ground.height*radio), width=width)
            canvas.create_image(int(ground.x*radio), int(ground.y*radio), anchor=NW, image=ground.sprite)
         else:
               canvas.create_rectangle(int(ground.x*radio), int(ground.y*radio), int(ground.x*radio + ground.width*radio), int(ground.y*radio + ground.height*radio), width=width)
   xLines = EditorComponents.mapSize[0] - 1
   yLines = EditorComponents.mapSize[1] - 1
   for i in range (xLines):
      canvas.create_line((i+1)*EditorComponents.tileViewSize,0,(i+1)*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize)
   for i in range (yLines):
      canvas.create_line(0,(i+1)*EditorComponents.tileViewSize,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,(i+1)*EditorComponents.tileViewSize)
   canvas.after(MS, canvasUpdate)


 # Budowa aplikacji

EditorComponents.root.title("Edytor")
canvasFrame = Frame(EditorComponents.root)
canvasFrame.grid(row = 1, column = 1)

 # Menu (pasek u gory)
menu = Menu(EditorComponents.root)
 # zakladka file
fileMenu = Menu(menu, tearoff=0)
fileMenu.add_command(label="New", command=MenuFuncs.reset)
fileMenu.add_command(label="Open", command=lambda: MenuFuncs.load(canvas=canvas))
fileMenu.add_command(label="Save", command=MenuFuncs.saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=EditorComponents.root.quit)
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
EditorComponents.root.config(menu=menu)

 # canvas

mousePositionLabel = Label(canvasFrame, text="(0,0)")
mousePositionLabel.pack()
canvas = Canvas (canvasFrame, bg="white",height=600,width=600, scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize), relief=SUNKEN, bd=3)
hbar = None
vbar = None
def changeOffsetH(a,b):
   canvas.xview(a,b)
   EditorComponents.windowOffset[0] = canvas.canvasx(0)
def changeOffsetV(a,b):
   canvas.yview(a,b)
   EditorComponents.windowOffset[1] = canvas.canvasy(0)
hbar=Scrollbar(canvasFrame,orient=HORIZONTAL, command=changeOffsetH)
hbar.pack(side=BOTTOM,fill=X)
vbar=Scrollbar(canvasFrame,orient=VERTICAL, command=changeOffsetV)
vbar.pack(side=RIGHT,fill=Y)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
# obsluga przyciskow myszy (musialem tutaj dac zeby wszystko bylo "swieze")
mouseTimer = False
def mouseSelect(event):
   global mouseTimer
   radio = EditorComponents.tileViewSize/TILE_SIZE
   x = canvas.canvasx(event.x)
   y = canvas.canvasy(event.y)
   mousePositionLabel.config(text = str((int(x/radio),int(y/radio))))
   if len(EditorComponents.grounds)>0:
      zs = {}
      for ground in EditorComponents.grounds:
         if (x <= radio*(ground.x + ground.width) and x >= radio*ground.x) and (y <= radio*(ground.y + ground.height) and y >= radio*ground.y):
            zs[ground.z] = ground
      if len(zs)>0:
         mouseTimer=True
         EditorComponents.selected = zs[max(zs.keys())]
         EditorComponents.offset = [EditorComponents.selected.x-x/radio,EditorComponents.selected.y-y/radio]
      else:
         EditorComponents.selected = False
         mouseTimer= False

def mouseMoveBlock(event):
   radio = EditorComponents.tileViewSize/TILE_SIZE
   if mouseTimer:
      x = event.x + canvas.winfo_width()/(hbar.get()[1]-hbar.get()[0])*hbar.get()[0]
      y = event.y + canvas.winfo_height()/(vbar.get()[1]-vbar.get()[0])*vbar.get()[0]
      if EditorComponents.keyFlags["Shift"]:
         tileHold = TILE_SIZE
         if EditorComponents.selected.width<TILE_SIZE or EditorComponents.selected.height<TILE_SIZE:
            tileHold/=2
         EditorComponents.selected.x = int(round((x/radio + EditorComponents.offset[0] - int(EditorComponents.tileViewSize*canvas.canvasx(event.x)/2700))/tileHold)*tileHold)
         EditorComponents.selected.y = int(round((y/radio + EditorComponents.offset[1] - int(EditorComponents.tileViewSize*canvas.canvasy(event.y)/2700))/tileHold)*tileHold)
      else:
         EditorComponents.selected.x = int(x/radio + EditorComponents.offset[0]- int(EditorComponents.tileViewSize*canvas.canvasx(event.x)/2700))
         EditorComponents.selected.y = int(y/radio + EditorComponents.offset[1]- int(EditorComponents.tileViewSize*canvas.canvasy(event.y)/2700))

def mouseRelease(event):
   global mouseTimer
   mouseTimer = False
canvas.bind("<Button-1>", mouseSelect)
canvas.bind("<B1-Motion>", mouseMoveBlock)
canvas.bind("<ButtonRelease-1>", mouseRelease)
canvas.bind("<Key>", keyBoardInput)
canvas.bind("<KeyRelease>", keyBoardInputRelease)
canvas.bind("<MouseWheel>", mouseWheelEvents)
canvas.focus_set()
canvas.pack()

# Zakladka "Tereny" (po prawej)

Terrains= Menubutton (EditorComponents.root, text="Terrains",width=30)
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

Edit= Menubutton (EditorComponents.root, text="Selected",width=30)
Edit.grid(row = 0, column=0,sticky="nsew")
Edit.menu = Menu ( Edit, tearoff = 0 )
Edit["menu"] = Edit.menu
Edit.menu.add_checkbutton (label="Ground sprites", command=openSpriteEditWindow)
Edit.menu.add_checkbutton (label="Ground size", command=openSizeEditWindow)
Edit.menu.add_checkbutton (label="Special settings", command=openSpecialEditWindow)

# Estetyka programu i odswiezanie okien

EditorComponents.root.columnconfigure(0, weight=1)
EditorComponents.root.columnconfigure(1, weight=1)
EditorComponents.root.columnconfigure(2, weight=1)
EditorComponents.root.rowconfigure(1, weight=1)
EditorComponents.root.geometry('1200x800')
canvas.after(MS, canvasUpdate)
EditorComponents.root.mainloop()