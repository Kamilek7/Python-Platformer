from entities import *
import math
class Camera:
    def __init__(self, focus_object:Player, other_objects = [], y_centre = 400) -> None:
        self.focus_object = focus_object
        self.other_objects = other_objects
        self.y_centre = y_centre
    def update(self, window):
        #run every tick
        #moves the camera by changing pos of all objects
        move_vec = -self.focus_object.last_movement
        move_vec.y = 0
        self.focus_object.move_by(move_vec)
        window_height = window.get_height()
        abs_f_obj_y = abs(self.focus_object.pos.y)
        offset = window_height/2.3
        if abs_f_obj_y < window_height/2 - offset or abs_f_obj_y > window_height/2 + offset:
            self.centre_camera(vector2d(window.get_width(), window.get_height()))

        for entity in self.other_objects:
            entity.move_by(vector2d((move_vec.x), (move_vec.y)))
    def centre_camera(self, window_dimensions):
        #centers the camera to the middle of window_dimensions
        window_centre = window_dimensions/2
        window_centre.y += window_dimensions.y/6
        move_vec = window_centre - self.focus_object.pos
        self.focus_object.move_by(move_vec)
        for entity in self.other_objects:
            entity.move_by(vector2d((move_vec.x), (move_vec.y)))