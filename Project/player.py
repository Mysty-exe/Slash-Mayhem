import pygame
import random
import Project.helpers as helpers
from Project.math import Vector
import Project.constants as constants
from uuid import uuid4

class Player:
    def __init__(self, name, image, colour=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0), main=False, movements=None):
        self.userId = uuid4()
        self.name = name
        self.image = image
        self.main = main
        self.size = 48

        self.player = pygame.image.load(self.image).convert_alpha()
        self.player = pygame.transform.scale(self.player, (self.size, self.size))
        self.player_rect = self.player.get_rect()
        if self.main:
            self.player_rect.x = random.randint(200, 800)
            self.player_rect.y = -1000

        self.arrow = pygame.image.load("Assets\\arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (32, 32))
        self.movements = movements
        self.lives = 5
        self.health = 1000
        self.damage = 20
        self.damageDealt = 0
        self.colour = colour
        self.nameTag = constants.smallFont.render(self.name, True, self.colour)
        self.nameTagRect = self.nameTag.get_rect()
        helpers.fill(self.arrow, self.colour)
        self.location = Vector(self.player_rect.x, self.player_rect.y)

        if self.main:
            self.xVel, self.yVel = 0, 0
            self.maxSpeed = 2
            self.terminalVel = 7
            self.decceleration = 0.3
            self.peakJump = 0.1
            self.gravity = 0.5
            self.jumpForce = 9.5
            self.jumping = False
            self.moveDown = False
            self.canLand = False
            self.inAir = True
            self.landed = False

    def draw(self, display):
        self.nameTagRect.x, self.nameTagRect.y = (self.player_rect.x + (self.size / 2)) - self.nameTag.get_width() / 2, self.player_rect.y - 10
        display.blit(self.player, self.player_rect)
        display.blit(self.nameTag, self.nameTagRect)
        if self.player_rect.y + self.size < 0:
            display.blit(self.arrow, (self.player_rect.x + (self.size / 2) - self.arrow.get_width() / 2, 10))

    def move(self, tiles):
        x = self.player_rect.x
        self.player_rect.x += self.xVel
        
        if self.yVel > -0.3 and self.yVel < 0.3 and self.jumping:
            force = self.peakJump
        else:
            force = self.gravity
        
        self.yVel += force
        
        if self.yVel > self.terminalVel or self.moveDown:
            self.yVel = self.terminalVel

        if self.landed:
            self.yVel = 0

        self.player_rect.y += self.yVel

        if len(self.collisions(tiles)) == 0:
            self.moveDown = False
            if not self.jumping:
                self.yVel = self.terminalVel

        if self.xVel != 0 and self.landed:
            self.player_rect.y += self.terminalVel
            if len(self.collisions(tiles)) == 0:
                self.landed = False
            else:
                self.landed = True

        for tile in self.collisions(tiles):
            if self.yVel > 0 and tile[2] >= (self.player_rect.y - self.yVel) + self.size:
                if not self.moveDown:
                    self.player_rect.bottom = pygame.Rect(tile[1], tile[2], 32, 16).top
                    self.jumping = False
                    self.inAir = False
                    self.landed = True

        self.location = Vector(self.player_rect.x, self.player_rect.y)

    def checkInput(self, events, keys, tiles):
        if keys[self.movements[3]]:
            self.xVel = self.maxSpeed
        elif keys[self.movements[1]]:
            self.xVel = -self.maxSpeed
        else:
            if self.xVel > 0:
                self.xVel -= self.decceleration
                if self.xVel < 0:
                    self.xVel = 0
            else:
                self.xVel += self.decceleration
                if self.xVel > 0:
                    self.xVel = 0

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.movements[0] and self.landed:
                    self.yVel = -self.jumpForce
                    self.jumping = True
                    self.inAir = True
                    self.VertInput = True
                    self.landed = False
                elif event.key == self.movements[2]:
                    if self.landed:
                        if tiles[-1][2] != self.player_rect.y + self.size:
                            self.moveDown = True
                            self.VertInput = True
                            self.inAir = True
                            self.landed = False

        self.move(tiles)

    def collisions(self, tiles):
        collisions = []
        for tile in tiles:
            if pygame.Rect(tile[1], tile[2], 32, 16).colliderect(self.player_rect):
                collisions.append(tile)
        return collisions

    def fell(self):
        if self.player_rect.y >= 800:
            self.respawn()
            return True
        return False

    def respawn(self):
        self.lives -= 1
        self.health = 1000
        self.player_rect.x = random.randint(200, 800)
        self.player_rect.y = -500

    def info(self):
        print(f"Id: {self.userId}\nMain: {self.main}\nPosition:({self.player_rect.x}, {self.player_rect.y})")
