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

selectionBackground = c.geT("WHITE")
selectionFont = 'Londrina Solid'
monoFont = 'Courier New'


homeButton = TextBox(tileSize//4, tileSize//4, font=selectionFont,fontSize=26, text="BACK", textColor=c.geT("BLACK"))
homeButton.setBoxColor(selectionBackground)
homeButton.setOutline(True, 5)
homeButton.selectable(True)
buttonList.append(homeButton)

#How to play button
howToPlayButton = TextBox(SCREEN_WIDTH - 150, tileSize//4, font=selectionFont,fontSize=26, text="HOW TO PLAY", textColor=c.geT("BLACK"))
howToPlayButton.setBoxColor(selectionBackground)
howToPlayButton.setOutline(True, 5)
howToPlayButton.selectable(True)
buttonList.append(howToPlayButton)

playButton = TextBox(SCREEN_WIDTH//2-84, 95, font=selectionFont,fontSize=52, text="PLAY", textColor=c.geT("BLACK"))
playButton.setBoxColor(selectionBackground)
playButton.setOutline(True, 5)
playButton.selectable(True)
buttonList.append(playButton)

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
imageScaler = 4
for i in range(8): # Generate all the tanks
    tankPath = os.path.join(currentDir, 'Sprites', 'tank' + str(i+1) + '.png')
    originalTankImage = pygame.image.load(tankPath).convert_alpha()
    tankImage = pygame.transform.scale(originalTankImage, (20*imageScaler, 13 * imageScaler))
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

verticalSpacing =40
choicesX = 420

TurretX = choicesX
HullX = TurretX + verticalSpacing
ColourX = HullX + verticalSpacing
ColourX2 = ColourX + verticalSpacing



buttonSize = 30
buttonFontSize = 30
textFontSize = 26
lArrowX = 70
cBoX = lArrowX + buttonSize
rArrowX = cBoX + 180 # 115 is the longest text width



lArrowP1Turret = Button(buttonPrimary, buttonPrimary, lArrowX, TurretX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP1Turret.selectable(False)
buttonList.append(lArrowP1Turret)
textP1Turret = TextBox(cBoX, TurretX, font=monoFont,fontSize=textFontSize, text=turretList[0], textColor=buttonText)
textP1Turret.setBoxColor(optionText)
textP1Turret.selectable(False)
textP1Turret.setPaddingHeight(0)
textP1Turret.setText(turretList[0])
buttonList.append(textP1Turret)
rArrowP1Turret = Button(buttonPrimary, buttonPrimary, rArrowX, TurretX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP1Turret.selectable(False)
buttonList.append(rArrowP1Turret)

lArrowP1Hull = Button(buttonPrimary, buttonPrimary, lArrowX, HullX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP1Hull.selectable(False)
buttonList.append(lArrowP1Hull)
textP1Hull = TextBox(cBoX, HullX, font=monoFont,fontSize=textFontSize, text=hullList[0], textColor=buttonText)
textP1Hull.setBoxColor(optionText)
textP1Hull.selectable(False)
textP1Hull.setPaddingHeight(0)
textP1Hull.setText(hullList[0])
buttonList.append(textP1Hull)
rArrowP1Hull = Button(buttonPrimary, buttonPrimary, rArrowX, HullX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP1Hull.selectable(False)
buttonList.append(rArrowP1Hull)

lArrowP1Colour = Button(buttonPrimary, buttonPrimary, lArrowX, ColourX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP1Colour.selectable(False)
buttonList.append(lArrowP1Colour)
textP1Colour = TextBox(cBoX, ColourX, font=monoFont,fontSize=textFontSize, text="", textColor=buttonText)
textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
textP1Colour.selectable(False)
textP1Colour.setPaddingHeight(0)
buttonList.append(textP1Colour)
rArrowP1Colour = Button(buttonPrimary, buttonPrimary, rArrowX, ColourX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP1Colour.selectable(False)
buttonList.append(rArrowP1Colour)

lArrowP1Colour2 = Button(buttonPrimary, buttonPrimary, lArrowX, ColourX2, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP1Colour2.selectable(False)
buttonList.append(lArrowP1Colour2)
textP1Colour2 = TextBox(cBoX, ColourX2, font=monoFont,fontSize=textFontSize, text="", textColor=buttonText)
textP1Colour2.setBoxColor(c.geT(ColorIndex[p1K]))
textP1Colour2.selectable(False)
textP1Colour2.setPaddingHeight(0)
buttonList.append(textP1Colour2)
rArrowP1Colour2 = Button(buttonPrimary, buttonPrimary, rArrowX, ColourX2, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP1Colour2.selectable(False)
buttonList.append(rArrowP1Colour2)

lArrow2X = 493
cBo2X = lArrow2X + buttonSize
rArrow2X = cBo2X + 180 # 115 is the longest text width

lArrowP2Turret = Button(buttonPrimary, buttonPrimary, lArrow2X, TurretX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP2Turret.selectable(False)
buttonList.append(lArrowP2Turret)
textP2Turret = TextBox(cBo2X, TurretX, font=monoFont,fontSize=textFontSize, text=turretList[0], textColor=buttonText)
textP2Turret.setBoxColor(optionText)
textP2Turret.selectable(False)
textP2Turret.setPaddingHeight(0)
buttonList.append(textP2Turret)
rArrowP2Turret = Button(buttonPrimary, buttonPrimary,rArrow2X, TurretX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP2Turret.selectable(False)
buttonList.append(rArrowP2Turret)

lArrowP2Hull = Button(buttonPrimary, buttonPrimary, lArrow2X, HullX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP2Hull.selectable(False)
buttonList.append(lArrowP2Hull)
textP2Hull = TextBox(cBo2X, HullX, font=monoFont,fontSize=textFontSize, text=hullList[0], textColor=buttonText)
textP2Hull.setBoxColor(optionText)
textP2Hull.selectable(False)
textP2Hull.setPaddingHeight(0)
buttonList.append(textP2Hull)
rArrowP2Hull = Button(buttonPrimary, buttonPrimary,  rArrow2X, HullX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP2Hull.selectable(False)
buttonList.append(rArrowP2Hull)

lArrowP2Colour = Button(buttonPrimary, buttonPrimary, lArrow2X, ColourX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP2Colour.selectable(False)
buttonList.append(lArrowP2Colour)
textP2Colour = TextBox(cBo2X, ColourX, font=monoFont,fontSize=textFontSize, text="", textColor=buttonText)
textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
textP2Colour.selectable(False)
textP2Colour.setPaddingHeight(0)
buttonList.append(textP2Colour)
rArrowP2Colour = Button(buttonPrimary, buttonPrimary,  rArrow2X, ColourX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP2Colour.selectable(False)
buttonList.append(rArrowP2Colour)

lArrowP2Colour2 = Button(buttonPrimary, buttonPrimary, lArrow2X, ColourX2, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP2Colour2.selectable(False)
buttonList.append(lArrowP2Colour2)
textP2Colour2 = TextBox(cBo2X, ColourX2, font=monoFont,fontSize=textFontSize, text="", textColor=buttonText)
textP2Colour2.setBoxColor(c.geT(ColorIndex[p2K]))
textP2Colour2.selectable(False)
textP2Colour2.setPaddingHeight(0)
buttonList.append(textP2Colour2)
rArrowP2Colour2 = Button(buttonPrimary, buttonPrimary,  rArrow2X, ColourX2, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP2Colour2.selectable(False)
buttonList.append(rArrowP2Colour2)




forceWidth = 0


# Player names
playerX = 100
playerY = 100

textP1 = TextBox(playerX, playerY, font=selectionFont,fontSize=38, text="PLAYER 1", textColor=c.geT("BLACK"))
textP1.setBoxColor(selectionBackground)
textP1.setOutline(True, outlineWidth = 5)
buttonList.append(textP1)

textP2 = TextBox(SCREEN_WIDTH - playerX*2.5, playerY, font=selectionFont,fontSize=38, text="PLAYER 2", textColor=c.geT("BLACK"))
textP2.setBoxColor(selectionBackground)
textP2.setOutline(True, outlineWidth = 5)
buttonList.append(textP2)

multiply_constant = 8.5
offset = 35
tankValue = 3

speedBarX = 250
healthBarX = speedBarX + offset
damageBarX = healthBarX + offset
reloadBarX = damageBarX + offset


#Other constants
rectX = 280
rectY = 25
barFontSize = 36
speedText = TextBox(50, speedBarX, font=selectionFont,fontSize=barFontSize, text="SPEED", textColor=c.geT("BLACK"))
speedText.setPaddingHeight(0)
speedText.setPaddingWidth(0)
speedText.setCharacterPad(7)
speedText.setBoxColor(selectionBackground)
speedText.setText("SPEED", 'right')
buttonList.append(speedText)

healthText = TextBox(42, healthBarX, font=selectionFont,fontSize=barFontSize, text="Health", textColor=c.geT("BLACK"))
healthText.setPaddingHeight(0)
healthText.setPaddingWidth(0)
healthText.setCharacterPad(7)
healthText.setBoxColor(selectionBackground)
healthText.setText("HEALTH", "right")
buttonList.append(healthText)

damageBar = TextBox(31, damageBarX, font=selectionFont,fontSize=barFontSize, text="Damage", textColor=c.geT("BLACK"))
damageBar.setPaddingHeight(0)
damageBar.setPaddingWidth(0)
damageBar.setCharacterPad(7)
damageBar.setBoxColor(selectionBackground)
damageBar.setText("DAMAGE", "right")
buttonList.append(damageBar)

reloadBar = TextBox(37, reloadBarX, font=selectionFont,fontSize=barFontSize, text="Reload", textColor=c.geT("BLACK"))
reloadBar.setPaddingHeight(0)
reloadBar.setPaddingWidth(0)
reloadBar.setCharacterPad(7)
reloadBar.setBoxColor(selectionBackground)
reloadBar.setText("RELOAD", "right")
buttonList.append(reloadBar)

speedText2 = TextBox(650, speedBarX, font=selectionFont,fontSize=barFontSize, text="Speed", textColor=c.geT("BLACK"))
speedText2.setPaddingHeight(0)
speedText2.setPaddingWidth(0)
speedText2.setCharacterPad(7)
speedText2.setBoxColor(selectionBackground)
speedText2.setText("SPEED", "left")
buttonList.append(speedText2)

healthText2 = TextBox(650, healthBarX, font=selectionFont,fontSize=barFontSize, text="Health", textColor=c.geT("BLACK"))
healthText2.setPaddingHeight(0)
healthText2.setPaddingWidth(0)
healthText2.setCharacterPad(7)
healthText2.setBoxColor(selectionBackground)
healthText2.setText("HEALTH", "left")
buttonList.append(healthText2)

damageBar2 = TextBox(650, damageBarX, font=selectionFont,fontSize=barFontSize, text="Damage", textColor=c.geT("BLACK"))
damageBar2.setPaddingHeight(0)
damageBar2.setPaddingWidth(0)
damageBar2.setCharacterPad(7)
damageBar2.setBoxColor(selectionBackground)
damageBar2.setText("DAMAGE", "left")
buttonList.append(damageBar2)

reloadBar2 = TextBox(650, reloadBarX, font=selectionFont,fontSize=barFontSize, text="Reload", textColor=c.geT("BLACK"))
reloadBar2.setPaddingHeight(0)
reloadBar2.setPaddingWidth(0)
reloadBar2.setCharacterPad(7)
reloadBar2.setBoxColor(selectionBackground)
reloadBar2.setText("RELOAD", "left")
buttonList.append(reloadBar2)

def checkButtons(mouse):
    global p1I, p2I, p1J, p2J, p1K, p2K
    if lArrowP1Turret.buttonClick(mouse):
        p1I = (p1I - 1) % turretListLength
        textP1Turret.setText(turretList[p1I])
    if rArrowP1Turret.buttonClick(mouse):
        p1I = (p1I + 1) % turretListLength
        textP1Turret.setText(turretList[p1I])
    if lArrowP1Hull.buttonClick(mouse):
        p1J = (p1J - 1) % hullListLength
        textP1Hull.setText(hullList[p1J])
    if rArrowP1Hull.buttonClick(mouse):
        p1J = (p1J + 1) % hullListLength
        textP1Hull.setText(hullList[p1J])
    if lArrowP2Turret.buttonClick(mouse):
        p2I = (p2I - 1) % turretListLength
        textP2Turret.setText(turretList[p2I])
    if rArrowP2Turret.buttonClick(mouse):
        p2I = (p2I + 1) % turretListLength
        textP2Turret.setText(turretList[p2I])
    if lArrowP2Hull.buttonClick(mouse):
        p2J = (p2J - 1) % hullListLength
        textP2Hull.setText(hullList[p2J])
    if rArrowP2Hull.buttonClick(mouse):
        p2J = (p2J + 1) % hullListLength
        textP2Hull.setText(hullList[p2J])
    if lArrowP1Colour.buttonClick(mouse):
        p1K = (p1K - 1) % len(hullColors)
        if p1K == p2K:
            p1K = (p1K - 1) % len(hullColors)
        textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
    if rArrowP1Colour.buttonClick(mouse):
        p1K = (p1K + 1) % len(hullColors)
        if p1K == p2K:
            p1K = (p1K + 1) % len(hullColors)
        textP1Colour.setBoxColor(c.geT(ColorIndex[p1K]))
    if lArrowP2Colour.buttonClick(mouse):
        p2K = (p2K - 1) % len(hullColors)
        if p2K == p1K:
            p2K = (p2K - 1) % len(hullColors)
        textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
    if rArrowP2Colour.buttonClick(mouse):
        p2K = (p2K + 1) % len(hullColors)
        if p2K == p1K:
            p2K = (p2K + 1) % len(hullColors)
        textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
    if playButton.buttonClick(mouse):
        print("Play")
    if homeButton.buttonClick(mouse):
        print("Back")
    if howToPlayButton.buttonClick(mouse):
        print("How to play")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
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
    screen.fill(selectionBackground)
    for button in buttonList:
        button.update_display(pygame.mouse.get_pos())
        button.draw(screen, outline = False)
    
    barBorder = 3
    
    #Blocks
    BarLevelX = 157
    cellWidth = 50
    speedBar = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, speedBarX, cellWidth * tankValue, rectY))
    #Outlines
    speedOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, speedBarX, cellWidth * 3, rectY), barBorder) # Raw outline
    speedBlockOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, speedBarX, cellWidth, rectY), barBorder) # Raw outline

    healthBar = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, healthBarX, cellWidth * tankValue, rectY))
    #Outlines
    healthOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, healthBarX, cellWidth * 3, rectY), barBorder)
    healthBlockOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, healthBarX, cellWidth,rectY), barBorder)

    damageBar = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, damageBarX, cellWidth * tankValue, rectY))
    #Outlines
    damageOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, damageBarX, cellWidth * 3, rectY), barBorder)
    damageBlockOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, damageBarX, cellWidth,rectY), barBorder)

    reloadBar = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, reloadBarX, cellWidth * tankValue, rectY))
    #Outlines
    reloadOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, reloadBarX, cellWidth * 3, rectY), barBorder)
    reloadBlockOutline = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, reloadBarX, cellWidth,rectY), barBorder)


    BarLevelRX = 493


    speedBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, speedBarX, cellWidth * tankValue, rectY))
    #Outlines
    speedOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, speedBarX, cellWidth * 3, rectY), barBorder)
    speedBlockOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, speedBarX, cellWidth,rectY), barBorder)

    healthBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, healthBarX, cellWidth * tankValue, rectY))
    #Outlines
    healthOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, healthBarX, cellWidth * 3, rectY), barBorder)
    healthBlockOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, healthBarX, cellWidth,rectY), barBorder)

    damageBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, damageBarX,cellWidth * tankValue, rectY))
    #Outlines
    damageOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, damageBarX, cellWidth*3, rectY), barBorder)
    damageBlockOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, damageBarX, cellWidth, rectY), barBorder)

    reloadBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, reloadBarX, cellWidth * tankValue, rectY))
    #Outlines
    reloadOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, reloadBarX, cellWidth * 3, rectY), barBorder)
    reloadBlockOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, reloadBarX, cellWidth,rectY), barBorder)







    # Update display

    hullImageX = 130
    hullImageY = 174

    #Draw the tank image
    screen.blit(hullColors[p1K], (hullImageX, hullImageY))
    screen.blit(hullColors[p2K], (SCREEN_WIDTH - hullImageX - imageScaler*20, hullImageY))
    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)

pygame.quit()