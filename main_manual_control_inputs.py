##########################################################################################################################################################################################################################################
#AUTHOR:
    #KNS357

#CONTROLS: 
    #left_key = right thrust (ADJUST FOR REINFORCEMENT LEARNING)
    #rigt_key = left thrust (ADJUST FOR REINFORCEMENT LEARNING)
    #r = restart simulation
    #esc = quit simulation
    #p = pause (sorry if it has input issues)
    #Activate both thruster to elevate evenly, hold only one to rotate
    #see sliders in simulation for parameter difficulty tuning

#THIS CODE IS OPEN-SOURCE ANND CAN BE USED FOR RNN TRAINING OR OTHER APPLICATIONS FOR GAMES
#SOURCE OF VEHICLE: https://www.vectorstock.com/royalty-free-vector/futurist-flying-car-autonomic-sci-fi-transport-vector-38404383
##########################################################################################################################################################################################################################################

import pygame
import sys
import math
from time import sleep

pygame.init()

DRONE_WIDTH, DRONE_HEIGHT = 50, 20
THRUST_WIDTH, THRUST_HEIGHT = 10, 5
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAVITY = 2.5
THRUST_POWER = 5
ROTATION_SPEED = 10
TILT_SENSITIVITY = 0.1
X_AXIS_SENS = 50
Y_AXIS_SENS = 1
ROTATION_DRAG = 0.7

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("2D Drone Simulation for RNN's or Other Applications")

surface = pygame.display.get_surface()
WIDTH, HEIGHT = size = surface.get_width(), surface.get_height()

image = pygame.image.load('2d-drone-simulator-for-reinforcement-learning-main/fancy_drone.png').convert_alpha()
image = pygame.transform.scale(image, (DRONE_WIDTH + 65, DRONE_HEIGHT + 45))

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, name):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.name = name
        self.dragging = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                rel_x = event.pos[0] - self.rect.x
                self.val = self.min_val + (self.max_val - self.min_val) * rel_x / self.rect.w
                self.val = max(self.min_val, min(self.max_val, self.val))

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        knob_x = self.rect.x + (self.rect.w * (self.val - self.min_val) / (self.max_val - self.min_val))
        pygame.draw.circle(screen, RED, (int(knob_x), self.rect.centery), self.rect.h // 2)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f'{self.name}: {self.val:.2f}', True, BLACK)
        screen.blit(text_surface, (self.rect.x, self.rect.y - 24))

sliders = [
    Slider(7.5, 30, 200, 20, 1, 40, ROTATION_SPEED, 'Rotation Speed'),
    Slider(7.5, 90, 200, 20, 0, 1.5, ROTATION_DRAG, 'Rotation Drag'),
    Slider(7.5, 150, 200, 20, 1, 40, THRUST_POWER, 'Thrust Power'),
    Slider(7.5, 210, 200, 20, 0, 10, GRAVITY, 'Gravity'),
    Slider(7.5, 270, 200, 20, 10, 200, X_AXIS_SENS, 'X Axis Sensitivity'),
    Slider(7.5, 330, 200, 20, 0.1, 10, Y_AXIS_SENS, 'Y Axis Sensitivity'),
]

drone_x = WIDTH // 2
drone_y = HEIGHT // 2
drone_angle = 0  # degrees
drone_speed_y = 0
drone_speed_x = 0
thrust_left = False
thrust_right = False
rotation_speed = 0
paused = False

def re_initialize_variables():
    global ROTATION_SPEED, ROTATION_DRAG, THRUST_POWER, GRAVITY, X_AXIS_SENS, Y_AXIS_SENS, paused, drone_x, drone_y, drone_angle, drone_speed_y, drone_speed_x, thrust_left, thrust_right, rotation_speed
    drone_x = WIDTH // 2
    drone_y = HEIGHT // 2
    drone_angle = 0  # Angle in degrees
    drone_speed_y = 0
    drone_speed_x = 0
    thrust_left = False
    thrust_right = False
    rotation_speed = 0
    paused = False

running = True
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        for slider in sliders:
            slider.handle_event(event)

    if keys[pygame.K_p]:
        if not paused:
            sleep(0.4)
        paused = not paused

    if not paused:
        keys = pygame.key.get_pressed()
        thrust_left = keys[pygame.K_LEFT]
        thrust_right = keys[pygame.K_RIGHT]

        ROTATION_SPEED = sliders[0].val
        ROTATION_DRAG = sliders[1].val
        THRUST_POWER = sliders[2].val
        GRAVITY = sliders[3].val
        X_AXIS_SENS = sliders[4].val
        Y_AXIS_SENS = sliders[5].val

        drone_speed_y += GRAVITY

        if thrust_left:
            rotation_speed -= ROTATION_SPEED
            thrust_power = THRUST_POWER * math.cos(math.radians(drone_angle))
            drone_speed_y -= Y_AXIS_SENS * thrust_power
        if thrust_right:
            rotation_speed += ROTATION_SPEED
            thrust_power = THRUST_POWER * math.cos(math.radians(drone_angle))
            drone_speed_y -= Y_AXIS_SENS * thrust_power

        rotation_speed *= ROTATION_DRAG
        drone_angle += rotation_speed
        drone_angle = drone_angle % 360
        angle_rad = math.radians(drone_angle)
        drone_speed_x = X_AXIS_SENS * math.sin(angle_rad)
        drone_x += 0.5 * drone_speed_x
        drone_y += 0.5 * drone_speed_y
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        def rotate_point(x, y, angle_rad):
            return (x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle)

        half_width = DRONE_WIDTH / 2
        half_height = DRONE_HEIGHT / 2

        points = [
            rotate_point(-half_width, -half_height, angle_rad),
            rotate_point(half_width, -half_height, angle_rad),
            rotate_point(half_width, half_height, angle_rad),
            rotate_point(-half_width, half_height, angle_rad)
        ]

        points = [(x + drone_x, y + drone_y) for x, y in points]

        thrust_offset_left = rotate_point(-half_width, 0, angle_rad)
        thrust_offset_right = rotate_point(half_width, 0, angle_rad)
        
        thrust_positions = [
            (drone_x + thrust_offset_left[0] - THRUST_WIDTH / 2, drone_y + thrust_offset_left[1] - THRUST_HEIGHT / 2),
            (drone_x + thrust_offset_right[0] - THRUST_WIDTH / 2, drone_y + thrust_offset_right[1] - THRUST_HEIGHT / 2)
        ]

    screen.fill(WHITE)
    pygame.draw.polygon(screen, BLACK, points)

    for pos in thrust_positions:
        pygame.draw.rect(screen, RED, (pos[0], pos[1], THRUST_WIDTH, THRUST_HEIGHT))

    rotated_image = pygame.transform.rotate(image, -drone_angle)
    rotated_rect = rotated_image.get_rect(center=(drone_x, drone_y))

    screen.blit(rotated_image, rotated_rect)

    for slider in sliders:
        slider.draw(screen)
        
    pygame.display.flip()
    pygame.time.Clock().tick(30)

    if keys[pygame.K_r]:
        re_initialize_variables()
