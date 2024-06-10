from components.GameConstants import *
from components.BackgroundManager import *
from pygame.math import lerp
import copy

class Camera:
    def __init__(self, focus_object, other_objects = []) -> None:
        self.focus_object = focus_object
        self.other_objects = other_objects
        self.camera_offset = 0
        self.cameraCenterOffset = 0
        self.lerpBgFlagX = False
        self.lerpBgFlagY = False
        self.targetOffset = vector2d(0,0)
        self.previousOffset = vector2d(0,0)
        self.beginFlag = True
        self.forceUpdate = False
        
    def update(self, window, force=False):
        focus_object_speed = self.focus_object.last_movement
        is_stationary = abs(focus_object_speed.x) < 0.5 and abs(focus_object_speed.y) < 0.5
        if not is_stationary or force or self.forceUpdate:
            self.centre_camera(vector2d(window.get_width(), window.get_height()))
            self.move_camera(window)

    def move_camera(self,window):

        self.camera_offset = -self.focus_object.pos
        newOffset = self.camera_offset + self.cameraCenterOffset
        newOffset = self.get_checks_for_background_bounds(window, newOffset)

        if abs(self.previousOffset.x-newOffset.x)>100 and not self.beginFlag:
            self.lerpBgFlagX = True
            self.targetOffset = copy.deepcopy(newOffset)
            self.forceUpdate = True
            self.focus_object.blockedMovement = True
        if abs(self.previousOffset.y-newOffset.y)>100 and not self.beginFlag:
            self.lerpBgFlagY = True
            self.targetOffset = copy.deepcopy(newOffset)
            self.forceUpdate = True
            self.focus_object.blockedMovement = True
        if self.lerpBgFlagX:
            if not(self.previousOffset-newOffset==vector2d(0,0)):
                newOffset.x = lerp(self.previousOffset.x, newOffset.x, 0.30)
            lerpx_tol = 0.1
            if abs(newOffset.x - self.targetOffset.x) < lerpx_tol:
                self.lerpBgFlagX = False
                self.forceUpdate = False
                self.focus_object.blockedMovement = False
        if self.lerpBgFlagY:
            if not(self.previousOffset-newOffset==vector2d(0,0)):
                newOffset.y = lerp(self.previousOffset.y, newOffset.y, 0.30)
            if newOffset.y == newOffset.y:
                self.lerpBgFlagY = False
                self.forceUpdate = False
                self.focus_object.blockedMovement = False

        self.focus_object.changeCameraOffset(newOffset)
        self.previousOffset = newOffset
        if self.beginFlag:
            self.beginFlag = False
        for entity in self.other_objects:
            entity.changeCameraOffset(newOffset)

    def get_checks_for_background_bounds(self, window, newOffset):
        backgroundTLCorn = -BackgroundManager.currentBGcoords
        backgroundBRCorn = backgroundTLCorn - BackgroundManager.currentBGsize
        check1 = (newOffset).x>=backgroundTLCorn.x
        check2 = self.camera_offset.y-backgroundBRCorn.y<240 + 0.5*(window.get_height()-600)
        check3 = window.get_height()<=BackgroundManager.currentBGsize.y+85 and (newOffset).y+-backgroundTLCorn.y>0
        check4a = window.get_width()<BackgroundManager.currentBGsize.x
        check4b = self.camera_offset.x-backgroundBRCorn.x<360 + 0.5*(window.get_width()-800)
        if check1:
            newOffset.x = backgroundTLCorn.x
        if check2:
            newOffset.y = backgroundBRCorn.y + window.get_height() - 80
        if check3:
            newOffset.y = backgroundTLCorn.y
        if check4a:
            if check4b:
                newOffset.x = backgroundBRCorn.x + window.get_width() - 40
        else:
            newOffset.x = backgroundTLCorn.x
        return newOffset

    def centre_camera(self, window_dimensions):
        window_centre = window_dimensions/2
        self.cameraCenterOffset = window_centre