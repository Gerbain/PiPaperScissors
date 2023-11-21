import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rock Paper Scissors Game')

# Load emoji images
rock_img = pygame.image.load('rock_emoji.png')
paper_img = pygame.image.load('paper_emoji.png')
scissors_img = pygame.image.load('scissors_emoji.png')

# Item properties
item_size = 20
num_items = 25
move_speed = 1
attraction_strength = 0.05
max_speed = 3

# Resize images
rock_img = pygame.transform.scale(rock_img, (item_size, item_size))
paper_img = pygame.transform.scale(paper_img, (item_size, item_size))
scissors_img = pygame.transform.scale(scissors_img, (item_size, item_size))

# Item images dictionary
ITEM_IMAGES = {
    "rock": rock_img,
    "paper": paper_img,
    "scissors": scissors_img
}

# Game logic for rock-paper-scissors
def rps_winner(item1, item2):
    if (item1 == "rock" and item2 == "scissors") or \
       (item1 == "scissors" and item2 == "paper") or \
       (item1 == "paper" and item2 == "rock"):
        return item1
    else:
        return item2

# Generate random items with random movement directions
items = []
for _ in range(num_items):
    item_type = random.choice(["rock", "paper", "scissors"])
    x = random.randint(0, screen_width - item_size)
    y = random.randint(0, screen_height - item_size)
    x_move = random.choice([-move_speed, move_speed])
    y_move = random.choice([-move_speed, move_speed])
    items.append([item_type, x, y, x_move, y_move])

# Function to calculate attraction between items
def calculate_attraction(item1, item2):
    dx = item2[1] - item1[1]
    dy = item2[2] - item1[2]
    distance = max(abs(dx), abs(dy), 1)  # Prevent division by zero

    # Only consider attraction for similar items and within a certain range
    if item1[0] == item2[0] and distance < 100:
        # Reduce or reverse attraction if too close
        if distance < item_size * 2:
            return -dx / distance * attraction_strength, -dy / distance * attraction_strength
        else:
            return dx / distance * attraction_strength, dy / distance * attraction_strength

    return 0, 0

# Function to cap the speed of an item
def cap_speed(x_move, y_move, max_speed):
    speed = (x_move**2 + y_move**2)**0.5  # Calculate the current speed
    if speed > max_speed:
        scale = max_speed / speed
        return x_move * scale, y_move * scale
    return x_move, y_move

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Move and draw items
    for i, item1 in enumerate(items):
        attraction_x, attraction_y = 0, 0

        # Calculate attraction to other items
        for j, item2 in enumerate(items):
            if i != j:
                ax, ay = calculate_attraction(item1, item2)
                attraction_x += ax
                attraction_y += ay

        # Update movement based on attraction
        item1[3] += attraction_x
        item1[4] += attraction_y

        # Cap the speed
        item1[3], item1[4] = cap_speed(item1[3], item1[4], max_speed)

        # Update x and y position
        item1[1] += item1[3]
        item1[2] += item1[4]

        # Bounce off the edges
        if item1[1] < 0 or item1[1] > screen_width - item_size:
            item1[3] = -item1[3]
        if item1[2] < 0 or item1[2] > screen_height - item_size:
            item1[4] = -item1[4]

        # Draw item
        screen.blit(ITEM_IMAGES[item1[0]], (item1[1], item1[2]))

    # Check for collisions and update items
    for i, item1 in enumerate(items):
        for j, item2 in enumerate(items):
            if i != j:
                # Check if items collide
                if pygame.Rect(item1[1], item1[2], item_size, item_size).colliderect((item2[1], item2[2], item_size, item_size)):
                    # Determine the winner and update the losing item
                    winner = rps_winner(item1[0], item2[0])
                    if item1[0] != winner:
                        item1[0] = winner
                    elif item2[0] != winner:
                        item2[0] = winner

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

