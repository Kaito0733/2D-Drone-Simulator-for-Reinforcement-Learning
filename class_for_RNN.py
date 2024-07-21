import pygame
import sys
import math
import numpy as np
from time import sleep

pygame.init()

class Drone2DSimulator:
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

    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("2D Drone Simulation for RNN's or Other Applications")
        self.surface = pygame.display.get_surface()
        self.WIDTH, self.HEIGHT = self.surface.get_width(), self.surface.get_height()

        self.image = pygame.image.load('2d-drone-simulator-for-reinforcement-learning-main/fancy_drone.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.DRONE_WIDTH + 65, self.DRONE_HEIGHT + 45))

        self.sliders = [
            Slider(7.5, 30, 200, 20, 1, 40, self.ROTATION_SPEED, 'Rotation Speed'),
            Slider(7.5, 90, 200, 20, 0, 1.5, self.ROTATION_DRAG, 'Rotation Drag'),
            Slider(7.5, 150, 200, 20, 1, 40, self.THRUST_POWER, 'Thrust Power'),
            Slider(7.5, 210, 200, 20, 0, 10, self.GRAVITY, 'Gravity'),
            Slider(7.5, 270, 200, 20, 10, 200, self.X_AXIS_SENS, 'X Axis Sensitivity'),
            Slider(7.5, 330, 200, 20, 0.1, 10, self.Y_AXIS_SENS, 'Y Axis Sensitivity'),
        ]

        self.re_initialize_variables()

    def re_initialize_variables(self):
        self.drone_x = self.WIDTH // 2
        self.drone_y = self.HEIGHT // 2
        self.drone_angle = 0  # degrees
        self.drone_speed_y = 0
        self.drone_speed_x = 0
        self.thrust_left = 0
        self.thrust_right = False
        self.rotation_speed = 0
        self.paused = False

    def rotate_point(self, x, y, angle_rad):
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        return (x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle)

    def update_sliders(self):
        for slider in self.sliders:
            slider.update_value()

    def get_feedback(self):
        return {"speed_x": self.drone_speed_x,
                "speed_y": self.drone_speed_y,
                "angle": self.drone_angle,
                "position_x": self.drone_x,
                "position_y": self.drone_y}

    def run(self, output):
        thrust_index = 0
        num_thrusts = len(output)
        running = True

        while running and thrust_index < num_thrusts:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                    running = False
                    break

                for slider in self.sliders:
                    slider.handle_event(event)

            if keys[pygame.K_p]:
                if not self.paused:
                    sleep(0.4)
                self.paused = not self.paused

            if not self.paused:
                thrust = output[thrust_index]
                thrust_index += 1

                self.thrust_left = thrust[0]
                self.thrust_right = thrust[1]

                self.ROTATION_SPEED = self.sliders[0].val
                self.ROTATION_DRAG = self.sliders[1].val
                self.THRUST_POWER = self.sliders[2].val
                self.GRAVITY = self.sliders[3].val
                self.X_AXIS_SENS = self.sliders[4].val
                self.Y_AXIS_SENS = self.sliders[5].val

                self.drone_speed_y += self.GRAVITY

                if self.thrust_left:
                    self.rotation_speed -= self.ROTATION_SPEED
                    thrust_power = self.THRUST_POWER * math.cos(math.radians(self.drone_angle))
                    self.drone_speed_y -= self.Y_AXIS_SENS * thrust_power
                if self.thrust_right:
                    self.rotation_speed += self.ROTATION_SPEED
                    thrust_power = self.THRUST_POWER * math.cos(math.radians(self.drone_angle))
                    self.drone_speed_y -= self.Y_AXIS_SENS * thrust_power

                self.rotation_speed *= self.ROTATION_DRAG
                self.drone_angle += self.rotation_speed
                self.drone_angle %= 360
                angle_rad = math.radians(self.drone_angle)
                self.drone_speed_x = self.X_AXIS_SENS * math.sin(angle_rad)
                self.drone_x += 0.5 * self.drone_speed_x
                self.drone_y += 0.5 * self.drone_speed_y

                half_width = self.DRONE_WIDTH / 2
                half_height = self.DRONE_HEIGHT / 2

                points = [
                    self.rotate_point(-half_width, -half_height, angle_rad),
                    self.rotate_point(half_width, -half_height, angle_rad),
                    self.rotate_point(half_width, half_height, angle_rad),
                    self.rotate_point(-half_width, half_height, angle_rad)
                ]

                points = [(x + self.drone_x, y + self.drone_y) for x, y in points]

                thrust_offset_left = self.rotate_point(-half_width, 0, angle_rad)
                thrust_offset_right = self.rotate_point(half_width, 0, angle_rad)
                
                thrust_positions = [
                    (self.drone_x + thrust_offset_left[0] - self.THRUST_WIDTH / 2, self.drone_y + thrust_offset_left[1] - self.THRUST_HEIGHT / 2),
                    (self.drone_x + thrust_offset_right[0] - self.THRUST_WIDTH / 2, self.drone_y + thrust_offset_right[1] - self.THRUST_HEIGHT / 2)
                ]

            self.screen.fill(self.WHITE)
            pygame.draw.polygon(self.screen, self.BLACK, points)

            for pos in thrust_positions:
                pygame.draw.rect(self.screen, self.RED, (pos[0], pos[1], self.THRUST_WIDTH, self.THRUST_HEIGHT))

            rotated_image = pygame.transform.rotate(self.image, -self.drone_angle)
            rotated_rect = rotated_image.get_rect(center=(self.drone_x, self.drone_y))

            self.screen.blit(rotated_image, rotated_rect)

            for slider in self.sliders:
                slider.draw(self.screen)
                
            pygame.display.flip()
            pygame.time.Clock().tick(30)

        return running

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
        pygame.draw.rect(screen, Drone2DSimulator.BLACK, self.rect, 2)
        knob_x = self.rect.x + (self.rect.w * (self.val - self.min_val) / (self.max_val - self.min_val))
        pygame.draw.circle(screen, Drone2DSimulator.RED, (int(knob_x), self.rect.centery), self.rect.h // 2)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f'{self.name}: {self.val:.2f}', True, Drone2DSimulator.BLACK)
        screen.blit(text_surface, (self.rect.x, self.rect.y - 24))
