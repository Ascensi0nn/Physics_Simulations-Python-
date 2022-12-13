import pygame
import main

WIDTH = main.WIDTH
HEIGHT = main.HEIGHT
WIN = main.WIN
FPS = main.FPS
BLACK = (0,0,0)

ball_size = 45

options = pygame.transform.scale(pygame.image.load("options.png"), (50, 50))

def change_ball_size():
    global ball_size
    if ball_size < 100:
        ball_size += 5
    else:
        ball_size = 5

def draw_window():
    WIN.fill((239, 231, 211), (0, 0, WIDTH, HEIGHT))
    WIN.blit(options, (int(WIDTH / 2 - options.get_width() / 2), 50))

    font = pygame.font.SysFont('helvetica', 24)
    size = font.render("Ball Size: " + str(round(ball_size)), True, BLACK)
    WIN.blit(size, (0, 0))

    pygame.display.update()

def start():
    pygame.display.set_caption("*Settings*")
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        draw_window()
    main.begin()