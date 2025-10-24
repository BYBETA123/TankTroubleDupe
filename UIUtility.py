import pygame

class Button:
    buttonState = False  # False = Not clicked, True = Clicked
    outline = False
    outlineWidth = 1
    def __init__(self, color=(0, 0, 0), secondaryColor=(255, 255, 255), x=0, y=0, width=0, height=0, text='', textColor=(0, 0, 0), textSize=20, hoverColor=(200, 200, 200)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.textColor = textColor
        self.secondaryColor = secondaryColor
        self.display = self.color
        self.textSize = textSize
        self.hoverColor = hoverColor  # New attribute for hover color
        self.hover = True

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.display, (self.x, self.y, self.width, self.height), 0)
        if outline or self.outline:
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), self.outlineWidth)

        if self.text != '':
            font = pygame.font.SysFont('Courier New', self.textSize)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def buttonClick(self, mouse):
        # If there is a click detected, check this button
        # Inputs: mouse: the current mouse coordinates
        # Outputs: None
        if not(self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height):
            return False
        self.buttonState = not self.buttonState
        if self.buttonState:
            self.display = self.secondaryColor
        else:
            self.display = self.color
        return True

    def getCorners(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def is_hovered(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def update_display(self, mouse_pos):
        if self.is_hovered(mouse_pos) and self.hover:
            self.display = self.hoverColor
        elif self.buttonState:
            self.display = self.secondaryColor
        else:
            self.display = self.color

    def selectable(self, value):
        self.hover = value

    def setOutline(self, outline, outlineWidth = 1):
        self.outline = outline
        self.outlineWidth = outlineWidth

    def getText(self):
        return self.text

    def setText(self, text):
        self.text = text

    def centerOnX(self, centerX):
        self.x = centerX - self.width // 2

class ButtonSlider:
    carrierX = 20
    carrierY = 10
    carLocationX = 0
    barY = 4
    buttonSpacing = 50
    clicked = False

    def __init__(self, color=(0, 0, 0), secondaryColor=(255, 255, 255), x=0, y=0, buttonWidth=0, buttonHeight=0, width=0, height=0, text='', textColor=(0, 0, 0), buttonColor=(0, 0, 0), buttonSecondaryColor=(0, 0, 0)):
        self.color = color
        self.x = x
        self.y = y
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight
        self.width = width
        self.height = height
        self.secondaryColor = secondaryColor
        self.carrierX = height // 5
        self.carrierY = height // 2
        self.carLocationX = self.x + self.width
        self.text = text
        self.textColor = textColor
        self.display = self.color
        self.buttonColor = buttonColor
        self.buttonSecondaryColor = buttonSecondaryColor

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.display, (self.x, self.y - self.buttonHeight / 2, self.buttonWidth, self.buttonHeight), 0)
        if self.text != '':
            font = pygame.font.SysFont('Ariel', 20)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (text.get_width() / 2) - self.buttonWidth / 4, self.y + (text.get_height() / 2) - self.buttonHeight / 4))

        pygame.draw.rect(screen, self.color, (self.x + self.buttonSpacing * 2, self.y - self.barY, self.width, self.barY * 2), 0)
        pygame.draw.rect(screen, self.secondaryColor, (self.carLocationX - self.carrierX / 2 + self.buttonSpacing * 2, self.y - self.carrierY / 2, self.carrierX, self.carrierY), 0)

        text = pygame.font.SysFont('Arial', 50).render(str(int(self.getPercentage())), True, (0, 0, 0))
        screen.blit(text, (self.x + self.width + self.buttonSpacing * 2.5, self.y - text.get_height() // 2))

        if outline:
            pygame.draw.rect(screen, (0, 0, 255), (self.x + self.buttonSpacing * 2, self.y - self.carrierY / 2, self.width, self.carrierY), 1)

    def buttonClick(self):
        self.clicked = not self.clicked
        if self.clicked:
            self.display = self.buttonSecondaryColor
        else:
            self.display = self.buttonColor

    def getCorners(self):
        return (self.x, self.y - self.buttonHeight / 2, self.x + self.buttonWidth, self.y + self.buttonHeight / 2)

    def updateSlider(self, mouseX, mouseY):
        if not(self.y - self.height / 2 < mouseY < self.y + self.height / 2 and self.x + self.buttonSpacing * 2 < mouseX < self.x + self.width + self.buttonSpacing * 2):
            return
        if self.clicked:
            self.buttonClick()
        self.carLocationX = mouseX - self.buttonSpacing * 2

    def getPercentage(self):
        percentage = round(round((self.carLocationX - self.x) / (self.width), 2) * 100, 3)
        return percentage

    def checkButtonClick(self, mouseX, mouseY):
        if self.x < mouseX < self.x + self.buttonWidth and self.y < mouseY + self.buttonHeight / 2 < self.y + self.buttonHeight:
            self.buttonClick()

    def getValue(self):
        if self.clicked:
            return 0
        return self.getPercentage() / 100

    def mute(self):
        self.clicked = True
        self.display = self.buttonSecondaryColor

class TextBox:
    paddingWidth, paddingHeight = 10, 10
    characterPad = 10
    hover = False # Whether or not we want to show a hover effect
    outline = False
    outlineWidth = 1
    def __init__(self, x, y, font, text='Click me!', fontSize = 20, textColor = (0,0,0)):
        self.x=x
        self.y=y
        self.font = font
        self.text = text.center(10)
        self.text_color = textColor
        self.box_color = (0,0,255)
        self.clicked = False
        self.fontSize = fontSize

        # Get the text surface and its dimensions
        self.text_surface = pygame.font.SysFont(self.font,fontSize, bold=True).render(self.text, True, self.text_color)
        self.text_width, self.text_height = self.text_surface.get_size()

        # Create a rect for the text box with some padding
        self.rect = pygame.Rect(x, y, self.text_width + 2 * self.paddingWidth, self.text_height + 2 * self.paddingHeight)

    def draw(self, screen, outline = False):
        # Draw the text box

        mouse = pygame.mouse.get_pos()


        pygame.draw.rect(screen, self.box_color, self.rect)

        if self.rect.x < mouse[0] < self.rect.x + self.rect.width and self.rect.y < mouse[1] < self.rect.y + self.rect.height and self.hover:
            pygame.draw.rect(screen, (100,100,255), self.rect)
            #We are hovering

        if outline or self.outline:
            pygame.draw.rect(screen, (0,0,0), self.rect, self.outlineWidth)


        # Center the text within the box
        text_x = self.rect.x + (self.rect.width - self.text_width) / 2
        text_y = self.rect.y + (self.rect.height - self.text_height) / 2
        screen.blit(self.text_surface, (text_x, text_y))

    def selectable(self, value):
        self.hover = value

    def getCorners(self):
        return [self.rect.x, self.rect.y, self.rect.x + self.rect.width, self.rect.y + self.rect.height]
    
    def getWidth(self):
        return self.rect.width

    def getHeight(self):
        return self.rect.height
    
    def setPaddingWidth(self, paddingWidth):
        self.paddingWidth = paddingWidth
        self.rect = pygame.Rect(self.x, self.y, self.text_width + 2 * self.paddingWidth, self.text_height + 2 * self.paddingHeight)

    def setPaddingHeight(self, paddingHeight):
        self.paddingHeight = paddingHeight
        self.rect = pygame.Rect(self.x, self.y, self.text_width + 2 * self.paddingWidth, self.text_height + 2 * self.paddingHeight)


    def setText(self, text, padType = 'center'):
        # Pad the text to at least 10 characters        
        if padType == 'left':
            self.text = text.ljust(self.characterPad)
        elif padType == 'right':
            self.text = text.rjust(self.characterPad)
        else:
            self.text = text.center(self.characterPad)

        # Update the text surface and its dimensions
        self.text_surface = pygame.font.SysFont(self.font,self.fontSize, bold = True).render(self.text, True, self.text_color)
        self.text_width, self.text_height = self.text_surface.get_size()
        
        # Update the text box rect size
        self.rect.width = self.text_width + 2 * self.paddingWidth
        self.rect.height = self.text_height + 2 * self.paddingHeight

    def buttonClick(self, mouse):
        # Just check if we are clicked
        if not(self.rect.x < mouse[0] < self.rect.x + self.rect.width and self.rect.y < mouse[1] < self.rect.y + self.rect.height):
            return False
        return True

    def setCharacterPad(self, characterPad):
        self.characterPad = characterPad

    def setBoxColor(self, color):
        self.box_color = color

    def setTextSize(self, textSize):
        self.fontSize = textSize
        self.text_surface = pygame.font.SysFont(self.font, textSize, bold=True).render(self.text, True, self.text_color)
        self.text_width, self.text_height = self.text_surface.get_size()

    def update_display(self, mouse):
        return
    
    def setOutline(self, outline, outlineWidth = 1):
        self.outline = outline
        self.outlineWidth = outlineWidth



class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.open = False
        self.buttonList = []
        self.options = options
        for i in range(len(options)):
            self.buttonList.append(Button((106, 76, 165), (106, 76, 165), x, y + height*i, width, height, options[i], (255, 255, 255), 20, (255, 255, 0)))
        self.arrow = Button((106, 76, 165), (106, 76, 165), x + width, y, height, height, "▼", (255, 255, 255), 30, (255, 255, 0))

    def draw(self, screen):
        if self.open:
            for i in range(len(self.options)):
                self.buttonList[i].draw(screen)
        else:
            self.buttonList[0].draw(screen)
        self.arrow.draw(screen)

    def getButtonList(self):
        return self.buttonList

    def click(self, mousepos):
        x, y = mousepos
        if not(x<self.x or x>self.x+self.width or y<self.y or y>self.y+self.height*len(self.options)) and self.open:
            for button in self.buttonList:
                if button.buttonClick(mousepos):
                    self.open = False
                    index = self.buttonList.index(button)
                    cindex = 0

                    t = self.buttonList[index].text
                    self.buttonList[index].text = self.buttonList[cindex].text
                    self.buttonList[cindex].text = t
                    return True

            self.open = False

        if x<self.arrow.x+self.arrow.width and x>self.arrow.x and y<self.arrow.y+self.arrow.height and y>self.arrow.y:
            self.open = not self.open
            return True
        return False

    def setTextSize(self, size):
        for button in self.buttonList:
            button.textSize = size
        self.arrow.textSize = size
    
    def setRect(self, width, height):
        for button in self.buttonList:
            button.width = width
            button.height = height
        self.width = width
        self.height = height
        for i in range(len(self.options)):
            self.buttonList[i].y = self.y + height*i
        self.arrow.x = self.x + width
        self.arrow.y = self.y
        self.arrow.width = 50
        self.arrow.height = 50

    def getValue(self):
        return self.buttonList[0].text
    
    def getState(self):
        return self.open
    
class Switch:

    def __init__(self, onColor = (0,0,0), offColor = (255, 255, 255), x=0, y=0, barWidth = 100, barHeight = 10, square = 10, barColor = (0,0,0)):

        self.onColor = onColor
        self.offColor = offColor
        self.x = x
        self.y = y
        self.barWidth = barWidth
        self.barHeight = barHeight
        self.square = square
        self.barColor = barColor
        self.on = True # default it to false to begin with

    def draw(self, screen):
        # pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        # we have a square to draw
        # draw the switch bar
        pygame.draw.rect(screen, self.barColor, (self.x + self.square//2, self.y + self.square//2 - self.barHeight//2, self.barWidth - self.square, self.barHeight), 0, self.square//10)

        if self.on:
            pygame.draw.rect(screen, self.onColor, (self.x + self.barWidth - self.square, self.y, self.square, self.square), 0, self.square//10)
        else:
            pygame.draw.rect(screen, self.offColor, (self.x, self.y, self.square, self.square), 0, self.square//10)

    def click(self, mousepos):
        x, y = mousepos
        if self.x < x < self.x + self.barWidth and self.y < y < self.y + self.square:
            self.on = not self.on
            return True
        return False

    def getColor(self):
        return self.onColor if self.on else self.offColor



