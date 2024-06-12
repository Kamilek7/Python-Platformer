from components.EditorConstants import *

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

