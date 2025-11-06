import pygame
import random
from fox import Fox
from hen import Hen
from obstacle import Obstacle
from config import BLACK, COLS, FPS, GOAL_SCORE, HEIGHT, NEST_RADIUS, MAX_OBSTACLES, ROWS, GRID_SIZE, SPEED, WHITE, WIDTH



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find the Nest")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48, bold=True)


background_image = pygame.image.load("image5.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
nest_image = pygame.image.load("image3.png").convert_alpha()
nest_image = pygame.transform.scale(nest_image, (NEST_RADIUS * 2, NEST_RADIUS * 2))

def get_cell(pos):
    x, y = pos
    col = x // GRID_SIZE
    row = y // GRID_SIZE
    return (col * GRID_SIZE, row * GRID_SIZE)

def get_cell_center(pos):
    x, y = pos
    col = x // GRID_SIZE
    row = y // GRID_SIZE
    center_x = col * GRID_SIZE + GRID_SIZE // 2
    center_y = row * GRID_SIZE + GRID_SIZE // 2
    return (center_x, center_y)
 
def draw_grid(screen):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT)) 
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y)) 

start_pos_hen = (500, 500)
start_pos_fox = (100, 100)
start_cell_fox = get_cell(start_pos_fox)
start_cell_hen = get_cell(start_pos_hen)


grid_cells = [(col * GRID_SIZE, row * GRID_SIZE) for row in range(ROWS) for col in range(COLS)]


valid_cells = [cell for cell in grid_cells if cell != start_cell_fox and cell != start_cell_hen]

obstacle_positions = random.sample(valid_cells, MAX_OBSTACLES)

obstacles = []
for x, y in obstacle_positions:
    obstacles.append(Obstacle(x, y, GRID_SIZE, GRID_SIZE))


def get_random_hole_position(obstacles):
       valid_cells = [cell for cell in grid_cells if not any(obs.rect.collidepoint(cell[0] + GRID_SIZE//2, cell[1] + GRID_SIZE//2) for obs in obstacles)]
    
       
       chosen_cell = random.choice(valid_cells)
        
      
       hole_x = chosen_cell[0] + GRID_SIZE // 2
       hole_y = chosen_cell[1] + GRID_SIZE // 2
       pos = hole_x, hole_y

       return pos
        
def is_valid_hole_position(pos, obstacles):
    x, y = pos
    hole_rect = pygame.Rect(x - NEST_RADIUS, y - NEST_RADIUS, NEST_RADIUS * 2, NEST_RADIUS * 2)

    for obs in obstacles:
        if hole_rect.colliderect(obs.rect):
            return False
    return True


fox = Fox(100,100,0,"image1.png")
hen = Hen(500,500,0,"image2.png")
hole_pos = get_random_hole_position(obstacles)

turn = 1
running = True
game_over = False

while running:
    clock.tick(FPS)
    screen.blit(background_image, (0, 0))
    draw_grid(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        if turn == 1:
            fox.move(hole_pos, SPEED, obstacles)
            if fox.check_goal(hole_pos):
                fox.score += 1
                hole_pos = get_random_hole_position(obstacles)
            turn = 2

        elif turn == 2:
            hen.move(hole_pos, SPEED, obstacles)
            if hen.check_goal(hole_pos):
                hen.score += 1
                hole_pos = get_random_hole_position(obstacles)
            turn = 1

        hole_rect = nest_image.get_rect(center=(int(hole_pos[0]), int(hole_pos[1])))
        screen.blit(nest_image, hole_rect)

        for obs in obstacles:
            obs.draw(screen)

        fox.draw(screen)
        hen.draw(screen)

        score_text = font.render(f"fox: {fox.score}   hen: {hen.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if fox.score >= GOAL_SCORE or hen.score >= GOAL_SCORE:
            game_over = True

    else:
        result_background = pygame.image.load("image5.png").convert_alpha()
        result_background = pygame.transform.scale(result_background, (WIDTH, HEIGHT))
        screen.blit(result_background, (0, 0))
        winner = "The fox Wins!" if fox.score > hen.score else "The hen Wins!"
        color = (220, 50, 50) if fox.score > hen.score else (50, 50, 220)
        

        result_text = big_font.render(winner, True, WHITE)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            

    pygame.display.update()

pygame.quit()
