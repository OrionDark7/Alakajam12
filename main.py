import pygame, math
from game import map

window = pygame.display.set_mode([800, 600])
screen = "game"
s = {"fullscreen": False}
running = True
gamedata = {"level": 0, "coal": 0, "iron": 1}
tiles = pygame.sprite.Group()
rails = pygame.sprite.Group()
carts = pygame.sprite.Group()
listmap = []


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.clickedcart = None
        self.tl = self.rect.topleft
        self.mode = "select"

    def pos(self, position):
        self.rect.topleft = position
        self.tl = self.rect.topleft


m = Mouse()


def snaptogrid(pos):
    return [int(math.floor(pos[0] / 40)), int(math.floor(pos[1] / 40))]


def loadlevel(number):
    global tiles, rails, carts, gamedata, listmap
    tiles, rails, listmap = map.loadmap(int(number))
    carts.empty()
    gamedata["level"] = number
    gamedata["coal"] = 0
    gamedata["iron"] = 1


loadlevel(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            m.pos(pygame.mouse.get_pos())
            if screen == "game":
                if pygame.sprite.spritecollide(m, carts, False) and m.mode == "select":
                    carts.update("select", m)
                    if m.clickedcart != None:
                        m.mode = "action"
                elif m.mode == "action" and m.clickedcart != None and pygame.sprite.spritecollide(m, rails, False):
                    m.clickedcart.pathfind(listmap, snaptogrid(m.tl))
                    m.clickedcart = None
                    m.mode = "select"
                print(m.mode, m.clickedcart, pygame.sprite.spritecollide(m, rails, False))
        elif event.type == pygame.MOUSEMOTION:
            m.pos(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                carts.add(map.Cart(snaptogrid(m.tl), "miner"))
    if screen == "game":
        window.fill([128, 128, 128])
        tiles.draw(window)
        carts.draw(window)
        carts.update("update", m)
    pygame.display.flip()
pygame.quit()
