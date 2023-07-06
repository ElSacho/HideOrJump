import pygame

class Block:
    def __init__(self, height, screen_width, screen_height):
        self.posX = 0
        self.width = screen_width
        self.height = height
        self.posY = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.posX, self.posY, self.width, self.height))

pygame.init()

# Définissez la largeur et la hauteur de l'écran.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Créez une instance de bloc.
block_height = screen_height // 2 # Pour diviser l'écran en deux.
block = Block(block_height, screen_width, screen_height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0)) # Remplissez l'écran avec une couleur (ici, noir).

    block.draw(screen) # Dessinez le bloc sur l'écran.

    pygame.display.flip() # Mettez à jour l'affichage de l'écran.

pygame.quit()
