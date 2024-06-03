from tkinter import *
from tkinter.ttk import *
from PIL import Image,ImageTk
from os import *
import xml.etree.cElementTree as ET
from xml.dom import minidom

 # stałe

MS = 15
TILE_SIZE = 40
CURRENT_DIR = path.dirname(path.abspath(__file__))
RESOURCES = path.join(path.dirname(CURRENT_DIR),"resources")
SPRITES_DIR = path.join(RESOURCES,"sprites")
BACKGROUNDS_DIR = path.join(RESOURCES,"backgrounds")
AVATARS_DIR = path.join(RESOURCES,"avatars")

 # Funkcje do wykorzystania

class Box:
   z=0
   def __init__(self, _x, _y, _width, _height):
      Box.z+=1
      self.z = Box.z
      self.x = _x
      self.y = _y
      self.width = _width
      self.height = _height
      self.sprite = None

   def resize(self,newWidth,newHeight):
      self.width = newWidth
      self.height = newHeight

   def sizeWindow(self,filewin):
      label1 = Label(filewin, text="Width (" + str(selected.width) + ")")
      label2 = Label(filewin, text="Height (" + str(selected.height) + ")")
      var1 = IntVar()
      var2 = IntVar()
      def updateFromSlider(cos):
         selected.resize(20*var1.get(),20*var2.get())
         label1.config(text="Width (" + str(selected.width) + ")")
         label2.config(text="Height (" + str(selected.height) + ")")
      width = Scale(filewin, from_=1, to=120, variable=var1,  command=updateFromSlider)
      height = Scale(filewin, from_=1, to=120, variable=var2, command=updateFromSlider)
      var1.set (int(selected.width/20)) 
      var2.set (int(selected.height/20)) 
      label1.pack()
      width.pack()
      label2.pack()
      height.pack()

   def spriteWindow(self, filewin):
      label = Label(filewin, text="This ground type has no sprite settings")
      label.pack()

class Trigger(Box):
   def __init__(self, _x, _y, _width, _height, cutsceneInfo="[]"):
      super().__init__(_x,_y,_width,_height)
      self.cutsceneInfo = eval(cutsceneInfo)

   def setMessage(self,message, icon, delay = 0):
      actionSpecs = {"type": "message","text": message, "icon" : icon, "delay": delay}
      self.cutsceneInfo.append(actionSpecs)


   def representXML(self, map):
      temp = ET.SubElement(map, "trigger")
      temp.set("x", str(self.x))
      temp.set("y", str(self.y))
      temp.set("width", str(self.width))
      temp.set("height",str(self.height))
      temp.set("cutsceneInfo",str(self.cutsceneInfo))

   def resetZ(self):
      temp = Trigger(windowOffset[0],windowOffset[1],self.width,self.height, cutsceneInfo=self.cutsceneInfo)
      return temp
   
   def specialWindow(self,filewin):
      label1 = Label(filewin, text="Configure cutscene")
      actions = Listbox(filewin)
      trigTypes = [str(i+1) + self.cutsceneInfo[i]["type"] for i in range (len(self.cutsceneInfo))]
      for i in range(len(trigTypes)):
         actions.insert(i, trigTypes[i])
      def showActionTypes(editFlag):
         nextWindow = Toplevel(root)
         actionsType = ["messageBox", "moveEntity", "killEntity", "endGame"]
         actionTypes = Listbox(nextWindow)
         selectionID = 0
         for i in range(len(actionsType)):
            actionTypes.insert(i, actionsType[i])
         selectionType = "messageBox"
         if editFlag:
            for i in actions.curselection():
               id = int(actions.get(i)[0])-1
               selectionType = self.cutsceneInfo[id]
               selectionID = id
            selectionType = selectionType["type"]
         actionTypes.select_set(actionsType.index(selectionType))
         def getToEditWindow(editflag):
            nextWindowNext = Toplevel(root)
            selection = {}
            movement_or_text = ""
            icon_or_id = 0
            delay = 0
            for i in actionTypes.curselection():
               selectionType = actionTypes.get(i)
            if editFlag:
               selection = self.cutsceneInfo[selectionID]
               if selectionType==selection["type"]:
                  values = list(selection.values())
                  movement_or_text = values[1]
                  if selectionType!="endGame":
                     icon_or_id = values[2]
                     if selectionType!="killEntity":
                        delay = values[3]
               else:
                  selection = {}
            delayText = Label(nextWindowNext,text="Enter action delay")
            delayT = Text(nextWindowNext,height=1, width=5)
            delayT.insert(END, delay)
            if selectionType=="messageBox":
               label2 = Label(nextWindowNext, text="Enter messageBox text")
               text = Text(nextWindowNext, height = 5, width = 20)
               text.insert(END,movement_or_text)
               spriteLabel = Label(nextWindowNext, text="Select avatar icon")
               spriters = listdir(AVATARS_DIR)
               spriters.append("None")
               list2 = Listbox(nextWindowNext)
               for i in range(len(spriters)):
                  list2.insert(i, spriters[i])
               if icon_or_id!=0:
                  icon_or_id = spriters.index(icon_or_id)
               list2.select_set(icon_or_id)
               def pushInfo():
                  selection2 = "None"
                  for i in list2.curselection():
                     selection2 = list2.get(i)
                  selection = {"type": selectionType,"text" : text.get("1.0", "end-1c"), "icon" : selection2, "delay": delayT.get("1.0", "end-1c")}
                  if editFlag:
                     self.cutsceneInfo[selectionID] = selection
                  else:
                     self.cutsceneInfo.append(selection)
                  nextWindow.destroy()
                  nextWindowNext.destroy()
                  filewin.destroy()
               button3 = Button(nextWindowNext,text="Confirm",command=pushInfo)
               label2.pack()
               text.pack()
               spriteLabel.pack()
               list2.pack()
               delayText.pack()
               delayT.pack()
               button3.pack()
            elif selectionType=="moveEntity":
               def decompress(tekst):
                  temp=""
                  num = ""
                  for i in tekst:
                     if i.isdigit():
                        num+= i
                     else:
                        temp+= int(num)*i
                        num=""
                  return temp
               label2 = Label(nextWindowNext, text="Enter entity id:")
               id = Text(nextWindowNext, height=1, width=10)
               id.insert(END,icon_or_id)
               labelMov = Label(nextWindowNext, text="Current movement:\nNone")
               move = []
               if movement_or_text!="":
                  temp = decompress(movement_or_text)
                  temp1 = ""
                  for i in temp:
                     if i=="L":
                        temp1+="Left\n"
                        move.append("Left")
                     elif i=="R":
                        temp1+="Right\n"
                        move.append("Right")
                     else:
                        temp1+="Wait\n"
                        move.append("Wait")
                  labelMov.config(text="Current movement:\n" + temp1)
               def createMovement(direction,move):
                  move.append(direction)
                  if labelMov.cget("text") == "Current movement:\nNone":
                     labelMov.config(text="Current movement:\n" + direction + "\n")
                  else:
                     labelMov.config(text=labelMov.cget("text")+ direction + "\n")
               buttonLeft = Button(nextWindowNext, text="Move entity 1 block left",command=lambda: createMovement("Left",move))
               buttonStop = Button(nextWindowNext, text="Make entity wait",command=lambda: createMovement("Wait",move))
               buttonRight = Button(nextWindowNext, text="Move entity 1 block left",command=lambda: createMovement("Right",move))
               def end():
                  def compress(tekst):
                     temp = ""
                     dig = 0
                     while dig<len(tekst):
                        num = 0
                        letter = tekst[dig]
                        while (tekst[dig+num:len(tekst)].find(letter))==(tekst[dig+num+1:len(tekst)].find(letter)):
                              num+=1
                        num+=1
                        dig+=num
                        temp+= (str(num) + letter)
                     return temp
                  temp = ""
                  for i in move:
                     if i=="Left":
                        temp+="L"
                     elif i=="Right":
                        temp+="R"
                     else:
                        temp+="W"
                  temp = {"type": "moveEntity","movement":compress(temp), "id": id.get("1.0", "end-1c"),"delay": delayT.get("1.0","end-1c")}
                  if editFlag:
                     self.cutsceneInfo[selectionID] = temp
                  else:
                     self.cutsceneInfo.append(temp)
                  nextWindow.destroy()
                  nextWindowNext.destroy()
                  filewin.destroy()
               buttonEnd = Button(nextWindowNext, text="Save", command=end)
               label2.pack()
               id.pack()
               labelMov.pack()
               buttonLeft.pack()
               buttonStop.pack()
               buttonRight.pack()
               delayText.pack()
               delayT.pack()
               buttonEnd.pack()
            elif selectionType=="killEntity":
               labelID = Label(nextWindowNext, text="Enter entity ID")
               id = Text(nextWindowNext, height=1, width=10)
               id.insert(END,movement_or_text)
               def end():
                  temp = {"type": "killEntity", "id": id.get("1.0", "end-1c")}
                  if editFlag:
                     self.cutsceneInfo[selectionID] = temp
                  else:
                     self.cutsceneInfo.append(temp)
                  nextWindow.destroy()
                  nextWindowNext.destroy()
                  filewin.destroy()
               button2 = Button(nextWindowNext, text="Save", command=end)
               labelID.pack()
               id.pack()
               button2.pack()
            elif selectionType=="endGame":
               temp = {"type": "endGame"}
               if editFlag:
                  self.cutsceneInfo[selectionID] = temp
               else:
                  self.cutsceneInfo.append(temp)
               nextWindow.destroy()
               nextWindowNext.destroy()
               filewin.destroy()
         button = Button(nextWindow, text="Proceed", command=lambda: getToEditWindow(editFlag))
         actionTypes.pack()
         button.pack()
      button = Button(filewin, text="Edit selected", command=lambda: showActionTypes(True))
      button1 = Button(filewin, text="Add new", command=lambda: showActionTypes(False))
      if len(trigTypes)==0:
         button["state"] = DISABLED
      else:
         actions.select_set(0)
      label1.pack()
      actions.pack()
      button.pack()
      button1.pack()

class Background(Box):
   z = 0
   def __init__(self, _x,_y,_width,_height, background=None):
      super().__init__(_x,_y,_width,_height)
      Background.z -=1
      self.z = Background.z
      self.background = background

   def resetZ(self):
      background = self.background
      return Background(windowOffset[0],windowOffset[1],self.width,self.height, background = background)
   
   def representXML(self, map):
      temp = ET.SubElement(map, "background")
      temp.set("x", str(self.x))
      temp.set("y", str(self.y))
      temp.set("width", str(self.width))
      temp.set("height",str(self.height))
      temp.set("background",self.background)

   def specialWindow(self, filewin):
      if self.background != None and self.background != "None":
         label1 = Label(filewin, text="Current background: " + self.background)
      else:
         label1 = Label(filewin, text="Current background: None")
      sprites = Listbox(filewin)
      spriters = listdir(BACKGROUNDS_DIR)
      for i in range(len(spriters)):
         sprites.insert(i, spriters[i])
      def updateFromList():
         selection = None
         for i in sprites.curselection():
            selection = sprites.get(i)
         self.background = selection
         label1.config(text="Current sprite: " + self.background)
      button = Button(filewin, text="Load", command=updateFromList)
      label1.pack()
      sprites.pack()
      button.pack()

class Grounds(Box):
   def __init__(self, _x,_y,_width,_height, _type, sprite=None, foreground=False):
      super().__init__(_x,_y,_width,_height)
      self.foreground=foreground
      self.type = _type
      if sprite!=None and sprite!="None":
         spriteLocation = path.join(SPRITES_DIR,sprite)
         img = Image.open(spriteLocation)
         img = img.resize((self.width,self.height))
         img= ImageTk.PhotoImage(img)
         self.sprite = img
         self.spriteLoc =sprite
      else:
         self.sprite = None

   def resize(self,newWidth,newHeight, sprite=None, foreground=None):
      self.width = newWidth
      self.height = newHeight
      if foreground!=None:
         self.foreground = foreground
      if self.sprite!=None and self.sprite!="None" or sprite!=None:
         if sprite!="Remove sprite":
            filename=sprite
            if sprite==None:
               filename = self.spriteLoc
            spriteLocation = path.join(SPRITES_DIR,filename)
            img = Image.open(spriteLocation)
            radio = tileViewSize/TILE_SIZE
            img = img.resize((int(radio*self.width),int(radio*self.height)))
            img= ImageTk.PhotoImage(img)
            self.sprite = img
            self.spriteLoc = filename
         else:
            self.sprite=None
            self.spriteLoc="None"

   def resetZ(self):
      sprite = self.sprite
      if self.sprite!=None:
         sprite = self.spriteLoc
      return Grounds(windowOffset[0],windowOffset[1],self.width,self.height,self.type, sprite = sprite)
   
   def representXML(self, map):
      temp = ET.SubElement(map, self.type)
      temp.set("x", str(self.x))
      temp.set("y", str(self.y))
      temp.set("width", str(self.width))
      temp.set("height",str(self.height))
      if self.sprite!=None:
         temp.set("sprite",str(self.spriteLoc))
      else:
         temp.set("sprite",str("None"))
      temp.set("foreground",str(self.foreground))

   def spriteWindow(self, filewin):
      if self.sprite != None and self.sprite != "None":
         label1 = Label(filewin, text="Current sprite: " + self.spriteLoc)
      else:
         label1 = Label(filewin, text="Current sprite: None")
      sprites = Listbox(filewin)
      spriters = listdir(SPRITES_DIR)
      for i in range(len(spriters)):
         sprites.insert(i, spriters[i])
      sprites.insert(len(spriters),"Remove sprite")
      check = IntVar()
      checkbutton = Checkbutton(filewin, variable=check, text="Foreground", onvalue=1, offvalue=0)
      check.set(False)
      if self.foreground=="True" or self.foreground == 1:
         check.set(True)
      def updateFromSlider():
         selection = None
         for i in sprites.curselection():
            selection = sprites.get(i)
         state = False
         if checkbutton.instate(['selected']):
            state=True
         test = check.get()
         self.resize(self.width, self.height, sprite=selection, foreground=state)
         label1.config(text="Current sprite: " + self.spriteLoc)
      button = Button(filewin, text="Load", command=updateFromSlider)
      label1.pack()
      sprites.pack()
      checkbutton.pack()
      button.pack()

   def specialWindow(self,filewin):
      label = Label(filewin, text="Ground type has no special settings")
      label.pack()

class EnemyPlaceholder(Box):
   def __init__(self, _x,_y, _enemyType="szczur", id=None):
      self.sizeChart = {"szczur" : [60,20],"zombieSzczur" : [60,20],"roboSzczur" : [60,20], "matkaKacpra" : [40,80]}
      super().__init__(_x,_y,self.sizeChart[_enemyType][0],self.sizeChart[_enemyType][1])
      self.id = id
      if id=="None":
         self.id=None
      self.type = _enemyType
      spriteName = self.type + "_idle.png"
      spriteLocation = path.join(SPRITES_DIR, spriteName)
      img = Image.open(spriteLocation)
      img = img.resize((self.width,self.height))
      img= ImageTk.PhotoImage(img)
      self.sprite = img
      self.spriteLoc =spriteLocation

   def resize(self,newWidth,newHeight,sprite=None):
      self.width = newWidth
      self.height = newHeight
      filename=self.spriteLoc
      if sprite!=None:
         filename = self.type + "_idle.png"
      spriteLocation = path.join(SPRITES_DIR,filename)
      img = Image.open(spriteLocation)
      radio = tileViewSize/TILE_SIZE
      img = img.resize((int(radio*self.width),int(radio*self.height)))
      img= ImageTk.PhotoImage(img)
      self.sprite = img
      self.spriteLoc = filename

   def sizeWindow(self,filewin):
      label1 = Label(filewin, text="Size edit option not available for enemy type.")
      label1.pack()

   def resetZ(self):
      return EnemyPlaceholder(windowOffset[0],windowOffset[1],self.type)
   
   def representXML(self, map):
      temp = ET.SubElement(map, "enemy")
      temp.set("x", str(self.x))
      temp.set("y", str(self.y))
      temp.set("type", self.type)
      temp.set("id", str(self.id))

   def spriteWindow(self, filewin):
      label = Label(filewin, text="Enemy type has no sprite settings - check special settings to change enemy type")
      label.pack()

   def specialWindow(self,filewin):
      idlabel = Label(filewin, text="Type in character ID for cutscene handling (leave blank for none)")
      id = Text(filewin, height=1, width=10)
      label = Label(filewin, text="Select type for enemy:")
      typesList = Listbox(filewin)
      types = ["szczur", "roboSzczur","zombieSzczur", "matkaKacpra"]
      for i in range(len(types)):
         typesList.insert(i, types[i])
      def updateEnemyType():
         selection = self.type
         for i in typesList.curselection():
            selection = typesList.get(i)
         self.type = selection
         self.resize(newHeight=self.sizeChart[self.type][1],newWidth=self.sizeChart[self.type][0],sprite=True)
         idTemp = id.get(1.0, "end-1c")
         if idTemp!="":
            self.id = idTemp
      button = Button(filewin, text="Save", command=updateEnemyType)
      idlabel.pack()
      id.pack()
      label.pack()
      typesList.pack()
      button.pack()

timer = 0
mapSize = (80,60)
tileViewSize = TILE_SIZE
offset = (0,0)
windowOffset = [0,0]
copyboard = None
loadedFilename = False
selected = False
grounds = []
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
      if type=="block":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="plat":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],40,40,type, sprite="floor.png"))
      elif type=="decor":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],120,40,type, sprite="lawka.png"))
      elif type=="key":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],40,40,type, sprite="key_red.png"))
      elif type=="door":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],20,80,type, sprite="door_side_red.png"))
      elif type=="ladder":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],40,40,type, sprite="ladder.png"))
      elif type=="spawn":
         grounds.append(Grounds(windowOffset[0],windowOffset[1],40,80,type))
      elif type=="background":
         grounds.append(Background(windowOffset[0],windowOffset[1],80,80))
      elif type=="trigger":
         grounds.append(Trigger(windowOffset[0],windowOffset[1],40,40))
      elif type=="enemy":
         grounds.append(EnemyPlaceholder(windowOffset[0],windowOffset[1]))

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
   global timer
   timer+=MS
   canvas.delete("all")
   radio = tileViewSize/TILE_SIZE
   for ground in grounds:
      width = 2
      if ground==selected:
         width=4
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
editMenu.add_command(label="Cut", command=cut)
editMenu.add_command(label="Copy", command=copy)
editMenu.add_command(label="Paste", command=paste)
editMenu.add_command(label="Delete", command=delete)
editMenu.add_separator()
editMenu.add_command(label="Map properties", command=openMapEditWindow)
menu.add_cascade(label="Edit", menu=editMenu)
 # zakladka help
helpMenu = Menu(menu, tearoff=0)
helpMenu.add_command(label="Help Index", command=donothing)
helpMenu.add_command(label="About...", command=donothing)
menu.add_cascade(label="Help", menu=helpMenu)
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