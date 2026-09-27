# Welcome to My Game!
# Please read the README.md before trying to play.
# Please do not alter any of the code for the best experience
# If you do want a harder challenge, go to the settings areas and change the values in the PLAYER SETTINGS and the PROJECTILE SETTINGS

import pygame # You need this installed in order to play
import time 
from random import randint

# GAME CONSTS #
window_width, window_height = 750, 600
pygame.display.set_caption("Dodge the Bullets")
background_image = pygame.transform.scale(pygame.image.load("C:/Users/LukeS/Downloads/Images/Random/Goober.png"), (window_width, window_height * 1.1))
font = pygame.font.SysFont("comicsans", 25)

# PLAYER SETTINGS #
player_width = 50 
player_height = 50 
player_velocity = 8

pygame.init()
window = pygame.display.set_mode((window_width, window_height))

def draw(player, elapsed_time, projectiles, projectiles_cooldown, projectile_velocity): 
    window.blit(background_image, (0, 0)) 

    time_text = font.render(f"Time: {round(elapsed_time)}s", 1, "#FF0000") 
    window.blit(time_text, (10, 10)) 

    # The cooldown_text and velocity_text are just diagnostics. If you wish to comment those, you may.
    cooldown_text = font.render(f"Cooldown: {round(projectiles_cooldown)}ms", 1, "#FF0000") 
    window.blit(cooldown_text, (10, 40))

    velocity_text = font.render(f"Velocity: {round(projectile_velocity)}", 1, "#FF0000") 
    window.blit(velocity_text, (10, 70)) 
    
    pygame.draw.rect(window, ("#FF0000"), player) 
    
    for projectile in projectiles: 
        pygame.draw.rect(window, "#0000FF", projectile) 
        
    pygame.display.update() 

def main(): 
    run = True 
    player = pygame.Rect(200, window_height - player_height, player_width, player_height) 
    clock = pygame.time.Clock() 
    start_time = time.time() 
    elapsed_time = 0 

    # PROJECTILE SETTINGS #
    projectiles_cooldown = 2400 # Amount of ms it takes initially to launch the first bullets
    min_projectiles_cooldown = 150 # I would recommend nothing below 100ms for the best experience
    game_tempo = 40 # The lower the number, the faster the game
    projectile_width, projectile_height = 20, 20 # Do NOT set above the window_width / window_height
    projectile_velocity = 3 # Set this to a positive number (not 0) below the max_projectile_velocity
    max_projectile_velocity = 10 # I would recommend nothing above 50
    projectile_quantity = 3

    projectile_count = 0
    projectiles = []
    hit = False

    while run: 
        projectile_count += clock.tick(60) 
        elapsed_time = time.time() - start_time 
        
        if projectile_count > projectiles_cooldown: 
            for _ in range(projectile_quantity): 
                projectile_x = randint(0, window_width - projectile_width) 
                projectile = pygame.Rect(projectile_x, -projectile_height, projectile_width, projectile_height) 
                projectiles.append(projectile) 
                
            if projectiles_cooldown >= 300: 
                projectiles_cooldown = max(min_projectiles_cooldown, projectiles_cooldown - (projectiles_cooldown / game_tempo)) 
            else: 
                projectiles_cooldown = max(min_projectiles_cooldown, projectiles_cooldown - (projectiles_cooldown / (game_tempo * 2)))
            if projectile_velocity < max_projectile_velocity:
                projectile_velocity = max(projectile_velocity, projectile_velocity + (max_projectile_velocity / (game_tempo * 2)))
            projectile_count = 0 
            
        keys = pygame.key.get_pressed() 
        
        if keys[pygame.K_LEFT] and player.x - player_velocity >= 0: 
            player.x -= player_velocity 
        if keys[pygame.K_RIGHT] and player.x + player_velocity + player_width <= window_width: 
            player.x += player_velocity 
        if keys[pygame.K_DOWN] and player.y + player_velocity + player_height <= window_height: 
            player.y += player_velocity 
        if keys[pygame.K_UP] and player.y - player_velocity >= 0: 
            player.y -= player_velocity 
            
        for projectile in projectiles[:]: 
            projectile.y += projectile_velocity 
            if projectile.y > window_height: 
                projectiles.remove(projectile) 
            elif projectile.y >= player.y and projectile.colliderect(player): 
                projectiles.remove(projectile) 
                hit = True 
                break 
                
        if hit: 
            if projectiles_cooldown > 150: 
                lost_text = font.render("You Lost!", 1, "#0000FF") 
                window.blit(lost_text, (window_width/2 - lost_text.get_width()/2, window_height/2 - lost_text.get_height()/2)) 
                pygame.display.update() 
                pygame.time.delay(1500) 
            else: 
                lost_text = font.render("You Won!", 1, "#FF0000")
                window.blit(lost_text, (window_width/2 - lost_text.get_width()/2, window_height/2 - lost_text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2500)
            break
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
                
        draw(player, elapsed_time, projectiles, projectiles_cooldown, projectile_velocity)
        
    pygame.quit()

if __name__ == "__main__":
    main()
