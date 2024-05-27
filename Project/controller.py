import pygame
import Project.constants as constants
import Project.instance as instance
import sys

class GameController:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption(constants.TITLE)
        # self.icon = pygame.image.load(constants.ICON)
        # pygame.display.set_icon(self.icon)

        self.game_state = "Game"
        self.game = instance.GameInstance()

        self.fps = constants.FPS
        self.dt = self.fps
        self.clock = pygame.time.Clock()

    def run(self):
        while self.game_state != 'Quit':
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.game_state = 'Quit'

            if self.game_state == 'Game':
                self.game_state = self.game.run(self.dt, self.game_state, events)

            pygame.display.update()
            self.dt = (self.clock.tick(self.fps) / 1000) * 60

        self.quit()

    def quit(self):
        pygame.quit()
        sys.exit()
