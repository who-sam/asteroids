import pygame
import sys
import random

# Initialize Pygame
pygame.init()
# Optionally initialize mixer for sound effects
try:
    pygame.mixer.init()
except Exception as e:
    print("Warning: pygame.mixer failed to initialize:", e)

# Screen resolution
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids - Main Menu")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Colors
BG_COLOR = (10, 10, 30)        # Dark blue background
STAR_COLOR = (255, 255, 255)   # White stars
TITLE_COLOR = (255, 255, 100)  # Yellowish title
BUTTON_TEXT_COLOR = (255, 255, 255)  # White text for buttons

# Define a simple Button class for the menu buttons
class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.text = text
        # Pre-render the text surface for efficiency
        self.text_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def update(self, mouse_pos):
        # Change color on hover
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.base_color

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.callback:
            self.callback()

# Callback functions for button actions
def start_game():
    print("Start button clicked - launching game...")

def show_leaderboard():
    print("Leaderboard button clicked - showing leaderboard...")

def exit_game():
    pygame.quit()
    sys.exit()

# Load sounds (place sound files in same directory or adjust path)
try:
    click_sound = pygame.mixer.Sound("click.wav")
except Exception as e:
    click_sound = None
    print("Warning: click sound not loaded:", e)

# (Optional) Play background music in a loop
try:
    pygame.mixer.music.load("retro_bg_music.mp3")
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Warning: background music not loaded:", e)

# Fonts
# Try to use a retro pixel font; fallback to system font if not available
try:
    title_font = pygame.font.Font("PressStart2P.ttf", 80)
except:
    title_font = pygame.font.SysFont("couriernew", 80)
    print("Warning: 'PressStart2P.ttf' not found, using 'couriernew'")

try:
    button_font = pygame.font.Font("PressStart2P.ttf", 50)
except:
    button_font = pygame.font.SysFont("couriernew", 50)
    print("Warning: 'PressStart2P.ttf' not found for buttons, using 'couriernew'")

# Create buttons with position, size, text, colors, and callback
button_width = 300
button_height = 70
button_x = (SCREEN_WIDTH - button_width) // 2
button_start_y = 300
button_gap = 100

# Define base and hover colors for buttons (neon style)
button_colors = [
    ((0, 100, 0), (0, 255, 0)),   # Start: dark green, bright green
    ((0, 0, 150), (0, 150, 255)), # Leaderboard: dark blue, bright cyan
    ((100, 0, 0), (255, 0, 0)),   # Exit: dark red, bright red
]

buttons = []
buttons.append(Button(button_x, button_start_y, button_width, button_height,
                      "START", button_font, button_colors[0][0], button_colors[0][1], start_game))
buttons.append(Button(button_x, button_start_y + button_gap, button_width, button_height,
                      "LEADERBOARD", button_font, button_colors[1][0], button_colors[1][1], show_leaderboard))
buttons.append(Button(button_x, button_start_y + 2*button_gap, button_width, button_height,
                      "EXIT", button_font, button_colors[2][0], button_colors[2][1], exit_game))

# Generate random star field (with blinking effect)
stars = []
num_stars = 100
for _ in range(num_stars):
    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(0, SCREEN_HEIGHT)
    # Each star has an 'on' state
    stars.append([x, y, True])

# Main loop for the dashboard
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Update button hover states
            for button in buttons:
                button.update(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        # Play click sound if available
                        if click_sound:
                            click_sound.play()
                        button.check_click(mouse_pos)

    # Draw background (stars)
    screen.fill(BG_COLOR)
    # Draw and update stars (simulate blinking)
    for star in stars:
        x, y, visible = star
        if visible:
            pygame.draw.circle(screen, STAR_COLOR, (x, y), 2)
        # Randomly toggle star visibility for blink effect
        if random.random() < 0.005:
            star[2] = not star[2]

    # Draw title text at top center
    title_surf = title_font.render("ASTEROIDS", True, TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, 100))
    screen.blit(title_surf, title_rect)

    # Draw all buttons
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

