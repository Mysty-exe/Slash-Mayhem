import pygame
from Project.math import Vector

class Player:
    def __init__(self, image, movements):
        self.image = image
        self.size = 48

        self.player = pygame.image.load(self.image).convert_alpha()
        self.player = pygame.transform.scale(self.player, (self.size, self.size))
        self.player_rect = self.player.get_rect()
        
        self.movements = movements

        self.location = Vector(self.player_rect.x, self.player_rect.y)
        self.xVel, self.yVel = 0, 0
        self.maxSpeed = 2
        self.terminalVel = 6
        self.decceleration = 0.3
        self.peakJump = 0.1
        self.gravity = 0.5
        self.jumpForce = 9.5
        self.jumping = False
        self.moveDown = False
        self.canLand = False
        self.inAir = True

    def draw(self, display):
        print(self.canLand)
        display.blit(self.player, self.player_rect)

    def move(self, tiles):

        self.player_rect.x += self.xVel

        if self.yVel > -0.3 and self.yVel < 0.3:
            force = self.peakJump
        else:
            force = self.gravity
        
        self.yVel += force
        if self.yVel > self.terminalVel:
            self.yVel = self.terminalVel

        self.player_rect.y += self.yVel

        if len(self.collisions(tiles)) == 0:
            self.moveDown = False
            self.inAir = True

        for tile in self.collisions(tiles):
            if self.canLand:
                if self.yVel > 0:
                    if not self.moveDown:
                        self.player_rect.bottom = pygame.Rect(tile[1], tile[2], 32, 16).top
                        self.jumping = False
                        self.inAir = False
            else:
                if tile[2] > (self.player_rect.y - self.yVel) + self.size:
                    self.canLand = True
                    
        self.location = Vector(self.player_rect.x, self.player_rect.y)

    def checkInput(self, events, keys, tiles):
        self.horizInput = True
        if keys[self.movements[3]]:
            self.xVel = self.maxSpeed
        elif keys[self.movements[1]]:
            self.xVel = -self.maxSpeed
        else:
            self.horizInput = False
            if self.xVel > 0:
                self.xVel -= self.decceleration
                if self.xVel < 0:
                    self.xVel = 0
            else:
                self.xVel += self.decceleration
                if self.xVel > 0:
                    self.xVel = 0

        self.VertInput = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.movements[0] and not self.jumping and not self.inAir:
                    self.yVel = -self.jumpForce
                    self.jumping = True
                    self.inAir = True
                    self.VertInput = True
                elif event.key == self.movements[2]:
                    if tiles[-1][2] != self.player_rect.y + self.size:
                        self.moveDown = True
                        self.VertInput = True
                        self.inAir = True

        self.move(tiles)

    def collisions(self, tiles):
        collisions = []
        for tile in tiles:
            if pygame.Rect(tile[1], tile[2], 32, 16).colliderect(self.player_rect):
                collisions.append(tile)
        return collisions
