import pygame
import random
from utils import Colors, GameParameters
from obstacles import Obstacles
from player import Player
from floor import Floor


class Game:
    def __init__(self):
        self.score = 0
        self.speed = GameParameters.INITIAL_SPEED

        self.screen = pygame.display.set_mode((GameParameters.WIDTH, GameParameters.HEIGHT))
        pygame.display.set_caption('Hide or Jump')
        self.clock = pygame.time.Clock()
        self.police = pygame.font.Font("arial.ttf", 28)
        
        self.floor = Floor()
        self.player = Player()
        self.obstacles = Obstacles()
        
    def update_speed(self):
        if self.speed < 50:
            self.speed +=0.01
        
    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()  # Obtenir l'état des touches

        if keys[pygame.K_DOWN]:
            action = -1
        elif keys[pygame.K_UP]:
            action = 1
        else:
            action = 0
        
        self.update_speed()
        self.player.move(action)
        
        self.obstacles.update(self.speed)
        
        self.draw()
        self.clock.tick(GameParameters.SPEED)
        
        gameOver = self.player.isCollision(self.obstacles)

        return gameOver
            
    def draw(self):
        self.screen.fill(Colors.BACKGROUND_COLOR)
        
        # pygame.draw.rect(self.screen, Colors.BLACK, (0, 200, GameParameters.WIDTH, GameParameters.HEIGHT))
        
        self.floor.draw(self.screen)
        self.obstacles.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_score()
        
        pygame.display.flip()
        pygame.display.update()
        
        # text = font.render("Score: " + str(self.score), True, Colors.BLACK)
        # self.display.blit(text, [0, 0])
        # pygame.display.flip()
        
    def draw_score(self):
        # Afficher le texte    
        self.screen.blit(self.police.render(f'Score : {self.obstacles.obstacles_killed}', True, Colors.POLICE_COLOR), (50,50))
        
if __name__ == '__main__':
    pygame.init()
    
    game = Game()
    
    #game loop
    while True:
        game_over = game.play_step()
        if game_over == True:
            break     
    pygame.quit()