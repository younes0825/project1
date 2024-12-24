import pygame
import math
import random

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
Player_health = 100

def Player():
    pygame.draw.circle(screen, (BLACK), (Player_pos), Player_radius)

#AI
kill_count = 0
AI_radius = 15
AI_speed = 3
AI_pos = [100,100]
AI_health = 100
damage_interval = 1000
last_hit_time = 0
Random_pos = [random.randint(0,800), random.randint(0,600)]

def move_ai():
    if AI_health > 0:
        global kill_count
        pygame.draw.circle(screen, (BLACK), (AI_pos), 15)
        dx = Player_pos[0] - AI_pos[0]
        dy = Player_pos[1] - AI_pos[1]
        distance = math.hypot(dx,dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        AI_pos[0] += dx * AI_speed
        AI_pos[1] += dy * AI_speed
    else:
        respawn_new_ai()
        kill_count += 1

#Respawn AI
def respawn_new_ai():
    global AI_health, AI_pos
    AI_health = 100
    AI_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]

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

#Time control
last_time_checked = pygame.time.get_ticks()
time_elapsed = 60
def timer(time):
    Font = pygame.font.Font(None, 50)
    timer = Font.render(time, True, BLACK)
    screen.blit(timer, (25, 25))

#Kill counter
def kill_counter():
    Font = pygame.font.Font(None, 50)
    Small_Font = pygame.font.Font(None, 30)
    kill_subtitle = Small_Font.render("Kills", True, BLACK)
    tracker = Font.render(str(kill_count), True, BLACK)
    screen.blit(tracker, (750, 50))
    screen.blit(kill_subtitle, (735, 20))

#Game loss screen
def game_lost():
    Font = pygame.font.Font(None, 74)
    restart_text_font = pygame.font.Font(None, 35)
    text = Font.render("Game lost", True, RED)
    restart_text = restart_text_font.render("Press 'R' to restart", True, RED)
    screen.fill(BLACK)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - 30))
    screen.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 + 40))
    pygame.display.update()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True

run = True
while run:

    screen.fill(WHITE)

    time_passed = pygame.time.get_ticks()

    Player()

    move_ai()

    #Timer
    time_tracker = pygame.time.get_ticks()
    if time_tracker - last_time_checked >= 1000:
        if time_elapsed >= 0:
            time_elapsed -= 1
        last_time_checked = time_tracker

    #Kill counter
    kill_counter()

    timer(str(time_elapsed))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot_bullet()

    #Bullet logic
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

    #AI health bar
    Health_bar_pos = [AI_pos[0] - 50, AI_pos[1] - 40]
    for i in range(AI_health):
        Health_bar = pygame.draw.rect(screen, (GREEN), (Health_bar_pos[0], Health_bar_pos[1], AI_health, 15))
        Death_bar = pygame.draw.rect(screen, (RED), (Health_bar_pos[0] + AI_health, Health_bar_pos[1], 100-AI_health, 15))

    #Player Health bar
    Health_bar_pos2 = [Player_pos[0] - 50, Player_pos[1] - 40]
    for i in range(Player_health):
        if AI_health > 0:
            Health_bar2 = pygame.draw.rect(screen, (GREEN), (Health_bar_pos2[0], Health_bar_pos2[1], Player_health, 15))
            Death_bar2 = pygame.draw.rect(screen, (RED), (Health_bar_pos2[0] + Player_health, Health_bar_pos2[1], 100 - Player_health, 15))

    #Damage logic
    if math.hypot(Player_pos[0] - AI_pos[0], Player_pos[1] - AI_pos[1]) < AI_radius + Player_radius:
        if time_passed - last_hit_time >= damage_interval:
            Player_health -= 20
            last_hit_time = time_passed

    if Player_health <= 0:
        if game_lost():
            AI_health = 100
            Player_health = 100
            Player_pos = [WIDTH/2, HEIGHT/2]
            AI_pos = [100,100]
            bullet_list = []
            time_elapsed = 60

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