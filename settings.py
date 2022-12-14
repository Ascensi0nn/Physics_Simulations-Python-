import pygame
import pygame_menu
import main

WIDTH = main.WIDTH
HEIGHT = main.HEIGHT
WIN = main.WIN
FPS = main.FPS
BLACK = (0,0,0)

ball_size = 30

options = pygame.transform.scale(pygame.image.load("options.png"), (50, 50))

def change_ball_size(x):
    global ball_size
    ball_size = x

def draw_window():
    WIN.fill((239, 231, 211), (0, 0, WIDTH, HEIGHT))
    WIN.blit(options, (100, 50))

    font = pygame.font.SysFont('helvetica', 24)
    size = font.render("Ball Size: " + str(round(ball_size)), True, BLACK)
    WIN.blit(size, (0, 0))

    pygame.display.update()

def go_back():
    main.begin()

def start():
    settings = pygame_menu.Menu('Settings', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_SOLARIZED)
    settings.add.range_slider(
        'Ball Size',
        30,
        (1,100),
        1,
        change_ball_size
    )
    settings.add.button('Return', go_back)
    settings.mainloop(WIN)