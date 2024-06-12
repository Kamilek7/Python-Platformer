from components.menuOptions import *

class InputEvents:
    def mouseWheelEvents(event):
        if event.num == 5 or event.delta <= -10:
            App.scaleMap("smaller")
        if event.num == 4 or event.delta >= 10:
            App.scaleMap("bigger")
    
    def keyBoardInput(event):
        if event.keysym == "Shift_L":
            EditorComponents.keyFlags["Shift"] = True
        if event.keysym == "Control_L":
            EditorComponents.keyFlags["Ctrl"] = True
        if EditorComponents.selected!=False:
            if event.keysym == "Delete":
                MenuFuncs.delete()
            if event.keysym == "x" and EditorComponents.keyFlags["Ctrl"]:
                MenuFuncs.cut()
            if event.keysym == "c" and EditorComponents.keyFlags["Ctrl"]:
                MenuFuncs.copy()

        if event.keysym == "v" and EditorComponents.keyFlags["Ctrl"] and EditorComponents.copyboard!=None:
            MenuFuncs.paste()
        if event.keysym == "s" and EditorComponents.keyFlags["Ctrl"]:
            MenuFuncs.saveFile()

    def keyBoardInputRelease(event):
        if event.keysym == "Shift_L":
            EditorComponents.keyFlags["Shift"] = False
        if event.keysym == "Control_L":
            EditorComponents.keyFlags["Ctrl"] = False