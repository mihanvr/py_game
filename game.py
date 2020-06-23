import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400
sc = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()

loop = True

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

circle_speed = 2
pos_x = WIDTH
pos_y = HEIGHT
radius = 100
speed_x = 0
speed_y = 0

rect1 = pygame.Rect()
rect2 = pygame.Rect()

key_map1 = {  # bind
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
}

key_map2 = {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
}

player1 = {'pos_x': 0, 'pos_y': 0, 'radius': 100, 'speed_x': 0, 'speed_y': 0, 'speed': 2, 'color': COLOR_WHITE,
           'keys': key_map1, 'enemy': False}
player2 = {'pos_x': WIDTH // 2, 'pos_y': HEIGHT // 2, 'radius': 50, 'speed_x': 0, 'speed_y': 0, 'speed': 4,
           'color': COLOR_RED, 'keys': key_map2, 'enemy': True}

game_objects = [player1, player2]


def handle_input(player, events):
    keys = player['keys']
    speed_x = player['speed_x']
    speed_y = player['speed_y']
    speed = player['speed']

    for i in events:
        if i.type == pygame.KEYDOWN:
            if i.key == keys['left']:
                speed_x -= speed
            if i.key == keys['right']:
                speed_x += speed
            if i.key == keys['up']:
                speed_y -= speed
            if i.key == keys['down']:
                speed_y += speed
        elif i.type == pygame.KEYUP:
            if i.key == keys['left']:
                speed_x += speed
            if i.key == keys['right']:
                speed_x -= speed
            if i.key == keys['up']:
                speed_y += speed
            if i.key == keys['down']:
                speed_y -= speed
    player['speed_x'] = speed_x
    player['speed_y'] = speed_y
    pass


def handle_transform(player):
    player['pos_x'] += player['speed_x']
    player['pos_y'] += player['speed_y']


def draw_player(player):
    pygame.draw.circle(sc, player['color'], (player['pos_x'], player['pos_y']), player['radius'])


def draw_objects():
    for player in game_objects:
        draw_player(player)


while True:
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.QUIT:
            pygame.quit()
            exit()

    for go in game_objects:
        handle_input(go, events)
        handle_transform(go)

    sc.fill(COLOR_BLACK)
    draw_objects()

    pygame.display.update()
    clock.tick(FPS)
