import pygame
import sys
import random

pygame.init()

width, height = 800, 600
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("it doesnt end")

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
bonus_color = (0, 255, 255)
penalty_color = (255, 165, 0)
enemy_color = (255, 0, 0)


clock = pygame.time.Clock()
snake_block = 10

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

eerie_captions = [
    "Death is a solution.",
    "There is only one way out.",
    "you'll eventually see what's not there.",
    "There is no escape.",
    "This is home.",
]

def your_score(score, time_left):
    value = score_font.render(f"Score: {score}  Time Left: {time_left}s", True, yellow)
    dis.blit(value, [10, 10])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [width / 6, (height / 3) + y_offset])


def choose_difficulty():
    dis.fill(black)
    message("Select Difficulty: E - Easy, M - Medium, H - Hard", white)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return 10, 0, 60  
                elif event.key == pygame.K_m:
                    return 15, 3, 40  
                elif event.key == pygame.K_h:
                    return 20, 5, 30  

def game_over_message(score):
    dis.fill(blue)
    random_caption = random.choice(eerie_captions) 
    message("You Lost! Press C-Play Again or Q-Quit", red)
    message(random_caption, red, 50)  
    your_score(score, 0)  
    pygame.display.update()

def gameLoop():
    game_over = False
    game_close = False
    x1, y1 = width // 2, height // 2
    x1_change, y1_change = 0, 0

    snake_list = []
    length_of_snake = 1
    score = 0

    
    snake_speed, enemy_speed, game_timer = choose_difficulty()
    start_ticks = pygame.time.get_ticks()

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    bonusx, bonusy = None, None
    if snake_speed >= 15:
        bonusx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        bonusy = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    penaltyx, penaltyy = None, None
    if snake_speed == 20:
        penaltyx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        penaltyy = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    enemy_x, enemy_y = None, None
    if snake_speed >= 15:
        enemy_x, enemy_y = random.randint(0, width // 10) * 10, random.randint(0, height // 10) * 10

    while not game_over:
        if game_close:
            game_over_message(score)  
            while game_close:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:  
                            gameLoop()
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(black)


        if enemy_x is not None and enemy_y is not None:
            if enemy_x < x1:
                enemy_x += min(enemy_speed, abs(enemy_x - x1))
            elif enemy_x > x1:
                enemy_x -= min(enemy_speed, abs(enemy_x - x1))

            if enemy_y < y1:
                enemy_y += min(enemy_speed, abs(enemy_y - y1))
            elif enemy_y > y1:
                enemy_y -= min(enemy_speed, abs(enemy_y - y1))

            pygame.draw.rect(dis, enemy_color, [enemy_x, enemy_y, snake_block, snake_block])

        
        pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])
        if bonusx is not None:
            pygame.draw.rect(dis, bonus_color, [bonusx, bonusy, snake_block, snake_block])
        if penaltyx is not None:
            pygame.draw.rect(dis, penalty_color, [penaltyx, penaltyy, snake_block, snake_block])

        
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1

        
        if bonusx is not None and x1 == bonusx and y1 == bonusy:
            bonusx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            bonusy = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            score += 3

        
        if penaltyx is not None and x1 == penaltyx and y1 == penaltyy:
            penaltyx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            penaltyy = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            score -= 1

        
        if enemy_x is not None and enemy_y is not None:
            if abs(x1 - enemy_x) < snake_block and abs(y1 - enemy_y) < snake_block:
                game_close = True

        
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)

        
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, game_timer - elapsed_seconds)
        your_score(score, time_left)

        if time_left <= 0:
            game_close = True

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()