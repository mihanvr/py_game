import pygame
import random

pygame.init()

SPAWN_STONE = pygame.USEREVENT + 0

stone_spawn_delay = 500
pygame.time.set_timer(SPAWN_STONE, stone_spawn_delay)

WIDTH = 600
HEIGHT = 400
sc = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()
stone_speed = 3

player = pygame.Rect(0, 0, 50, 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_GRAY = (128, 128, 128)

stones = []


def spawn_stone():
    stone_width = random.randint(10, 20)
    stone_height = random.randint(10, 20)
    stone_x = random.randint(stone_width // 2, WIDTH - stone_width // 2)
    stone = pygame.Rect(stone_x, 0, stone_width, stone_height)
    stones.append(stone)
    pass


def process_stones():
    for stone in stones:
        center = stone.center
        stone.center = (center[0], center[1] + stone_speed)
    pass


def draw_stones():
    for stone in stones:
        pygame.draw.rect(sc, COLOR_GRAY, stone)
    pass


def change_stone_spawn_delay(delta_ms):
    global stone_spawn_delay
    stone_spawn_delay += delta_ms
    stone_spawn_delay = max(50, stone_spawn_delay)
    pygame.time.set_timer(SPAWN_STONE, stone_spawn_delay)


while True:
    events = pygame.event.get()
    process_stones()
    for i in events:
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()
        if i.type == SPAWN_STONE:
            spawn_stone()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                change_stone_spawn_delay(50)
            if i.key == pygame.K_DOWN:
                change_stone_spawn_delay(-50)

    pos_x = pygame.mouse.get_pos()[0]
    pos_x = max(pos_x, player.width // 2)
    pos_x = min(pos_x, WIDTH - player.width // 2)
    player.center = (pos_x, HEIGHT - player.height // 2)

    sc.fill(COLOR_BLACK)
    pygame.draw.rect(sc, COLOR_RED, player)
    draw_stones()
    pygame.display.update()
    clock.tick(FPS)
