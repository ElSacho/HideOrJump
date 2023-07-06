import pygame
import random
from utils import Colors, GameParameters
from obstacles import Obstacles
from player import Player
from floor import Floor
import numpy as np


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
        
    def step(self, action):        
        self.update_speed()
        self.player.move(action)
        
        self.obstacles.update(self.speed)
                
        game_over = self.player.isCollision(self.obstacles)
        
        # update the reward : +1 if you passed an obstacle, -5 if you loose, or zero if nothing happened
        reward = self.obstacles.obstacles_killed - self.score
        self.score = self.obstacles.obstacles_killed
        if game_over:
            reward = -1
        
        next_state = self.get_state()
        
        self.draw()
        self.clock.tick(GameParameters.SPEED)
        
        return next_state, reward, game_over, {}
    
    def get_state(self):
        obstacles_state = self.obstacles.get_state()
        player_state = self.player.get_state()
        general_state = np.array([self.speed / GameParameters.MAX_SPEED])
        
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
        
        # pygame.draw.rect(self.screen, Colors.BLACK, (0, 200, GameParameters.WIDTH, GameParameters.HEIGHT))
        
        self.floor.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_score()
        self.draw_state()
        
        pygame.display.flip()
        pygame.display.update()
        
        # text = font.render("Score: " + str(self.score), True, Colors.BLACK)
        # self.display.blit(text, [0, 0])
        # pygame.display.flip()
        
    def draw_score(self):
        # Afficher le texte    
        self.screen.blit(self.police.render(f'Score : {self.score}', True, Colors.POLICE_COLOR), (50,50))
        
    def draw_state(self):
        np.set_printoptions(precision=2)
        self.screen.blit(self.police.render(f'State : {self.state}', True, Colors.POLICE_COLOR), (50,30))
        
if __name__ == '__main__':
    pygame.init()
    
    game = GameAI()
    
    #game loop
    while True:
        action = random.randint(0,2)
        action = game.player.get_actions()[action]
        
        next_state, reward, game_over, dict = game.step(action)

        if game_over == True:
            game.reset() 
                           
    pygame.quit()