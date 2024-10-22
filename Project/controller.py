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

        self.game_state = "Main Menu"
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

            if self.game_state == 'Main Menu':
                self.game_state = self.game.main_menu(self.dt, self.game_state, events)
            elif self.game_state == 'Single Options':
                self.game_state = self.game.single_options(self.dt, self.game_state, events)
            elif self.game_state == 'Multiple Options':
                self.game_state = self.game.multiple_options(self.dt, self.game_state, events)
            elif 'Change Name' in self.game_state:
                self.game_state = self.game.change_name(self.dt, self.game_state, events)
            elif 'Change Keys' in self.game_state:
                self.game_state = self.game.change_keys(self.dt, self.game_state, events)
            elif self.game_state == 'Lobby':
                self.game_state = self.game.lobby(self.dt, self.game_state, events)
            elif self.game_state == 'Game':
                self.game_state = self.game.run(self.dt, self.game_state, events)
            elif self.game_state == 'Multiplayer Game':
                self.game_state = self.game.multiplayerRun(self.dt, self.game_state, events)
            elif self.game_state == 'End':
                self.game_state = self.game.end(self.dt, self.game_state, events)

            pygame.display.update()
            self.dt = (self.clock.tick(self.fps) / 1000) * 60

        self.quit()

    def quit(self):
        self.game.client.disconnect()
        pygame.quit()
        sys.exit()
