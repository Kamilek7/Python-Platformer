from tkinter import *
from tkinter.ttk import *
from PIL import Image,ImageTk
from os import *
import xml.etree.cElementTree as ET
from xml.dom import minidom

MS = 15
TILE_SIZE = 40
CURRENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
RESOURCES = path.join(path.dirname(CURRENT_DIR),"resources")
SPRITES_DIR = path.join(RESOURCES,"sprites")
BACKGROUNDS_DIR = path.join(RESOURCES,"backgrounds")
AVATARS_DIR = path.join(RESOURCES,"avatars")

# non consts

selected = None
mapSize = (80,60)
tileViewSize = TILE_SIZE
offset = (0,0)
windowOffset = [0,0]
copyboard = None
loadedFilename = False
selected = False
grounds = []
keyFlags = {"Shift": False, "Ctrl": False}
root = Tk()