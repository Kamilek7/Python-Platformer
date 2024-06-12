from components.Background import *
from components.Grounds import *
from components.Enemy import *
from components.Trigger import *

def reset():
   global grounds, selected
   grounds = []
   selected = False

def saveFile():
   global loadedFilename
   map = ET.Element('map')
   for ground in grounds:
      ground.representXML(map)
   plik = ET.ElementTree(map)
   fileNum = len(listdir(CURRENT_DIR))
   filename = path.join(CURRENT_DIR, "mapa" + str(fileNum) +".xml")
   if loadedFilename!=False:
      filename = path.join(CURRENT_DIR, loadedFilename)
   plik.write(filename)
   loadedFilename = filename

def loadfile(_filename,filewin):
   filename = _filename.get(1.0, "end-1c")
   filenameLong = path.join(CURRENT_DIR, filename)
   if path.isfile(filenameLong):
      global grounds, selected, loadedFilename
      grounds = []
      selected = False
      loadedFilename = filename
      plik = minidom.parse(filenameLong)
      mapa = plik.getElementsByTagName('map')[0]
      for child in mapa.childNodes:
         if child.tagName=="background":
            grounds.append(Background(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")), background=child.getAttribute("background")))
         elif child.tagName=="trigger":
            grounds.append(Trigger(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")), cutsceneInfo=child.getAttribute("cutsceneInfo")))
            
         elif child.tagName=="enemy":
            grounds.append(EnemyPlaceholder(int(child.getAttribute("x")),int(child.getAttribute("y")), child.getAttribute("type"), id=child.getAttribute("id")))
         else:
            grounds.append(Grounds(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, sprite=child.getAttribute("sprite"), foreground=child.getAttribute("foreground")))
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
      ratio = TILE_SIZE/tileViewSize
      if type=="block":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="plat":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="decor":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],120,40,type, sprite="lawka.png"))
      elif type=="key":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],40,40,type, sprite="key_red.png"))
      elif type=="door":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],20,80,type, sprite="door_side_red.png"))
      elif type=="ladder":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],40,40,type, sprite="ladder.png"))
      elif type=="spawn":
         grounds.append(Grounds(ratio*windowOffset[0],ratio*windowOffset[1],40,80,type))
      elif type=="background":
         grounds.append(Background(ratio*windowOffset[0],ratio*windowOffset[1],80,80))
      elif type=="trigger":
         grounds.append(Trigger(ratio*windowOffset[0],ratio*windowOffset[1],40,40))
      elif type=="enemy":
         grounds.append(EnemyPlaceholder(ratio*windowOffset[0],ratio*windowOffset[1]))

def copy():
   global copyboard
   if selected!=False:
      copyboard = selected
def paste():
   if copyboard!=None:
      new = copyboard.resetZ()
      grounds.append(new)
def cut():
   copy()
   delete()
def delete():
   global selected
   if selected!=False:
      for i in grounds:
         if i == selected:
            grounds.remove(i)
            selected = False

def scaleMap(how):
   global tileViewSize
   if how =="bigger" and tileViewSize<250:
      tileViewSize +=5
   elif how =="smaller" and tileViewSize>10:
      tileViewSize -=5
   canvas.config(scrollregion=(0,0,mapSize[0]*tileViewSize,mapSize[1]*tileViewSize))

def openMapEditWindow():
   filewin = Toplevel(root)
   global mapSize
   label1 = Label(filewin, text="Map properties")
   label2 = Label(filewin, text="Map size: " + str(mapSize))
   label3 = Label(filewin, text="Width:")
   label4 = Label(filewin, text="Height:")
   tempX = mapSize[0]
   tempY = mapSize[1]
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
   width.set(mapSize[0])
   height.set(mapSize[1])
   def updateFromSlider():
      global mapSize
      mapSize= (int(width.get()), int(height.get()))
      canvas.config(scrollregion=(0,0,mapSize[0]*tileViewSize,mapSize[1]*tileViewSize))
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
      keyFlags["Shift"] = True
   if event.keysym == "Control_L":
      keyFlags["Ctrl"] = True
   if selected!=False:
      if event.keysym == "Delete":
         delete()
      if event.keysym == "x" and keyFlags["Ctrl"]:
         cut()
      if event.keysym == "c" and keyFlags["Ctrl"]:
         copy()

   if event.keysym == "v" and keyFlags["Ctrl"] and copyboard!=None:
      paste()
   if event.keysym == "s" and keyFlags["Ctrl"]:
      saveFile()
def keyBoardInputRelease(event):
   global keyFlags
   if event.keysym == "Shift_L":
      keyFlags["Shift"] = False
   if event.keysym == "Control_L":
      keyFlags["Ctrl"] = False

def openSpriteEditWindow():
   filewin = Toplevel(root)
   if selected==False:
      label = Label(filewin, text="Nothing selected")
      label.pack()
   else:
      selected.spriteWindow(filewin)

def openSizeEditWindow():
   filewin = Toplevel(root)
   if selected==False:
      label = Label(filewin, text="Nothing selected")
      label.pack()
   else:
      selected.sizeWindow(filewin)


def openSpecialEditWindow():
   filewin = Toplevel(root)
   if selected==False:
      label = Label(filewin, text="Nothing selected")
      label.pack()
   else:
      selected.specialWindow(filewin)

def canvasUpdate():
   canvas.delete("all")
   radio = tileViewSize/TILE_SIZE
   for ground in grounds:
      width = 2
      if ground==selected:
         width=4
      bounds = (windowOffset[0]-ground.width*radio, windowOffset[1]-ground.height*radio, radio+windowOffset[0]+ canvas.winfo_width(),windowOffset[1]+ canvas.winfo_height())
      if (int(ground.x*radio)>=bounds[0] and int(ground.y*radio)>=bounds[1] and int(ground.x*radio)<=bounds[2] and int(ground.y*radio)<=bounds[3]):
         if ground.sprite!=None:
            ground.resize(ground.width, ground.height)
            canvas.create_rectangle(int(ground.x*radio), int(ground.y*radio), int(ground.x*radio) + int(ground.width*radio), int(ground.y*radio + ground.height*radio), width=width)
            canvas.create_image(int(ground.x*radio), int(ground.y*radio), anchor=NW, image=ground.sprite)
         else:
               canvas.create_rectangle(int(ground.x*radio), int(ground.y*radio), int(ground.x*radio + ground.width*radio), int(ground.y*radio + ground.height*radio), width=width)
   xLines = mapSize[0] - 1
   yLines = mapSize[1] - 1
   for i in range (xLines):
      canvas.create_line((i+1)*tileViewSize,0,(i+1)*tileViewSize,mapSize[1]*tileViewSize)
   for i in range (yLines):
      canvas.create_line(0,(i+1)*tileViewSize,mapSize[0]*tileViewSize,(i+1)*tileViewSize)
   canvas.after(MS, canvasUpdate)


 # Budowa aplikacji

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
editMenu.add_command(label="Cut", command=cut)
editMenu.add_command(label="Copy", command=copy)
editMenu.add_command(label="Paste", command=paste)
editMenu.add_command(label="Delete", command=delete)
editMenu.add_separator()
editMenu.add_command(label="Map properties", command=openMapEditWindow)
menu.add_cascade(label="Edit", menu=editMenu)
 # zakladka help
root.config(menu=menu)

 # canvas

mousePositionLabel = Label(canvasFrame, text="(0,0)")
mousePositionLabel.pack()
canvas = Canvas (canvasFrame, bg="white",height=600,width=600, scrollregion=(0,0,mapSize[0]*tileViewSize,mapSize[1]*tileViewSize), relief=SUNKEN, bd=3)
hbar = None
vbar = None
def changeOffsetH(a,b):
   canvas.xview(a,b)
   global windowOffset
   windowOffset[0] = canvas.canvasx(0)
def changeOffsetV(a,b):
   canvas.yview(a,b)
   global windowOffset
   windowOffset[1] = canvas.canvasy(0)
hbar=Scrollbar(canvasFrame,orient=HORIZONTAL, command=changeOffsetH)
hbar.pack(side=BOTTOM,fill=X)
vbar=Scrollbar(canvasFrame,orient=VERTICAL, command=changeOffsetV)
vbar.pack(side=RIGHT,fill=Y)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
# obsluga przyciskow myszy (musialem tutaj dac zeby wszystko bylo "swieze")
mouseTimer = False
def mouseSelect(event):
   global mouseTimer, selected, offset
   radio = tileViewSize/TILE_SIZE
   x = canvas.canvasx(event.x)
   y = canvas.canvasy(event.y)
   mousePositionLabel.config(text = str((int(x/radio),int(y/radio))))
   if len(grounds)>0:
      zs = {}
      for ground in grounds:
         if (x <= radio*(ground.x + ground.width) and x >= radio*ground.x) and (y <= radio*(ground.y + ground.height) and y >= radio*ground.y):
            zs[ground.z] = ground
      if len(zs)>0:
         mouseTimer=True
         selected = zs[max(zs.keys())]
         offset = [selected.x-x/radio,selected.y-y/radio]
      else:
         selected = False
         mouseTimer= False

def mouseMoveBlock(event):
   radio = tileViewSize/TILE_SIZE
   if mouseTimer:
      global selected
      x = event.x + canvas.winfo_width()/(hbar.get()[1]-hbar.get()[0])*hbar.get()[0]
      y = event.y + canvas.winfo_height()/(vbar.get()[1]-vbar.get()[0])*vbar.get()[0]
      if keyFlags["Shift"]:
         tileHold = TILE_SIZE
         if selected.width<TILE_SIZE or selected.height<TILE_SIZE:
            tileHold/=2
         selected.x = int(round((x/radio + offset[0])/tileHold)*tileHold)
         selected.y = int(round((y/radio + offset[1])/tileHold)*tileHold)
      else:
         selected.x = int(x/radio + offset[0])
         selected.y = int(y/radio + offset[1])

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

Terrains= Menubutton (root, text="Terrains",width=30)
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

Edit= Menubutton (root, text="Edit selected",width=30)
Edit.grid(row = 0, column=0,sticky="nsew")
Edit.menu = Menu ( Edit, tearoff = 0 )
Edit["menu"] = Edit.menu
Edit.menu.add_checkbutton (label="Ground sprites", command=openSpriteEditWindow)
Edit.menu.add_checkbutton (label="Ground size", command=openSizeEditWindow)
Edit.menu.add_checkbutton (label="Special settings", command=openSpecialEditWindow)

# Estetyka programu i odswiezanie okien

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(1, weight=1)
root.geometry('1200x800')
canvas.after(MS, canvasUpdate)
root.mainloop()