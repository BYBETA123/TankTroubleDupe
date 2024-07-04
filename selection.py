import pygame
from UIUtility import Button, TextBox
# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
tileSize = 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop
running = True
clock = pygame.time.Clock()
buttonList = []
homeButton = Button((0,0,0), (0,0,255), tileSize//4, tileSize//4, tileSize, tileSize, 'back', (255, 255, 255))
buttonList.append(homeButton)


lArrowP1Turret = Button((0,0,0), (0,0,255), tileSize, 350, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP1Turret)
textP1Turret = TextBox(tileSize*2, 350, font='Courier New',fontSize=26, text="Sidewinder")
buttonList.append(textP1Turret)
rArrowP1Turret = Button((0,0,0), (0,0,255), tileSize*2 + textP1Turret.getWidth(), 350, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP1Turret)

lArrowP1Hull = Button((0,0,0), (0,0,255), tileSize, 425, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP1Hull)
textP1Hull = TextBox(tileSize*2, 425, font='Courier New',fontSize=26, text="Cicada")
buttonList.append(textP1Hull)
rArrowP1Hull = Button((0,0,0), (0,0,255), tileSize*2 + textP1Turret.getWidth(), 425, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP1Hull)

lArrowP1Colour = Button((0,0,0), (0,0,255), tileSize, 500, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP1Colour)
textP1Colour = TextBox(tileSize*2, 500, font='Courier New',fontSize=26, text="Red")
buttonList.append(textP1Colour)
rArrowP1Colour = Button((0,0,0), (0,0,255), tileSize*2 + textP1Turret.getWidth(), 500, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP1Colour)

lArrowP2Turret = Button((0,0,0), (0,0,255), SCREEN_WIDTH-tileSize, 350, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP2Turret)
textP2Turrent = TextBox(tileSize*2, 350, font='Courier New',fontSize=26, text="Sidewinder")
rArrowP2Turret = Button((0,0,0), (0,0,255), 750, 350, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP2Turret)

lArrowP2Hull = Button((0,0,0), (0,0,255), tileSize, 425, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP2Hull)
textP2Hull = TextBox(tileSize*2, 425, font='Courier New',fontSize=26, text="Cicada")
rArrowP2Hull = Button((0,0,0), (0,0,255), 750, 425, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP2Hull)

lArrowP2Colour = Button((0,0,0), (0,0,255), tileSize, 500, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP2Colour)
textP3Colour = TextBox(tileSize*2, 500, font='Courier New',fontSize=26, text="Red")
rArrowP2Colour = Button((0,0,0), (0,0,255), 750, 500, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP2Colour)

turretList = ["Avalanche", "Bucket", "Judge", "Boxer", "Huntsman", "Sidewinder", "Chamber", "Silencer", "Watcher"]
hullList = ["Cicada", "Panther", "Gater", "Bonsai", "Fossil"]

turretListLength = len(turretList)
hullListLength = len(hullList)

i=0
j=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                i = (i + 1) % turretListLength
                j = (j + 1) % hullListLength
                textP1Turret.setText(turretList[i])
                textP1Hull.setText(hullList[j])
                for button in buttonList:
                    if button.ButtonClick(pygame.mouse.get_pos()):
                        button.clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_i:
                print(pygame.mouse.get_pos())
    # Clear screen with the chosen soft white color
    screen.fill((255,0,0))
    for button in buttonList:
        button.draw(screen, outline = False)
    # Update display
    # pygame.draw.rect(screen, (0, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], tileSize, tileSize), 0)

    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
