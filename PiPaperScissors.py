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

# Load background image
background_img = pygame.image.load('background_image.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Load emoji images
rock_img = pygame.image.load('rock_emoji.png')
paper_img = pygame.image.load('paper_emoji.png')
scissors_img = pygame.image.load('scissors_emoji.png')

# Item properties
item_size = 20
num_items = 25
move_speed = 2
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

# Arena boundaries
arena_margin = 50
left_bound = arena_margin
right_bound = screen_width - arena_margin - item_size
top_bound = arena_margin
bottom_bound = screen_height - arena_margin - item_size

# Generate random items with random movement directions, within arena bounds
items = []
for _ in range(num_items):
    item_type = random.choice(["rock", "paper", "scissors"])
    x = random.randint(left_bound, right_bound)
    y = random.randint(top_bound, bottom_bound)
    x_move = random.choice([-move_speed, move_speed])
    y_move = random.choice([-move_speed, move_speed])
    items.append([item_type, x, y, x_move, y_move])

# Function to calculate attraction between items
def calculate_attraction(item1, item2):
    dx = item2[1] - item1[1]
    dy = item2[2] - item1[2]
    distance = max(abs(dx), abs(dy), 1)  # Prevent division by zero

    # Attraction adjustment near edges
    edge_proximity = 50  # Distance from edge to start reducing attraction
    edge_reduction_factor = 0.5 if min(item1[1], item1[2], screen_width - item1[1], screen_height - item1[2]) < edge_proximity else 1

    # Only consider attraction for similar items and within a certain range
    if item1[0] == item2[0] and distance < 100:
        # Reduce or reverse attraction if too close
        if distance < item_size * 2:
            return -dx / distance * attraction_strength * edge_reduction_factor, -dy / distance * attraction_strength * edge_reduction_factor
        else:
            return dx / distance * attraction_strength * edge_reduction_factor, dy / distance * attraction_strength * edge_reduction_factor

    return 0, 0

# Function to cap the speed of an item
def cap_speed(x_move, y_move, max_speed):
    speed = (x_move**2 + y_move**2)**0.5  # Calculate the current speed
    if speed > max_speed:
        scale = max_speed / speed
        return x_move * scale, y_move * scale
    return x_move, y_move

# Function to render text
def render_text(message, font_size, color, x, y):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

# Variable to store the winning type
winner_type = None

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(background_img, (0, 0))

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

        # Enhanced edge bounce logic
        if item1[1] + item1[3] < left_bound or item1[1] + item1[3] > right_bound:
            item1[3] = -item1[3]
        item1[1] += item1[3]

        if item1[2] + item1[4] < top_bound or item1[2] + item1[4] > bottom_bound:
            item1[4] = -item1[4]
        item1[2] += item1[4]

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

    # Check for a winner if not already determined
    if not winner_type:
        types = set(item[0] for item in items)
        if len(types) == 1:
            winner_type = types.pop()

    # Update the display
    pygame.display.flip()

    # If there's a winner, display the winning message
    if winner_type:
        screen.fill((0, 0, 0))  # Optional: Clear the screen
        render_text(f"{winner_type.upper()} WINS!", 60, (255, 255, 255), screen_width // 2, screen_height // 2)
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing
        break

# Quit Pygame
pygame.quit()
sys.exit()
