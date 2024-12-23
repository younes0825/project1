import pygame
import math
import time

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

#Player
Player_radius = 15
Player_speed = 5
Player_pos = [WIDTH/2, HEIGHT/2]

def Player():
    pygame.draw.circle(screen, (BLACK), (Player_pos), Player_radius)

#AI
AI_radius = 15
AI_speed = 3
AI_pos = [100,100]
AI_health = 100

def move_ai():
    if AI_health > 0:
        pygame.draw.circle(screen, (BLACK), (AI_pos), 15)
        dx = Player_pos[0] - AI_pos[0]
        dy = Player_pos[1] - AI_pos[1]
        distance = math.hypot(dx,dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        AI_pos[0] += dx * AI_speed
        AI_pos[1] += dy * AI_speed

#Bullets
Bullet_radius = 5
Bullet_speed = 10
Bullet_list = []

def shoot_bullet():
    shoot_pos = pygame.mouse.get_pos()
    dx = Player_pos[0] - shoot_pos[0]
    dy = Player_pos[1] - shoot_pos[1]
    distance = math.hypot(dx, dy)

    if distance > 0:
        dx /= distance
        dy /= distance

    x = Player_pos[0]
    y = Player_pos[1]
    
    Bullet_list.append([x, y, dx, dy])

run = True
while run:

    screen.fill(WHITE)

    Player()

    move_ai()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot_bullet()

    for bullet in Bullet_list[:]:
        pygame.draw.circle(screen, (BLACK), (bullet[0], bullet[1]), Bullet_radius)
        if bullet[0] < 0 or bullet[0] > 800:
            Bullet_list.remove(bullet)
        elif bullet[1] < 0 or bullet[1] > 600:
            Bullet_list.remove(bullet)
        else:
            bullet[0] -= bullet[2] * Bullet_speed
            bullet[1] -= bullet[3] * Bullet_speed

        bullet_distance = math.hypot(bullet[0] - AI_pos[0], bullet[1] - AI_pos[1])
        if bullet_distance < AI_radius + Bullet_radius:
            AI_health -= 20
            Bullet_list.remove(bullet)

    Health_bar_pos = [AI_pos[0] - 50, AI_pos[1] - 40]
    for i in range(AI_health):
        Health_bar = pygame.draw.rect(screen, (GREEN), (Health_bar_pos[0], Health_bar_pos[1], AI_health, 15))
        Death_bar = pygame.draw.rect(screen, (RED), (Health_bar_pos[0] + AI_healtha, Health_bar_pos[1], 100-AI_health, 15))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        Player_pos[1] -= 5
    if keys[pygame.K_s]:
        Player_pos[1] += 5
    if keys[pygame.K_a]:
        Player_pos[0] -= 5
    if keys[pygame.K_d]:
        Player_pos[0] += 5

    if Player_pos[0] < -10:
        Player_pos[0] = 810
    if Player_pos[0] > 811:
        Player_pos[0] = -9
    if Player_pos[1] > 611:
        Player_pos[1] = -9
    if Player_pos[1] < -10:
        Player_pos[1] = 610

    pygame.display.update()

    clock.tick(60)