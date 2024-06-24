import pygame
import os
import Project.helpers as helpers

pygame.init()

TITLE = "Under The Stars"
ICON = ""
WIDTH = 1000
HEIGHT = 600
FPS = 60
COLOURS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 220, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "indigo": (75, 0, 130),
    "magenta": (255, 0, 255),
    "lime": (118, 186, 27),
    "grey": (24, 25, 26),
    "light grey": (97, 97, 97),
    "light blue": (38, 171, 255),
    "red2": (229, 57, 53),
    "purple": (124, 82, 149),
    "gold": (255, 218, 0)
}
bigFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 112)
font = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 64)
medfont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 36)
regFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 24)
smallFont = pygame.font.Font("Assets\\Fonts\\dpcomic.ttf", 18)

