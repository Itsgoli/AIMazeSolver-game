import math

import pygame
from player import Player, circle_rect_collision
from config import BALL_RADIUS, GRID_SIZE


class Fox(Player):
    def __init__(self,width,height,score,image):
        self.x = width
        self.y = height
        self.image = pygame.image.load(image).convert_alpha()
        
        
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))

        
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.score = score
    def update_position(self, x, y):
            self.x = x
            self.y = y
            self.rect.center = (self.x, self.y)

    def move(self, target, speed, obstacles):
        dx = target[0] - self.x
        dy = target[1] - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        base_angle = math.atan2(dy, dx)

        max_rotation = math.pi  # 180 درجه
        rotation_step = math.pi/18   # 10 درجه
        for i in range(int(max_rotation / rotation_step) + 1):
            for sign in [1, -1]:
                test_angle = base_angle + sign * i * rotation_step
                
                vx = speed * math.cos(test_angle)
                vy = speed * math.sin(test_angle)
                new_x = self.x + vx
                new_y = self.y + vy

                collision = False
                for obs in obstacles:
                    if circle_rect_collision(new_x, new_y, BALL_RADIUS, obs.rect):
                        collision = True
                        break

                if not collision:
                    self.update_position(new_x, new_y)
                    return

   

