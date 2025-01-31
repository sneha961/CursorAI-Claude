import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 900
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Racing")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
ROAD_COLOR = (64, 64, 64)  # Dark gray for asphalt
YELLOW_LINE = (255, 240, 60)  # Yellow for side lines
ROAD_EDGE_COLOR = (169, 169, 169)  # Light gray for road edges
SKY_COLOR = (135, 206, 235)  # Light blue for sky
TREE_COLOR = (46, 139, 87)    # Sea green for trees
TREE_DARK = (40, 100, 60)     # Darker green for shading
TRUNK_COLOR = (101, 67, 33)   # More natural brown for trunk
TRUNK_DARK = (86, 57, 28)     # Darker brown for trunk shading

# Add these constants after the color definitions
BUTTON_COLOR = (50, 200, 50)  # Green color for button
BUTTON_HOVER_COLOR = (70, 220, 70)  # Lighter green for hover effect
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Increase road width by 5% (original width was 400, 5% increase = 420)
ROAD_LEFT = WIDTH//2 - 210   # Changed from 200 to 210
ROAD_RIGHT = WIDTH//2 + 210  # Changed from 200 to 210

# Load car images after pygame initialization
PLAYER_CAR_IMG = pygame.image.load(os.path.join("images", "playerCar.png"))
NPC_CAR_IMG = pygame.image.load(os.path.join("images", "npcCar.png"))

# Resize images to larger dimensions (increased by 10% from 54x90 to 60x99)
PLAYER_CAR_IMG = pygame.transform.scale(PLAYER_CAR_IMG, (60, 99))
NPC_CAR_IMG = pygame.transform.scale(NPC_CAR_IMG, (60, 99))

# Load and scale background image after pygame initialization
# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))
background_path = os.path.join(current_dir, "images", "bkc.png")

try:
    print(f"Attempting to load background from: {background_path}")  # Debug print
    # Try different loading methods
    try:
        BACKGROUND_IMG = pygame.image.load(background_path).convert_alpha()  # Try with alpha channel
    except:
        BACKGROUND_IMG = pygame.image.load(background_path).convert()  # Try without alpha channel
    print("Successfully loaded background image")  # Debug print
    # Scale background to be taller for perspective effect
    BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (ROAD_LEFT, int(HEIGHT * 1.2)))  # Made taller
    USE_BACKGROUND_IMG = True
except Exception as e:
    print(f"Warning: Could not load background image. Error: {e}")
    USE_BACKGROUND_IMG = False

# Load tree image after pygame initialization
try:
    TREE_IMG = pygame.image.load(os.path.join("images", "tree.png"))
    # Convert and set initial scale for the tree image to a fixed size
    TREE_IMG = pygame.transform.scale(TREE_IMG, (80, 120))  # Fixed size for all trees
    USE_TREE_IMG = True
except Exception as e:
    print(f"Warning: Could not load tree image. Error: {e}")
    USE_TREE_IMG = False

# Add cloud color
CLOUD_COLOR = (255, 255, 255)  # White for clouds

# Add sun colors
SUN_COLOR = (255, 255, 0)  # Bright yellow
SUN_GLOW = (255, 255, 150)  # Light yellow for glow effect

# Add cloud class
class Cloud:
    def __init__(self, is_left_side):
        self.height = random.randint(100, 160)
        self.width = random.randint(25, 40)
        if is_left_side:
            self.x = random.randint(0, ROAD_LEFT - self.width - 10)  # Adjusted for new road width
        else:
            self.x = random.randint(ROAD_RIGHT + 10, WIDTH - self.width)  # Adjusted for new road width
        self.y = random.randint(-self.height, HEIGHT)
        self.is_left_side = is_left_side
        
    def move(self, speed):
        self.y += speed
        if self.y > HEIGHT:
            self.y = -self.height
            if self.is_left_side:
                self.x = random.randint(0, ROAD_LEFT - self.width - 10)
            else:
                self.x = random.randint(ROAD_RIGHT + 10, WIDTH - self.width)
            
    def draw(self, screen):
        # Draw a more elongated cloud shape
        pygame.draw.ellipse(screen, CLOUD_COLOR, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, CLOUD_COLOR, (self.x - self.width*0.2, self.y + self.height*0.3, 
                                                self.width*0.8, self.height*0.5))
        pygame.draw.ellipse(screen, CLOUD_COLOR, (self.x + self.width*0.1, self.y + self.height*0.4, 
                                                self.width*0.8, self.height*0.4))

# Create clouds for both sides
clouds = []
for _ in range(3):  # 3 clouds per side
    clouds.append(Cloud(True))  # Left side clouds
    clouds.append(Cloud(False))  # Right side clouds

# Player car
class PlayerCar:
    def __init__(self):
        self.width = 60  # Update to match new image width
        self.height = 99  # Update to match new image height
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 8
        self.image = PLAYER_CAR_IMG
        
    def move(self, direction):
        if direction == "left" and self.x > ROAD_LEFT:  # Changed boundary
            self.x -= self.speed
        if direction == "right" and self.x < ROAD_RIGHT - self.width:  # Changed boundary
            self.x += self.speed
        if direction == "up" and self.y > 0:
            self.y -= self.speed
        if direction == "down" and self.y < HEIGHT - self.height:
            self.y += self.speed
            
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Obstacle car
class ObstacleCar:
    def __init__(self):
        self.width = 60  # Update to match new image width
        self.height = 99  # Update to match new image height
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.width)  # Spawn within road boundaries
        self.y = -self.height
        self.speed = 5  # Increased from 3 to 5
        self.image = NPC_CAR_IMG
        
    def move(self):
        self.y += self.speed
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
    def off_screen(self):
        return self.y > HEIGHT

# Game setup
def reset_game():
    global player, obstacles, spawn_timer, score
    player = PlayerCar()
    obstacles = []
    spawn_timer = 0
    score = 0

reset_game()  # Initial game setup
game_over = False
clock = pygame.time.Clock()

# Add this function before the game loop
def draw_button(screen, text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)  # Return the button rectangle for click detection

# Add these variables after the game setup
line_spacing = 100  # Distance between lines
line_length = 50    # Length of each line
line_width = 10     # Width of each line
line_positions = [i for i in range(-line_length, HEIGHT + line_spacing, line_spacing)]  # Store y-positions of lines
line_speed = 5  # Speed at which lines move down

# Add these variables after game setup
tree_positions = []
# Initialize random tree positions
for i in range(8):  # Number of trees on each side
    # Random x-offset for left side trees
    left_x = random.randint(-280, -140)
    # Random x-offset for right side trees
    right_x = random.randint(20, 160)
    # Random y-spacing
    y_spacing = random.randint(150, 250)
    tree_positions.append((left_x, y_spacing))  # Left side tree
    tree_positions.append((right_x, y_spacing))  # Right side tree

# Improved tree drawing function with perspective scaling
def draw_tree(screen, x, y, scale=1.0):
    # Scale all dimensions based on perspective
    trunk_width = int(24 * scale)
    trunk_height = int(60 * scale)
    base_width = int(80 * scale)
    
    # Draw main trunk
    pygame.draw.rect(screen, TRUNK_COLOR, (x + int(8 * scale), y - int(10 * scale), trunk_width, trunk_height))
    pygame.draw.rect(screen, TRUNK_DARK, (x + int(8 * scale), y - int(10 * scale), int(8 * scale), trunk_height))
    
    # Draw tree layers (from bottom to top)
    for i in range(4):
        width = int((base_width - (i * 15 * scale)))  # Each layer gets narrower
        height = int((45 - (i * 5)) * scale)  # Each layer gets shorter
        
        # Calculate points for each triangular layer
        points = [
            (x + (base_width - width)//2, y - int(20 * scale) - int(i * 30 * scale)),
            (x + (base_width - width)//2 + width, y - int(20 * scale) - int(i * 30 * scale)),
            (x + base_width//2, y - int(50 * scale) - int(i * 30 * scale))
        ]
        
        # Draw main triangle
        pygame.draw.polygon(screen, TREE_COLOR, points)
        
        # Draw darker triangle for depth
        dark_points = [
            (x + (base_width - width)//2, y - int(20 * scale) - int(i * 30 * scale)),
            (x + base_width//2, y - int(20 * scale) - int(i * 30 * scale)),
            (x + base_width//2, y - int(50 * scale) - int(i * 30 * scale))
        ]
        pygame.draw.polygon(screen, TREE_DARK, dark_points)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle restart when game is over
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Press 'R' to restart
                game_over = False
                reset_game()
            
    # Only process game logic if not game over
    if not game_over:
        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_DOWN]:
            player.move("down")
            
        # Spawn obstacles
        spawn_timer += 1
        if spawn_timer > 45:  # Decreased from 60 to 45
            obstacles.append(ObstacleCar())
            spawn_timer = 0
            
        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.move()
            # Check collision
            if (obstacle.x < player.x + player.width and 
                obstacle.x + obstacle.width > player.x and
                obstacle.y < player.y + player.height and
                obstacle.y + obstacle.height > player.y):
                game_over = True
            
            # Remove off-screen obstacles
            if obstacle.off_screen():
                obstacles.remove(obstacle)
                score += 1
    
    # Drawing
    screen.fill(SKY_COLOR)
    
    # Draw sun (before clouds and trees)
    sun_radius = 30
    sun_x = WIDTH - 80  # Adjusted for narrower screen
    sun_y = 80
    
    # Draw sun glow
    pygame.draw.circle(screen, SUN_GLOW, (sun_x, sun_y), sun_radius + 8)
    pygame.draw.circle(screen, SUN_GLOW, (sun_x, sun_y), sun_radius + 4)
    # Draw main sun
    pygame.draw.circle(screen, SUN_COLOR, (sun_x, sun_y), sun_radius)
    
    # Update and draw clouds
    if not game_over:
        for cloud in clouds:
            cloud.move(line_speed * 0.7)
    for cloud in clouds:
        cloud.draw(screen)
    
    if USE_TREE_IMG:
        # Draw trees in straight lines
        tree_spacing = 150
        tree_offset = (pygame.time.get_ticks() * line_speed/1000) % tree_spacing if not game_over else 0
        
        # Draw trees from top to bottom
        for y in range(-100, HEIGHT + tree_spacing, tree_spacing):
            current_y = y + tree_offset
            
            # Left side trees (adjusted for wider road)
            screen.blit(TREE_IMG, (ROAD_LEFT - 100, current_y - 120))
            
            # Right side trees (adjusted for wider road)
            screen.blit(TREE_IMG, (ROAD_RIGHT + 20, current_y - 120))
    else:
        # Fallback to drawn trees if image loading fails
        tree_spacing = 150
        tree_offset = (pygame.time.get_ticks() * line_speed/1000) % tree_spacing if not game_over else 0
        
        for y in range(-100, HEIGHT + tree_spacing, tree_spacing):
            current_y = y + tree_offset
            
            # Left side trees (single line)
            draw_tree(screen, ROAD_LEFT - 140, current_y)
            
            # Right side trees (single line)
            draw_tree(screen, ROAD_RIGHT + 20, current_y)
    
    # Draw road shoulder/edges (light gray)
    pygame.draw.rect(screen, ROAD_EDGE_COLOR, (ROAD_LEFT - 15, 0, 15, HEIGHT))
    pygame.draw.rect(screen, ROAD_EDGE_COLOR, (ROAD_RIGHT, 0, 15, HEIGHT))
    
    # Draw the main road surface (dark gray)
    pygame.draw.rect(screen, ROAD_COLOR, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))
    
    # Draw yellow side lines
    pygame.draw.rect(screen, YELLOW_LINE, (ROAD_LEFT, 0, 4, HEIGHT))
    pygame.draw.rect(screen, YELLOW_LINE, (ROAD_RIGHT - 4, 0, 4, HEIGHT))
    
    # Update and draw moving white center lines only if game is not over
    if not game_over:
        for i in range(len(line_positions)):
            line_positions[i] += line_speed
            if line_positions[i] > HEIGHT:
                line_positions[i] = -line_length
    
    # Draw all center lines in white
    for pos in line_positions:
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - line_width//2, pos, line_width, line_length))

    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
        
    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render('Score: ' + str(score), True, BLACK)  # Changed from WHITE to BLACK
    screen.blit(score_text, (10, 10))
    
    # Display game over message and restart button
    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render('GAME OVER', True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        # Draw restart button
        button_x = WIDTH/2 - BUTTON_WIDTH/2
        button_y = HEIGHT/2 + 50
        
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        if button_rect.collidepoint(mouse_pos):
            restart_button = draw_button(screen, "RESTART", button_x, button_y, 
                                      BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_HOVER_COLOR)
        else:
            restart_button = draw_button(screen, "RESTART", button_x, button_y, 
                                       BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR)
        
        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if restart_button.collidepoint(event.pos):
                game_over = False
                reset_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
