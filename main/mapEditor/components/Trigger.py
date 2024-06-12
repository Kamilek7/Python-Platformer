from components.Box import *

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
      ratio = TILE_SIZE/tileViewSize
      temp = Trigger(ratio*windowOffset[0],ratio*windowOffset[1],self.width,self.height, cutsceneInfo=self.cutsceneInfo)
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
