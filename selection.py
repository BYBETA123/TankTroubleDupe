import pygame
import os
from UIUtility import Button, TextBox
from ColorDictionary import ColorDicionary
# Initialize Pygame
c=ColorDicionary()

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
homeButton = Button(c.geT("BLACK"), c.geT("GREEN"), tileSize//4, tileSize//4, tileSize, tileSize, 'back', (255, 255, 255))
buttonList.append(homeButton)
buttonPrimary = c.geT("BLACK")
buttonSecondary = c.geT("WHITE")
buttonText = c.geT("WHITE")
optionText = c.geT("GREY")
#Hull and turret list
turretList = ["Sidewinder", "Avalanche", "Boxer", "Bucket", "Chamber", "Huntsman", "Silencer", "Judge", "Watcher"]
hullList = ["Panther", "Cicada", "Gater", "Bonsai", "Fossil"]
turretListLength = len(turretList)
hullListLength = len(hullList)

hullColors = []

# Load all the images
currentDir = os.path.dirname(__file__)
for i in range(8): # Generate all the tanks
    tankPath = os.path.join(currentDir, 'Sprites', 'tank' + str(i+1) + '.png')
    originalTankImage = pygame.image.load(tankPath).convert_alpha()
    tankImage = pygame.transform.scale(originalTankImage, (100, 65))
    hullColors.append(tankImage)


ColorIndex = ["TANK_GREEN", "BURGUNDY", "ORANGE", "YELLOW", "SKY_BLUE", "LIGHT_BROWN", "DARK_LILAC", "BRIGHT_PINK"]

#List indexes for player selection
#Turret index
p1I = 0
p2I = 0
#Hull index
p1J = 0
p2J = 0
#Colour index
p1K = 0
p2K = 1

verticalSpacing = 75
choicesX = 250

TurretX = choicesX
HullX = TurretX + verticalSpacing
ColourX = HullX + verticalSpacing

lArrowP1Turret = Button(buttonPrimary, buttonPrimary, tileSize, TurretX, tileSize, tileSize, '<', buttonText, 50)
buttonList.append(lArrowP1Turret)
textP1Turret = TextBox(tileSize*2, TurretX, font='Courier New',fontSize=26, text=turretList[0], textColor=buttonText)
textP1Turret.setBoxColor(optionText)
forceWidth = textP1Turret.getWidth()
buttonList.append(textP1Turret)
rArrowP1Turret = Button(buttonPrimary, buttonPrimary, tileSize*2 + forceWidth, TurretX, tileSize, tileSize, '>', buttonText, 50)
buttonList.append(rArrowP1Turret)

lArrowP1Hull = Button(buttonPrimary, buttonPrimary, tileSize, HullX, tileSize, tileSize, '<', buttonText, 50)
buttonList.append(lArrowP1Hull)
textP1Hull = TextBox(tileSize*2, HullX, font='Courier New',fontSize=26, text=hullList[0], textColor=buttonText)
textP1Hull.setBoxColor(optionText)
buttonList.append(textP1Hull)
rArrowP1Hull = Button(buttonPrimary, buttonPrimary, tileSize*2 + forceWidth, HullX, tileSize, tileSize, '>', buttonText, 50)
buttonList.append(rArrowP1Hull)

lArrowP1Colour = Button(buttonPrimary, buttonPrimary, tileSize, ColourX, tileSize, tileSize, '<', buttonText, 50)
buttonList.append(lArrowP1Colour)
textP1Colour = TextBox(tileSize*2, ColourX, font='Courier New',fontSize=26, text="", textColor=buttonText)
textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
buttonList.append(textP1Colour)
rArrowP1Colour = Button(buttonPrimary, buttonPrimary, tileSize*2 + forceWidth, ColourX, tileSize, tileSize, '>', buttonText, 50)
buttonList.append(rArrowP1Colour)

rArrowP2Turret = Button(buttonPrimary, buttonPrimary, SCREEN_WIDTH-tileSize*2, TurretX, tileSize, tileSize, '>', buttonText, 50)
buttonList.append(rArrowP2Turret)
textP2Turret = TextBox(SCREEN_WIDTH - tileSize*2 - forceWidth, TurretX, font='Courier New',fontSize=26, text=turretList[0], textColor=buttonText)
textP2Turret.setBoxColor(optionText)
buttonList.append(textP2Turret)
lArrowP2Turret = Button(buttonPrimary, buttonPrimary, SCREEN_WIDTH - tileSize*3 - forceWidth, TurretX, tileSize, tileSize, '<', buttonText, 50)
buttonList.append(lArrowP2Turret)

rArrowP2Hull = Button(buttonPrimary, buttonPrimary,  SCREEN_WIDTH-tileSize*2, HullX, tileSize, tileSize, '>', buttonText, 50)
buttonList.append(rArrowP2Hull)
textP2Hull = TextBox(SCREEN_WIDTH - tileSize*2 - forceWidth, HullX, font='Courier New',fontSize=26, text=hullList[0], textColor=buttonText)
textP2Hull.setBoxColor(optionText)
buttonList.append(textP2Hull)
lArrowP2Hull = Button(buttonPrimary, buttonPrimary, SCREEN_WIDTH - tileSize*3 - forceWidth, HullX, tileSize, tileSize, '<', buttonText, 50)
buttonList.append(lArrowP2Hull)

rArrowP2Colour = Button(buttonPrimary, buttonPrimary,  SCREEN_WIDTH-tileSize*2, ColourX, tileSize, tileSize, '>', buttonText, 50)
buttonList.append(rArrowP2Colour)
textP2Colour = TextBox(SCREEN_WIDTH - tileSize*2 - forceWidth, ColourX, font='Courier New',fontSize=26, text="", textColor=buttonText)
textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
buttonList.append(textP2Colour)
lArrowP2Colour = Button(buttonPrimary, buttonPrimary, SCREEN_WIDTH - tileSize*3 - forceWidth, ColourX, tileSize, tileSize, '<', buttonText, 50)
buttonList.append(lArrowP2Colour)

# Player names
textP1 = TextBox(tileSize*2, tileSize*1.5, font='Courier New',fontSize=26, text="Player 1", textColor=buttonText)
textP1.setBoxColor(c.geT("GREEN"))
buttonList.append(textP1)
textP2 = TextBox(SCREEN_WIDTH - tileSize*2 - forceWidth, tileSize*1.5, font='Courier New',fontSize=26, text="Player 2", textColor=buttonText)
textP2.setBoxColor(c.geT("GREEN"))
buttonList.append(textP2)



#Other constants
rectX = tileSize*2 + forceWidth
rectY = tileSize//2

pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*9.25, rectX, rectY), 1)
speedText = TextBox(tileSize, tileSize*9.25, font='Courier New',fontSize=26, text="Speed", textColor=buttonText)
# speedText.setPaddingHeight(0)
# speedText.
buttonList.append(speedText)


def checkButtons(mouse):
    global p1I, p2I, p1J, p2J, p1K, p2K
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
        textP2Turret.setText(turretList[p2I])
    if rArrowP2Turret.ButtonClick(mouse):
        p2I = (p2I + 1) % turretListLength
        textP2Turret.setText(turretList[p2I])
    if lArrowP2Hull.ButtonClick(mouse):
        p2J = (p2J - 1) % hullListLength
        textP2Hull.setText(hullList[p2J])
    if rArrowP2Hull.ButtonClick(mouse):
        p2J = (p2J + 1) % hullListLength
        textP2Hull.setText(hullList[p2J])
    if lArrowP1Colour.ButtonClick(mouse):
        p1K = (p1K - 1) % len(hullColors)
        if p1K == p2K:
            p1K = (p1K - 1) % len(hullColors)
        textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
    if rArrowP1Colour.ButtonClick(mouse):
        p1K = (p1K + 1) % len(hullColors)
        if p1K == p2K:
            p1K = (p1K + 1) % len(hullColors)
        textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
    if lArrowP2Colour.ButtonClick(mouse):
        p2K = (p2K - 1) % len(hullColors)
        if p2K == p1K:
            p2K = (p2K - 1) % len(hullColors)
        textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
    if rArrowP2Colour.ButtonClick(mouse):
        p2K = (p2K + 1) % len(hullColors)
        if p2K == p1K:
            p2K = (p2K + 1) % len(hullColors)
        textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                textP1Turret.setText(turretList[p1I])
                textP2Turret.setText(turretList[p2I])
                textP1Hull.setText(hullList[p1J])
                textP2Hull.setText(hullList[p2J])
                checkButtons(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_i:
                print(pygame.mouse.get_pos(), screen.get_at(pygame.mouse.get_pos()))
            if event.key == pygame.K_UP:
                pass
            if event.key == pygame.K_DOWN:
                pass
            if event.key == pygame.K_LEFT:
                pass                
            if event.key == pygame.K_RIGHT:
                pass

    # Clear screen with the chosen soft white color
    screen.fill((250,250,240))
    for button in buttonList:
        button.draw(screen, outline = False)
    # Update display
    # pygame.draw.rect(screen, (0, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], rectX, rectY), 1)
    multiply_constant = 9.25
    offset = 35
    # pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*multiply_constant, rectX, rectY), 1)
    pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*multiply_constant+ offset, rectX, rectY), 1)
    pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*multiply_constant+ offset*2, rectX, rectY), 1)
    pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*multiply_constant+ offset*3, rectX, rectY), 1)

    pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant, rectX, rectY), 1)
    pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant+ offset, rectX, rectY), 1)
    pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant+ offset*2, rectX, rectY), 1)
    pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant+ offset*3, rectX, rectY), 1)


    #Draw the tank image
    screen.blit(hullColors[p1K], (tileSize*2 + forceWidth//2-50, tileSize*3))
    screen.blit(hullColors[p2K], (SCREEN_WIDTH - tileSize*2 - forceWidth//2-50, tileSize*3))

    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()