import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Button Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)

# Fonts
font = pygame.font.Font(None, 40)

# Button properties
button_text = "Click Me"
button_action_message = "Button was clicked!"

# Create a Rect object for the button
button_rect = pygame.Rect(300, 250, 200, 100) # x, y, width, height

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                if button_rect.collidepoint(event.pos):
                    print(button_action_message)

    # Get mouse position for hover effect
    mouse_pos = pygame.mouse.get_pos()

    # Clear the screen
    screen.fill(WHITE)

    # Draw the button with hover effect
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        
    # Render and blit the button text
    text_surface = font.render(button_text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
