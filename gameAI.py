import pygame
import random
from utils import Colors, GameParameters
from obstacles import Obstacles
from player import Player
from floor import Floor
import numpy as np
from PIL import Image
import os
import ffmpeg
import shutil


class GameAI:
    def __init__(self):
        self.score = 0
        self.speed = GameParameters.INITIAL_SPEED

        self.screen = pygame.display.set_mode((GameParameters.WIDTH, GameParameters.HEIGHT))
        pygame.display.set_caption('Hide or Jump')
        self.clock = pygame.time.Clock()
        self.police = pygame.font.Font("assets/arial.ttf", 28)
        
        self.floor = Floor()
        self.player = Player()
        self.obstacles = Obstacles()
        
        self.action_space = self.player.action_space
        self.global_observation_space = 1
        self.observation_space = self.player.observation_player_space + self.obstacles.observation_obstacles_space + self.global_observation_space
        
    def update_speed(self):
        if self.speed < GameParameters.MAX_SPEED :
            self.speed +=0.01
        
    def step(self, action, draw=True):        
        self.update_speed()
        self.player.move(action)
        
        self.obstacles.update(self.speed)
                
        game_over = self.player.isCollision(self.obstacles)
        
        # update the reward : +1 if you passed an obstacle, -5 if you loose, or zero if nothing happened
        reward = self.obstacles.obstacles_killed - self.score
        self.score = self.obstacles.obstacles_killed
        if game_over:
            reward = -1
        
        if draw:
            self.draw()
            self.clock.tick(GameParameters.SPEED)
        else :
            self.player.update_size()
            
        next_state = self.get_state()
        
        return next_state, reward, game_over, {}
    
    def get_state(self):
        obstacles_state = self.obstacles.get_state()
        player_state = self.player.get_state()
        general_state = np.array([self.speed / GameParameters.MAX_LEARNING_SPEED])
        # general_state = np.array([self.speed / 50])
        
        self.state = np.concatenate((obstacles_state, player_state, general_state))
        
        return np.concatenate((obstacles_state, player_state, general_state))
           
    def reset(self):
        self.floor = Floor()
        self.player = Player()
        self.obstacles = Obstacles()
        
        self.score = 0
        self.speed = GameParameters.INITIAL_SPEED
        
        return self.get_state()
            
    def draw(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)
                
        self.floor.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_score()
        self.draw_state()
        
        pygame.display.flip()
        pygame.display.update()

        if GameParameters.RENDER_GAMEPLAY:
            self.capture_frame()
 
    def draw_score(self):
        # Afficher le texte    
        self.screen.blit(self.police.render(f'Score : {self.score}', True, Colors.POLICE_COLOR), (50,50))
        
    def draw_state(self):
        np.set_printoptions(precision=2)
        self.screen.blit(self.police.render(f'State : {self.state}', True, Colors.POLICE_COLOR), (50,30))
        
    def start_video(self, name):
        self.image_folder = name
        os.makedirs(self.image_folder, exist_ok=True)
        self.frame_number = 0
                
    def make_video(self, name):
        if not os.path.exists(GameParameters.RENDER_FOLDER):
            os.makedirs(GameParameters.RENDER_FOLDER)

        (
            ffmpeg
            .input(os.path.join(self.image_folder, 'frame_%04d.png'), framerate=25)
            .output(os.path.join(GameParameters.RENDER_FOLDER, name), vcodec='libx264', pix_fmt='yuv420p')
            .run()
        )
        
        shutil.rmtree(self.image_folder)
        
    def capture_frame(self):
        pygame.display.flip()
        data = pygame.surfarray.array3d(pygame.display.get_surface())
        data = data.transpose(1,0,2)
        img = Image.fromarray(data, 'RGB')
        img.save(os.path.join(self.image_folder, f'frame_{self.frame_number:04d}.png'))
        self.frame_number += 1
     