import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
PLAYER_SIZE = 70
STARTING_HEIGHT = 330  # Adjust this value to set the starting height

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Penguin Game")

# Load the background image
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load the penguin images
player_image1 = pygame.image.load("penguin2.png")
player_image1 = pygame.transform.scale(player_image1, (PLAYER_SIZE, PLAYER_SIZE))
player_image2 = pygame.image.load("penguin1.png")
player_image2 = pygame.transform.scale(player_image2, (PLAYER_SIZE, PLAYER_SIZE))

# Load the coin, fish, and skull images
coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (30, 30))  # Adjust the size as needed
fish_image = pygame.image.load("fish.png")
fish_image = pygame.transform.scale(fish_image, (40, 40))  # Adjust the size as needed
skull_image = pygame.image.load("skull.png")
skull_image = pygame.transform.scale(skull_image, (40, 40))  # Adjust the size as needed

# Create the player with the starting height
player = pygame.Rect(50, STARTING_HEIGHT, PLAYER_SIZE, PLAYER_SIZE)  # Adjust the starting height here

# Variables
player_speed = 5  # Increase player speed for smoother movement
jump_power = 30  # Adjust jump power for better gameplay
gravity = 1
is_jumping = False

# Falling objects variables
falling_objects = []
spawn_chance = 2  # Adjust the spawn chance as needed
score = 0
game_over = False

# Use a boolean to track the current image state
use_alternate_image = False

# Initialize the mixer module
pygame.mixer.init()

# Load the background music
pygame.mixer.music.load("background_music.mp3")

# Load the sound effects
coin_sound = pygame.mixer.Sound("coin_sound.mp3")
fish_sound = pygame.mixer.Sound("fish_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over_sound.mp3")


# Play the background music (loop indefinitely)
pygame.mixer.music.play(-1)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Check for Enter key
                # Toggle between the two images
                use_alternate_image = not use_alternate_image

    keys = pygame.key.get_pressed()

    # Move the player
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed

    # Jumping mechanics
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            player.y -= jump_power
    else:
        player.y += gravity

        # Check for collision with the ground
        if player.y >= HEIGHT - PLAYER_SIZE:
            is_jumping = False
            player.y = HEIGHT - PLAYER_SIZE

    # Spawn objects (coins, fish, skulls)
    if random.randint(1, 100) < spawn_chance:
        choice = random.choice(["coin", "fish", "skull"])
        if choice == "coin":
            coin = pygame.Rect(random.randint(0, WIDTH - 30), 0, 30, 30)
            falling_objects.append((coin, coin_image))
        elif choice == "fish":
            fish = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
            falling_objects.append((fish, fish_image))
        else:
            skull = pygame.Rect(random.randint(0, WIDTH - 40), 0, 40, 40)
            falling_objects.append((skull, skull_image))

    # Update positions of falling objects and check for collisions
    for obj, obj_image in falling_objects:
        obj.y += 2  # Adjust the falling speed as needed
        if player.colliderect(obj):
            if obj_image == coin_image:
                score += 1  # Increase the score when the penguin collects a coin
                coin_sound.play()
            elif obj_image == fish_image:
                score += 5  # Increase the score when the penguin collects a fish
                fish_sound.play()
            elif obj_image == skull_image:
                game_over = True  # Game over if the penguin hits a skull
                game_over_sound.play()
            falling_objects.remove((obj, obj_image))

    # Remove objects that have gone off the screen
    falling_objects = [(obj, obj_image) for obj, obj_image in falling_objects if obj.y < HEIGHT]

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the falling objects
    for obj, obj_image in falling_objects:
        screen.blit(obj_image, obj)

    # Draw the appropriate player image
    if use_alternate_image:
        screen.blit(player_image1, player)
    else:
        screen.blit(player_image2, player)

    # Draw the score on the screen
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Check for game over condition
    if game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text,
                    (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting
        running = False

    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# When the game ends (e.g., game over), stop the background music
pygame.mixer.music.stop()

# Quit the game
pygame.quit()
sys.exit()
