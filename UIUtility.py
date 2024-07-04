import pygame

class Button:
    buttonState = False  # False = Not clicked, True = Clicked
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

    def draw(self, screen, outline=None):
        pygame.draw.rect(screen, self.display, (self.x, self.y, self.width, self.height), 0)
        if outline:
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)

        if self.text != '':
            font = pygame.font.SysFont('Ariel', self.textSize)
            text = font.render(self.text, 1, self.textColor)
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def ButtonClick(self, mouse):
        if not(self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height):
            return
        self.buttonState = not self.buttonState
        if self.buttonState:
            self.display = self.secondaryColor
        else:
            self.display = self.color

    def getCorners(self):
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def is_hovered(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def update_display(self, mouse_pos):
        if self.is_hovered(mouse_pos):
            self.display = self.hoverColor
        elif self.buttonState:
            self.display = self.secondaryColor
        else:
            self.display = self.color


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

    def ButtonClick(self):
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
            self.ButtonClick()
        self.carLocationX = mouseX - self.buttonSpacing * 2

    def getPercentage(self):
        percentage = round(round((self.carLocationX - self.x) / (self.width), 2) * 100, 3)
        return percentage

    def checkButtonClick(self, mouseX, mouseY):
        if self.x < mouseX < self.x + self.buttonWidth and self.y < mouseY + self.buttonHeight / 2 < self.y + self.buttonHeight:
            self.ButtonClick()

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
    def __init__(self, x, y, font, text='Click me!', fontSize = 20):
        self.font = font
        self.text = text.center(10)
        self.text_color = (0,0,0)
        self.box_color = (0,0,255)
        self.clicked = False
        self.fontSize = fontSize

        # Get the text surface and its dimensions
        # self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_surface = pygame.font.SysFont(self.font,fontSize, bold=True).render(self.text, True, self.text_color)
        self.text_width, self.text_height = self.text_surface.get_size()

        # Create a rect for the text box with some padding
        self.rect = pygame.Rect(x, y, self.text_width + 2 * self.paddingWidth, self.text_height + 2 * self.paddingHeight)

    def draw(self, screen, outline = False):
        # Draw the text box
        pygame.draw.rect(screen, self.box_color, self.rect)
        if outline:
            pygame.draw.rect(screen, (0,0,0), self.rect, 1)

        # Center the text within the box
        text_x = self.rect.x + (self.rect.width - self.text_width) / 2
        text_y = self.rect.y + (self.rect.height - self.text_height) / 2
        screen.blit(self.text_surface, (text_x, text_y))


    def getCorners(self):
        return [self.rect.x, self.rect.y, self.rect.x + self.rect.width, self.rect.y + self.rect.height]
    
    def getWidth(self):
        return self.rect.width

    def getHeight(self):
        return self.rect.height
    
    def setPaddingWidth(self, paddingWidth):
        self.paddingWidth = paddingWidth

    def setPaddingHeight(self, paddingHeight):
        self.paddingHeight = paddingHeight

    def setText(self, text):
        # Pad the text to at least 10 characters
        self.text = text.center(self.characterPad)
        
        # Update the text surface and its dimensions
        self.text_surface = pygame.font.SysFont(self.font,self.fontSize, bold = True).render(self.text, True, self.text_color)
        self.text_width, self.text_height = self.text_surface.get_size()
        
        # Update the text box rect size
        self.rect.width = self.text_width + 2 * self.paddingWidth
        self.rect.height = self.text_height + 2 * self.paddingHeight

    def ButtonClick(self, _):
        pass

    def setCharacterPad(self, characterPad):
        self.characterPad = characterPad