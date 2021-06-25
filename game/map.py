import pygame, pytmx

tframecount = {"stone": 1, "rail": 1}
tframes = {}
cframecount = {"miner": 1}
cframes = {}

for i in tframecount.keys():
    f = []
    img = pygame.image.load("./resources/images/tiles/" + str(i) + ".png")
    f.append(img)
    if tframecount[str(i)] > 1:
        for j in range(tframecount[str(i)] - 1):
            img = pygame.image.load("./resources/images/tiles/" + str(i) + str(j) + ".png")
            f.append(img)
    tframes[str(i)] = f

for i in cframecount.keys():
    f = []
    img = pygame.image.load("./resources/images/carts/" + str(i) + ".png")
    f.append(img)
    if cframecount[str(i)] > 1:
        for j in range(cframecount[str(i)] - 1):
            img = pygame.image.load("./resources/images/carts/" + str(i) + str(j) + ".png")
            f.append(img)
    cframes[str(i)] = f

def loadmap(level):
    tiles = pygame.sprite.Group()
    rails = pygame.sprite.Group()
    mapdata = pytmx.TiledMap("./resources/map/" + str(level) + ".tmx")
    listmap = []
    for x in range(20):
        listmap.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for y in range(15):
            data = mapdata.get_tile_properties(x, y, 0)
            if not data == None:
                print(x, y, data)
                tile = Tile([x, y], data["type"])
                tiles.add(tile)
                if tile.type.startswith("rail"):
                    rails.add(tile)
                    listmap[x][y] = 1
    # for i in listmap:
    #    print(i)
    return tiles, rails, listmap


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
            oc = self.rect.center
            self.image = self.frames[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = oc


class Cart(pygame.sprite.Sprite):
    def __init__(self, gamepos, type):
        global cframes
        pygame.sprite.Sprite.__init__(self)
        self.type = str(type)
        self.image = cframes[str(type)][0]
        self.pos = list(gamepos)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[0] * 40, self.pos[1] * 40
        self.data = {"storage": 0, "max": 10}
        self.animated = bool(cframecount[str(self.type)] > 1)
        self.frame = 0
        self.moving = False
        self.path = []
        self.target = self.rect.center
        if self.animated:
            self.frames = cframes[self.type]

    def pathfind(self, listmap, position):
        if not self.moving:
            queue = []
            visited = {}
            if listmap[position[0]][position[1]] == 1:
                queue.append([self.pos, None])
            i = None
            j = None
            k = 0
            stop = False
            while len(queue) > 0 and not stop:
                i = queue[0][0]
                j = queue[0][1]
                queue.pop(0)
                if listmap[i[0]][i[1]] == 1 and not str(i) in visited:
                    visited[str(i)] = j
                    if i == position:
                        stop = True
                    else:
                        if i[1] + 1 < 15:
                            queue.append([[i[0], i[1] + 1], i])
                        if i[1] - 1 > -1:
                            queue.append([[i[0], i[1] - 1], i])
                        if i[0] + 1 < 20:
                            queue.append([[i[0] + 1, i[1]], i])
                        if i[0] - 1 > -1:
                            queue.append([[i[0] - 1, i[1]], i])
                k += 1
                if k > 10000:
                    break
            retraced = []
            i = position
            if stop and not position == self.pos:
                while str(i) in visited and visited[str(i)] != None:
                    if i != None:
                        retraced.append(i)
                    i = visited[str(i)]
                retraced.reverse()
                self.path = retraced
                self.moving = True
                self.target = (20 + self.path[0][0] * 40, 20 + self.path[0][1] * 40)

    def update(self, action, mouse):
        if action == "update":
            if self.animated:
                if self.frame + 1 >= self.frames:
                    self.frame = 0
                else:
                    self.frame += 1
                oc = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = oc
            if self.moving:
                if self.target[0] < self.rect.centerx:
                    self.rect.centerx -= 1
                elif self.target[0] > self.rect.centerx:
                    self.rect.centerx += 1
                elif self.target[1] < self.rect.centery:
                    self.rect.centery -= 1
                elif self.target[1] > self.rect.centery:
                    self.rect.centery += 1
                elif self.target == self.rect.center:
                    self.pos = self.path[0]
                    self.path.pop(0)
                    if len(self.path) > 0:
                        self.target = (20 + self.path[0][0] * 40, 20 + self.path[0][1] * 40)
                    else:
                        self.moving = False
        if action == "select":
            if self.rect.collidepoint(mouse.tl):
                mouse.clickedcart = self
                print("in")
