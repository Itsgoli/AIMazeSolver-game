import math
import pygame
from config import BALL_RADIUS

class Player :
 
 def check_goal(self, hole_pos):
        dx = self.x - hole_pos[0]
        dy = self.y - hole_pos[1]
        return math.hypot(dx, dy) < BALL_RADIUS + 20 
 
 def draw(self, screen):
            screen.blit(self.image, self.rect)

def circle_rect_collision(cx, cy, radius, rect):
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return (dx*dx + dy*dy) < (radius*radius)
