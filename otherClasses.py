import pygame
import os, sys
import constants as const
import globalVariables as g
import random
from ColorDictionary import ColourDictionary as c # colors
from DifficultyTypes import *


class Tile(pygame.sprite.Sprite):
    # border = [False, False, False, False]
    #Border format is [Top, Right, Bottom, Left]
    border = [True, True, True, True]
    borderWidth = 2
    spawn = 0

    def __init__(self, index, x, y, color, spawn = 0):
        self.index = index
        self.x = x
        self.y = y
        self.color = color
        self.spawn = 0
        self.border = self.borderControl()
        self.neighbours, self.bordering = self.neighbourCheck()
        self.AITarget = False
        self.supply = None
        self.timer = 8372 # Roughly one minute?
        self.supplyTimer = self.timer # This is the timer for the supply
        self.picked = False
        self.supplyIndex = None # The index of the supply that is on the tile
        self.borderindex = 0 # the index of the border
        self.flag = 0
        self.flagPicked = False # This is the flag that is picked up by the player
        # Determine the correct base path
        if getattr(sys, 'frozen', False):  # Running as an .exe
            base_path = sys._MEIPASS
        else:  # Running as a .py script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the tile path dynamically
        self.tilePath = os.path.join(base_path, "Assets", "Tile")
        cardinal = ["N", "E", "S", "W"]
        self.rect = pygame.Rect(self.x, self.y, const.TILE_SIZE, const.TILE_SIZE)

        for idx, el in enumerate(self.bordering):
            if el != -1:
                self.tilePath += str(cardinal[idx])  # Append direction suffix

        self.tilePath += ".png"  # Add the file extension

        # Load the correct tile image
        self.image = pygame.image.load(self.tilePath).convert_alpha()

        # Load the debug tile image
        debugPath = os.path.join(base_path, "Assets", "TileDebug.png")
        self.debug = pygame.image.load(debugPath).convert_alpha()

    def update(self):
        if self.picked:
            self.supplyTimer -= 1
        if self.supplyTimer < 0:
            self.supplyTimer = 0
            self.picked = False
        
        if self.supply is not None and not self.picked:
            for i in range(g.difficultyType.playerCount):
                if not g.tankDead[i] and g.tankList[i].invincibility == 0:
                    if self.isWithin(g.tankList[i].getCenter()):
                        if self.supplyIndex == 0:
                            g.tankList[i].applyDoubleDamage()
                        elif self.supplyIndex == 1:
                            g.tankList[i].applyDoubleArmor()
                        elif self.supplyIndex == 2:
                            g.tankList[i].applySpeedBoost()
                        self.picked = True
                        self.supplyTimer = self.timer

    def neighbourCheck(self):
        #This function will return a list of the indexes of the neighbours based on the current list of border
        # No inputs are needed
        # The output will be an updated list of neighbours
        #
        neighbours = [self.index - const.COLUMN_AMOUNT, self.index + 1, self.index + const.COLUMN_AMOUNT, self.index - 1]
        #Check if there are any invalid neighbours
        newlist = []
        oldlist = [-1, -1, -1, -1]
        for idx, neighbour in enumerate(neighbours):
            if neighbour < 1 or neighbour > const.ROW_AMOUNT*const.COLUMN_AMOUNT:
                #We do not want this
                pass
            elif self.border[idx] == True:
                #We do not want this
                oldlist[idx] = neighbour
            else:
                newlist.append(neighbour)
        return newlist, oldlist

    def updateBorder(self):
        total = 0
        if self.border[0]:
            total += 8
        if self.border[1]:
            total += 4
        if self.border[2]:
            total += 2
        if self.border[3]:
            total += 1

        self.borderindex = total

    def borderControl(self):
        # This function checks and validates the borders for the tile
        # No inputs
        # Outputs: A list of boolean values representing whether the border is present
        #
        localIndex = self.index
        border = [False, False, False, False] # Start with everything false
        #Sides
        # Top Row
        if localIndex in range(1, const.COLUMN_AMOUNT+1):
            border[0] = True
        # Right Row
        if localIndex in range(const.COLUMN_AMOUNT, const.ROW_AMOUNT*const.COLUMN_AMOUNT+1, const.COLUMN_AMOUNT):
            border[1] = True
        # Bottom Row
        if localIndex in range(99, const.ROW_AMOUNT*const.COLUMN_AMOUNT + 1):
            border[2] = True
        #Left Row
        if localIndex in range(1, const.ROW_AMOUNT*const.COLUMN_AMOUNT, const.COLUMN_AMOUNT):
            border[3] = True

        if self.spawn:
            #If the tile is a spawn then its border should be handled carefully
            return border

        for i in range(len(border)):
            if not border[i]:
                border[i] = random.choices([True, False], weights = (0.16, 1-0.16))[0]
        return border

    def drawText(self, screen):
        # access the "tileFont" key from the dictionary
        text = const.FONT_DICTIONARY["tileFont"].render(str(self.index), True, c.geT("BLACK"))
        screen.blit(text, [self.x + const.TILE_SIZE/2 - text.get_width()/2, self.y + const.TILE_SIZE/2 - text.get_height()/2])

    def draw(self, screen):
        # Draw the tile w/ borders
        match self.borderindex: # 0 - 15
            case 0:
                # nothing
                pass
            case 1:
                # West (0001)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x, self.y+const.TILE_SIZE - 1], 1) # West
            case 2:
                # South (0010)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y + const.TILE_SIZE - 1], [self.x+const.TILE_SIZE - 1, self.y+const.TILE_SIZE - 1], 1) # South
            case 3:
                # South West (0011)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x, self.y + const.TILE_SIZE - 1], [self.x + const.TILE_SIZE - 1, self.y + const.TILE_SIZE - 1]], 1) # South West
            case 4:
                # East (0100)
                pygame.draw.line(screen, (0,0,0), [self.x + const.TILE_SIZE - 1, self.y], [self.x+const.TILE_SIZE - 1, self.y+const.TILE_SIZE - 1], 1) # East
            case 5:
                # East West (0101)
                pygame.draw.line(screen, (0,0,0), [self.x + const.TILE_SIZE - 1, self.y], [self.x+const.TILE_SIZE - 1, self.y+const.TILE_SIZE - 1], 1) # East
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x, self.y+const.TILE_SIZE - 1], 1) # West
            case 6:
                # South East (0110)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y + const.TILE_SIZE - 1], [self.x+const.TILE_SIZE - 1, self.y+const.TILE_SIZE - 1], [self.x + const.TILE_SIZE - 1, self.y]], 1) # South East
            case 7:
                # South East West (0111)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x, self.y + const.TILE_SIZE-1], [self.x + const.TILE_SIZE - 1, self.y + const.TILE_SIZE-1], [self.x + const.TILE_SIZE - 1, self.y]], 1)
            case 8:
                # North (1000)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x+const.TILE_SIZE - 1, self.y], 1) # North
            case 9:
                # North West (1001)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x + const.TILE_SIZE - 1, self.y], [self.x, self.y], [self.x, self.y+const.TILE_SIZE - 1]], 1) # North West
            case 10:
                # North South (1010)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x+const.TILE_SIZE - 1, self.y], 1) # North
                pygame.draw.line(screen, (0,0,0), [self.x, self.y + const.TILE_SIZE - 1], [self.x+const.TILE_SIZE - 1, self.y+const.TILE_SIZE - 1], 1) # South
            case 11:
                # North South West (1011)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x + const.TILE_SIZE - 1, self.y], [self.x, self.y], [self.x, self.y+const.TILE_SIZE-1], [self.x + const.TILE_SIZE - 1, self.y + const.TILE_SIZE-1]], 1) # North South West
            case 12:
                # North East (1100)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x+const.TILE_SIZE - 1, self.y], [self.x + const.TILE_SIZE - 1, self.y + const.TILE_SIZE - 1]], 1)
            case 13:
                # North East West (1101)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y+const.TILE_SIZE], [self.x, self.y], [self.x + const.TILE_SIZE - 1, self.y], [self.x + const.TILE_SIZE - 1, self.y + const.TILE_SIZE]], 1) # North East West
            case 14:
                # North South East (1110)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x+const.TILE_SIZE -1, self.y], [self.x + const.TILE_SIZE -1, self.y + const.TILE_SIZE -1], [self.x, self.y + const.TILE_SIZE -1]], 1) # North South East
            case 15:
                # North South East West (1111)
                pygame.draw.rect(screen, (0,0,0), [self.x, self.y, const.TILE_SIZE, const.TILE_SIZE], 1) # all

        # self.drawUpdate(screen)
    def drawUpdate(self, screen):
        if self.flag: # automatically filters 0
            if g.flag[self.flag - 1].isHome():

            # if self.flagPicked:
                pygame.draw.polygon(screen, (self.spawnColor()), [[self.x + 35, self.y + 25], [self.x + 20, self.y + 35], [self.x + 20, self.y + 15]])
            else:
                pygame.draw.polygon(screen, (self.spawnColor()), [[self.x + 35, self.y + 25], [self.x + 20, self.y + 35], [self.x + 20, self.y + 15]], 3)

        if self.supply is not None:
            # draw the supply icon
            if self.picked:
                screen.blit(self.supply[0], (self.x + const.TILE_SIZE//2 - self.supply[0].get_width()//2, self.y + const.TILE_SIZE//2 - self.supply[0].get_height()//2))
            else:
                screen.blit(self.supply[1], (self.x + const.TILE_SIZE//2 - self.supply[1].get_width()//2, self.y + const.TILE_SIZE//2 - self.supply[1].get_height()//2))
        # self.drawText(screen)


    def spawnColor(self):
        if self.flag == 1:
            return c.geT("RED")
        if self.flag == 2:
            return c.geT("BLUE")

    def getNeighbours(self):
        return self.neighbours

    def getIndex(self):
        return self.index

    def getBordering(self):
        return self.bordering

    def setColor(self):
        self.color = c.geT("WHITE")

    def getCorners(self):
        return [(self.x, self.y), (self.x + const.TILE_SIZE, self.y), (self.x + const.TILE_SIZE, self.y + const.TILE_SIZE), (self.x, self.y + const.TILE_SIZE)]

    def isWithin(self, crds = None):
        # This function will check if the mouse is within the tile
        # Inputs: None
        # Outputs: Boolean value representing whether the mouse is within the tile
        if crds == None:
            mouseX, mouseY = pygame.mouse.get_pos()
        else:
            mouseX, mouseY = crds[0], crds[1]

        if mouseX >= self.x and mouseX <= self.x + const.TILE_SIZE and mouseY >= self.y and mouseY <= self.y + const.TILE_SIZE:
            if crds == None:
                self.printDebug()
            return True
        return False

    def setBorder(self, borderidx, value = True):
        self.border[borderidx] = value
        self.neighbours, self.bordering = self.neighbourCheck() # Update the neighbours list
        # Determine the correct base path
        if getattr(sys, 'frozen', False):  # Running as an .exe
            base_path = sys._MEIPASS
        else:  # Running as a .py script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the tile path dynamically
        self.tilePath = os.path.join(base_path, "Assets", "Tile")
        cardinal = ["N", "E", "S", "W"]
        self.rect = pygame.Rect(self.x, self.y, const.TILE_SIZE, const.TILE_SIZE)

        for idx, el in enumerate(self.bordering):
            if el != -1:
                self.tilePath += str(cardinal[idx])  # Append direction suffix

        self.tilePath += ".png"  # Add the file extension

        # Load the correct tile image
        self.image = pygame.image.load(self.tilePath).convert_alpha()

        # Load the debug tile image
        debugPath = os.path.join(base_path, "Assets", "TileDebug.png")
        self.debug = pygame.image.load(debugPath).convert_alpha()

    def setSupply(self, supplyPath, index = None):
        # This function will set the supply icon for the tile
        # Inputs: supplyPath: The path to the supply icon
        # Outputs: None
        if supplyPath is not None:
            self.supply = [None, None]
            self.supply[0] = pygame.image.load(supplyPath[0]).convert_alpha()
            self.supply[0] = pygame.transform.scale(self.supply[0], (const.TILE_SIZE//2, const.TILE_SIZE//2))
            self.supply[1] = pygame.image.load(supplyPath[1]).convert_alpha()
            self.supply[1] = pygame.transform.scale(self.supply[1], (const.TILE_SIZE//2, const.TILE_SIZE//2))
            self.supplyIndex = index

    def getCenter(self):
        return (self.x + const.TILE_SIZE//2, self.y + const.TILE_SIZE//2) 

    def setTarget(self, value):
        self.AITarget = value

    def setBorderIndex(self, index):
        self.border = [index>=8,(index%8)>=4, (index%4)>=2, (index%2)==1]
        self.borderindex = index

    def printDebug(self):
        print("Index: ", self.index, end = " ")
        print(self.index%14, self.index//14)
        print("Neighbours: ", self.neighbours, end = " ")
        print("Bordering: ", self.bordering, end = " ")
        print("Border: ", self.border)
        print("Border Index: ", self.borderindex)

    def setSpawn(self, spawn):
        self.spawn = spawn

    def setSpecial(self, num):
        if num == 1 or num == 2:
            # spawnpoint
            self.spawn = True
        if num == 3:
            self.flag = 1 # red
            g.flag[0].setxy((self.x, self.y))
            g.flag[0].setHome((self.x, self.y))
        if num == 4:
            self.flag = 2 # blue
            g.flag[1].setxy((self.x, self.y))
            g.flag[1].setHome((self.x, self.y))

class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.images = []
        # Determine the correct base path
        if getattr(sys, 'frozen', False):  # Running as an .exe
            base_path = sys._MEIPASS
        else:  # Running as a .py script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the correct path for the sprite sheet
        sprite_sheet_path = os.path.join(base_path, "Assets", "explosion.png")

        # Load the sprite sheet
        SpriteSheetImage = pygame.image.load(sprite_sheet_path).convert_alpha()
        for i in range(48):
            self.images.append(self.getImage(SpriteSheetImage, i, 128, 128, 0.5))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lastUpdate = pygame.time.get_ticks()
        self.animationCooldown = 12

    def getImage(self, sheet, frame, width, height, scale):
        # This function will use the spritesheet to get the respective image from the sprite sheet
        # Inputs: Sheet: The required sprite sheet for the animation
        # Inputs: Frame: The frame index of the animation
        # Inputs: Width: The width of the frame
        # Inputs: Height: The height of the frame
        # Inputs: Scale: The scale of which to scale the image to
        # Outputs: The image of the frame
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), ((frame*width%1024), (frame//8 * width), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey((0, 0, 0)) # Black
        return image

    def update(self):
        # This function will update the explosion animation every frame
        # Inputs: None
        # Outputs: None
        currentTime = pygame.time.get_ticks()
        if currentTime - self.lastUpdate >= self.animationCooldown:
            self.lastUpdate = currentTime
            self.index += 1
        if self.index >= len(self.images):
            self.kill()
        else:
            self.image = self.images[self.index]

    def setCooldown(self, num):
        self.animationCooldown = num

    def getCooldown(self):
        return self.animationCooldown


class Flag():
    def __init__(self, team, coords):
        self.team = team
        self.dropped = False
        self.returnTimer = 1400
        self.xy = coords
        self.homexy = coords
        self.tank = None
        self.score = 0
    def update(self):
        if self.dropped:
            self.returnTimer -= 1
        if self.returnTimer < 0:
            self.returnTimer = 0
            # return the flag
            self.returnFlag()
        for i in range(g.difficultyType.playerCount):
            if not g.tankDead[i]:
                if self.isWithin(g.tankList[i].getCenter()):
                    # if we are within, award the flag
                    # if the tank is on the same team as the flag, then auto return
                    # if not, then give the flag

                    if g.tankList[i].getTeam() != (self.team): # if they are not the same team
                        if not self.isHome() and self.dropped:
                            self.returnFlag()
                        # if the tank has a flag, return the flag
                        elif g.tankList[i].flag != None:
                            # if one of the two flags is not home, return the flag
                            if g.flag[0].isHome() or g.flag[1].isHome(): # if one is home
                                g.flag[0].returnFlag()
                                g.flag[1].returnFlag()
                                g.flag[0].setTank(None)
                                g.flag[1].setTank(None)
                                g.tankList[i].setFlag(None)
                                # we need to update the score
                                self.score += 1
                    else:
                        if self.dropped or self.isHome():
                            self.dropped = False
                            self.returnTimer = 1400
                            g.flag[self.team].setTank(g.tankList[i])
                            g.tankList[i].setFlag(self.team) # give the tank the flag property
        if self.tank is not None: # if we have been picked up
            self.xy = self.tank.getCenter()
        else: # if it is none
            if self.xy != self.homexy:
                self.dropped = True # it's been dropped somewhere
                self.tank = None

    def isWithin(self, coords):
        cX, cY = coords[0], coords[1]
        if cX >= self.xy[0] and cX <= self.xy[0] + const.TILE_SIZE and cY >= self.xy[1] and cY <= self.xy[1] + const.TILE_SIZE:
            return True
        return False

    def isHome(self):
        return self.xy == self.homexy # if these are equal we are at the spawn location of the flag

    def draw(self, screen):
        if self.team == 1:
            pygame.draw.rect(screen, c.geT("BLUE"), [self.xy[0], self.xy[1], 50, 50])
            # pygame.draw.polygon(screen, c.geT("BLUE"), [[self.xy[0] + const.SCREEN_WIDTH//2, self.xy[1] + const.SCREEN_HEIGHT//2], [self.xy[0] + const.SCREEN_WIDTH//2 - 10, self.xy[1] + const.SCREEN_HEIGHT//2 + 10], [self.xy[0] + const.SCREEN_WIDTH//2 - 10, self.xy[1] + const.SCREEN_HEIGHT//2 - 10]])
        else:
            pygame.draw.rect(screen, c.geT("RED"), [self.xy[0], self.xy[1], 50, 50])
            # pygame.draw.polygon(screen, c.geT("RED"), [[self.xy[0] + const.SCREEN_WIDTH//2, self.xy[1] + const.SCREEN_HEIGHT//2], [self.xy[0] + const.SCREEN_WIDTH//2 - 10, self.xy[1] + const.SCREEN_HEIGHT//2 + 10], [self.xy[0] + const.SCREEN_WIDTH//2 - 10, self.xy[1] + const.SCREEN_HEIGHT//2 - 10]]

    def returnFlag(self):
        self.xy = self.homexy
        self.returnTimer = 1400
        self.dropped = False
        self.tank = None # remove the tank

    def getTeam(self):
        return self.team

    def setxy(self, xy):
        self.xy = xy
    
    def setHome(self, home):
        self.homexy = home

    def setTank(self, tank):
        self.tank = tank

    def drop(self):
        self.dropped = True

    def getScore(self):
        return self.score