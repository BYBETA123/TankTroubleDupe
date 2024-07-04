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
textP1Turret = TextBox(tileSize*2, 350, font='Courier New',fontSize=26, text="Sidewinder", textColor=(255,255,255))
buttonList.append(textP1Turret)
rArrowP1Turret = Button((0,0,0), (0,0,255), tileSize*2 + textP1Turret.getWidth(), 350, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP1Turret)

lArrowP1Hull = Button((0,0,0), (0,0,255), tileSize, 425, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP1Hull)
textP1Hull = TextBox(tileSize*2, 425, font='Courier New',fontSize=26, text="Cicada", textColor=(255,255,255))
buttonList.append(textP1Hull)
rArrowP1Hull = Button((0,0,0), (0,0,255), tileSize*2 + textP1Turret.getWidth(), 425, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP1Hull)

lArrowP1Colour = Button((0,0,0), (0,0,255), tileSize, 500, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP1Colour)
textP1Colour = TextBox(tileSize*2, 500, font='Courier New',fontSize=26, text="Red", textColor=(255,255,255))
buttonList.append(textP1Colour)
rArrowP1Colour = Button((0,0,0), (0,0,255), tileSize*2 + textP1Turret.getWidth(), 500, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP1Colour)

rArrowP2Turret = Button((0,0,0), (0,0,255), SCREEN_WIDTH-tileSize*2, 350, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP2Turret)
textP2Turrent = TextBox(SCREEN_WIDTH - tileSize*2 - textP1Turret.getWidth(), 350, font='Courier New',fontSize=26, text="Sidewinder", textColor=(255,255,255))
buttonList.append(textP2Turrent)
lArrowP2Turret = Button((0,0,0), (0,0,255), SCREEN_WIDTH - tileSize*3 - textP1Turret.getWidth(), 350, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP2Turret)

rArrowP2Hull = Button((0,0,0), (0,0,255),  SCREEN_WIDTH-tileSize*2, 425, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP2Hull)
textP2Hull = TextBox(SCREEN_WIDTH - tileSize*2 - textP1Turret.getWidth(), 425, font='Courier New',fontSize=26, text="Cicada", textColor=(255,255,255))
buttonList.append(textP2Hull)
lArrowP2Hull = Button((0,0,0), (0,0,255), SCREEN_WIDTH - tileSize*3 - textP1Turret.getWidth(), 425, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP2Hull)

rArrowP2Colour = Button((0,0,0), (0,0,255),  SCREEN_WIDTH-tileSize*2, 500, tileSize, tileSize, '>', (255, 255, 255), 50)
buttonList.append(rArrowP2Colour)
textP3Colour = TextBox(SCREEN_WIDTH - tileSize*2 - textP1Turret.getWidth(), 500, font='Courier New',fontSize=26, text="Red", textColor=(255,255,255))
buttonList.append(textP3Colour)
lArrowP2Colour = Button((0,0,0), (0,0,255), SCREEN_WIDTH - tileSize*3 - textP1Turret.getWidth(), 500, tileSize, tileSize, '<', (255, 255, 255), 50)
buttonList.append(lArrowP2Colour)

# Player names
textP1 = TextBox(tileSize*2, tileSize*1.5, font='Courier New',fontSize=26, text="Player 1", textColor=(255,255,255))
buttonList.append(textP1)
textP2 = TextBox(SCREEN_WIDTH - tileSize*2 - textP1Turret.getWidth(), tileSize*1.5, font='Courier New',fontSize=26, text="Player 2", textColor=(255,255,255))
buttonList.append(textP2)







turretList = ["Sidewinder", "Avalanche", "Bucket", "Judge", "Boxer", "Huntsman", "Chamber", "Silencer", "Watcher"]
hullList = ["Cicada", "Panther", "Gater", "Bonsai", "Fossil"]

turretListLength = len(turretList)
hullListLength = len(hullList)

#List indexes for player selection
p1I = 0
p2I = 0
p1J = 0
p2J = 0

rectX = 20
rectY = 13



def checkButtons(mouse):
    global p1I, p2I, p1J, p2J
    if lArrowP1Turret.ButtonClick(mouse):
        p1I = (p1I - 1) % turretListLength
        textP1Turret.setText(turretList[p1I])
    if rArrowP1Turret.ButtonClick(mouse):
        p1I = (p1I + 1) % turretListLength
        textP1Turret.setText(turretList[p1I])
    if lArrowP1Hull.ButtonClick(mouse):
        p1J = (p1J - 1) % hullListLength
        textP1Hull.setText(hullList[p1J])
    if rArrowP1Hull.ButtonClick(mouse):
        p1J = (p1J + 1) % hullListLength
        textP1Hull.setText(hullList[p1J])
    if lArrowP2Turret.ButtonClick(mouse):
        p2I = (p2I - 1) % turretListLength
        textP2Turrent.setText(turretList[p2I])
    if rArrowP2Turret.ButtonClick(mouse):
        p2I = (p2I + 1) % turretListLength
        textP2Turrent.setText(turretList[p2I])
    if lArrowP2Hull.ButtonClick(mouse):
        p2J = (p2J - 1) % hullListLength
        textP2Hull.setText(hullList[p2J])
    if rArrowP2Hull.ButtonClick(mouse):
        p2J = (p2J + 1) % hullListLength
        textP2Hull.setText(hullList[p2J])




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                textP1Turret.setText(turretList[p1I])
                textP2Turrent.setText(turretList[p2I])
                textP1Hull.setText(hullList[p1J])
                textP2Hull.setText(hullList[p2J])
                checkButtons(pygame.mouse.get_pos())
                # for button in buttonList:
                #     if button.ButtonClick(pygame.mouse.get_pos()):
                #         print(button.text)
                #         button.clicked = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_i:
                print(pygame.mouse.get_pos())
            if event.key == pygame.K_UP:
                rectY -= 13
                rectX -= 20
                print(rectX, rectY)
            if event.key == pygame.K_DOWN:
                rectY += 13
                rectX += 20
                print(rectX, rectY)
            if event.key == pygame.K_LEFT:
                pass                
            if event.key == pygame.K_RIGHT:
                pass

    # Clear screen with the chosen soft white color
    screen.fill((250,250,240))
    for button in buttonList:
        button.draw(screen, outline = False)
    # Update display
    # pygame.draw.rect(screen, (0, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], rectX, rectY), 0)
    pygame.draw.rect(screen, (0, 0, 0), (tileSize*2 + textP1Turret.getWidth()//2-50, 150, 100, 65)) #p1 display
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH - tileSize*2 - textP1Turret.getWidth()//2 - 50, 150, 100, 65)) #p2 display

    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()