"""
    A simple game of Snakes and Ladders using Pygame
"""

# Importing the required libraries
import pygame
from pygame import mixer
import random
import time

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((800, 600))
# Set the title and icon
pygame.display.set_caption("Rafts and Alligators")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background (Credits to tahbikat: https://www.deviantart.com/tahbikat/art/Swamp-Background-440292485)
background = pygame.image.load('background.png')
# Background Music
mixer.music.load('background.mp3')
mixer.music.play(-1)

"""
Drawing the images
"""
playerImg = pygame.image.load('player1.png')
boardImg = pygame.image.load('board.png')
diceImgs = [pygame.image.load(f'dice{i}.png') for i in range(1, 7)]
fruitImg = pygame.image.load('fruit.png')

"""
Player
"""
class Player:
    def __init__(self, name):
        self.name = name
        self.position = 0

    def draw(self):
        if self.position <= 99:
            # Face right if the player is on an even row
            if self.position // 10 % 2 == 0:
                screen.blit(playerImg, (board.tiles[self.position].x+7.5, board.tiles[self.position].y+7.5))
            # Otherwise, face left and should start from the right
            else:
                screen.blit(pygame.transform.flip(playerImg, True, False), (730-board.tiles[self.position].x, board.tiles[self.position].y+7.5))

    def move(self, steps, board):
        # Move the player (with animation)
        for _ in range(steps):
            footstep_sound = mixer.Sound('footstep.mp3')
            footstep_sound.play()
            self.position += 1
            if self.position > board.end:
                self.position = 80
            board.draw()
            self.draw()
            pygame.display.flip()
            time.sleep(0.5)

        # Check if the player is on a raft
        if board.tiles[self.position].raft:
            self.position = board.tiles[self.position].raft
        elif board.tiles[self.position].alligator:
            alligator_sound = mixer.Sound('alligator.mp3')
            alligator_sound.play()
            self.position = board.tiles[self.position].alligator

"""
Tile
"""
class Tile:
    def __init__(self, x, y, raft = None, alligator = None):
        self.x = x
        self.y = y
        self.raft = raft
        self.alligator = alligator

"""
Board
"""
class Board:
    def __init__(self):
        self.tiles = []
        self.create_tiles()
        self.set_rafts_and_alligators()
        self.end = 99

    def create_tiles(self):
        # Create the tiles
        for i in range(100):
            x = 60 * (i % 10) + 100
            y = 540 - 60 * (i // 10)
            self.tiles.append(Tile(x, y))
    
    # Manual setting of rafts and alligators
    def set_rafts_and_alligators(self):
        # Set the rafts
        self.tiles[3].raft = 14
        self.tiles[8].raft = 30
        self.tiles[19].raft = 37
        self.tiles[27].raft = 83
        self.tiles[39].raft = 58
        self.tiles[62].raft = 80
        self.tiles[70].raft = 90
        # Set the alligators
        self.tiles[16].alligator = 6
        self.tiles[53].alligator = 33
        self.tiles[61].alligator = 17
        self.tiles[63].alligator = 59
        self.tiles[86].alligator = 23
        self.tiles[92].alligator = 72
        self.tiles[94].alligator = 74
        self.tiles[98].alligator = 77

    def draw(self):
        screen.blit(boardImg, (100, 2.5))
        screen.blit(fruitImg, (108, 10))

"""
Dice
"""
class Dice:
    def __init__(self):
        self.x = 718
        self.y = 500
        self.face = 1

    def roll(self):
        self.face = random.randint(1, 6)
    
    def draw(self):
        screen.blit(diceImgs[self.face - 1], (self.x, self.y))

"""
Game Loop
"""
def display_score(player):
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(f"Player: {player.position+1}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def gameover():
    font = pygame.font.Font('freesansbold.ttf', 64)
    subfont = pygame.font.Font('freesansbold.ttf', 32)
    screen.blit(background, (0, 0))
    # Create the text
    main_text = font.render("Game Over", True, (255, 255, 255))
    sub_text = subfont.render("Press Space to exit", True, (255, 255, 255))
    # Center the text
    text_rect = main_text.get_rect(center=(400, 250))
    screen.blit(main_text, text_rect)
    text_rect = sub_text.get_rect(center=(400, 350))
    screen.blit(sub_text, text_rect)
    pygame.display.update()
    # Play winning sound
    mixer.music.load('win.mp3')
    mixer.music.play(-1)
    # Press any key to exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.quit()

player1 = Player("Player 1")
board = Board()
dice = Dice()
running = True
rolling = False
while running:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not rolling:
            rolling = True

    if rolling:
        dice_sound = mixer.Sound('dice_roll.mp3')
        dice_sound.play()
        for _ in range(10):
            dice.roll()
            dice.draw()
            board.draw()
            player1.draw()
            pygame.display.flip()
            time.sleep(0.1)

        player1.move(dice.face, board)
        rolling = False

    dice.draw()
    board.draw()
    player1.draw()
    display_score(player1)
    if player1.position == 99:
        gameover()

    pygame.display.update()
    