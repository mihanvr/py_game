import pygame
import random

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

pygame.init()

sc = pygame.display.set_mode((300, 200))
pos = (0, 0)

sc.fill(COLOR_BLACK)

rect = pygame.Rect(0, 0, 40, 40)

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.MOUSEMOTION:
            pos = i.pos
    pygame.time.delay(16)
    print(pygame.key.get_pressed()[pygame.K_DOWN])
    sc.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    rect.center = pos

    pygame.display.update(rect)
