import pygame
import Project.constants as constants
from Project.player import Player
from Project.map import Map
import random

class GameInstance():

    def __init__(self):
        self.width, self.height = constants.WIDTH, constants.HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.display = pygame.Surface((self.width, self.height))
        self.timer = 0
        
        self.background = pygame.image.load("Assets\\background.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.map = Map("Project\\map.txt")
        self.players = []
        self.p1 = Player("Assets\\player.png", [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d])
        # self.p2 = Player("Assets\\player.png", [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT])
        self.players.append(self.p1)
        # self.players.append(self.p2)
        for player in self.players:
            player.player_rect.x = random.randint(200, 700)

    def main_menu(self):
        pass

    def run(self, dt, state, events):
        self.display.fill(constants.COLOURS["black"])
        self.display.blit(self.background, (0, 0))

        self.map.draw(self.display)
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.draw(self.display)
            player.checkInput(events, keys, self.map.tiles)

        for event in events:
            pass

        self.screen.blit(self.display, (0, 0))
        
        return state
