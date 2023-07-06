import pygame
import random
from utils import Colors, GameParameters
import os 

class Player:
    def __init__(self):
        self.posX = GameParameters.PLAYER_POS_X
        self.relativePosY = 0
        self.t_jump = 0
        self.gravity = GameParameters.GRAVITY
        self.halt_time_jump = GameParameters.JUMP_HALF_TIME
        self.width = GameParameters.PLAYER_WIDTH
        self.posY = self.relativePosY + GameParameters.FLOOR_HEIGHT
        self.drawer = PlayerDrawer()
        self.is_hide = False
        self.height = GameParameters.PLAYER_STAND_HEIGHT
        
    def move(self, action):
        if self.relativePosY > 0:
            self.jump()
            return
        if action == 1:
            self.jump()
            return
        if action == -1:
            self.hide()
        else :
            # self.height = GameParameters.PLAYER_STAND_HEIGHT
            self.is_hide = False
        
    def jump(self):
        self.t_jump += 1
        self.relativePosY = - self.gravity * ( (self.t_jump - self.halt_time_jump)**2 - self.halt_time_jump**2)
        # self.height = GameParameters.PLAYER_STAND_HEIGHT
        # self.width = GameParameters.PLAYER_WIDTH
        if self.t_jump == 2*self.halt_time_jump:
            self.t_jump = 0
        self.posY = self.relativePosY + GameParameters.FLOOR_HEIGHT
        self.is_hide = False
        
    def hide(self):
        # self.height = GameParameters.PLAYER_HIDE_HEIGHT
        self.is_hide = True
        
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.RED, (self.posX, GameParameters.HEIGHT - self.posY - self.height, self.width,  self.height ))
        self.drawer.draw(self, screen)
    
    def draw2(self, screen):
        pygame.draw.rect(screen, Colors.RED, (self.posX, GameParameters.HEIGHT - self.posY - self.height, self.width,  self.height ))
        #  [left, top, width, height]
        
    def isCollision(self, obstacles):
        for obstacle in obstacles.listObstacles:
            # Si l'obstacle n'est pas encore au niveau du joueur, les autres non plus et c'est bon
            if obstacle.posX > self.posX + self.width :
                return False
            gameOver = obstacle.isCollision(self)
            if gameOver:
                return True
        return False
    
class PlayerDrawer:
    def __init__(self):
        self.animation_time = 0
        self.current_frame_timer = 0
        self.actual_animation = 'run'
        folder_run = 'assets/course/'
        self.images_run = [pygame.image.load(os.path.join(folder_run, file)) 
                   for file in sorted(os.listdir(folder_run)) 
                   if file.endswith('.png')]
        folder_down = 'assets/down/'
        self.images_down = [pygame.image.load(os.path.join(folder_down, file)) 
                   for file in sorted(os.listdir(folder_down)) 
                   if file.endswith('.png')]
    
    def draw(self, player, screen):
        if not player.is_hide:
            if not self.actual_animation == 'run':
                self.actual_animation = 'run'
                self.animation_time = 0
                self.current_frame_timer = 0
            player.height = self.images_run[self.animation_time].get_rect().height
            player.width = self.images_run[self.animation_time].get_rect().width
            
            screen.blit(self.images_run[self.animation_time], (player.posX, GameParameters.HEIGHT - player.posY - player.height ))
            if player.relativePosY == 0:
                self.current_frame_timer += 1
                if self.current_frame_timer == GameParameters.TIME_PER_FRAME:
                    self.current_frame_timer = 0
                    self.animation_time += 1
                    self.animation_time = self.animation_time % len(self.images_run)
        else :
            if not self.actual_animation == 'down':
                self.actual_animation = 'down'
                self.animation_time = 0
                self.current_frame_timer = 0
            player.height = self.images_down[self.animation_time].get_rect().height
            player.width = self.images_down[self.animation_time].get_rect().width
            
            screen.blit(self.images_down[self.animation_time], (player.posX, GameParameters.HEIGHT - player.posY - player.height ))
            self.current_frame_timer += 1
            if self.current_frame_timer == GameParameters.TIME_PER_FRAME:
                self.current_frame_timer = 0
                self.animation_time += 1
                self.animation_time = self.animation_time % len(self.images_down)
                    
        