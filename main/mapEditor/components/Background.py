from components.Box import *

class Background(Box):
   z = 0
   def __init__(self, _x,_y,_width,_height, background=None):
      super().__init__(_x,_y,_width,_height)
      Background.z -=1
      self.z = Background.z
      self.background = background

   def resetZ(self):
      ratio = TILE_SIZE/tileViewSize
      background = self.background
      return Background(ratio*windowOffset[0],ratio*windowOffset[1],self.width,self.height, background = background)
   
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
