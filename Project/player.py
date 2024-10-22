import pygame
import random
import os
import Project.helpers as helpers
from Project.math import Vector
from Project.weapon import Projectile
import Project.constants as constants
from uuid import uuid4

class Player:
    size = 55

    def __init__(self, name, colour=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 0), main=False, movements=None):
        self.userId = uuid4()
        self.name = name
        self.main = main
        self.colour = colour

        self.playerImages = {"right": {"idle": [], "running": [], "jumping": [], "falling": []}, "left": {"idle": [], "running": [], "jumping": [], "falling": []}}
        self.getImages("Assets\\Player", self.colour, 55)
        self.direction = "right"
        self.state = "idle"
        self.player = self.playerImages["right"]["idle"][0]
        self.player_rect = self.player.get_rect()
        if self.main:
            self.player_rect.x = random.randint(200, 800)
            self.player_rect.y = -1000
        self.mask = pygame.mask.from_surface(self.player)

        self.arrow = pygame.image.load("Assets\\arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (32, 32))
        self.movements = movements
        self.lives = 5
        self.health = 1000
        self.damage = 20
        self.damageDealt = 0
        self.nameTag = constants.smallFont.render(self.name, True, self.colour)
        self.nameTagRect = self.nameTag.get_rect()
        helpers.fill(self.arrow, self.colour)
        self.location = Vector(self.player_rect.x, self.player_rect.y)
        self.animationTimer = 3
        self.frame = 0
        self.projectileCooldown = 30

        if self.main:
            self.xVel, self.yVel = 0, 0
            self.maxSpeed = 2
            self.terminalVel = 7
            self.decceleration = 0.2
            self.peakJump = 0.1
            self.gravity = 0.5
            self.jumpForce = 9.5
            self.jumping = False
            self.moveDown = False
            self.canLand = False
            self.inAir = True
            self.landed = False

    def getImages(self, folder, colour, size):
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            if os.path.isdir(f):
                self.getImages(f, colour, size)
            elif os.path.isfile(f):
                image = pygame.image.load(f).convert_alpha()
                image = pygame.transform.scale(image, (size, size))
                image = helpers.setPlayerColour(image, colour)
                if f.split("\\")[-3] == "Left":
                    if f.split("\\")[-2] == "Idle":
                        self.playerImages["left"]["idle"].append(image)
                    elif f.split("\\")[-2] == "Running":
                        self.playerImages["left"]["running"].append(image)
                    elif f.split("\\")[-2] == "Jumping":
                        self.playerImages["left"]["jumping"].append(image)
                    elif f.split("\\")[-2] == "Falling":
                        self.playerImages["left"]["falling"].append(image)
                elif f.split("\\")[-3] == "Right":
                    if f.split("\\")[-2] == "Idle":
                        self.playerImages["right"]["idle"].append(image)
                    elif f.split("\\")[-2] == "Running":
                        self.playerImages["right"]["running"].append(image)
                    elif f.split("\\")[-2] == "Jumping":
                        self.playerImages["right"]["jumping"].append(image)
                    elif f.split("\\")[-2] == "Falling":
                        self.playerImages["right"]["falling"].append(image)
    
    def draw(self, display):
        if self.main:
            if self.player in self.playerImages[self.direction][self.state]:
                if self.animationTimer > 0:
                    self.animationTimer -= 1
                else:
                    if self.frame < len(self.playerImages[self.direction][self.state]) - 1:
                        self.frame += 1
                        self.animationTimer = 3
                    else:
                        if self.state == "running":
                            self.frame = 0
            else:
                self.animationTimer = 3
                self.frame = 0
        
        self.player = self.playerImages[self.direction][self.state][self.frame]

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

        if self.yVel > 0:
            self.state = "falling"
        elif self.yVel < 0 or self.jumping:
            self.state = "jumping"

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
                    self.player_rect.bottom = pygame.Rect(tile[1], tile[2], 32, 5).top
                    self.jumping = False
                    self.inAir = False
                    self.landed = True

        self.location = Vector(self.player_rect.x, self.player_rect.y)

    def checkInput(self, events, keys, tiles, projectiles):
        if self.projectileCooldown > 0:
            self.projectileCooldown -= 1
        
        self.state = "running"
        if keys[self.movements[3]]:
            self.direction = "right"
            if self.xVel < self.maxSpeed:
                self.xVel += 1
        elif keys[self.movements[1]]:
            self.direction = "left"
            if self.xVel > -self.maxSpeed:
                self.xVel -= 1
        else:
            self.state = "idle"
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
                elif event.key == self.movements[4] and self.projectileCooldown <= 0:
                    projectiles.append((self.userId, Projectile(self.direction, (self.player_rect.x + self.size / 2, self.player_rect.y + 10), self.colour)))
                    self.projectileCooldown = 30

        self.move(tiles)
        return projectiles

    def collisions(self, tiles):
        collisions = []
        for tile in tiles:
            mask = pygame.mask.Mask((16, 5))
            mask.fill()
            offset = (tile[1] - self.player_rect.x, tile[2] - self.player_rect.y)
            if self.mask.overlap(mask, offset):
                collisions.append(tile)
        return collisions

    def hit(self, projectiles):
        for projectile in projectiles:
            if projectile[0] != self.userId:
                mask = pygame.mask.Mask((projectile[1].size, projectile[1].size))
                mask.fill()
                offset = (projectile[1].projectile.x - self.player_rect.x, projectile[1].projectile.y - self.player_rect.y)
                if self.mask.overlap(mask, offset):
                    self.health -= random.randint(50, 100)
                    moveBy = 10
                    if projectile[1].direction == "left":
                        moveBy *= -1
                        
                    self.xVel += moveBy
                    projectiles.remove(projectile)

        return projectiles

    def dead(self):
        if self.player_rect.y >= 800 or self.health <= 0:
            self.respawn()
            return True
        return False

    def respawn(self):
        if self.lives >= 1:
            self.lives -= 1
        self.health = 1000
        self.player_rect.x = random.randint(200, 800)
        self.player_rect.y = -500

    def info(self):
        print(f"Id: {self.userId}\nMain: {self.main}\nPosition:({self.player_rect.x}, {self.player_rect.y})")
