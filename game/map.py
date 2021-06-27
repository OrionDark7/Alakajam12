import pygame, pytmx

tframecount = {"stone": 1, "rail": 1, "railh" : 1, "mine":1, "railx":1, "coalcontainer":4, "ironcontainer":4, "coppercontainer":4}
tframes = {}
cframecount = {"miner": 2}
cframes = {}

hovers = ["miner", "mine", "coalcontainer", "ironcontainer", "coppercontainer"]

for i in tframecount.keys():
    f = []
    img = pygame.image.load("./resources/images/tiles/" + str(i) + ".png")
    f.append(img)
    if tframecount[str(i)] > 1:
        for j in range(tframecount[str(i)] - 1):
            print("./resources/images/tiles/" + str(i) + str(j) + ".png")
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
    global hovers
    tiles = pygame.sprite.Group()
    rails = pygame.sprite.Group()
    hover = pygame.sprite.Group()
    mapdata = pytmx.TiledMap("./resources/map/" + str(level) + ".tmx")
    listmap = []
    for x in range(20):
        listmap.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        for y in range(15):
            data = mapdata.get_tile_properties(x, y, 0)
            if not data == None:
                tile = Tile([x, y], data["type"])
                tiles.add(tile)
                if tile.type.startswith("rail"):
                    rails.add(tile)
                    listmap[x][y] = 1
                if tile.type in hovers:
                    hover.add(tile)
                    listmap[x][y] = 2
    # for i in listmap:
    #    print(i)
    return tiles, rails, hover, listmap


class Tile(pygame.sprite.Sprite):
    def __init__(self, gamepos, type):
        global tframes
        pygame.sprite.Sprite.__init__(self)
        self.type = str(type)
        self.image = tframes[str(type)][0]
        self.pos = list(gamepos)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos[0] * 40, self.pos[1] * 40
        self.data = {"storage": 0, "max": 10, "carts":0}
        self.animated = bool(tframecount[str(self.type)] > 1)
        self.frame = 0
        if self.animated:
            self.frames = tframes[self.type]
    def update(self):
        if self.animated:
            if self.type.endswith("container"):
                pass
            else:
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
        self.frames = cframes[self.type]
    def pathfind(self, listmap, position, interactables, mouse):
        if not self.moving:
            queue = []
            visited = {}
            if listmap[position[0]][position[1]] > 0:
                queue.append([self.pos, None])
            i = None
            j = None
            k = 0
            stop = False
            while len(queue) > 0 and not stop:
                i = queue[0][0]
                j = queue[0][1]
                queue.pop(0)
                if bool(listmap[i[0]][i[1]] == 1 or [i[0], i[1]] == position) and not str(i) in visited:
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
                if listmap[position[0]][position[1]] == 2:
                    retraced.pop(0)
                retraced.reverse()
                if len(retraced) > 0:
                    self.path = retraced
                    self.moving = True
                    self.target = (20 + self.path[0][0] * 40, 20 + self.path[0][1] * 40)
                if pygame.sprite.spritecollide(mouse, interactables, False):
                    type = pygame.sprite.spritecollide(mouse, interactables, False)[0]

    def update(self, action, mouse, listmap):
        if action == "update":
            oc = self.rect.center
            if self.moving:
                if self.target[0] < self.rect.centerx:
                    self.image = self.frames[1]
                    self.rect = self.image.get_rect()
                    self.rect.center = oc
                    self.rect.centerx -= 4
                elif self.target[0] > self.rect.centerx:
                    self.image = self.frames[1]
                    self.rect = self.image.get_rect()
                    self.rect.center = oc
                    self.rect.centerx += 4
                elif self.target[1] < self.rect.centery:
                    self.image = self.frames[0]
                    self.rect = self.image.get_rect()
                    self.rect.center = oc
                    self.rect.centery -= 4
                elif self.target[1] > self.rect.centery:
                    self.image = self.frames[0]
                    self.rect = self.image.get_rect()
                    self.rect.center = oc
                    self.rect.centery += 4
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
