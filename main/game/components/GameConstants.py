from os import *
import pygame
from pygame.locals import *

CURRENT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
RESOURCES = path.join(path.dirname(CURRENT_DIR),"resources")
SYSTEM_DIR = path.join(RESOURCES,"system")
SPRITES_DIR = path.join(RESOURCES,"sprites")
BACKGROUNDS_DIR = path.join(RESOURCES,"backgrounds")
MAPS_DIR = path.join(RESOURCES,"maps")
AVATARS_DIR = path.join(RESOURCES,"avatars")
APP_HEIGHT = 600
APP_WIDTH = 800
MAX_FPS = 60
vector2d = pygame.math.Vector2