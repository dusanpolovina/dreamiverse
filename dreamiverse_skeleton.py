import pygame
import sys

pygame.init()

# Font for displaying text
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((900,600))

# info = pygame.display.Info()
# fullscreen = False
# screen = pygame.display.set_mode(
#     (info.current_w, info.current_h), pygame.FULLSCREEN
# )

pygame.display.set_caption("Dreamiverse Display")
clock = pygame.time.Clock()

#constants
TILESIZE = 32
ENEMYSIZE = 64

# Health system
player_health = 3  # Start with 3 hearts
max_health = 3

# Health system
player_health = 3  # Start with 3 hearts
max_health = 3

#floor_image
floor_image = pygame.image.load("floor_level1.png").convert_alpha()
floor_image = pygame.transform.scale(floor_image, (900, 100))
floor_rect = floor_image.get_rect(bottomleft = (0,screen.get_height()))

#PLAYER
PLAYER_W = int(TILESIZE * 1.5)  # 48px wide
PLAYER_H = int(TILESIZE * 2.5)  # 80px tall
player_image = pygame.image.load("run_frame_1.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_W, PLAYER_H))
player_image_original = player_image

# Run animation frames (right-facing, then pre-flipped for left)
run_frames_right = [
    pygame.transform.scale(pygame.image.load("run_frame_1.png").convert_alpha(), (PLAYER_W, PLAYER_H)),
    pygame.transform.scale(pygame.image.load("run_frame_2.png").convert_alpha(), (PLAYER_W, PLAYER_H)),
    pygame.transform.scale(pygame.image.load("run_frame_3.png").convert_alpha(), (PLAYER_W, PLAYER_H)),
]
run_frames_left = [pygame.transform.flip(f, True, False) for f in run_frames_right]

# Animation state
anim_frame = 0
anim_timer = 0
anim_speed = 8  # game ticks between frame changes

player_rect = player_image.get_rect(center=(screen.get_width() / 2,
                                    screen.get_height() -
                                    floor_image.get_height() -
                                    player_image.get_height() / 2
                                    )
                                    )
# player_rect.inflate_ip(-128, -128)
# player_rect.x += 0  # Move right (use negative to move left)
# player_rect.y += 0  # Move down (use negative to move up)

# Player physics variables
player_vel_x = 0
player_vel_y = 0
speed = 5
jump_speed = -22.5# Negative because up is negative in pygame
gravity = 1       # Pulls player down each frame

#ENEMY - Load all animation frames
# Load enemy images
enemy_stationary_img = pygame.image.load("enemy_noattack_2.png").convert_alpha()
enemy_look_left_img = pygame.image.load("enemy_leftlook_2_sized.png").convert_alpha()  
enemy_attack_left_img = pygame.image.load("enemy_leftattack_2_sized.png").convert_alpha()

# Scale all enemy images
enemy_stationary_img = pygame.transform.scale(enemy_stationary_img, (ENEMYSIZE, ENEMYSIZE*2))
enemy_look_left_img = pygame.transform.scale(enemy_look_left_img, (ENEMYSIZE, ENEMYSIZE*2))

# Attack images need more width for the sword - make them wider!
enemy_attack_left_img = pygame.transform.scale(enemy_attack_left_img, (int(ENEMYSIZE*1.5), ENEMYSIZE*2))

# Create flipped versions for right-facing
enemy_look_right_img = pygame.transform.flip(enemy_look_left_img, True, False)
enemy_attack_right_img = pygame.transform.flip(enemy_attack_left_img, True, False)

# Start with stationary image
enemy_image = enemy_stationary_img

enemy_rect = enemy_image.get_rect(center=(700,  # X position (700 pixels from left)
                                          screen.get_height() - 
                                          floor_image.get_height() - 
                                          enemy_image.get_height() / 2
                                          ))

# Enemy movement variables
enemy_speed = 2              # How fast enemy moves
enemy_direction = -1         # -1 = left, 1 = right
enemy_patrol_left = 600      # Left boundary
enemy_patrol_right = 800     # Right boundary
attack_range = 150           # Distance at which enemy attacks

# Ground is where the player's feet should be (their starting position)
ground_y = player_rect.bottom
facing_right = True

on_ground = True
running = True
game_over = False  # Track if game is over

def jump():
    global player_vel_y, on_ground
    if on_ground:
        player_vel_y = jump_speed
        on_ground = False

def update():
    global player_vel_y, on_ground, player_image, facing_right, enemy_direction, player_health, game_over, enemy_image, anim_frame, anim_timer
    
    # Handle left/right movement
    keys = pygame.key.get_pressed()
    moving = False

    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
        facing_right = False
        moving = True

    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
        facing_right = True
        moving = True

    # Pick frame list based on direction
    frames = run_frames_right if facing_right else run_frames_left

    if not on_ground:
        # In the air — show jump pose (run_frame_3)
        player_image = frames[2]
    elif moving:
        # Running — cycle through frames
        anim_timer += 1
        if anim_timer >= anim_speed:
            anim_timer = 0
            anim_frame = (anim_frame + 1) % len(frames)
        player_image = frames[anim_frame]
    else:
        # Standing still — reset to idle image
        anim_frame = 0
        anim_timer = 0
        player_image = player_image_original if facing_right else pygame.transform.flip(player_image_original, True, False)
    
    # Apply gravity (always pulling down)
    player_vel_y += gravity
    
    # Move player vertically based on velocity
    player_rect.y += player_vel_y
    
    # Check if player hit the ground
    if player_rect.bottom >= ground_y:
        player_rect.bottom = ground_y  # Place player exactly on ground
        player_vel_y = 0               # Stop falling
        on_ground = True               # Now can jump again
    else:
        on_ground = False              # In the air

    # Keep player on screen (boundaries)
    if player_rect.left < 0:
        player_rect.left = 0  # Stop at left edge
    if player_rect.right > screen.get_width():
        player_rect.right = screen.get_width()  # Stop at right edge

    # Enemy movement (patrol)
    enemy_rect.x += enemy_speed * enemy_direction
    
    # Turn around at patrol boundaries
    if enemy_rect.left <= enemy_patrol_left:
        enemy_direction = 1  # Go right
    if enemy_rect.right >= enemy_patrol_right:
        enemy_direction = -1  # Go left
    
    # Enemy animation - change image based on player distance and direction
    distance_to_player = abs(player_rect.centerx - enemy_rect.centerx)
    
    if distance_to_player <= attack_range:
        # Player is close - show attack animation
        if enemy_direction == -1:  # Facing left
            enemy_image = enemy_attack_left_img
        else:  # Facing right
            enemy_image = enemy_attack_right_img
    else:
        # Player is far - show walking animation
        if enemy_direction == -1:  # Moving left
            enemy_image = enemy_look_left_img
        else:  # Moving right
            enemy_image = enemy_look_right_img

    # Check collision between player and enemy
    if player_rect.colliderect(enemy_rect):
        player_health -= 1  # Lose one heart
        print(f"Hit! Health: {player_health}")
        
        # Reset player position
        player_rect.x = screen.get_width() / 2
        player_rect.y = ground_y - player_rect.height
        player_vel_y = 0
        
        # Check if game over
        if player_health <= 0:
            game_over = True
            print("Game Over!")

def draw():
    screen.fill("lightblue")
    screen.blit(floor_image, floor_rect)
    screen.blit(enemy_image, enemy_rect)
    screen.blit(player_image, player_rect)
    
    # Draw hearts as red circles in top-left corner
    for i in range(player_health):
        pygame.draw.circle(screen, (255, 0, 0), (20 + i * 30, 25), 10)  # Red filled circles
    
    #pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)    # player rect (red)
    #pygame.draw.rect(screen, (0, 255, 0), enemy_rect, 2)     # enemy rect (green)

def draw_game_over():
    # Semi-transparent dark overlay
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(200)  # 0 = transparent, 255 = opaque
    overlay.fill((0, 0, 0))  # Black
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_font = pygame.font.Font(None, 72)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 50))
    screen.blit(game_over_text, game_over_rect)
    
    # Instructions text
    instruction_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    instruction_rect = instruction_text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + 50))
    screen.blit(instruction_text, instruction_rect)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game_over:
                # Game over screen controls
                if event.key == pygame.K_r:
                    # Restart game
                    player_health = max_health
                    game_over = False
                    player_rect.x = screen.get_width() / 2
                    player_rect.y = ground_y - player_rect.height
                    player_vel_y = 0
                elif event.key == pygame.K_q:
                    # Quit game
                    running = False
            else:
                # Normal game controls
                if event.key == pygame.K_SPACE:
                    jump()

    # Only update game if not game over
    if not game_over:
        update()
    
    draw()
    
    # Draw game over screen on top
    if game_over:
        draw_game_over()

    clock.tick(60)
    pygame.display.update()

    

