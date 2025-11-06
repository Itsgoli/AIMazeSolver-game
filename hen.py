import math

import pygame
from player import Player, circle_rect_collision
from config import COLS, HEIGHT, ROWS, GRID_SIZE, WIDTH,BALL_RADIUS

class Hen(Player):
 def __init__(self,width,height,score,image):
        self.x = width
        self.y = height
        self.image = pygame.image.load(image).convert_alpha()
        
      
        self.image = pygame.transform.scale(self.image, (GRID_SIZE, GRID_SIZE))

       
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.score = score
        self.move_target = (self.x, self.y)

 def update_position(self, x, y):
            self.x = x
            self.y = y
            self.rect.center = (self.x, self.y)
    
 def move(self, target, speed, obstacles):
        

        def get_neighbors(col, row):
            neighbors = [
                (col, row - 1), (col, row + 1),
                (col - 1, row), (col + 1, row)
            ]
            return [(c, r) for c, r in neighbors if 0 <= c < COLS and 0 <= r < ROWS]

       
        dx = self.move_target[0] - self.x
        dy = self.move_target[1] - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist > speed:
           
            self.update_position( self.x + speed * dx / dist, self.y + speed * dy / dist)
            
            return

        
       
        self.update_position(self.move_target[0],self.move_target[1])
        

        
        col = int(self.x) // GRID_SIZE
        row = int(self.y) // GRID_SIZE

        
        target_col = int(target[0]) // GRID_SIZE
        target_row = int(target[1]) // GRID_SIZE

        neighbors = get_neighbors(col, row)
        neighbors.sort(key=lambda c: abs(c[0] - target_col) + abs(c[1] - target_row))

        for c, r in neighbors:
            new_x = c * GRID_SIZE + GRID_SIZE // 2
            new_y = r * GRID_SIZE + GRID_SIZE // 2

            ball_rect = pygame.Rect(new_x - BALL_RADIUS, new_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
            if any(ball_rect.colliderect(obs.rect) for obs in obstacles):
                continue

            self.move_target = (new_x, new_y)
            return