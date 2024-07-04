import pygame
from UIUtility import Button
# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop
running = True
clock = pygame.time.Clock()
buttonList = []
homeButton = Button((0,0,0), (0,0,255), 50, 50, 50, 50, 'back', (255, 255, 255))
buttonList.append(homeButton)
lArrowP1Turret = Button((0,0,0), (0,0,255), 100, 100, 50, 50, '<', (255, 255, 255), 50)
buttonList.append(lArrowP1Turret)





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttonList:
                    if button.ButtonClick(pygame.mouse.get_pos()):
                        button.clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # Clear screen with the chosen soft white color
    screen.fill((255,0,0))
    for button in buttonList:
        button.draw(screen, outline = False)
    # Update display
    pygame.display.flip()

    if pygame.mouse.get_pressed()[0]:
        pass
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
