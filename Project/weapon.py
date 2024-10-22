import pygame

class Weapon:
    pass

class Projectile(Weapon):
    size = 10
    def __init__(self, direction, coords, colour):
        self.direction = direction
        self.projectile = pygame.Rect(coords[0], coords[1], Projectile.size, Projectile.size)
        self.colour = colour
        self.maxSpeed = 50
        self.acceleration = 1
        if self.direction == "left":
            self.acceleration *= -1
        self.velocity = 0

    def draw(self, display):
        pygame.draw.rect(display, self.colour, self.projectile)

    def move(self):
        self.projectile.x += self.velocity
        
        if self.velocity < self.maxSpeed:
            self.velocity += self.acceleration
        else:
            self.velocity = self.maxSpeed

    def boundary(self):
        if self.projectile.x < -100 or self.projectile.x > 1100:
            return True
        return False
