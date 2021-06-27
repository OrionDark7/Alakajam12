import pygame, math
from game import map, ui

window = pygame.display.set_mode([800, 600])
ui.window = window
screen = "game"
s = {"fullscreen": False}
running = True
gamedata = {"level": 0, "coal": 0, "iron": 1, "copper":0}
tiles = pygame.sprite.Group()
rails = pygame.sprite.Group()
carts = pygame.sprite.Group()
interactables = pygame.sprite.Group()
listmap = []
clock = pygame.time.Clock()
selected = pygame.image.load("./resources/images/selected.png")
selected2 = pygame.image.load("./resources/images/selected2.png")
box = pygame.image.load("./resources/images/box.png")
uibox = pygame.image.load("./resources/images/ui box.png")

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([1, 1])
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]
        self.clickedcart = None
        self.hoveritem = None
        self.tl = self.rect.topleft
        self.mode = "select"

    def pos(self, position):
        self.rect.topleft = position
        self.tl = self.rect.topleft


m = Mouse()


def snaptogrid(pos):
    return [int(math.floor(pos[0] / 40)), int(math.floor(pos[1] / 40))]


def loadlevel(number):
    global tiles, rails, carts, gamedata, listmap, interactables
    tiles, rails, interactables, listmap = map.loadmap(int(number))
    carts.empty()
    gamedata["level"] = number
    gamedata["coal"] = 0
    gamedata["iron"] = 1
    gamedata["copper"] = 0

loadlevel(0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            m.pos(pygame.mouse.get_pos())
            if screen == "game":
                if pygame.sprite.spritecollide(m, carts, False) and m.mode == "select":
                    carts.update("select", m, listmap)
                    if m.clickedcart != None:
                        m.mode = "action"
                elif m.mode == "action" and m.clickedcart != None and listmap[snaptogrid(m.tl)[0]][snaptogrid(m.tl)[1]] > 0:
                    m.clickedcart.pathfind(listmap, snaptogrid(m.tl))
                    m.clickedcart = None
                    m.mode = "select"
        elif event.type == pygame.MOUSEMOTION:
            m.pos(pygame.mouse.get_pos())
            if screen == "game":
                m.hoveritem = None
                if len(pygame.sprite.spritecollide(m, carts, False)) > 0:
                    m.hoveritem = pygame.sprite.spritecollide(m, carts, False)[0]
                elif len(pygame.sprite.spritecollide(m, interactables, False)) > 0:
                    m.hoveritem = pygame.sprite.spritecollide(m, interactables, False)[0]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                carts.add(map.Cart(snaptogrid(m.tl), "miner"))
    if screen == "game":
        window.fill([100, 100, 100])
        tiles.draw(window)
        carts.draw(window)
        carts.update("update", m, listmap)
        if not m.hoveritem == None and not m.mode == "action":
            window.blit(box, [m.rect.left+10, m.rect.top+10])
            ui.Resize(30)
            ui.Text(m.hoveritem.type.upper(), [m.rect.left+27, m.rect.top+25])
            if m.hoveritem.type.startswith("mine") and m.hoveritem not in carts:
                ui.Resize(18)
                ui.Text("Carts Inside: " + str(m.hoveritem.data["carts"]), [m.rect.left+27, m.rect.top+47])
                ui.Text("Max Carts: " + str(m.hoveritem.data["max"]), [m.rect.left+27, m.rect.top+60])
        if not m.clickedcart == None:
            window.blit(selected2, [m.clickedcart.rect.left-2, m.clickedcart.rect.top-2])
            if m.mode == "action":
                window.blit(box, [m.rect.left+10, m.rect.top+10])
                ui.Resize(30)
                try:
                    ui.Text(m.hoveritem.type.upper(), [m.rect.left+27, m.rect.top+25])
                except:
                    ui.Text(m.clickedcart.type.upper(), [m.rect.left+27, m.rect.top+25])
                if listmap[snaptogrid(m.tl)[0]][snaptogrid(m.tl)[1]] > 0:
                    ui.Resize(22)
                    ui.Text("Click to move", [m.rect.left+27, m.rect.top+45])
                    ui.Text("Cart Here", [m.rect.left+27, m.rect.top+60])
        window.blit(selected, [snaptogrid(m.tl)[0]*40-2, snaptogrid(m.tl)[1]*40-2])
        window.blit(uibox, [555, 475])
    pygame.display.flip()
    clock.tick(60)
    fps = clock.get_fps()
pygame.quit()
