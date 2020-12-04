import sys
from random import randint
from random import random
import pygame
import time

game_on = True

pygame.init()

while game_on:

    #thememusic
    pygame.mixer.music.load("data\I Write Sins Not Tragedies.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.3)

    # soundeffects
    explsnd = pygame.mixer.Sound("data\soundeffects\explosion1.wav")
    heartbeat = pygame.mixer.Sound("data\soundeffects\heartbeat.wav")
    # gameoversound =
    maybenexttime = pygame.mixer.Sound("data\soundeffects\maybe-next-time-huh.wav")

    # soundchannels
    soundChannel1 = pygame.mixer.Channel(1)
    soundChannel2 = pygame.mixer.Channel(2)
    soundChannel3 = pygame.mixer.Channel(3)
    soundChannel3.set_volume(1.0)
    soundChannel4 = pygame.mixer.Channel(4)

    # images
    explosion = pygame.image.load("data\images\explosion.png")
    steveimg = pygame.image.load("data\images\steve2.png")
    patti = pygame.image.load("data\images\patti.png")
    creeperimg = pygame.image.load("data\images\creeper.png")

    # colors
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)

    # screens
    WIDTH = 800
    HEIGHT = 800

    startscreenimg = pygame.image.load("data\images\startscreen.png")
    startscreen = pygame.display.set_mode((WIDTH, HEIGHT))

    gamescreenimg = pygame.image.load("data\images\gamescreen.jpg")
    gamescreen = pygame.display.set_mode((WIDTH, HEIGHT))

    gameoverscreenimg = pygame.image.load("data\images\gameoverscreen.png")
    gameoverscreen = pygame.display.set_mode((WIDTH, HEIGHT))

    # playerattributes
    player_size = 50
    player_pos = [int(WIDTH / 2), int(HEIGHT - 2 * player_size)]

    # enemyatrributes
    enemy_size = 50
    enemy_pos = [randint(0, WIDTH - enemy_size), 0]
    enemy_list = [enemy_pos]

    pygame.display.set_caption("PattisGame")

    # gamesettings
    life = 5
    score = 0
    SPEED = 10

    startgame = True
    game_over = False

    clock = pygame.time.Clock()

    myFont = pygame.font.SysFont("monospace", 35)


    def set_lvl(score, SPEED):
        # if score < 20:
        #     SPEED = 5
        # elif score < 40:
        #     SPEED = 8
        # elif score < 60:
        #     SPEED = 12
        # elif score < 90:
        #     SPEED = 15
        # elif score < 120:
        #     15
        # else:
        #     SPEED = 20
        if score < 100:
            SPEED = score / 5 + 4
        return SPEED


    def drop_enemies(enemy_list):
        delay = random()
        if len(enemy_list) < 10 and delay < 0.1:
            x_pos = randint(0, WIDTH - enemy_size)
            y_pos = 0
            enemy_list.append([x_pos, y_pos])


    def draw_enemies(enemy_list):
        for enemy_pos in enemy_list:
            #pygame.draw.rect(gamescreen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
            gamescreen.blit(creeperimg, (int(enemy_pos[0]) - 25, int(enemy_pos[1]) - 25))


    def detect_collision(player_pos, enemy_pos):
        p_x = player_pos[0]
        p_y = player_pos[1]

        e_x = enemy_pos[0]
        e_y = enemy_pos[1]

        if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
            if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
                return True
            return False


    def collision_check(enemy_list, player_pos):
        for enemy_pos in enemy_list:
            if detect_collision(player_pos, enemy_pos):
                return True
        return False


    def update_enemy_positions(enemy_list, score):
        for idx, enemy_pos in enumerate(enemy_list):
            if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
                enemy_pos[1] += SPEED
            else:
                enemy_list.pop(idx)
                score += 1
        return score


    def kill_enemy(enemy_list, player_pos, life):
        for idx, enemy_pos in enumerate(enemy_list):
            if not detect_collision(player_pos, enemy_pos):
                pass
            else:
                enemy_list.pop(idx)
                soundChannel1.play(explsnd)
                gamescreen.blit(explosion, enemy_pos)
                life -= 1
                #if life == 2:
                 #   soundChannel2.play(heartbeat, loops=-1)
        return life


    # startscreen

    while startgame:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startgame = False
                    break
                if event.type == pygame.QUIT:
                    sys.exit()
        pygame.display.update()
        startscreen.blit(startscreenimg, (0, 0))

    # gamescreen

    while not game_over and not startgame:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]
                if event.key == pygame.K_LEFT:
                    if x > 0:
                        x -= player_size
                elif event.key == pygame.K_RIGHT:
                    if x < (WIDTH - player_size):
                        x += player_size
                elif event.key == pygame.K_UP:
                    if y > (HEIGHT - 250):
                        y -= player_size
                elif event.key == pygame.K_DOWN:
                    if y < (HEIGHT - player_size):
                        y += player_size
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()

                player_pos = [x, y]

        gamescreen.blit(gamescreenimg, (-900, -400))

        drop_enemies(enemy_list)


        score = update_enemy_positions(enemy_list, score)



        if collision_check(enemy_list, player_pos):
            if life == 1:
                soundChannel3.play(maybenexttime)
                game_over = True

        life = kill_enemy(enemy_list, player_pos, life)
        SPEED = set_lvl(score, SPEED)

        lifetext = "Life: " + str(life)
        lifelabel = myFont.render(lifetext, 1, RED)
        gamescreen.blit(lifelabel, (WIDTH - 750, HEIGHT - 40))

        scoretext = "Score: " + str(score)
        scorelabel = myFont.render(scoretext, 1, BLACK)
        gamescreen.blit(scorelabel, (WIDTH - 200, HEIGHT - 40))

        draw_enemies(enemy_list)

        pygame.draw.rect(gamescreen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
        gamescreen.blit(patti, (player_pos[0] - 25, player_pos[1] - 25))

        #framerate
        clock.tick(30)

        pygame.display.update()

    # gameoverscreen

    while game_over:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    break
                if event.type == pygame.K_ESCAPE:
                    sys.exit()
        pygame.display.update()
        gameoverscreen.blit(gameoverscreenimg, (0, 0))
