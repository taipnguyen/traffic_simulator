import pygame
from enum import Enum
screen = pygame.display.set_mode((1280, 720))

class car():
    def __init__(self, x, next_car = None):
        self.car_pos = pygame.Vector2(x, screen.get_height()/2)
        self.car_size = pygame.Vector2(200,100)
        self.velocity = 100
        self.next_car = next_car
    def get_pos(self):
        return self.car_pos
    def get_velocity(self):
        return self.velocity
    def get_next(self):
        return self.next_car
    def get_size(self):
        return self.car_size
    
class light_color(Enum):
    RED = 1
    GREEN = 2