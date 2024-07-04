import pygame
import os
from UIUtility import Button
pygame.init()
#Menu and selection screen
windowWidth = 800
windowHeight = 600

screen = pygame.display.set_mode((windowWidth,windowHeight))
running = True

clock = pygame.time.Clock()
buttonList = []
playButton = Button((0, 0, 0), (0, 0, 255), 150, 400, 175, 70, 'Play', (255, 255, 255), hoverColor=(100, 100, 255))
settingsButton = Button((0, 0, 0), (0, 0, 255), 475, 400, 175, 70, 'Settings', (255, 255, 255), hoverColor=(100, 100, 255))
quitButton = Button((0, 0, 0), (0, 0, 255), 10, 10, 130, 50, 'Quit', (255, 255, 255), hoverColor=(100, 100, 255))
buttonList.append(playButton)
buttonList.append(settingsButton)
buttonList.append(quitButton)
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttonList:
                    if button.ButtonClick(pygame.mouse.get_pos()):
                        print('Hello')
                        button.clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear screen with the chosen color
    screen.fill((255, 0, 0))

    # Handle hover effect and draw buttons
    mouse_pos = pygame.mouse.get_pos()
    for button in buttonList:
        button.update_display(mouse_pos)
        button.draw(screen, outline=True)
    
    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

