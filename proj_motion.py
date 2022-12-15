import math
import pygame
import main
import settings

#CONSTANT
WIDTH = main.WIDTH
HEIGHT = main.HEIGHT
FPS = main.FPS
BALL_SIZE = settings.ball_size
BALL_STARTING_CIRCLE_RADIUS = 100
BLACK = (0,0,0)
RED = (255,0,0)

#VARIABLES ==> FOR CALCULATIONS
angle = 45
vel = 50
mass = 5
gravity = -9.8
time = 0
ball_starting_height = 100
ball_position_list = []

#SCREEN
WIN = main.WIN

#VARIABLES FOR LATER
vel_x, vel_yi, ball_x, ball_y, BALL_STARTING_POINT, ground_height = 0, 0, 0, 0, [0.0,0.0], HEIGHT - 100

ball = pygame.transform.scale(pygame.image.load("ball.png"), (BALL_SIZE, BALL_SIZE))
options = pygame.transform.scale(pygame.image.load("options.png"), (50, 50))
shot = False
ball_hit = False

def init_vars():
    global vel_x, vel_yi, BALL_STARTING_POINT, ball_x, ball_y, ground_height, ball, BALL_SIZE

    BALL_STARTING_POINT[0] = 100
    BALL_STARTING_POINT[1] = HEIGHT - BALL_SIZE - ball_starting_height

    BALL_SIZE = settings.ball_size
    ball = pygame.transform.scale(pygame.image.load("ball.png"), (BALL_SIZE, BALL_SIZE))

    ball_x, ball_y = BALL_STARTING_POINT[0], BALL_STARTING_POINT[1]

def reset():
    global ball_x, ball_y, time, shot, angle, ball_starting_height, ball_hit, ground_height, ball_position_list, vel
    ball_starting_height = 100
    ball_x = BALL_STARTING_POINT[0]
    ball_y = BALL_STARTING_POINT[1] - BALL_SIZE - ball_starting_height
    time = 0
    shot = False
    ball_hit = False
    vel = 50
    angle = 45
    ball_position_list = []
    ground_height = HEIGHT - ball_starting_height

def move_ball():
    global ball_x, ball_y, time, vel_x, vel_yi, ball_hit, ball_position_list
    vel_x = vel * math.cos(math.radians(angle))
    vel_yi = -1 * vel * math.sin(math.radians(angle))

    current_vel_y = -1 * (vel_yi - gravity * time)

    if not ball_hit:
        if current_vel_y < 0 and ball_y + BALL_SIZE >= ground_height and time > 0.1:
            ball_y = ground_height - BALL_SIZE
            if HEIGHT - ball_starting_height < ground_height:
                t = (-1 * vel_yi + math.sqrt((math.pow(vel_yi, 2) + 2 * gravity * (HEIGHT - ball_starting_height - ground_height)))) / (-1 * gravity)
            else:
                t = 2 * vel_yi / gravity
            ball_x = BALL_STARTING_POINT[0] + vel_x * t
            ball_hit = True
        else:
            ball_x = vel_x * time + BALL_STARTING_POINT[0]
            ball_y = vel_yi * time - 0.5 * gravity * math.pow(time, 2) + BALL_STARTING_POINT[1]
            time += 0.1
        ball_position_list.append((ball_x, ball_y))

def change_ball_angle(k):
    global angle
    h = -1 * (HEIGHT - ball_starting_height - ground_height)
    if k[pygame.K_LEFT] and angle < 90:
        angle += 1
    if k[pygame.K_RIGHT] and angle > -90:
        if angle > 0:
            angle -=1
        elif h > 0:
            angle -= 1
    init_vars()

def change_ball_speed(k):
    global vel
    if k[pygame.K_UP]:
        vel += 1
    if k[pygame.K_DOWN] and vel > 0:
        vel -= 1
    init_vars()

def change_ball_height(k):
    global ball_starting_height
    if k[pygame.K_w]:
        ball_starting_height += 1
    if k[pygame.K_s] and ball_starting_height > 0:
        ball_starting_height -= 1
    init_vars()

def change_ground_height(k):
    global ground_height
    if k[pygame.K_e]:
        ground_height -= 1
    if k[pygame.K_d]:
        ground_height += 1
    init_vars()

def draw_text():
    global ball_x, ball_y, vel, ball_starting_height
    font = pygame.font.SysFont('helvetica', 24)
    bx = font.render("X position: " + str(round(ball_x - BALL_STARTING_POINT[0])) + "m", True, BLACK)
    by = font.render("Y position: " + str(round(-1 * (ball_y - BALL_STARTING_POINT[1]))) + "m", True, BLACK)
    v = font.render("Initial Velocity: " + str(round(vel)) + "m/s", True, BLACK)
    ang = font.render("Angle: " + str(round(angle)) + " degrees", True, BLACK)
    h = font.render("h: " + str(round(-1 * (HEIGHT - ball_starting_height - ground_height))) + "m", True, BLACK)
    ground = font.render("ground height: " + str(round(HEIGHT - ground_height - 100)) + "m", True, BLACK)

    WIN.blit(bx, (20, 20))
    WIN.blit(by, (20, 50))
    WIN.blit(ang, (20, 80))
    WIN.blit(v, (20, 110))
    WIN.blit(h, (20, 140))
    WIN.blit(ground, (20, 170))

def draw_ground():
    global ground_height
    line_width = 3
    pygame.draw.line(WIN, BLACK, (0, ground_height), (WIDTH, ground_height), line_width)

def draw_speed_arrows():
    global ball_x, ball_y, vel, vel_x, vel_yi, time

    LINE_CONSTANT = 1
    LINE_WIDTH = 3
    ARROW_CONSTANT = 6
    vel_x = vel * math.cos(math.radians(angle))
    vel_y = vel * math.sin(math.radians(angle)) + gravity * time
    x_line_length = vel_x / LINE_CONSTANT
    y_line_length = vel_y / LINE_CONSTANT

    if shot:
        current_angle = math.degrees(math.atan(vel_y / vel_x))
    else:
        current_angle = angle

    #   X line
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2 + x_line_length - ARROW_CONSTANT, ball_y + BALL_SIZE / 2 + ARROW_CONSTANT), width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2 + x_line_length - ARROW_CONSTANT, ball_y + BALL_SIZE / 2 - ARROW_CONSTANT), width=LINE_WIDTH)

    #   Y line
    if vel_y > 0:
        pt1 = (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2)
        pt2 = (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2 - y_line_length)
        a_pt1 = (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2 - y_line_length)
        a1_pt2 = (ball_x + BALL_SIZE / 2 - ARROW_CONSTANT, ball_y + BALL_SIZE / 2 - y_line_length + ARROW_CONSTANT)
        a2_pt2 = (ball_x + BALL_SIZE / 2 + ARROW_CONSTANT, ball_y + BALL_SIZE / 2 - y_line_length + ARROW_CONSTANT)
    else:
        pt1 = (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2)
        pt2 = (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2 - y_line_length)
        a_pt1 = (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2 - y_line_length)
        a1_pt2 = (ball_x + BALL_SIZE / 2 - ARROW_CONSTANT, ball_y + BALL_SIZE / 2 - y_line_length - ARROW_CONSTANT)
        a2_pt2 = (ball_x + BALL_SIZE / 2 + ARROW_CONSTANT, ball_y + BALL_SIZE / 2 - y_line_length - ARROW_CONSTANT)

    pygame.draw.line(WIN, BLACK, pt1, pt2, width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, a_pt1, a1_pt2, width=LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, a_pt1, a2_pt2, width=LINE_WIDTH)

    #DIAGONAL LINE
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2, ball_y + BALL_SIZE / 2), (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2 - y_line_length), LINE_WIDTH)
    p_1 = (ball_x + BALL_SIZE / 2 + x_line_length + ARROW_CONSTANT * math.cos(math.radians(current_angle + 135)), ball_y + BALL_SIZE / 2 - y_line_length - ARROW_CONSTANT * math.sin(math.radians(current_angle + 135)))
    p_2 = (ball_x + BALL_SIZE / 2 + x_line_length + ARROW_CONSTANT * math.cos(math.radians(current_angle - 135)), ball_y + BALL_SIZE / 2 - y_line_length - ARROW_CONSTANT * math.sin(math.radians(current_angle - 135)))

    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2 - y_line_length), p_1, LINE_WIDTH)
    pygame.draw.line(WIN, BLACK, (ball_x + BALL_SIZE / 2 + x_line_length, ball_y + BALL_SIZE / 2 - y_line_length), p_2, LINE_WIDTH)

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

def draw_window():
    #Background
    WIN.fill((239, 231, 211), (0, 0, WIDTH, HEIGHT))
    draw_background_graph()

    #Other
    draw_speed_arrows()
    draw_path()
    WIN.blit(ball, (ball_x, ball_y))
    draw_text()
    draw_ground()
    pygame.display.update()

def draw_path():
    global ball_x, ball_y, ball_position_list
    circle_radius = round(BALL_SIZE / 8)

    for i in range(len(ball_position_list)):
        selected_items_0 = [item[0] for item in ball_position_list]
        selected_items_1 = [item[1] for item in ball_position_list]
        pygame.draw.circle(WIN, (255, 0, 0), (selected_items_0[i] + BALL_SIZE / 2, selected_items_1[i] + BALL_SIZE / 2), circle_radius)

def start():
    global shot, angle, ball_x, ball_y, BALL_SIZE

    pygame.display.set_caption("Projectile Motion Simulator")
    clock = pygame.time.Clock()
    run = True

    init_vars()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shot = True
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_ESCAPE:
                    reset()
                    run = False
        if not shot:
            keys_pressed = pygame.key.get_pressed()
            change_ball_angle(keys_pressed)
            change_ball_speed(keys_pressed)
            change_ball_height(keys_pressed)
            change_ground_height(keys_pressed)
        else:
            move_ball()
        draw_window()
    main.begin()