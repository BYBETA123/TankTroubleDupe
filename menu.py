import pygame
import os
from UIUtility import Button

pygame.init()

# Menu and selection screen dimensions
windowWidth = 800
windowHeight = 600

screen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Tank Game Menu')  # Set the window title

running = True

clock = pygame.time.Clock()
homeButtonList = []

# Load the tank image
currentDir = os.path.dirname(__file__)
tankPath = os.path.join(currentDir, 'tank_menu_logo.png')
originalTankImage = pygame.image.load(tankPath).convert_alpha()



# Create buttons with specified positions and text
playButtonHome = Button((0, 0, 0), (0, 0, 255), 150, 400, 175, 70, 'Play', (255, 255, 255), 30, hoverColor=(100, 100, 255))
settingsButton = Button((0, 0, 0), (0, 0, 255), 475, 400, 175, 70, 'Settings', (255, 255, 255), 30, hoverColor=(100, 100, 255))
quitButtonHome = Button((0, 0, 0), (0, 0, 255), 10, 10, 130, 50, 'Quit', (255, 255, 255), 25, hoverColor=(100, 100, 255))

homeButtonList.append(playButtonHome)
homeButtonList.append(settingsButton)
homeButtonList.append(quitButtonHome)

# Define title text properties
titleFont = pygame.font.SysFont('Arial', 60)
titleText = titleFont.render('Tank Game Menu', True, (0, 0, 0))  # Render the title text

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in homeButtonList:
                    if button.buttonClick(pygame.mouse.get_pos()):
                        button.clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Clear screen with the chosen color
    screen.fill((255, 255, 255))



    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
