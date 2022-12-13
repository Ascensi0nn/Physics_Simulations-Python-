import pygame
import main
import settings
import math

# CONSTANTS
WIDTH = main.WIDTH
HEIGHT = main.HEIGHT
FPS = main.FPS
BLACK = (0,0,0)
BALL_SIZE = settings.ball_size
GROUND_HEIGHT = HEIGHT - 100

triangle_height = 25
length = 100        # in cm
gravity = -9.8
time = 0

ball = pygame.transform.scale(pygame.image.load("ball.png"), (BALL_SIZE, BALL_SIZE))
ball_mass = 25
ball_x = WIDTH / 2 - BALL_SIZE / 2
ball_y = triangle_height + length
max_angle = 0
#current_angle = 0

#SCREEN
WIN = main.WIN

launch = False

def reset():
    global launch
    global ball_x, ball_y, length, max_angle, time, current_angle
    launch = False
    ball_x = WIDTH / 2 - BALL_SIZE / 2
    ball_y = triangle_height + length
    length = 100
    max_angle = 0
    current_angle = 0
    time = 0

def move_ball():
    global ball_x, ball_y, length, max_angle, current_angle, time

    period = 2 * math.pi * math.sqrt((length / 100) / (-1 * gravity))
    ang_frequency = (2 * math.pi) / period
    amplitude = length * math.sin(math.radians(abs(max_angle)))
    phase = (math.pi / 2)
    x = amplitude * math.sin(ang_frequency * time - phase)
    ball_x = WIDTH / 2 + x - BALL_SIZE / 2

    y = math.sqrt(math.pow(length, 2) - math.pow(x, 2))
    ball_y = y - BALL_SIZE / 2 + triangle_height

    current_angle = math.degrees(math.acos(x / length)) - math.degrees(phase)

    time += 0.01

    '''
    T = 2 * math.pi * math.sqrt(length / gravity)
    x(t) = A * math.cos(wt)
    v(t) = -1 * A * w * math.sin(wt)            ==> speed arrows
    w = (2 * math.pi) / T
    '''

def change_length(k):
    global length, ball_x, ball_y
    if k[pygame.K_UP]:
        length -= 1
    if k[pygame.K_DOWN] and length > 1:
        length += 1

def change_angle(k):
    global max_angle, ball_x, ball_y
    if k[pygame.K_LEFT]:
        max_angle += 1
    if k[pygame.K_RIGHT]:
        max_angle -= 1

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
    global time, current_angle

    LINE_CONSTANT = 1
    LINE_WIDTH = 3
    ARROW_CONSTANT = 6

    period = 2 * math.pi * math.sqrt((length / 100) / (-1 * gravity))
    amplitude = length * math.sin(math.radians(abs(max_angle)))
    ang_frequency = (2 * math.pi) / period

    vel = -1 * amplitude * ang_frequency * math.sin(ang_frequency * time)
    vel_x = vel * math.cos(current_angle)       # maybe not current angle
    vel_y = vel * math.sin(current_angle)       # "                     "

    line_length = vel / LINE_CONSTANT
    x_line_length = vel_x / LINE_CONSTANT
    y_line_length = vel_y / LINE_CONSTANT

    '''
    v(t) = -1 * A * w * math.sin(wt)            ==> speed arrows
    '''

    # X
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2), LINE_WIDTH)

    # Y
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2 + y_line_length), LINE_WIDTH)

    # VEL
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2 + y_line_length), LINE_WIDTH)

    '''
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE + x_line_length, ball_red_y + BALL_SIZE / 2), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE + x_line_length, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE + x_line_length - ARROW_CONSTANT, ball_y + BALL_SIZE / 2 + ARROW_CONSTANT), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE + x_line_length, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE + x_line_length - ARROW_CONSTANT, ball_y + BALL_SIZE / 2 - ARROW_CONSTANT), width=LINE_WIDTH)
    '''

def draw_triangle():
    line_width = 8
    pygame.draw.line(WIN, BLACK, (WIDTH / 2, triangle_height), (WIDTH / 2 + triangle_height, 0), width=line_width)
    pygame.draw.line(WIN, BLACK, (WIDTH / 2, triangle_height), (WIDTH / 2 - triangle_height, 0), width=line_width)

def draw_text():
    global current_angle, length, ball_mass

    font = pygame.font.SysFont('helvetica', 24)
    ang = font.render("Angle: " + str(round(current_angle, 2)) + " degrees", True, BLACK)
    l = font.render("Length: " + str(round(length, 2)) + "cm", True, BLACK)
    mass = font.render("Mass: " + str(round(ball_mass, 2)) + "kg", True, BLACK)

    WIN.blit(ang, (20, 20))
    WIN.blit(l, (20, 50))
    WIN.blit(mass, (20, 80))

def draw_string():
    pygame.draw.line(WIN, BLACK, (WIDTH / 2, triangle_height), (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2), width=2)

def draw_window():
    #Background
    WIN.fill((239, 231, 211), (0, 0, WIDTH, HEIGHT))
    draw_background_graph()

    #Other
    draw_speed_arrows()
    draw_triangle()
    draw_string()
    WIN.blit(ball, (ball_x, ball_y))
    draw_ground()
    draw_text()
    pygame.display.update()

def start():
    global launch, ball_x, ball_y, current_angle

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
            move_ball()
        else:
            keys_pressed = pygame.key.get_pressed()
            change_length(keys_pressed)
            change_angle(keys_pressed)
            ball_x = length * math.cos(math.radians(max_angle + 90)) + WIDTH / 2 - BALL_SIZE / 2
            ball_y = length * math.sin(math.radians(max_angle + 90)) + triangle_height - BALL_SIZE / 2
            current_angle = max_angle
        draw_window()
    main.begin()