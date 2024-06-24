import pygame
import socket
import Project.constants as constants
from Project.player import Player
from Project.client import Client
from Project.map import Map 
import random
import json

class GameInstance():
    def __init__(self):
        self.width, self.height = constants.WIDTH, constants.HEIGHT

        self.client = Client()
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.display = pygame.Surface((self.width, self.height))
        self.displayCopy = self.display.copy()
        self.timer = 0
        self.screenshake = 0

        self.titleTxt = constants.bigFont.render(constants.TITLE, True, (107, 107, 107))
        self.singleTxt = constants.font.render("Singleplayer", True, (255, 255, 255))
        self.multiTxt = constants.font.render("Multiplayer", True, (255, 255, 255)) 
        self.quitTxt = constants.font.render("Quit", True, (255, 255, 255))
        self.singleTxtHover = constants.font.render("Singleplayer", True, (107, 107, 107))
        self.multiTxtHover = constants.font.render("Multiplayer", True, (107, 107, 107)) 
        self.quitTxtHover = constants.font.render("Quit", True, (107, 107, 107))
        self.singleTxtRect = self.singleTxt.get_rect()
        self.singleTxtRect.x, self.singleTxtRect.y = 100, 200
        self.multiTxtRect = self.multiTxt.get_rect()
        self.multiTxtRect.x, self.multiTxtRect.y = 100, 300
        self.quitTxtRect = self.quitTxt.get_rect()
        self.quitTxtRect.x, self.quitTxtRect.y = 100, 400
        self.continueTxt = constants.regFont.render("Press Enter to Continue", True, (255, 255, 255))
        
        self.trash = pygame.image.load("Assets\\trash.png").convert_alpha()
        self.trash = pygame.transform.scale(self.trash, (32, 32))
        self.trashHover = pygame.image.load("Assets\\trashHover.png").convert_alpha()
        self.trashHover = pygame.transform.scale(self.trashHover, (32, 32))

        self.background = pygame.image.load("Assets\\bg.jpg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.transparentBg = pygame.Surface((self.width, self.height))
        self.transparentBg = self.transparentBg.convert_alpha()
        self.transparentBg.fill((255, 255, 255, 196))

        self.map = Map("Project\\map.txt")
        self.players = []
        self.projectiles = []
        self.newName = []

        self.gameUICoords = [[[500 - 150 / 2, 475]], [[250 - 150 / 2, 475], [750 - 150 / 2, 475]], [[167 - 150 / 2, 475], [500 - 150 / 2, 475], [833 - 150 / 2, 475]], [[125 - 150 / 2, 475], [375 - 150 / 2, 475], [625 - 150 / 2, 475], [875 - 150 / 2, 475]]]

    def main_menu(self, dt, state, events):
        self.display.fill(constants.COLOURS["black"])
        self.display.blit(self.background, (0, 0))

        self.display.blit(self.titleTxt, (50, 50))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        if self.singleTxtRect.collidepoint(mouse):
            self.display.blit(self.singleTxtHover, self.singleTxtRect)
            if click:
                state = "Single Options"
        else:
            self.display.blit(self.singleTxt, self.singleTxtRect)

        if self.multiTxtRect.collidepoint(mouse):
            self.display.blit(self.multiTxtHover, self.multiTxtRect)
            if click:
                self.players.append(Player("Anonymous", main=True, movements=[pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]))
                state = "Multiple Options"
        else:
            self.display.blit(self.multiTxt, self.multiTxtRect)

        if self.quitTxtRect.collidepoint(mouse):
            self.display.blit(self.quitTxtHover, self.quitTxtRect)
            if click:
                state = "Quit"
        else:
            self.display.blit(self.quitTxt, self.quitTxtRect)
        
        self.screen.blit(self.display, (0, 0))
    
        return state
    
    def single_options(self, dt, state, events):
        self.display.fill((0, 0, 0))
        self.display.blit(self.singleTxt, (30, 20))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for player in self.players:
                        if len(player.movements) == 0:
                            break
                    else:
                        if len(self.players) > 1:
                            state = "Game"
                elif event.key == pygame.K_ESCAPE:
                    self.players = []
                    state = "Main Menu"
        
        x = 100
        for n in range(4):
            pygame.draw.rect(self.display, (255, 255, 255), (x, 150, 195, 350), border_radius=10)
            if len(self.players) - 1 >= n:
                self.playerTxt = constants.regFont.render(self.players[n].name, True, (0, 0, 0))
                self.playerTxtRect = self.playerTxt.get_rect()
                self.playerTxtRect.x, self.playerTxtRect.y = x + 20, 170
                self.playerTxtHover = constants.regFont.render(self.players[n].name, True, (107, 107, 107))

                if self.playerTxtRect.collidepoint(mouse):
                    self.display.blit(self.playerTxtHover, self.playerTxtRect)
                    if click:
                        state = f"Change Name, Single, {self.players[n].userId}"
                else:
                    self.display.blit(self.playerTxt, self.playerTxtRect)
    
                if len(self.players[n].movements) != 0:
                    self.upTxt = constants.regFont.render(f"Up: {pygame.key.name(self.players[n].movements[0])}", True, (0, 0, 0))
                    self.downTxt = constants.regFont.render(f"Down: {pygame.key.name(self.players[n].movements[2])}", True, (0, 0, 0))
                    self.leftTxt = constants.regFont.render(f"Left: {pygame.key.name(self.players[n].movements[1])}", True, (0, 0, 0))
                    self.rightTxt = constants.regFont.render(f"Right: {pygame.key.name(self.players[n].movements[3])}", True, (0, 0, 0))
                    self.spearTxt = constants.regFont.render(f"Spear: {pygame.key.name(self.players[n].movements[4])}", True, (0, 0, 0))
                    self.projectileTxt = constants.regFont.render(f"Projectile: {pygame.key.name(self.players[n].movements[5])}", True, (0, 0, 0))
                    self.display.blit(self.upTxt, (x + 30, 225))
                    self.display.blit(self.downTxt, (x + 30, 255))
                    self.display.blit(self.leftTxt, (x + 30, 285))
                    self.display.blit(self.rightTxt, (x + 30, 315))
                    self.display.blit(self.spearTxt, (x + 30, 345))
                    self.display.blit(self.projectileTxt, (x + 30, 375))

                self.changeKeys = constants.regFont.render("Change Keys", True, (0, 0, 0))
                self.changeKeysRect = self.changeKeys.get_rect()
                self.changeKeysRect.x, self.changeKeysRect.y = (x + 98) - self.changeKeys.get_width() / 2, (150 + 350) - self.changeKeys.get_height() - 20
                self.changeKeysHover = constants.regFont.render("Change Keys", True, (107, 107, 107))

                if self.changeKeysRect.collidepoint(mouse):
                    self.display.blit(self.changeKeysHover, self.changeKeysRect)
                    if click:
                        self.players[n].movements = []
                        state = f"Change Keys, Single, {self.players[n].userId}"
                else:
                    self.display.blit(self.changeKeys, self.changeKeysRect)

                if n > 1 and n + 1 == len(self.players):
                    if pygame.Rect(x + 195 - self.trash.get_width() - 15, 150 + 15, 32, 32).collidepoint(mouse):
                        self.display.blit(self.trashHover, (x + 195 - self.trash.get_width() - 15, 150 + 15))
                        if click:
                            self.players.remove(self.players[n])
                    else:
                        self.display.blit(self.trash, (x + 195 - self.trash.get_width() - 15, 150 + 15))
    
            else:
                if n == len(self.players):
                    self.createNew = constants.regFont.render("Create Player", True, (0, 0, 0))
                    self.createNewRect = self.createNew.get_rect()
                    self.createNewRect.x, self.createNewRect.y = (x + 98) - self.createNew.get_width() / 2, (150 + 175) - self.createNew.get_height() / 2
                    self.createNewHover = constants.regFont.render("Create Player", True, (107, 107, 107))

                    if self.createNewRect.collidepoint(mouse):
                        self.display.blit(self.createNewHover, self.createNewRect)
                        if click:
                            colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0)
                            self.players.append(Player(f"Player {n + 1}", main=True, colour=colour, movements=[]))
                    else:
                        self.display.blit(self.createNew, self.createNewRect)

            x += 200
        self.display.blit(self.continueTxt, (1000 - self.continueTxt.get_width() - 20, 600 - self.continueTxt.get_height() - 10))

        self.displayCopy = self.display.copy()
        self.screen.blit(self.display, (0, 0))

        return state

    def multiple_options(self, dt, state, events):
        self.display.fill((0, 0, 0))
        self.display.blit(self.multiTxt, (30, 20))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        x = 500 - 150 / 2
        pygame.draw.rect(self.display, (255, 255, 255), (x, 150, 195, 350), border_radius=10)

        self.playerTxt = constants.regFont.render(self.players[0].name, True, (0, 0, 0))
        self.playerTxtRect = self.playerTxt.get_rect()
        self.playerTxtRect.x, self.playerTxtRect.y = x + 20, 170
        self.playerTxtHover = constants.regFont.render(self.players[0].name, True, (107, 107, 107))

        if self.playerTxtRect.collidepoint(mouse):
            self.display.blit(self.playerTxtHover, self.playerTxtRect)
            if click:
                state = f"Change Name, Multiple, {self.players[0].userId}"
        else:
            self.display.blit(self.playerTxt, self.playerTxtRect)

        if len(self.players[0].movements) != 0:
            self.upTxt = constants.regFont.render(f"Up: {pygame.key.name(self.players[0].movements[0])}", True, (0, 0, 0))
            self.downTxt = constants.regFont.render(f"Down: {pygame.key.name(self.players[0].movements[2])}", True, (0, 0, 0))
            self.leftTxt = constants.regFont.render(f"Left: {pygame.key.name(self.players[0].movements[1])}", True, (0, 0, 0))
            self.rightTxt = constants.regFont.render(f"Right: {pygame.key.name(self.players[0].movements[3])}", True, (0, 0, 0))
            self.spearTxt = constants.regFont.render(f"Spear: {pygame.key.name(self.players[0].movements[4])}", True, (0, 0, 0))
            self.projectileTxt = constants.regFont.render(f"Projectile: {pygame.key.name(self.players[0].movements[5])}", True, (0, 0, 0))
            self.display.blit(self.upTxt, (x + 30, 225))
            self.display.blit(self.downTxt, (x + 30, 255))
            self.display.blit(self.leftTxt, (x + 30, 285))
            self.display.blit(self.rightTxt, (x + 30, 315))
            self.display.blit(self.spearTxt, (x + 30, 345))
            self.display.blit(self.projectileTxt, (x + 30, 375))

        self.changeKeys = constants.regFont.render("Change Keys", True, (0, 0, 0))
        self.changeKeysRect = self.changeKeys.get_rect()
        self.changeKeysRect.x, self.changeKeysRect.y = (x + 98) - self.changeKeys.get_width() / 2, (150 + 350) - self.changeKeys.get_height() - 20
        self.changeKeysHover = constants.regFont.render("Change Keys", True, (107, 107, 107))

        if self.changeKeysRect.collidepoint(mouse):
            self.display.blit(self.changeKeysHover, self.changeKeysRect)
            if click:
                self.players[0].movements = []
                state = f"Change Keys, Multiple, {self.players[0].userId}"
        else:
            self.display.blit(self.changeKeys, self.changeKeysRect)

        self.display.blit(self.continueTxt, (1000 - self.continueTxt.get_width() - 20, 600 - self.continueTxt.get_height() - 10))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for player in self.players:
                        if len(player.movements) == 0:
                            break
                    else:
                        self.players = [self.players[0]]
                        state = "Lobby"
                elif event.key == pygame.K_ESCAPE:
                    self.players = []
                    state = "Main Menu"

        self.displayCopy = self.display.copy()
        self.screen.blit(self.display, (0, 0))

        return state

    def change_name(self, dt, state, events):
        userId = state.split(", ")[-1]
        self.display.blit(self.displayCopy, (0, 0))
        self.display.blit(self.transparentBg, (0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.newName = []
                    if state.split(", ")[1] == "Single":
                        state = "Single Options"
                    elif state.split(", ")[1] == "Multiple":
                        state = "Multiple Options"
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.newName) != 0:
                        self.newName.pop()
                elif event.key == pygame.K_RETURN:
                    if len(self.newName) != 0:
                        for player in self.players:
                            if player.name == "".join(self.newName) and player.userId != userId:
                                break
                        else:
                            for player in self.players:
                                if str(player.userId) == str(userId):
                                    player.name = "".join(self.newName)
                                    player.nameTag = constants.smallFont.render(player.name, True, player.colour)
                                    self.newName = []
                                    if state.split(", ")[1] == "Single":
                                        state = "Single Options"
                                    elif state.split(", ")[1] == "Multiple":
                                        state = "Multiple Options"

                else:
                    if len(pygame.key.name(event.key)) == 1 and len(self.newName) < 10:
                        self.newName.append(pygame.key.name(event.key))

        directionsTxt = constants.medfont.render("Enter Your Preffered Username", True, (0, 0, 0))
        nameTxt = constants.regFont.render(f"Username: {''.join(self.newName)}", True, (0, 0, 0))
        self.display.blit(directionsTxt, (500 - directionsTxt.get_width() / 2, 200))
        self.display.blit(nameTxt, (500 - nameTxt.get_width() / 2, 250))

        self.screen.blit(self.display, (0, 0))

        return state

    def change_keys(self, dt, state, events):
        userId = state.split(", ")[-1]
        registeredKeys = []
        for player in self.players:
            for key in player.movements:
                registeredKeys.append(key)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key not in registeredKeys and event.key != pygame.K_ESCAPE:
                    for player in self.players:
                        if str(player.userId) == str(userId):
                            player.movements.append(event.key)
                            if len(player.movements) == 6:
                                if state.split(", ")[1] == "Single":
                                    state = "Single Options"
                                elif state.split(", ")[1] == "Multiple":
                                    state = "Multiple Options"
                if event.key == pygame.K_ESCAPE:
                    if state.split(", ")[1] == "Single":
                        for player in self.players:
                            if str(player.userId) == str(userId):
                                player.movements = []
                        state = "Single Options"
                    elif state.split(", ")[1] == "Multiple":
                        self.players[0].movements = []
                        state = "Multiple Options"

        keysTxt = constants.medfont.render("Enter Your Keys In The Order Of Up, Down, Left, Right...", True, (0, 0, 0))
        noteTxt = constants.regFont.render("(Keys that are already registered won't work)", True, (0, 0, 0))
        self.display.blit(self.displayCopy, (0, 0))
        self.display.blit(self.transparentBg, (0, 0))

        self.display.blit(keysTxt, (500 - keysTxt.get_width() / 2, 200))
        self.display.blit(noteTxt, (500 - noteTxt.get_width() / 2, 300))

        self.screen.blit(self.display, (0, 0))

        return state

    def lobby(self, dt, state, events):
        self.client.connect(self.players[0])

        self.display.fill((0, 0, 0))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "Multiple Options"
                    self.client.disconnect()                    
                if event.key == pygame.K_RETURN:
                    if not self.client.ready:
                        self.client.ready = True
        else:
            if self.client.connected:
                if self.client.ready:
                    self.client.send(json.dumps({"disconnect": False, "ready": True}))
                else:
                    self.client.send(json.dumps({"disconnect": False, "ready": False}))

        data = ""
        if self.client.connected:
            data = self.client.receive()
            data = json.loads(data)
            
            if data["started"]:
                for key, value in data["players"].items():
                    if key != str(self.players[0].userId):
                        player = Player(value["name"], colour=value["colour"])
                        self.players.append(player)
                        player.userId = key

                state = "Multiplayer Game"

        if state == "Lobby":
            waitingTxt = constants.medfont.render(f"Waiting for Players...", True, (255, 255, 255))
            playersTxt = constants.regFont.render(f'Players Ready: {data["connections"]}/{data["players"]}', True, (255, 255, 255))
            enterTxt = constants.regFont.render(f"Press Enter if You're Ready", True, (255, 255, 255))
            
            self.display.blit(waitingTxt, (500 - waitingTxt.get_width() / 2, 300 - waitingTxt.get_height() / 2))
            self.display.blit(playersTxt, (500 - playersTxt.get_width() / 2, (300 + waitingTxt.get_height() / 2) + 20))
            self.display.blit(enterTxt, (1000 - enterTxt.get_width() - 10, 600 - enterTxt.get_height() - 10))
            self.screen.blit(self.display, (0, 0))

        return state

    def run(self, dt, state, events):
        renderOffset = (0, 0)
        if self.screenshake > 0:
            self.screenshake -= 1
            renderOffset = (random.randint(-8, 8), random.randint(-8, 8))
        
        self.display.fill(constants.COLOURS["black"])
        self.display.blit(self.background, (0, 0))
        self.gameUI()

        self.map.draw(self.display)
        keys = pygame.key.get_pressed()
        for player in self.players:
            player.draw(self.display)
            self.projectiles = player.checkInput(events, keys, self.map.tiles, self.projectiles)
            if player.fell():
                self.screenshake = 45

            self.projectiles = player.hit(self.projectiles)

        for projectile in self.projectiles:
            projectile[1].draw(self.display)
            projectile[1].move()
            if projectile[1].boundary():
                self.projectiles.remove(projectile)

        for event in events:
            pass

        self.screen.blit(self.display, renderOffset)
        
        return state

    def multiplayerRun(self, dt, state, events):
        renderOffset = (0, 0)
        if self.screenshake > 0:
            self.screenshake -= 1
            renderOffset = (random.randint(-8, 8), random.randint(-8, 8))
        
        self.display.fill(constants.COLOURS["black"])
        self.display.blit(self.background, (0, 0))
        self.gameUI()

        self.client.send(json.dumps({"disconnect": False, "coords": [self.players[0].player_rect.x, self.players[0].player_rect.y], "direction": self.players[0].direction, "state": self.players[0].state, "frame": self.players[0].frame}))
        msg = self.client.receive()
        msg = json.loads(msg)
        for key, value in msg["players"].items():
            for player in self.players[1:]:
                if key == str(player.userId):
                    player.direction = value["direction"]
                    player.state = value["state"]
                    player.frame = value["frame"]
                    player.player_rect.x, player.player_rect.y = value["coords"][0], value["coords"][1]

        self.map.draw(self.display)
        keys = pygame.key.get_pressed()
        for player in reversed(self.players):
            if player.movements is not None:
                self.projectiles = player.checkInput(events, keys, self.map.tiles, self.projectiles)
                if player.fell():
                    self.screenshake = 45
            player.draw(self.display)

        for event in events:
            pass

        self.screen.blit(self.display, renderOffset)

        return state

    def gameUI(self):
        for n, player in enumerate(self.players):
            name = constants.regFont.render(player.name, True, player.colour)
            lives = constants.smallFont.render("Lives: " + str(player.lives), True, (0, 0, 0))
            health = constants.smallFont.render("Health: " + str(player.health), True, (0, 0, 0))
            x, y = self.gameUICoords[len(self.players) - 1][n]
            pygame.draw.rect(self.display, (255, 255, 255), (x, y, 150, 100), border_radius=10)
            self.display.blit(name, (x + 10, y + 10))
            self.display.blit(lives, (x + 20, y + 10 + name.get_height() + 10))
            self.display.blit(health, (x + 20, y + 20 + name.get_height() + lives.get_height() + 10))
