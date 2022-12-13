import pygame
import main
import settings

# CONSTANTS
WIDTH = main.WIDTH
HEIGHT = main.HEIGHT
FPS = main.FPS
BLACK = (0,0,0)
RED = (255,0,0)
BALL_SIZE = settings.ball_size
GROUND_HEIGHT = HEIGHT - 100

# Red Ball Variables
ball_red = pygame.transform.scale(pygame.image.load("ballred.png"), (BALL_SIZE, BALL_SIZE))
ball_red_x = BALL_SIZE
ball_red_y = GROUND_HEIGHT - BALL_SIZE
ball_red_vel = 10
ball_red_mass = 25.0

#Blue Ball Variables
ball_blue = pygame.transform.scale(pygame.image.load("ballblue.png"), (BALL_SIZE, BALL_SIZE))
ball_blue_x = WIDTH - BALL_SIZE - BALL_SIZE
ball_blue_y = GROUND_HEIGHT - BALL_SIZE
ball_blue_vel = -10
ball_blue_mass = 25.0

#SCREEN
WIN = main.WIN

launch = False
contact = False

def reset():
    global launch, contact
    global ball_red_x, ball_red_vel, ball_red_mass
    global ball_blue_x, ball_blue_vel, ball_blue_mass
    contact = False
    launch = False
    ball_red_vel = 10
    ball_red_x = BALL_SIZE
    ball_red_mass = 25
    ball_blue_vel = -10
    ball_blue_x = WIDTH - 2 * BALL_SIZE
    ball_blue_mass = 25

def move_balls():
    global ball_red_vel, ball_red_x, ball_red_y
    global ball_blue_vel, ball_blue_x, ball_blue_y
    global contact

    red_rect = pygame.Rect((ball_red_x, ball_red_y),(BALL_SIZE, BALL_SIZE))
    blue_rect = pygame.Rect((ball_blue_x, ball_blue_y), (BALL_SIZE, BALL_SIZE))
    if pygame.Rect.colliderect(red_rect, blue_rect) and not contact:
        t1_b = ball_blue_vel * (ball_blue_mass - ball_red_mass) / (ball_blue_mass + ball_red_mass)
        t2_b = ball_red_vel * (2 * ball_red_mass) / (ball_blue_mass + ball_red_mass)
        ball_blue_vel_f = t1_b + t2_b
        t1_r = ball_blue_vel * (2 * ball_blue_mass) / (ball_blue_mass + ball_red_mass)
        t2_r = ball_red_vel * (ball_red_mass - ball_blue_mass) / (ball_blue_mass + ball_red_mass)
        ball_red_vel_f = t1_r + t2_r

        ball_red_vel = ball_red_vel_f
        ball_blue_vel = ball_blue_vel_f

        contact = True

    vel_const = 5
    # red move
    if ball_red_x >= WIDTH - BALL_SIZE:
        ball_red_x = WIDTH - BALL_SIZE
        ball_red_vel = 0
    elif ball_red_x < 0:
        ball_red_x = 0
        ball_red_vel = 0
    else:
        ball_red_x += ball_red_vel / vel_const

    #blue move
    if ball_blue_x >= WIDTH - BALL_SIZE:
        ball_blue_x = WIDTH - BALL_SIZE
        ball_blue_vel = 0
    elif ball_blue_x < 0:
        ball_blue_x = 0
        ball_blue_vel = 0
    else:
        ball_blue_x += ball_blue_vel / vel_const

def change_velocities(k):
    global ball_red_vel, ball_blue_vel
    if k[pygame.K_d]:
        ball_red_vel += 1
    if k[pygame.K_a] and ball_red_vel > 0:
        ball_red_vel -= 1
    if k[pygame.K_RIGHT] and ball_blue_vel < 0:
        ball_blue_vel += 1
    if k[pygame.K_LEFT]:
        ball_blue_vel -= 1

def change_masses(k):
    global ball_red_mass, ball_blue_mass
    if k[pygame.K_w]:
        ball_red_mass += 0.1
    if k[pygame.K_s] and ball_red_mass > 0:
        ball_red_mass -= 0.1
    if k[pygame.K_UP]:
        ball_blue_mass += 0.1
    if k[pygame.K_DOWN] and ball_blue_mass > 0:
        ball_blue_mass -= 0.1

def draw_ground():
    global GROUND_HEIGHT
    line_width = 3
    pygame.draw.line(WIN, BLACK, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), line_width)

def draw_background_graph():
    tile_size = 50
    line_width = 1

    #   VERTICAL LINES
    i = 0
    while i < WIDTH:
        pygame.draw.line(WIN, BLACK, (i, 0), (i, HEIGHT), line_width)
        i += tile_size

    #   HORIZONTAL LINES
    k = 0
    while k < HEIGHT:
        pygame.draw.line(WIN, BLACK, (0, k), (WIDTH, k), line_width)
        k += tile_size

def draw_speed_arrows():
    global ball_red_vel, ball_red_x, ball_red_y
    global ball_blue_vel, ball_blue_x, ball_blue_y

    LINE_CONSTANT = 1
    LINE_WIDTH = 3
    ARROW_CONSTANT = 6
    red_x_line_length = ball_red_vel / LINE_CONSTANT
    blue_x_line_length = -1 * ball_blue_vel / LINE_CONSTANT

    #red
    pygame.draw.line(WIN, BLACK, (ball_red_x + BALL_SIZE, ball_red_y + BALL_SIZE / 2), (ball_red_x + BALL_SIZE + red_x_line_length, ball_red_y + BALL_SIZE / 2), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_red_x + BALL_SIZE + red_x_line_length, ball_red_y + BALL_SIZE / 2), (ball_red_x + BALL_SIZE + red_x_line_length - ARROW_CONSTANT, ball_red_y + BALL_SIZE / 2 + ARROW_CONSTANT), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_red_x + BALL_SIZE + red_x_line_length, ball_red_y + BALL_SIZE / 2), (ball_red_x + BALL_SIZE + red_x_line_length - ARROW_CONSTANT, ball_red_y + BALL_SIZE / 2 - ARROW_CONSTANT), width=LINE_WIDTH)

    # red
    pygame.draw.line(WIN, BLACK, (ball_blue_x, ball_blue_y + BALL_SIZE / 2), (ball_blue_x - blue_x_line_length, ball_blue_y + BALL_SIZE / 2), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_blue_x - blue_x_line_length, ball_blue_y + BALL_SIZE / 2), (ball_blue_x - blue_x_line_length + ARROW_CONSTANT, ball_blue_y + BALL_SIZE / 2 - ARROW_CONSTANT), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_blue_x - blue_x_line_length, ball_blue_y + BALL_SIZE / 2), (ball_blue_x - blue_x_line_length + ARROW_CONSTANT, ball_blue_y + BALL_SIZE / 2 + ARROW_CONSTANT), width=LINE_WIDTH)

def draw_text():
    global ball_red_vel
    global ball_blue_vel

    font = pygame.font.SysFont('helvetica', 24)
    red_vel = font.render("Red vel: " + str(round(ball_red_vel, 2)) + "m/s", True, BLACK)
    red_mass = font.render("Red mass: " + str(round(ball_red_mass, 1)) + "kg", True, BLACK)
    blue_vel = font.render("Blue vel: " + str(round(ball_blue_vel, 2)) + "m/s", True, BLACK)
    blue_mass = font.render("Blue mass: " + str(round(ball_blue_mass, 1)) + "kg", True, BLACK)

    WIN.blit(red_vel, (20, 20))
    WIN.blit(red_mass, (20, 50))
    WIN.blit(blue_vel, (WIDTH - 200, 20))
    WIN.blit(blue_mass, (WIDTH - 200, 50))

def draw_window():
    #Background
    WIN.fill((239, 231, 211), (0, 0, WIDTH, HEIGHT))
    draw_background_graph()

    #Other
    draw_speed_arrows()
    WIN.blit(ball_blue, (ball_blue_x, ball_blue_y))
    WIN.blit(ball_red, (ball_red_x, ball_red_y))
    draw_ground()
    draw_text()
    pygame.display.update()

def start():
    global launch

    pygame.display.set_caption("Object Collision Simulator")
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    launch = True
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_ESCAPE:
                    reset()
                    run = False
        if launch:
            move_balls()
        else:
            keys_pressed = pygame.key.get_pressed()
            change_velocities(keys_pressed)
            change_masses(keys_pressed)
        draw_window()
    main.begin()