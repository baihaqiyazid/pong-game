import pygame
from pygame import gfxdraw
import random
import os
#https://github.com/bapiraj/pong-game

pygame.init()
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

bg_color = pygame.Color("#001219")
WHITE = pygame.Color("#fefae0")
YELLOW = pygame.Color("#ffba08")
RED = pygame.Color("#d00000")
GREEN = pygame.Color("#06d6a0")

ball_radius = 15
player_width1, player_height1 = 15, 150
player_width2, player_height2 = 15, 150

ball = pygame.Rect(screen_width//2-ball_radius, screen_height//2-ball_radius, ball_radius*2, ball_radius*2)
player1 = pygame.Rect(0, screen_height//2-player_height1//2, player_width1, player_height1)
player2 = pygame.Rect(screen_width-player_width2, screen_height//2-player_height2//2, player_width2, player_height2)

ball_speed_x, ball_speed_y = 5, 5
player_speed = 5
player1_delta, player2_delta = 0, 0
player1_score, player2_score = 0, 0

clock = pygame.time.Clock()
font = pygame.font.SysFont("inkfree", 35)

collides_sound = pygame.mixer.Sound(os.getcwd()+'/sounds/sound1.wav')
wrong_sound = pygame.mixer.Sound(os.getcwd()+'/sounds/wrong.wav')
winner_sound = pygame.mixer.Sound(os.getcwd()+'/sounds/winner.wav')
ball_sound = pygame.mixer.Sound(os.getcwd()+'/sounds/ball.wav')
Game_Music_sound = pygame.mixer.Sound(os.getcwd()+'/sounds/Game_Music.mp3')

second = 60
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player1_delta = player_speed
            if event.key == pygame.K_w:
                player1_delta = -player_speed
            if event.key == pygame.K_DOWN:
                player2_delta = player_speed
            if event.key == pygame.K_UP:
                player2_delta = -player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s or event.key == pygame.K_w:
                player1_delta = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                player2_delta = 0
    
    player1.y += player1_delta
    player2.y += player2_delta
    player1.top = max(0, player1.top)
    player2.top = max(0, player2.top)
    player1.bottom = min(screen_height, player1.bottom)
    player2.bottom = min(screen_height, player2.bottom)

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
        pygame.mixer.Sound.play(ball_sound)
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
        if ball.left <= 0: 
            player2_score += 1
            pygame.mixer.Sound.play(wrong_sound) 
        else: 
            player1_score += 1
            pygame.mixer.Sound.play(wrong_sound)
    
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
        pygame.mixer.Sound.play(collides_sound)

    screen.fill(bg_color)
    ball_speed_text = font.render('Ball Speed: {}'.format(round(second)), True, WHITE)
    ball_speed_text_rect = ball_speed_text.get_rect()
    ball_speed_text_rect.center = (screen_width//2, 20)
    screen.blit(ball_speed_text, ball_speed_text_rect)

    player1_text = font.render('Player 1: {}'.format(player1_score), True, WHITE)
    player1_text_rect = player1_text.get_rect()
    player1_text_rect.center = (screen_width//4, 20)
    screen.blit(player1_text, player1_text_rect)

    player2_text = font.render('Player 2: {}'.format(player2_score), True, WHITE)
    player2_text_rect = player2_text.get_rect()
    player2_text_rect.center = (screen_width-screen_width//4, 20)
    screen.blit(player2_text, player2_text_rect)
    
    pygame.draw.aaline(screen, WHITE, (screen_width//2, 0), (screen_width//2, screen_height))
    gfxdraw.aacircle(screen, screen_width//2, screen_height//2, 200, WHITE)
    pygame.draw.rect(screen, YELLOW, player1)
    pygame.draw.rect(screen, RED, player2)
    gfxdraw.filled_circle(screen, ball.centerx, ball.centery, ball_radius, WHITE)

    game_over = False

    if player1_score == 3 or player2_score == 3:
        pygame.mixer.Sound.play(winner_sound)
        game_over = True

        ball.center = (screen_width//2, screen_height//2)
        ball_speed_x *= random.choice([-1, 1])
        ball_speed_y *= random.choice([-1, 1])
        ball_speed_x, ball_speed_y = 0, 0

        if player1_score > player2_score:
            winner_text = font.render('The Winner is Player 1', True, GREEN)
            winner_text_rect = winner_text.get_rect()
            winner_text_rect.center = (screen_width-screen_width//2, 150)
            screen.blit(winner_text, winner_text_rect)
        elif player1_score < player2_score:
            winner_text = font.render('The Winner is Player 2', True, GREEN)
            winner_text_rect = winner_text.get_rect()
            winner_text_rect.center = (screen_width-screen_width//2, 150)
            screen.blit(winner_text, winner_text_rect)
        
        play_again_text = font.render('Play Again? Enter (y/n)', True, WHITE)
        play_again_text_rect = play_again_text.get_rect()
        play_again_text_rect.center = (screen_width-screen_width//2, 200)
        screen.blit(play_again_text, play_again_text_rect)

        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                game_over = False
                running = False
                
            # get the user's input (y or n)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # reset the ga
                    gameover = False   
                
                    player1_score = 0
                    player2_score = 0

                    second = 60
                    ball_speed_x, ball_speed_y = 5, 5


                elif event.key == pygame.K_n:
                    # exit the loops
                    gameover = False
                    running = False

        pygame.display.update()
        clock.tick(second)

    else:

        pygame.display.update()
        clock.tick(second)
        second += 0.02