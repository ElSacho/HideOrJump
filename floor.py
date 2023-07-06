from utils import Colors, GameParameters
import pygame

class Floor():
    def __init__(self):
        self.height = GameParameters.HEIGHT - GameParameters.FLOOR_HEIGHT
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.FLOOR_COLORS, (0, self.height, GameParameters.WIDTH, GameParameters.HEIGHT))
        #  [left, top, width, height]