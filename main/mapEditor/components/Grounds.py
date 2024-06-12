from components.Box import *

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
      ratio = TILE_SIZE/tileViewSize
      sprite = self.sprite
      if self.sprite!=None:
         sprite = self.spriteLoc
      return Grounds(ratio*windowOffset[0],ratio*windowOffset[1],self.width,self.height,self.type, sprite = sprite)
   
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
