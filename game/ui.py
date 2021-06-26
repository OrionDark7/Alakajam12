import pygame

pygame.font.init()

font = pygame.font.Font("./resources/FORCED SQUARE.ttf", 24)
size = 24
color = [255, 255, 255]
window = pygame.surface.Surface([800, 600])

def Resize(s):
    global font, size
    font = pygame.font.Font("./resources/FORCED SQUARE.ttf", int(round(s)))
    size = int(round(s))

def Text(msg, pos, centered=False):
    render = font.render(str(msg), 1, list(color))
    rect = None
    if centered:
        rect = render.get_rect()
        window.blit(render, [pos[0] - rect.width/2, pos[1] - rect.height/2])
    else:
        window.blit(render, list(pos))
    return rect