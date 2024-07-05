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
choicesX = 200

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
textP1 = TextBox(tileSize*2, tileSize*0.5, font='Courier New',fontSize=26, text="Player 1", textColor=buttonText)
textP1.setBoxColor(c.geT("GREEN"))
buttonList.append(textP1)
textP2 = TextBox(SCREEN_WIDTH - tileSize*2 - forceWidth, tileSize*0.5, font='Courier New',fontSize=26, text="Player 2", textColor=buttonText)
textP2.setBoxColor(c.geT("GREEN"))
buttonList.append(textP2)

#Play button
playButton = TextBox(SCREEN_WIDTH//2 - tileSize*1.75, tileSize//2, font='Courier New',fontSize=26, text="Play", textColor=buttonText)
playButton.setBoxColor(c.geT("BLACK"))
buttonList.append(playButton)


multiply_constant = 8.5
offset = 35
tankValue = 3


#Other constants
rectX = tileSize*2 + forceWidth
rectY = tileSize//2
 
speedText = TextBox(tileSize, tileSize*multiply_constant, font='Courier New',fontSize=21, text="Speed", textColor=buttonText)
speedText.setPaddingHeight(0)
buttonList.append(speedText)

healthText = TextBox(tileSize, tileSize*multiply_constant + offset, font='Courier New',fontSize=21, text="Health", textColor=buttonText)
healthText.setPaddingHeight(0)
buttonList.append(healthText)

damageBar = TextBox(tileSize, tileSize*multiply_constant + offset*2, font='Courier New',fontSize=21, text="Damage", textColor=buttonText)
damageBar.setPaddingHeight(0)
buttonList.append(damageBar)

reloadBar = TextBox(tileSize, tileSize*multiply_constant + offset*3, font='Courier New',fontSize=21, text="Reload", textColor=buttonText)
reloadBar.setPaddingHeight(0)
buttonList.append(reloadBar)

speedText2 = TextBox(SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant, font='Courier New',fontSize=21, text="Speed", textColor=buttonText)
speedText2.setPaddingHeight(0)
buttonList.append(speedText2)

healthText2 = TextBox(SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant + offset, font='Courier New',fontSize=21, text="Health", textColor=buttonText)
healthText2.setPaddingHeight(0)
buttonList.append(healthText2)

damageBar2 = TextBox(SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant + offset*2, font='Courier New',fontSize=21, text="Damage", textColor=buttonText)
damageBar2.setPaddingHeight(0)
buttonList.append(damageBar2)

reloadBar2 = TextBox(SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant + offset*3, font='Courier New',fontSize=21, text="Reload", textColor=buttonText)
reloadBar2.setPaddingHeight(0)
buttonList.append(reloadBar2)

    # pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant, rectX, rectY), 1)
    # pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant+ offset, rectX, rectY), 1)

    # pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant+ offset*2, rectX, rectY), 1)
    # pygame.draw.rect(screen,(0,0,0), (SCREEN_WIDTH - tileSize*2 - forceWidth - tileSize, tileSize*multiply_constant+ offset*3, rectX, rectY), 1)


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

    pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*multiply_constant, rectX, rectY), 1)
    for button in buttonList:
        button.draw(screen, outline = False)
    
    barBorder = 3
    
    #Blocks
    speedBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiply_constant, rectX, rectY),barBorder)
    speedBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiply_constant, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    speedOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiply_constant, rectX - speedText.getWidth(), rectY), barBorder)
    speedBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant, (rectX - speedText.getWidth())/3,rectY), barBorder)

    healthBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiply_constant + offset, rectX, rectY),barBorder)
    healthBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiply_constant + offset, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    healthOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiply_constant + offset, rectX - speedText.getWidth(), rectY), barBorder)
    healthBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant + offset, (rectX - speedText.getWidth())/3,rectY), barBorder)

    damageBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiply_constant + offset*2, rectX, rectY),barBorder)
    damageBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiply_constant + offset*2, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    damageOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiply_constant + offset*2, rectX - speedText.getWidth(), rectY), barBorder)
    damageBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant + offset*2, (rectX - speedText.getWidth())/3,rectY), barBorder)

    reloadBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiply_constant + offset*3, rectX, rectY),barBorder)
    reloadBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiply_constant + offset*3, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    reloadOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiply_constant + offset*3, rectX - speedText.getWidth(), rectY), barBorder)
    reloadBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant + offset*3, (rectX - speedText.getWidth())/3,rectY), barBorder)

    speedBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant, rectX, rectY),barBorder)
    speedBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    speedOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant, rectX - speedText.getWidth(), rectY), barBorder)
    speedBlockOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant, (rectX - speedText.getWidth())/3,rectY), barBorder)

    healthBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant + offset, rectX, rectY),barBorder)
    healthBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant + offset, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    healthOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant + offset, rectX - speedText.getWidth(), rectY), barBorder)
    healthBlockOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant + offset, (rectX - speedText.getWidth())/3,rectY), barBorder)

    damageBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant + offset*2, rectX, rectY),barBorder)
    damageBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant + offset*2, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    damageOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant + offset*2, rectX - speedText.getWidth(), rectY), barBorder)
    damageBlockOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant + offset*2, (rectX - speedText.getWidth())/3,rectY), barBorder)

    reloadBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (SCREEN_WIDTH - tileSize*3 - forceWidth, tileSize*multiply_constant + offset*3, rectX, rectY),barBorder)
    reloadBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant + offset*3, (rectX - speedText.getWidth()) * tankValue/3, rectY))
    #Outlines
    reloadOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiply_constant + offset*3, rectX - speedText.getWidth(), rectY), barBorder)
    reloadBlockOutline2 = pygame.draw.rect(screen, (0,0,0), (SCREEN_WIDTH - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3, tileSize*multiply_constant + offset*3, (rectX - speedText.getWidth())/3,rectY), barBorder)







    # Update display



    #Draw the tank image
    screen.blit(hullColors[p1K], (tileSize*2 + forceWidth//2-50, tileSize*2))
    screen.blit(hullColors[p2K], (SCREEN_WIDTH - tileSize*2 - forceWidth//2-50, tileSize*2))

    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()