from entities import *

class Camera:
    def __init__(self, focus_object:Player, other_objects = []) -> None:
        self.focus_object = focus_object
        self.other_objects = other_objects
    def update(self):
        #run every tick
        move_vec = -self.focus_object.last_movement
        self.focus_object.move_by(move_vec)
        for entity in self.other_objects:
            entity.move_by(vector2d((move_vec.x), (move_vec.y)))
            print(entity.pos)
    def centre_camera(self, window_dimensions):
        window_centre = window_dimensions/2

        move_vec = window_centre - self.focus_object.pos
        self.focus_object.move_by(move_vec)
        for entity in self.other_objects:
            entity.move_by(vector2d((move_vec.x), (move_vec.y)))
            print(entity.pos)