import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Eyes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 50)

# Eye properties
eye_radius = 80
pupil_radius = 30
blink_timer = 0
blink_interval = random.randint(2000, 5000)
expression = "neutral"
running = True
clock = pygame.time.Clock()

# Eye positions
eye_centers = [(WIDTH // 3, HEIGHT // 2), (2 * WIDTH // 3, HEIGHT // 2)]

def draw_eye(center, pupil_offset, eye_color, blink):
    pygame.draw.ellipse(screen, WHITE, (center[0] - eye_radius, center[1] - eye_radius, 2 * eye_radius, 2 * eye_radius))
    if not blink:
        pygame.draw.circle(screen, eye_color, (center[0] + pupil_offset[0], center[1] + pupil_offset[1]), pupil_radius)

def get_pupil_offset(expr):
    if expr == "happy":
        return (0, -10)
    elif expr == "sad":
        return (0, 10)
    elif expr == "angry":
        return (-10, -10)
    elif expr == "surprised":
        return (0, -20)
    return (0, 0)

def get_eye_color(expr):
    if expr == "happy":
        return YELLOW
    elif expr == "angry":
        return RED
    return BLUE

while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()
    blink = current_time - blink_timer < 200

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                expression = "neutral"
            elif event.key == pygame.K_2:
                expression = "happy"
            elif event.key == pygame.K_3:
                expression = "sad"
            elif event.key == pygame.K_4:
                expression = "angry"
            elif event.key == pygame.K_5:
                expression = "surprised"

    pupil_offset = get_pupil_offset(expression)
    eye_color = get_eye_color(expression)
    
    for center in eye_centers:
        draw_eye(center, pupil_offset, eye_color, blink)
    
    if current_time - blink_timer > blink_interval:
        blink_timer = current_time
        blink_interval = random.randint(2000, 5000)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
