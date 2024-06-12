from components.editorComponents import *

class App:
    root = Tk()
    canvasFrame = Frame(root)
    canvasFrame.grid(row = 1, column = 1)
    root.title("Edytor")
    mousePositionLabel = Label(canvasFrame, text="(0,0)")
    mousePositionLabel.pack()
    canvas = Canvas (canvasFrame, bg="white",height=600,width=600, scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize), relief=SUNKEN, bd=3)
    hbar=Scrollbar(canvasFrame,orient=HORIZONTAL)
    vbar=Scrollbar(canvasFrame,orient=VERTICAL)
    
    @staticmethod
    def scaleMap(how):
        if how =="bigger" and EditorComponents.tileViewSize<250:
            EditorComponents.tileViewSize +=5
        elif how =="smaller" and EditorComponents.tileViewSize>10:
            EditorComponents.tileViewSize -=5
        App.canvas.config(scrollregion=(0,0,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize))
    @staticmethod
    def canvasUpdate():
        App.canvas.delete("all")
        radio = EditorComponents.tileViewSize/TILE_SIZE
        for ground in EditorComponents.grounds:
            width = 2
            if ground==EditorComponents.selected:
                width=4
            bounds = (EditorComponents.windowOffset[0]-ground.width*radio, EditorComponents.windowOffset[1]-ground.height*radio, radio+EditorComponents.windowOffset[0]+ App.canvas.winfo_width(),EditorComponents.windowOffset[1]+ App.canvas.winfo_height())
            if (int(ground.x*radio)>=bounds[0] and int(ground.y*radio)>=bounds[1] and int(ground.x*radio)<=bounds[2] and int(ground.y*radio)<=bounds[3]):
                if ground.sprite!=None:
                    ground.resize(ground.width, ground.height)
                    App.canvas.create_rectangle(int(ground.x*radio), int(ground.y*radio), int(ground.x*radio) + int(ground.width*radio), int(ground.y*radio + ground.height*radio), width=width)
                    App.canvas.create_image(int(ground.x*radio), int(ground.y*radio), anchor=NW, image=ground.sprite)
                else:
                    App.canvas.create_rectangle(int(ground.x*radio), int(ground.y*radio), int(ground.x*radio + ground.width*radio), int(ground.y*radio + ground.height*radio), width=width)
        xLines = EditorComponents.mapSize[0] - 1
        yLines = EditorComponents.mapSize[1] - 1
        for i in range (xLines):
            App.canvas.create_line((i+1)*EditorComponents.tileViewSize,0,(i+1)*EditorComponents.tileViewSize,EditorComponents.mapSize[1]*EditorComponents.tileViewSize)
        for i in range (yLines):
            App.canvas.create_line(0,(i+1)*EditorComponents.tileViewSize,EditorComponents.mapSize[0]*EditorComponents.tileViewSize,(i+1)*EditorComponents.tileViewSize)
        App.canvas.after(MS, App.canvasUpdate)
    @staticmethod
    def mouseSelect(event):
        radio = EditorComponents.tileViewSize/TILE_SIZE
        x = App.canvas.canvasx(event.x)
        y = App.canvas.canvasy(event.y)
        App.mousePositionLabel.config(text = str((int(x/radio),int(y/radio))))
        if len(EditorComponents.grounds)>0:
            zs = {}
            for ground in EditorComponents.grounds:
                if (x <= radio*(ground.x + ground.width) and x >= radio*ground.x) and (y <= radio*(ground.y + ground.height) and y >= radio*ground.y):
                    zs[ground.z] = ground
            if len(zs)>0:
                EditorComponents.mouseTimer=True
                EditorComponents.selected = zs[max(zs.keys())]
                EditorComponents.offset = [EditorComponents.selected.x-x/radio,EditorComponents.selected.y-y/radio]
            else:
                EditorComponents.selected = False
                EditorComponents.mouseTimer= False
    @staticmethod
    def mouseMoveBlock(event):
        radio = EditorComponents.tileViewSize/TILE_SIZE
        if EditorComponents.mouseTimer:
            x = event.x + App.canvas.winfo_width()/(App.hbar.get()[1]-App.hbar.get()[0])*App.hbar.get()[0]
            y = event.y + App.canvas.winfo_height()/(App.vbar.get()[1]-App.vbar.get()[0])*App.vbar.get()[0]
            if EditorComponents.keyFlags["Shift"]:
                tileHold = TILE_SIZE
                if EditorComponents.selected.width<TILE_SIZE or EditorComponents.selected.height<TILE_SIZE:
                    tileHold/=2
                EditorComponents.selected.x = int(round((x/radio + EditorComponents.offset[0] - int(EditorComponents.tileViewSize*App.canvas.canvasx(event.x)/2700))/tileHold)*tileHold)
                EditorComponents.selected.y = int(round((y/radio + EditorComponents.offset[1] - int(EditorComponents.tileViewSize*App.canvas.canvasy(event.y)/2700))/tileHold)*tileHold)
            else:
                EditorComponents.selected.x = int(x/radio + EditorComponents.offset[0]- int(EditorComponents.tileViewSize*App.canvas.canvasx(event.x)/2700))
                EditorComponents.selected.y = int(y/radio + EditorComponents.offset[1]- int(EditorComponents.tileViewSize*App.canvas.canvasy(event.y)/2700))
    @staticmethod
    def mouseRelease(event):
        EditorComponents.mouseTimer = False
    @staticmethod
    def changeOffsetH(a,b):
        App.canvas.xview(a,b)
        EditorComponents.windowOffset[0] = App.canvas.canvasx(0)
    @staticmethod
    def changeOffsetV(a,b):
        App.canvas.yview(a,b)
        EditorComponents.windowOffset[1] = App.canvas.canvasy(0)