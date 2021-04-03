import pygame

from pygame.locals import (
    K_ESCAPE
)

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    # Un rectangulo donde llenar cosas
    surf = pygame.Surface((200, 200))
    surf_center = (
        (SCREEN_WIDTH/2)-(surf.get_width() /2),
        (SCREEN_HEIGHT/2)-(surf.get_height() /2)
    )
    # Give the surface a color to separate it from the background
    surf.fill((0, 0, 0))
    surf_face_color = (255,0,0)
    # Circle in surf: surf, color, position of circle center (relative to surf), radius
    pygame.draw.circle(surf, surf_face_color, (surf.get_width()/ 2, surf.get_height()), surf.get_width() / 2)
    pygame.draw.circle(surf, surf_face_color, (surf.get_width() / 4, surf.get_height() / 4), surf.get_width() / 10)
    pygame.draw.circle(surf, surf_face_color, ((surf.get_width() / 4) * 3, surf.get_height() / 4), surf.get_width() / 10)
    # Flip the display
    
    screen.blit(surf, surf_center)
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()