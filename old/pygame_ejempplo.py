# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 500])

# Run until the user asks to quit
running = True
i = 0
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((i, i, i))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255-i), (i, 250), 75)

    # Flip the display
    pygame.display.flip()
    
    i = i+1
    if i > 255:
        i =0

# Done! Time to quit.
pygame.quit()
