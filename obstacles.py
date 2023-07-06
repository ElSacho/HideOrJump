import pygame
import random
from utils import Colors, GameParameters


class Bird():
    def __init__(self):
        self.posX = GameParameters.WIDTH
        self.width = GameParameters.BIRD_WIDTH
        self.height = GameParameters.BIRD_HEIGHT
        self.posY = GameParameters.FLOOR_HEIGHT + self.height
        
    def move(self, speed):
        self.posX -= speed
        
    def isCollision(self, player):
        if self.posX > player.posX + player.width :
            return False
        # Si les deux objets se supperposent, on regarde la hauteur
        if not self.posX + self.width < player.posX :
            if player.posY + player.height > self.posY:
                print("Player : ", player.posY + player.height )
                print("Box : ", self.posY)
                return True
        return False
        
    def to_kill(self):
        return self.posX + self.width < 0        
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.ROCK_COLOR, (self.posX, 0, self.width, GameParameters.HEIGHT - self.posY))
        #  [left, top, width, height]


class Rock():
    def __init__(self):
        self.posX = GameParameters.WIDTH
        self.width = GameParameters.ROCK_WIDTH
        self.height = GameParameters.ROCK_HEIGHT
        self.posY = GameParameters.FLOOR_HEIGHT + self.height
        
    def move(self, speed):
        self.posX -= speed
        
    def isCollision(self, player):
        if self.posX > player.posX + player.width :
            return False
        # Si les deux objets se supperposent, on regarde la hauteur
        if not self.posX + self.width < player.posX :
            if player.posY < self.posY:
                print("Player : ",player.posY)
                print("Box : ",self.posY)
                return True
        return False
        
    def to_kill(self):
        return self.posX + self.width < 0        
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.ROCK_COLOR, (self.posX, GameParameters.HEIGHT - self.posY, self.width, self.height))
        
class Obstacles():
    def __init__(self):
        self.listObstacles = []
        self.lastCreationTime = 0
        self.obstacles_killed = 0
        
    def move(self, speed):
        for obstacle in self.listObstacles:
            obstacle.move(speed)
            
    def draw(self, screen):
        for obstacle in self.listObstacles:
            obstacle.draw(screen)
            
    def generateObstacle(self):
        self.lastCreationTime += 1
        if self.lastCreationTime > 50:
            self.lastCreationTime = 0
            type = random.randint(0,2)
            if type == 0:
                self.listObstacles.append(Rock())
            else:
                self.listObstacles.append(Bird())
            
    def kill_obstacles(self):
        while len(self.listObstacles) > 0 and self.listObstacles[0].to_kill():
            self.listObstacles.pop(0)
            self.obstacles_killed += 1
               
    def update(self, speed):
        self.move(speed)
        self.generateObstacle()
        self.kill_obstacles()