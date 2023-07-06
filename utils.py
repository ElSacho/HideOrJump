from enum import Enum

def hex_to_rgb(hex_color):
    # Converti un code couleur hexadécimal en un tuple RGB
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
class Colors:
    WHITE = hex_to_rgb("fdfffc")
    RED = hex_to_rgb("ff6b6b")
    BLUE1 = hex_to_rgb("05668e")
    BLUE2 = hex_to_rgb("00a896")
    BLACK = hex_to_rgb("000000")
    YELLOW = hex_to_rgb("f0f3bc")
    
    FLOOR_COLORS = YELLOW
    ROCK_COLOR = YELLOW
    BACKGROUND_COLOR = BLUE1
    POLICE_COLOR = YELLOW
    
class GameParameters:
    # General parameters
    BLOCK_SIZE = 20
    SPEED = 25
    INITIAL_SPEED = 20
    
    # Screen parameters
    WIDTH = 680
    HEIGHT = 420
    
    # Obstacles parameters
    ROCK_HEIGHT = 30
    ROCK_WIDTH = BLOCK_SIZE
    BIRD_HEIGHT = 120
    BIRD_WIDTH = BLOCK_SIZE
        
    # Floor parameters
    FLOOR_HEIGHT = 70
    
    # Player parameters
    PLAYER_POS_X = 30
    PLAYER_STAND_HEIGHT = 70
    PLAYER_HIDE_HEIGHT = 20
    JUMP_HALF_TIME = 10
    PLAYER_WIDTH = BLOCK_SIZE
    
    # Physics parameters
    GRAVITY = 1
    
    # Animation
    TIME_PER_FRAME = 2