from components.Box import *

class EnemyPlaceholder(Box):
   def __init__(self, _x,_y, _enemyType="szczur", id=None):
      self.sizeChart = {"szczur" : [60,20],"zombieSzczur" : [60,20],"roboSzczur" : [60,20], "matkaKacpra" : [40,80], "szczurBoss" : [120,80]}
      super().__init__(_x,_y,self.sizeChart[_enemyType][0],self.sizeChart[_enemyType][1])
      self.id = id
      if id=="None":
         self.id=None
      self.type = _enemyType
      spriteName = self.type + "_left0.png"
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
         filename = self.type + "_left0.png"
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
      ratio = TILE_SIZE/tileViewSize
      return EnemyPlaceholder(ratio*windowOffset[0],ratio*windowOffset[1],self.type)
   
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
      types = ["szczur", "roboSzczur","zombieSzczur", "matkaKacpra", "szczurBoss"]
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
