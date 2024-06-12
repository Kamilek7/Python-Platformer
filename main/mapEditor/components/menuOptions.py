from components.trigger import *
from components.background import *
from components.grounds import *
from components.enemy import *
from components.applicationBuild import *

class MenuFuncs:
    def donothing():
        filewin = Toplevel(App.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def reset():
        EditorComponents.grounds = []
        EditorComponents.selected = False

    def saveFile():
        map = ET.Element('map')
        map.set("width",str(EditorComponents.mapSize[0]))
        map.set("height",str(EditorComponents.mapSize[1]))
        for ground in EditorComponents.grounds:
            ground.representXML(map)
        plik = ET.ElementTree(map)
        fileNum = len(listdir(CURRENT_DIR)) - 1
        filename = path.join(CURRENT_DIR, "mapa" + str(fileNum) +".xml")
        if EditorComponents.loadedFilename!=False:
            filename = path.join(CURRENT_DIR, EditorComponents.loadedFilename)
        plik.write(filename)
        EditorComponents.loadedFilename = filename

    def load(canvas):
        filewin = Toplevel(App.root)
        label = Label(filewin, text="Type in the filename")
        filename = Text(filewin, height = 1,  width = 20) 
        button = Button(filewin, text="Load", command= lambda: MenuFuncs.loadfile(filename,filewin, canvas))
        label.pack()
        filename.pack()
        button.pack()


    def loadfile(_filename, filewin, canvas):
        filename = _filename.get(1.0, "end-1c")
        filenameLong = path.join(CURRENT_DIR, filename)
        if path.isfile(filenameLong):
            EditorComponents.grounds = []
            EditorComponents.selected = False
            EditorComponents.loadedFilename = filename
            plik = minidom.parse(filenameLong)
            mapa = plik.getElementsByTagName('map')[0]
            EditorComponents.mapSize = (int(mapa.getAttribute("width")),int(mapa.getAttribute("height")))
            canvas.config(scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize))
            for child in mapa.childNodes:
                if child.tagName=="background":
                    EditorComponents.grounds.append(Background(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")), background=child.getAttribute("background")))
                elif child.tagName=="trigger":
                    EditorComponents.grounds.append(Trigger(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")), cutsceneInfo=child.getAttribute("cutsceneInfo")))
                    
                elif child.tagName=="enemy":
                    EditorComponents.grounds.append(EnemyPlaceholder(int(child.getAttribute("x")),int(child.getAttribute("y")), child.getAttribute("type"), id=child.getAttribute("id")))
                else:
                    EditorComponents.grounds.append(Grounds(int(child.getAttribute("x")),int(child.getAttribute("y")),int(child.getAttribute("width")),int(child.getAttribute("height")),child.tagName, sprite=child.getAttribute("sprite"), foreground=child.getAttribute("foreground")))
            filewin.destroy()
        else:
            filewin = Toplevel(App.root)
            label = Label(filewin, text="ERROR: Wrong filename")
            label.pack()

    def copy():
        if EditorComponents.selected!=False:
            EditorComponents.copyboard = EditorComponents.selected
    
    def paste():
        if EditorComponents.copyboard!=None:
            new = EditorComponents.copyboard.resetZ()
            EditorComponents.grounds.append(new)
    
    def cut():
        MenuFuncs.copy()
        MenuFuncs.delete()
    
    def delete():
        if EditorComponents.selected!=False:
            for i in EditorComponents.grounds:
                if i == EditorComponents.selected:
                    EditorComponents.grounds.remove(i)
                    EditorComponents.selected = False
