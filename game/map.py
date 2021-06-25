import pygame, pytmx

tframecount = {"stone": 1}
tframes = {}

for i in tframecount.keys():
    f = []
    img = pygame.image.load("./resources/images/tiles/" + str(i) + ".png")
    f.append(img)
    if tframecount[str(i)] > 1:
        for j in range(tframecount[str(i)] - 1):
            img = pygame.image.load("./resources/images/tiles/" + str(i) + str(j) + ".png")
            f.append(img)
    tframes[str(i)] = f


def loadmap(level):
    tiles = pygame.sprite.Group()
    rails = pygame.sprite.Group()
    mapdata = pytmx.TiledMap("./resources/map/" + str(level) + ".tmx")
    for x in range(20):
        for y in range(15):
            data = mapdata.get_tile_properties(x, y, 0)
            if not data == None:
                print(x, y, data)
                tile = Tile([x, y], data["type"])
                tiles.add(tile)
                if tile.type.startswith("rail"):
                    rails.add(tile)
    print(tiles)
    return tiles, rails


class Tile(pygame.sprite.Sprite):
    def __init__(self, gamepos, type):
        global tframes
        pygame.sprite.Sprite.__init__(self)
        self.type = str(type)
        self.image = tframes[str(type)][0]
        self.pos = list(gamepos)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[0] * 40, self.pos[1] * 40
        self.data = {"storage": 0, "max": 10}
        self.animated = bool(tframecount[str(self.type)] > 1)
        self.frame = 0
        if self.animated:
            self.frames = tframes[self.type]

    def update(self):
        if self.animated:
            if self.frame + 1 >= self.frames:
                self.frame = 0
            else:
                self.frame += 1
            self.image = self.frames[self.frame]


class Cart(pygame.sprite.Sprite):
    def __init__(self, gamepos, type):
        pygame.sprite.Sprite.__init__(self)
        self.pos = list(gamepos)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[0] * 40, self.pos[1] * 40
