from tkinter import *
from PIL import Image, ImageTk
root = Tk()
root.title("Edytor")
frame = Frame(root)
frame.pack()
img = ImageTk.PhotoImage(Image.open("joe_mama.jpg"))
elements = []
elements.append(Label(frame, text ="Tutaj cos bedzie."))
elements.append(Label(root, image = img))
for element in elements:
    element.pack()
root.geometry('800x600')
root.mainloop()