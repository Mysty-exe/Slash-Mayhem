import pygame

class Map:
    def __init__(self, mapFile):
        self.mapFile = mapFile
        self.tiles = self.load_map()
        self.middleTile = pygame.image.load("Assets\\Tiles\\middleplatform.png")
        self.leftTile = pygame.image.load("Assets\\Tiles\\leftplatform.png")
        self.rightTile = pygame.image.load("Assets\\Tiles\\rightplatform.png")
        self.tileWidth = self.middleTile.get_width()
        self.tileHeight = self.middleTile.get_height()

    def load_map(self):
        tiles = []

        with open(self.mapFile, 'r') as f:
            rows = f.readlines()
            x, y = 0, 0
            for row in rows:
                for tile in row:
                    if tile == "1" or tile == "2" or tile == "3":
                        tiles.append((tile, x, y))
                    x += 16
                y += 40
                x = 0
            f.close()

        return tiles

    def draw(self, display):
        for tile in self.tiles:
            if tile[0] == "1":
                display.blit(self.middleTile, (tile[1], tile[2]))
            if tile[0] == "2":
                display.blit(self.leftTile, (tile[1], tile[2]))
            if tile[0] == "3":
                display.blit(self.rightTile, (tile[1], tile[2]))
