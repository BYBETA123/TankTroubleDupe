import pygame
import random
import math
import time
import os
from ColorDictionary import ColorDicionary
from enum import Enum
from UIUtility import Button, ButtonSlider, TextBox
#Classes

# Tank sprite class
class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, controls, name = "Default"):
        super().__init__()
        try:
            # Load the tank image
            currentDir = os.path.dirname(__file__)
            tankPath = os.path.join(currentDir, 'Sprites', 'tank1.png')
            self.originalTankImage = pygame.image.load(tankPath).convert_alpha()
            print(f"Original tank image size: {self.originalTankImage.get_size()}")

            # Scale the tank image to a smaller size
            self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
            print(f"Scaled tank image size: {self.tankImage.get_size()}")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            pygame.quit()
            exit()

        # Setting variables
        self.angle = 0
        self.center = (x, y)
        self.controls = controls
        self.health = 100
        self.image = self.tankImage
        self.maxHealth = 100
        self.name = name
        self.rect = self.tankImage.get_rect(center=(x, y))
        self.rotationSpeed = 0
        self.speed = 0
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.updateCorners() #Set the corners
        self.soundPlaying = False

    def updateCorners(self):
        # This function will update the corners of the tank based on the new position
        # Inputs: None
        # Outputs: None
        cx, cy = self.rect.center
        w, h = self.width / 2, self.height / 2
        rad = math.radians(self.angle)
        rad = math.pi * 2 - rad
        cosA = math.cos(rad)
        sinA = math.sin(rad)

        self.corners = [
            (cx + cosA * -w - sinA * -h, cy + sinA * -w + cosA * -h),
            (cx + cosA * w - sinA * -h, cy + sinA * w + cosA * -h),
            (cx + cosA * w - sinA * h, cy + sinA * w + cosA * h),
            (cx + cosA * -w - sinA * h, cy + sinA * -w + cosA * h),
        ] # Using trigonomety to calculate the corners

    def fixMovement(self, dx, dy):
        # This function checks if the tank is moving into illegeal locations and corrects it
        # Inputs: dx, dy: The change in x and y coordinates
        # Outputs: The corrected x and y coordinates

        tempX = self.x + dx
        tempY = self.y - dy

        #We are outside of the maze
        if tempX <= mazeX + self.originalTankImage.get_size()[0]/2:
            tempX = mazeX + self.originalTankImage.get_size()[0]/2
        if tempY <= mazeY + self.originalTankImage.get_size()[0]/2:
            tempY = mazeY + self.originalTankImage.get_size()[0]/2
        if tempX > mazeWidth + mazeX - self.originalTankImage.get_size()[0]/2:
            tempX = mazeWidth + mazeX - self.originalTankImage.get_size()[0]/2
        if tempY > mazeHeight + mazeY - self.originalTankImage.get_size()[0]/2:
            tempY = mazeHeight + mazeY - self.originalTankImage.get_size()[0]/2

        if satCollision(tank1, tank2): #If the tanks are colliding
            if self.name == p1TankName:
                #If there is a collision here, move the other tank
                    #This player is being pushed
                    tank2.setCoords(tank2.x + dx, tank2.y - dy)
                    tempX = self.x - dx
                    tempY = self.y + dy
            elif self.name == p2TankName:
                #If there is a collision here, move the other tank
                    #This player is being pushed
                    tank1.setCoords(tank1.x + dx, tank1.y - dy)
                    tempX = self.x - dx
                    tempY = self.y + dy
            else:
                print("Error: Invalid tank name")

        #Check for collision with walls
        #We are going to calculate the row and column
        row = math.ceil((self.getCenter()[1] - mazeY)/tileSize)
        col = math.ceil((self.getCenter()[0] - mazeX)/tileSize)
        #Find the file at the exact index
        index = (row-1)*colAmount + col

        #Check if the tank is colliding with the walls
        tile = tileList[index-1]
        if tile.border[0] and tempY - self.originalTankImage.get_size()[1] <= tile.y: #If the top border is present
            tempY = tile.y + self.originalTankImage.get_size()[1]
        if tile.border[1] and tempX + self.originalTankImage.get_size()[0]/2 >= tile.x + tileSize: #If the right border is present
            tempX = tile.x + tileSize - self.originalTankImage.get_size()[0]/2
        if tile.border[2] and tempY + self.originalTankImage.get_size()[1] > tile.y + tileSize: #If the bottom border is present
            tempY = tile.y + tileSize - self.originalTankImage.get_size()[1]
        if tile.border[3] and tempX - self.originalTankImage.get_size()[0]/2 < tile.x: #If the left border is present
            tempX = tile.x + self.originalTankImage.get_size()[0]/2

        #finalise the changes
        self.rect.centerx = int(tempX)
        self.rect.centery = int(tempY)
        return tempX, tempY

    def update(self):
        # This function updates the tank's position and rotation based on the current controls
        # Inputs: None
        # Outputs: None

        keys = pygame.key.get_pressed()
        global tankSpeed
        if keys[self.controls['up']]:
            self.speed = tankSpeed
        elif keys[self.controls['down']]:
            self.speed = -tankSpeed
        else:
            self.speed = 0
        if keys[self.controls['left']]:
            self.rotationSpeed = rotationalSpeed
        elif keys[self.controls['right']]:
            self.rotationSpeed = -rotationalSpeed
        else:
            self.rotationSpeed = 0

        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if self.speed != 0 or self.rotationSpeed != 0:
            if not self.soundPlaying:
                tankMoveSFX.play(-1)  # Play sound indefinitely
                self.soundPlaying = True
        else:
            if self.soundPlaying:
                tankMoveSFX.stop()
                self.soundPlaying = False

        self.angle += self.rotationSpeed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.originalTankImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        angleRad = math.radians(self.angle)
        dx = math.cos(angleRad) * self.speed
        dy = math.sin(angleRad) * self.speed
        self.x, self.y = self.fixMovement(dx,dy) # Adjust the movement

    def getHealth(self):
        return self.health, self.maxHealth

    def damage(self, damage):
        # This function will adjust the damage that the tank has taken
        # Inputs: damage: The amount of damage that the tank has taken
        # Outputs: None
        self.health -= damage
        global tank1Health, tank2Health
        if self.name == p1TankName:
            print("Damage: ", tank1Health)
            tank1Health -= damage
        elif self.name == p2TankName:
            print("Damage Updated: ", tank2Health)
            tank2Health -= damage
        else:
            print("Error: Invalid tank name")

        if self.health <= 0:
            global explosionGroup
            if self.name == p1TankName:
                gun1.setCooldown()
                gun1.kill()
                tankMoveSFX.stop()
                turretRotateSFX.stop()
                global gun1Cooldown
                gun1Cooldown = 300
                tank1.setCentre(2000, 2000)
                self.kill()
                allSprites.remove(gun1)
                allSprites.remove(self)
                explosion = Explosion(self.x, self.y)
                explosionGroup.add(explosion)
            elif self.name == p2TankName:
                explosion = Explosion(tank2.getCenter()[0], tank2.getCenter()[1])
                gun2.setCooldown()
                tankMoveSFX.stop()
                turretRotateSFX.stop()
                global gun2Cooldown
                gun2Cooldown = 300
                gun2.kill()
                tank2.setCentre(1000, 1000)
                self.kill()
                allSprites.remove(gun2)
                allSprites.remove(self)
                explosionGroup.add(explosion)
            else:
                print("Error: Invalid tank name")

    def getCoords(self):
        return [self.rect.x, self.rect.y, self.rect.x + self.originalTankImage.get_size()[0], self.rect.y + self.originalTankImage.get_size()[1]]

    def getCorners(self):
        return self.corners
    
    def getCenter(self):
        return self.rect.center
    
    def setCoords(self, newx, newy):
        self.x, self.y = newx, newy

    def setCentre(self, x, y):
        self.rect.center = (x, y)

class Gun(pygame.sprite.Sprite):
    def __init__(self, tank, controls, name):
        """
        Initializes the Gun class.

        Parameters:
        ----------
        tank : pygame.sprite.Sprite
            The tank object to which the gun is attached.
        controls : dict
            A dictionary mapping control actions (e.g., 'rotate_left', 'fire') to specific keys.
        """
        super().__init__()

        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'gun1.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        self.gunImage = self.originalGunImage
        self.image = self.gunImage
        self.rect = self.gunImage.get_rect(center=tank.rect.center)
        self.angle = 0
        self.rotationSpeed = 0
        self.tank = tank
        self.gunLength = -24
        self.gunRotationDirection = 0
        self.tipOffSet = 30
        self.controls = controls
        self.name = name
        self.originalGunLength = self.gunLength
        self.gunBackStartTime = 0
        self.gunBackDuration = 200
        self.canShoot = True
        self.shootCooldown = 0
        self.cooldownDuration = 300
        self.soundPlaying=False
        self.lastUpdateTime = pygame.time.get_ticks()

        # Initialize the gun's floating-point position
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def update(self):
        """
        Updates the gun's position, rotation, and shooting state based on the current controls and time.

        This method checks for key presses to rotate the gun, 
        handles shooting if the fire key is pressed, 
        and updates the gun's visual position and rotation. 
        It also manages the shooting cooldown.

        Inputs:
        -------
        None

        Outputs:
        --------
        None
        """
        keys = pygame.key.get_pressed()
        #Checks what keys are pressed, and changes speed accordingly
        #If tank hull moves left or right, the gun will also move simultaneously
        #with the tank hull at the same speed and direction.
        global turretSpeed, rotationalSpeed
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed = turretSpeed
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed = -turretSpeed
        elif  keys[self.controls['left']]:
            self.rotationSpeed = rotationalSpeed
        elif keys[self.controls['right']]:
            self.rotationSpeed = -rotationalSpeed
        else:
            self.rotationSpeed = 0

        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if keys[self.controls['rotate_left']] or keys[self.controls['rotate_right']]:
            if self.rotationSpeed != 0:
                if not self.soundPlaying:
                    turretRotateSFX.play(loops = -1, fade_ms = 100)  # Play sound indefinitely
                    self.soundPlaying = True
            else:
                if self.soundPlaying:
                    turretRotateSFX.stop()
                    self.soundPlaying = False
        else:
            if self.soundPlaying:
                turretRotateSFX.stop()
                self.soundPlaying = False
                
    
        self.angle += self.rotationSpeed
        self.angle %= 360
        
        #Reload cooldown of bullet and determines the angle to fire the bullet,
        #which is relative to the posistion of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            self.gunBackStartTime = pygame.time.get_ticks()  # Start moving the gun back
            bulletAngle = self.angle
            bulletX = self.rect.centerx + (self.gunLength + self.tipOffSet) * math.cos(math.radians(bulletAngle))
            bulletY = self.rect.centery - (self.gunLength + self.tipOffSet) * math.sin(math.radians(bulletAngle))
            bullet = Bullet(bulletX, bulletY, bulletAngle, self.gunLength, self.tipOffSet)
            allSprites.add(bullet)
            bulletSprites.add(bullet)

            self.canShoot = False
            self.shootCooldown = self.cooldownDuration
            #If either tank shoots, play this sound effect.
            tankShootSFX.play()

        #Here is the bullet cooldown
        elapsedTime = pygame.time.get_ticks() - self.gunBackStartTime
        if elapsedTime <= self.gunBackDuration:
            progress = elapsedTime / self.gunBackDuration
            self.gunLength = self.originalGunLength - 5 * progress
        else:
            self.gunLength = self.originalGunLength

        angleRad = math.radians(self.angle)
        gunEndX = self.tank.rect.centerx + (self.gunLength + self.tipOffSet) * math.cos(angleRad)
        gunEndY = self.tank.rect.centery - (self.gunLength + self.tipOffSet) * math.sin(angleRad)

        rotatedGunImage = pygame.transform.rotate(self.originalGunImage, self.angle)
        self.image = rotatedGunImage
        self.rect = self.image.get_rect(center=(gunEndX, gunEndY))

        if self.name == p1GunName:
            global gun1Cooldown
            gun1Cooldown = self.shootCooldown
        elif self.name == p2GunName:
            global gun2Cooldown
            gun2Cooldown = self.shootCooldown
        else:
            print("Error: Invalid gun name")

        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.shootCooldown = 0
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

    def setCooldown(self):
        self.shootCooldown = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, gunLength, tipOffSet):
        """
        Initializes the Bullet class.

        Parameters:
        ----------
        x : int
            The x-coordinate of the bullet's starting position.
        y : int
            The y-coordinate of the bullet's starting position.
        angle : float
            The angle at which the bullet is fired.
        gunLength : float
            The length of the gun.
        tipOffSet : float
            The offset from the gun's tip to the bullet's starting position.
        """
        super().__init__()
        currentDir = os.path.dirname(__file__)
            
        bulletPath = os.path.join(currentDir, 'bullet.png')
        self.originalBulletImage = pygame.image.load(bulletPath).convert_alpha()
        self.bulletImage = self.originalBulletImage
        self.image = self.bulletImage
        self.angle = angle
        self.speed = bulletSpeed

        angleRad = math.radians(self.angle)

        dx = (gunLength + tipOffSet) * math.cos(angleRad)
        dy = -(gunLength + tipOffSet) * math.sin(angleRad)

        self.rect = self.bulletImage.get_rect(center=(x + dx, y + dy))
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.bounce = 5 #Abitrary number but the amount of bounces before the bullet is removed
        self.corners = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), (self.rect.x, self.rect.y + self.rect.height)]
        self.damage = 100
    def update(self):
        """
        Updates the bullet's position based on its speed and direction.

        This method calculates the new position of the bullet and updates its rect attribute accordingly.

        Inputs:
        -------
        None

        Outputs:
        --------
        None
        """
        angleRad = math.radians(self.angle)
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)
        tempX = self.x + dx
        tempY = self.y + dy
        #Check for collision with walls
        #We are going to calculate the row and column
        row = math.ceil((self.getCenter()[1] - mazeY)/tileSize)
        col = math.ceil((self.getCenter()[0] - mazeX)/tileSize)
        #Find the file at the exact index
        index = (row-1)*colAmount + col

        #If we are outside of the maze, delete the bullet
        if tempX <= mazeX or tempY <= mazeY or tempX >= mazeWidth + mazeX or tempY >= mazeHeight + mazeY:
            self.kill()
            return
        
        #If we hit a tank
        tank1Collision = satCollision(self, tank1)
        tank2Collision = satCollision(self, tank2)
        if tank1Collision or tank2Collision:
            global p1Score, p2Score, gameOverFlag
            #If either tank dies, play this tank dead sound effect.
            tankDeadSFX.play()
            if tank1Collision: #If we hit tank1 then give p2 a point
                tank1.damage(self.damage)
                self.kill()
                
            else:
                tank2.damage(self.damage)
                self.kill()
            global tank1Dead, tank2Dead
            if tank1.getHealth()[0] <= 0:
                gameOverFlag = True #The game is over
                self.kill()
                gun1.setCooldown()
                #The tank is dead
                if not tank1Dead:
                    print("Player 2 Wins")
                    p2Score += 1
                    tank1Dead = True
            if tank2.getHealth()[0] <= 0:
                gameOverFlag = True #The game is over
                self.kill()
                gun2.setCooldown()
                if not tank2Dead:
                    print("Player 1 Wins")
                    p1Score += 1
                    tank2Dead = True
                #The tank is dead


            return

        tile = tileList[index-1]
        wallCollision = False
        if tile.border[0] and tempY - self.originalBulletImage.get_size()[1] <= tile.y: #If the top border is present
            wallCollision = True
            self.angle = 180 - self.angle
        if tile.border[1] and tempX + self.originalBulletImage.get_size()[1] >= tile.x + tileSize: #If the right border is present
            wallCollision = True
            self.angle = 360 - self.angle
        if tile.border[2] and tempY + self.originalBulletImage.get_size()[1] >= tile.y + tileSize: #If the bottom border is present
            wallCollision = True
            self.angle = 180 - self.angle
        if tile.border[3] and tempX - self.originalBulletImage.get_size()[1] <= tile.x: #If the left border is present
            wallCollision = True
            self.angle = 360 - self.angle
        if wallCollision:
            self.bounce -= 1
            self.speed *= -1
            if self.bounce == 0:
                self.kill() # delete the bullet
        self.updateCorners()
        self.rect.x = int(tempX)
        self.rect.y = int(tempY)
        self.x = tempX
        self.y = tempY

    def getCenter(self):
        return (self.x, self.y)

    def updateCorners(self):
        self.corners = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height), (self.rect.x, self.rect.y + self.rect.height)]

class Tile:
    # border = [False, False, False, False]
    #Border format is [Top, Right, Bottom, Left]
    border = [True, True, True, True]
    borderWidth = 2
    spawn = False
    def __init__(self, index, x, y, color, spawn = False):
        self.index = index
        self.x = x
        self.y = y
        self.color = color
        self.spawn = spawn
        if spawn:
            self.color = c.geT('GREEN')
        self.border = self.borderControl()
        self.neighbours, self.bordering = self.neighbourCheck()

    def neighbourCheck(self):
        #This function will return a list of the indexes of the neighbours based on the current list of border
        # No inputs are needed
        # The output will be an updated list of neighbours
        #
        neighbours = [self.index - colAmount, self.index + 1, self.index + colAmount, self.index - 1]
        #Check if there are any invalid neighbours
        newlist = []
        oldlist = [-1, -1, -1, -1]
        for idx, neighbour in enumerate(neighbours):
            if neighbour < 1 or neighbour > rowAmount*colAmount:
                #We do not want this
                pass
            elif self.border[idx] == True:
                #We do not want this
                oldlist[idx] = neighbour
            else:
                newlist.append(neighbour)
        return newlist, oldlist

    def borderControl(self):
        # This function checks and validates the borders for the tile
        # No inputs
        # Outputs: A list of boolean values representing whether the border is present
        #
        localIndex = self.index
        border = [False, False, False, False] # Start with everything false
        #Sides
        # Top Row
        if localIndex in range(1, colAmount+1):
            border[0] = True
        # Right Row
        if localIndex in range(colAmount, rowAmount*colAmount+1, colAmount):
            border[1] = True
        # Bottom Row
        if localIndex in range(99, rowAmount*colAmount + 1):
            border[2] = True
        #Left Row
        if localIndex in range(1, rowAmount*colAmount, colAmount):
            border[3] = True

        if self.spawn:
            #If the tile is a spawn then its border should be handled carefully
            return border

        for i in range(len(border)):
            if not border[i]:
                # border[i] = random.choices([True, False])
                border[i] = random.choices([True, False], weights = (weightTrue, 1-weightTrue))[0]

        return border


    def drawText(self, screen):
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(str(self.index), True, c.geT("BLACK"))
        screen.blit(text, [self.x + tileSize/2 - text.get_width()/2, self.y + tileSize/2 - text.get_height()/2])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, tileSize, tileSize])
        #Draw the border
        if self.border[0]:
            pygame.draw.line(screen, c.geT("BLACK"), [self.x, self.y], [self.x+tileSize, self.y], self.borderWidth)
        if self.border[1]:
            pygame.draw.line(screen, c.geT("BLACK"), [self.x + tileSize, self.y], [self.x+tileSize, self.y+tileSize], self.borderWidth)
        if self.border[2]:
            pygame.draw.line(screen, c.geT("BLACK"), [self.x, self.y + tileSize], [self.x+tileSize, self.y+tileSize], self.borderWidth)
        if self.border[3]:
            pygame.draw.line(screen, c.geT("BLACK"), [self.x, self.y], [self.x, self.y+tileSize], self.borderWidth)
        #Draw the index
        # self.drawText(screen)

    def getNeighbours(self):
        return self.neighbours

    def getIndex(self):
        return self.index

    def getBordering(self):
        return self.bordering

    def setColor(self):
        self.color = c.geT("WHITE")

    def setBorder(self, borderidx, value = True):
        self.border[borderidx] = value
        self.neighbours, self.bordering = self.neighbourCheck() # Update the neighbours list

class Explosion(pygame.sprite.Sprite):    
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        SpriteSheetImage = pygame.image.load('explosion.png').convert_alpha()
        for i in range(48):
            self.images.append(self.get_image(SpriteSheetImage, i, 128, 128, 0.5))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lastUpdate = pygame.time.get_ticks()
        global animationCool
        self.animationCooldown = animationCool

    def get_image(self, sheet, frame, width, height, scale):
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

class GameMode(Enum):
    #This class is responsible for the game mode
    # This class doesn't have other function as they are not needed
    pause = 0
    play = 1
    home = 2
    settings = 3
    selection = 4

#Functions
def tileGen():
    # This function is responsible for generating the tiles for the maze
    # Inputs: No inputs
    # Outputs: A list of tiles that make up the maze
    #
    def validateChoice(option, choices):
        # This function validates whether or not a spawn location is valid with some arbitrary parameters
        # Inputs: option: the current proposed spawn location
        # Inputs: choices: the current list of spawn locations
        # Outputs: True if the spawn location is valid, False otherwise

        #Make sure the spawns are far away from each other
        columnOffset = 6 # Max = 14
        rowOffset = 3 # Max = 8
        if len(choices)>0: # We have elements in the list
            #We need to check how close it is to the other spawn
            if option in choices:
                return False
            
            #Extracting the row/col
            # print("rowAmount: ", rowAmount, "colAmount: ", colAmount)
            row1, col1 = choices[0]//colAmount, choices[0]%colAmount
            row2, col2 = option//colAmount, option%colAmount

            if abs(col1-col2) < columnOffset:
                print("Column Check Failed, ", col1, col2, "Difference: ", abs(col1-col2), "Offset: ", columnOffset)
                return False
            if abs(row1-row2) < rowOffset:
                print("Row Check Failed, ", row1, row2, "Difference: ", abs(row1-row2), "Offset: ", rowOffset)
                return False
            #If they are edge cases, try the other side
            if col1 == 0:
                col1 = rowAmount
            if col2 == 0:
                col2 = rowAmount
            if row1 == 0:
                row1 = colAmount
            if row2 == 0:
                row2 = colAmount

            #Sanity check with edge cases
            if abs(col1-col2) < columnOffset:
                print("Column Check Failed, ", col1, col2, "Difference: ", abs(col1-col2), "Offset: ", columnOffset)
                return False
            if abs(row1-row2) < rowOffset:
                print("Row Check Failed, ", row1, row2, "Difference: ", abs(row1-row2), "Offset: ", rowOffset)
                return False
            return True # If we pass both checks then there is no other concern
        else:
            return True

    def breathFirstSearch(tileList, choices, option):
        # This function will search the maze in a breath first manner to see if we can reach the second spawn
        # Inputs: tileList: The current list of tiles
        # Inputs: Choices: The locations of both spawns
        # Outputs: True if the second spawn is reachable, False otherwise


        #Setting up the BFS
        visitedQueue = []
        tracking = [False for _ in range(rowAmount*colAmount+1)]
        queue = [choices[option]]
        visitedQueue.append(choices[option])
        tracking[choices[option]] = True
        while len(queue) > 0: # While there are still elements to check
            current = queue.pop(0)
            for neighbour in tileList[current-1].getNeighbours():
                if not tracking[neighbour]:
                    queue.append(neighbour)
                    visitedQueue.append(neighbour)
                    tracking[neighbour] = True

        if choices[(option +1) % 2] in visitedQueue: # If the second spawn is reachable
            return True
        else:
            return False

    validMaze = False
    while not validMaze: # While our maze isn't valid
        tileList = []
        index = 1
        choice = [i for i in range(1,rowAmount*colAmount+1)] # Make all the choices
        choices = []
        option = random.choice(choice) # Select the spawn zones
        failsafe = 0
        while len(choices) < 2 and failsafe < 10: # We only 2 spawns
            if validateChoice(option, choices):
                choices.append(option)
                tempChoice = choices.copy()
                #Remove close choices that are invalid so that we can choose a valid one more easily
                for i in range(2, len(choice)):
                    row1, col1 = choices[0]//colAmount, choices[0]%colAmount
                    row2, col2 = i//colAmount, i%colAmount
                    if abs(col1-col2) >= 6 and abs(row1-row2) >= 3:
                        tempChoice.append(i)
            option = random.choice(tempChoice) # Try again
            failsafe += 1
        if failsafe == 10: # In case we are running for too long
            print("failsafe activated")
            choices = [1,rowAmount*colAmount]
        for j in range(mazeY, mazeHeight + 1, tileSize): # Assign the tiles and spawns once everything is found
            for i in range(mazeX, mazeWidth + 1, tileSize):
                if index in choices:
                    spawn = True
                else:
                    spawn = False

                tileList.append(Tile(index, i, j, c.geT("LIGHT_GREY"), spawn))
                index += 1

        #We need to make sure that all the borders are bordered on both sides
        for tile in tileList:
            bordering = tile.getBordering()
            for border in bordering:
                if border != -1:
                    tileList[border-1].setBorder((bordering.index(border)+2)%4, tile.border[bordering.index(border)])

        #Validate the tileList
        validMaze = breathFirstSearch(tileList, choices, 0) and breathFirstSearch(tileList, choices, 1)
    global spawnpoint
    spawnpoint = []
    spawnpoint = choices

    return tileList

# Helper functions for SAT
def getEdges(corners):
    #This function will return the edges of the polygon
    # Inputs: corners: The corners of the polygon
    # Outputs: A list of edges
    edges = []
    for i in range(len(corners)):
        edge = (corners[i][0] - corners[i - 1][0], corners[i][1] - corners[i - 1][1])
        edges.append(edge)
    return edges

def getPerpendicularVector(edge):
    #This function will return the perpendicular vector to the edge
    # Inputs: edge: The edge of the polygon
    # Outputs: The perpendicular vector
    return (-edge[1], edge[0])

def dotProduct(v1, v2):
    #This function will return the dot product of two vectors
    # Inputs: v1, v2: The two vectors
    # Outputs: The dot product
    return v1[0] * v2[0] + v1[1] * v2[1]

def projectPolygon(corners, axis):
    #This function will project the polygon onto the axis
    # Inputs: corners: The corners of the polygon
    # Inputs: axis: The axis to project onto
    # Outputs: The projection
    minProj = dotProduct(corners[0], axis)
    maxProj = minProj
    for corner in corners[1:]:
        projection = dotProduct(corner, axis)
        if projection < minProj:
            minProj = projection
        if projection > maxProj:
            maxProj = projection
    return minProj, maxProj

def overlap(proj1, proj2):
    #This function will check if the projections overlap
    # Inputs: proj1, proj2: The two projections
    # Outputs: True if they overlap, False otherwise
    return proj1[0] < proj2[1] and proj2[0] < proj1[1]

def satCollision(rect1, rect2):
    #This function will check if two rectangles are colliding
    # Inputs: rect1, rect2: The two rectangles
    # Outputs: True if they are colliding, False otherwise
    for rect in [rect1, rect2]:
        edges = getEdges(rect.corners)
        for edge in edges:
            axis = getPerpendicularVector(edge)
            proj1 = projectPolygon(rect1.corners, axis)
            proj2 = projectPolygon(rect2.corners, axis)
            if not overlap(proj1, proj2):
                return False
    return True

def playGame():
    # This function controls the main execution of the game
    # Inputs: None
    # Outputs: None
    # Because of the way the game is structured, these global variables can't be avoided
    global gameOverFlag, cooldownTimer, startTime, tank1Health, tank2Health, p1Score, p2Score
    global tank1Dead, tank2Dead, gun1Cooldown, gun2Cooldown, tileList, spawnpoint
    global tank1, tank2, gun1, gun2, allSprites, bulletSprites

    if gameOverFlag:
        #The game is over
        startTime = time.time() #Start a 5s timer
        gameOverFlag = False
        cooldownTimer = True
    if cooldownTimer:
        if time.time() - startTime >= 3:
            #Reset the game
            reset()

    #UI Elements
    
    #Making the string for score
    p1ScoreText = str(p1Score)
    p2ScoreText = str(p2Score)
    
    #Setting up the text
    fontScore = pygame.font.SysFont('Calibri', 100, True, False)
    fontName = pygame.font.SysFont('Calibri', 35, True, False)
    # Player 1 Text
    textp1 = fontScore.render(p1ScoreText, True, c.geT("WHITE"))
    textp1Name = fontName.render(" Plwasd1", True, c.geT("WHITE"))

    # Player 2 Text
    textp2 = fontScore.render(p2ScoreText, True, c.geT("WHITE"))
    textp2Name = fontName.render(" Plarro2", True, c.geT("WHITE"))

    #Misc Text
    text3 = fontScore.render("-",True,c.geT("WHITE"))

    #Visualing player 1
    screen.blit(textp1,[windowWidth/2 - textp1.get_width()-text3.get_width()/2, 0.8*windowHeight]) # This is the score on the left
    screen.blit(textp1Name,[p1NameIndent, 0.783*windowHeight]) # This is the name on the left
    #Health bars outline
    #Health bar
    pygame.draw.rect(screen, c.geT("RED"), [p1NameIndent, 0.8*windowHeight + textp1Name.get_height(), barWidth*((tank1Health)/100), barHeight]) # Bar
    pygame.draw.rect(screen, c.geT("BLACK"), [p1NameIndent, 0.8*windowHeight + textp1Name.get_height(), barWidth, barHeight], 2) # Outline
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [p1NameIndent, 0.8*windowHeight + textp1Name.get_height() + mazeY, barWidth*((300-gun1Cooldown)/300), barHeight]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, c.geT("BLACK"), [p1NameIndent, 0.8*windowHeight + textp1Name.get_height() + mazeY, barWidth, barHeight], 2) # Outline
    #Visualising player 2
    screen.blit(textp2,[windowWidth/2 + text3.get_width()*1.5, 0.8*windowHeight]) # This is the score on the right 
    screen.blit(textp2Name,[p2NameIndent - textp2Name.get_width(), 0.783*windowHeight]) # This is the name on the left
    #Health bars
    pygame.draw.rect(screen, c.geT("RED"), [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height(), barWidth, barHeight])
    pygame.draw.rect(screen, c.geT("GREY"), [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height(), barWidth*((100-tank2Health)/100), barHeight])
    pygame.draw.rect(screen, c.geT("BLACK"), [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height(), barWidth, barHeight], 2)
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height() + mazeY, barWidth*((300-gun2Cooldown)/300), barHeight]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, c.geT("BLACK"), [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height() + mazeY, barWidth, barHeight], 2) # Outline

    # Misc text and other little pieces
    screen.blit(text3,[windowWidth/2,0.79*windowHeight])

    # Draw the border
    pygame.draw.rect(screen, c.geT("BLACK"), [mazeX, mazeY, mazeWidth,mazeHeight], 1) # The maze border


    for tile in tileList:
        tile.draw(screen)

    #Anything below here will be drawn on top of the maze and hence is game updates

    #Update the location of the corners
    tank1.updateCorners()
    tank2.updateCorners()
    # pygame.draw.polygon(screen, GREEN, tank1.getCorners(), 2) #Hit box outline
    # pygame.draw.polygon(screen, GREEN, tank2.getCorners(), 2) #Hit box outline
    allSprites.update()
    bulletSprites.update()
    explosionGroup.update()
    allSprites.draw(screen)
    bulletSprites.draw(screen)
    explosionGroup.draw(screen)

def pauseScreen():
    # This function will draw the pause screen
    # Inputs: None
    # Outputs: None
    pauseWidth = windowWidth - mazeX * 2
    pauseHeight = windowHeight - mazeY * 2
    pygame.draw.rect(screen, c.geT("OFF_WHITE"), [mazeX, mazeY, pauseWidth, pauseHeight])
    pygame.draw.rect(screen, c.geT("BLACK"), [mazeX, mazeY, pauseWidth, pauseHeight], 5)

    #Buttons

    unPause.draw(screen, outline = True)
    home.draw(screen, outline = True)
    quitButton.draw(screen, outline = True)
    mute.draw(screen, outline = False)
    sfx.draw(screen, outline = False)
    pass

def reset():
    # This function is to reset the board everytime we want to restart the game
    # Inputs: None
    # Outputs: None
    # Because of the way it's coded, these global declarations can't be avoided
    global gameOverFlag, cooldownTimer, startTime, tank1Health, tank2Health, p1Score, p2Score
    global tank1Dead, tank2Dead, gun1Cooldown, gun2Cooldown, tileList, spawnpoint
    global tank1, tank2, gun1, gun2, allSprites, bulletSprites
    gameOverFlag = False
    cooldownTimer = False
    #Removee all the sprites
    for sprite in allSprites:
        sprite.kill()
    for sprite in bulletSprites:
        sprite.kill()
    #Nautural constants
    startTime = 0
    gameOverFlag = False
    tank1Health = 100
    tank2Health = 100
    tank1Dead = False
    tank2Dead = False
    gun1Cooldown = 0
    gun2Cooldown = 0

    tileList = tileGen() # Get a new board
    spawnTank1 = [tileList[spawnpoint[0]-1].x + tileSize//2, tileList[spawnpoint[0]-1].y + tileSize//2]
    spawnTank2 = [tileList[spawnpoint[1]-1].x + tileSize//2, tileList[spawnpoint[1]-1].y + tileSize//2]
    tank1.setCoords(spawnTank1[0], spawnTank1[1])
    tank2.setCoords(spawnTank2[0], spawnTank2[1])
    tank1 = Tank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
    tank2 = Tank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName)
    gun1 = Gun(tank1, controlsTank1, p1GunName)
    gun2 = Gun(tank2, controlsTank2, p2GunName)
    allSprites = pygame.sprite.Group()
    allSprites.add(tank1, gun1, tank2, gun2)
    bulletSprites = pygame.sprite.Group()

#Game setup
#Start the game setup
pygame.init()
pygame.display.set_caption("TankTroubleDupe") # Name the window
clock = pygame.time.Clock() # Start the clock
#Keeping the mouse and its location
mouse = pygame.mouse.get_pos()


#Music setup
#Sound effects for shooting, tank dying, tank moving and tank turret rotating.
global tankShootSFX, tankDeadSFX, turretRotateSFX, tankMoveSFX
tankShootSFX = pygame.mixer.Sound("Sounds/tank_shoot.mp3")
tankDeadSFX = pygame.mixer.Sound("Sounds/tank_dead.mp3")
turretRotateSFX = pygame.mixer.Sound("Sounds/tank_turret_rotate.wav")
tankMoveSFX = pygame.mixer.Sound("Sounds/tank_moving.mp3")
lobbyMusic = pygame.mixer.Sound("Sounds/lobby_music.wav")
selectionMusic = pygame.mixer.Sound("Sounds/selection_music.mp3")
gameMusic = pygame.mixer.Sound("Sounds/game_music.mp3")
tankShootMax = 1
tankDeadMax = 0.5
turretRotateMax = 0.2
tankMoveMax = 0.05
lobbyMusicMax = 0.2
gameMusicMax = 0.2
selectionMusicMax = 1
global music, musicMax
music = lobbyMusic
musicMax = lobbyMusicMax
initialStartTime = pygame.time.get_ticks()
soundPlayed = False

#Setting up the window


# global variables
global tankSpeed, rotationalSpeed, turretSpeed, bulletSpeed
global gameOverFlag
global animationCool
global explosionGroup
resetFlag = True
tankSpeed = 0.15
rotationalSpeed = 0.5
turretSpeed = 0.8
bulletSpeed = 0.5
gameOverFlag = False
startTime = 0
cooldownTimer = False
animationCool = 12
explosionGroup = pygame.sprite.Group() #All the explosions

global arbitraryWidth, arbitraryHeight
arbitraryWidth = 50
arbitraryHeight = 50

#Colors
c = ColorDicionary() # All the colors we will use

#Constants
done = False
windowWidth = 800
windowHeight = 600
screen = pygame.display.set_mode((windowWidth,windowHeight))
tileSize = 50
weightTrue = 0.16 # The percentage change that side on a tile will have a border
rowAmount = 14
colAmount = 8
# Keeping track of score
p1Score = 0
p2Score = 0

p1NameIndent = 25
p2NameIndent = windowWidth - 25

#Defining the variables that make up the main maze screen
mazeX = 50 # We want at least a little indent or border
mazeY = 25
mazeWidth = windowWidth - mazeX*2 # We want it to span most of the screen
mazeHeight = windowHeight - mazeY*8
rowAmount = mazeHeight//tileSize # Assigning the amount of rows
colAmount = mazeWidth//tileSize # Assigning the amount of columns
barWidth = 150
barHeight = 20
bg = c.geT('GREY')
gameMode = GameMode.home
#Changing variables
p1TankName = "Plwasd1"
p2TankName = "Plarro2"

p1GunName = "Gun1"
p2GunName = "Gun2"

tileList = tileGen()

#defining buttons in pause menu
indentFromLeft = mazeX
indentFromRight = mazeY
sliderX = indentFromLeft * 2.5
sliderY = windowHeight/8
#Buttons
home = Button(c.geT("GREEN"), c.geT("WHITE"),indentFromLeft * 1.5 , indentFromRight * 1.8, tileSize, tileSize, 'Home')
quitButton = Button(c.geT("GREEN"), c.geT("WHITE"), windowWidth - indentFromLeft * 2.5, indentFromRight * 1.8, tileSize, tileSize, 'Quit')
unPause = Button(c.geT("GREEN"), c.geT("WHITE"), windowWidth/2 - 200, 0.8 * windowHeight, 400, tileSize, 'Return to Game')
mute = ButtonSlider(c.geT("BLACK"), c.geT("BLUE"), sliderX, sliderY*3, tileSize, tileSize, tileSize*8,
                    tileSize*2, 'mute', c.geT("WHITE"), c.geT("BLACK"), c.geT("RED"))
sfx = ButtonSlider(c.geT("BLACK"), c.geT("BLUE"), sliderX, sliderY*5 - tileSize, tileSize, tileSize,
                   tileSize*8, tileSize*2, 'SFX', c.geT("WHITE"), c.geT("BLACK"), c.geT("RED"))

#Selection Screen
buttonList = []
homeButton = Button(c.geT("BLACK"), c.geT("BLACK"), tileSize//4, tileSize//4,
                    tileSize, tileSize, 'back', (255, 255, 255), hoverColor=(100, 100, 255))
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
gunColors = []

# Load all the images
currentDir = os.path.dirname(__file__)
for i in range(8): # Generate all the tanks
    tankPath = os.path.join(currentDir, 'Sprites', 'tank' + str(i+1) + '.png')
    originalTankImage = pygame.image.load(tankPath).convert_alpha()
    tankImage = pygame.transform.scale(originalTankImage, (100, 65))
    hullColors.append(tankImage)
    gunPath = os.path.join(currentDir, 'Sprites', 'gun' + str(i+1) + '.png')
    originalGunImage = pygame.image.load(gunPath).convert_alpha()
    gunImage = pygame.transform.scale(originalGunImage, (75, 10))
    gunColors.append(gunImage)    


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
lArrowP1Turret.selectable(False) # Left arrow button for turret
buttonList.append(lArrowP1Turret)
textP1Turret = TextBox(tileSize*2, TurretX, font='Courier New',fontSize=26, text=turretList[0], textColor=buttonText)
textP1Turret.setBoxColor(optionText) # Textbox for turret
textP1Turret.selectable(False)
forceWidth = textP1Turret.getWidth()
buttonList.append(textP1Turret)
rArrowP1Turret = Button(buttonPrimary, buttonPrimary, tileSize*2 + forceWidth, TurretX, tileSize, tileSize, '>', buttonText, 50)
rArrowP1Turret.selectable(False) # Right arrow button for turret
buttonList.append(rArrowP1Turret)

lArrowP1Hull = Button(buttonPrimary, buttonPrimary, tileSize, HullX, tileSize, tileSize, '<', buttonText, 50)
lArrowP1Hull.selectable(False) # Left arrow button for hull
buttonList.append(lArrowP1Hull)
textP1Hull = TextBox(tileSize*2, HullX, font='Courier New',fontSize=26, text=hullList[0], textColor=buttonText)
textP1Hull.setBoxColor(optionText) # Textbox for hull
textP1Hull.selectable(False)
buttonList.append(textP1Hull)
rArrowP1Hull = Button(buttonPrimary, buttonPrimary, tileSize*2 + forceWidth, HullX, tileSize, tileSize, '>', buttonText, 50)
rArrowP1Hull.selectable(False) # Right arrow button for hull
buttonList.append(rArrowP1Hull)

lArrowP1Colour = Button(buttonPrimary, buttonPrimary, tileSize, ColourX, tileSize, tileSize, '<', buttonText, 50)
lArrowP1Colour.selectable(False)
buttonList.append(lArrowP1Colour) # Left arrow button for colour
textP1Colour = TextBox(tileSize*2, ColourX, font='Courier New',fontSize=26, text="", textColor=buttonText)
textP1Colour.setBoxColor(c.geT(ColorIndex[p1K])) # Textbox for colour
textP1Colour.selectable(False)
buttonList.append(textP1Colour)
rArrowP1Colour = Button(buttonPrimary, buttonPrimary, tileSize*2 + forceWidth, ColourX, tileSize, tileSize, '>', buttonText, 50)
rArrowP1Colour.selectable(False) # Right arrow button for colour
buttonList.append(rArrowP1Colour)

rArrowP2Turret = Button(buttonPrimary, buttonPrimary, windowWidth-tileSize*2, TurretX, tileSize, tileSize, '>', buttonText, 50)
rArrowP2Turret.selectable(False)
buttonList.append(rArrowP2Turret) # Right arrow button for turret
textP2Turret = TextBox(windowWidth - tileSize*2 - forceWidth, TurretX, font='Courier New',fontSize=26, text=turretList[0], textColor=buttonText)
textP2Turret.setBoxColor(optionText)
textP2Turret.selectable(False)
buttonList.append(textP2Turret)  # Textbox for turret
lArrowP2Turret = Button(buttonPrimary, buttonPrimary, windowWidth - tileSize*3 - forceWidth, TurretX, tileSize, tileSize, '<', buttonText, 50)
lArrowP2Turret.selectable(False)
buttonList.append(lArrowP2Turret) # Left arrow button for turret

rArrowP2Hull = Button(buttonPrimary, buttonPrimary,  windowWidth-tileSize*2, HullX, tileSize, tileSize, '>', buttonText, 50)
rArrowP2Hull.selectable(False)
buttonList.append(rArrowP2Hull) # Right arrow button for hull
textP2Hull = TextBox(windowWidth - tileSize*2 - forceWidth, HullX, font='Courier New',fontSize=26, text=hullList[0], textColor=buttonText)
textP2Hull.setBoxColor(optionText)
textP2Hull.selectable(False) # Textbox for hull
buttonList.append(textP2Hull)
lArrowP2Hull = Button(buttonPrimary, buttonPrimary, windowWidth - tileSize*3 - forceWidth, HullX, tileSize, tileSize, '<', buttonText, 50)
lArrowP2Hull.selectable(False) # Left arrow button for hull
buttonList.append(lArrowP2Hull)

rArrowP2Colour = Button(buttonPrimary, buttonPrimary,  windowWidth-tileSize*2, ColourX, tileSize, tileSize, '>', buttonText, 50)
rArrowP2Colour.selectable(False)
buttonList.append(rArrowP2Colour) # Right arrow button for colour
textP2Colour = TextBox(windowWidth - tileSize*2 - forceWidth, ColourX, font='Courier New',fontSize=26, text="", textColor=buttonText)
textP2Colour.setBoxColor(c.geT(ColorIndex[p2K]))
textP2Colour.selectable(False) # Textbox for colour
buttonList.append(textP2Colour)
lArrowP2Colour = Button(buttonPrimary, buttonPrimary, windowWidth - tileSize*3 - forceWidth, ColourX, tileSize, tileSize, '<', buttonText, 50)
lArrowP2Colour.selectable(False) # Left arrow button for colour
buttonList.append(lArrowP2Colour)

# Player names
textP1 = TextBox(tileSize*2, tileSize*0.5, font='Courier New',fontSize=26,
                 text="Player 1", textColor=buttonText)
textP1.setBoxColor(c.geT("GREEN"))
buttonList.append(textP1) # Textbox for player 1
textP2 = TextBox(windowWidth - tileSize*2 - forceWidth, tileSize*0.5,
                 font='Courier New',fontSize=26, text="Player 2", textColor=buttonText)
textP2.setBoxColor(c.geT("GREEN"))
buttonList.append(textP2)

#Play button
playButton = TextBox(windowWidth//2 - tileSize*1.75, tileSize//2,
                     font='Courier New',fontSize=26, text="Play", textColor=buttonText)
playButton.setBoxColor(c.geT("BLACK")) # Play button
playButton.selectable(True)
buttonList.append(playButton)


multiplyConstant = 8.5
offset = 35
tankValue = 3

#Other constants
rectX = tileSize*2 + forceWidth
rectY = tileSize//2
#Player 1 Statistics 
speedText = TextBox(tileSize, tileSize*multiplyConstant, font='Courier New',
                    fontSize=21, text="Speed", textColor=buttonText)
speedText.setPaddingHeight(0)
buttonList.append(speedText)
#Health bar
healthText = TextBox(tileSize, tileSize*multiplyConstant + offset, font='Courier New',
                     fontSize=21, text="Health", textColor=buttonText)
healthText.setPaddingHeight(0)
buttonList.append(healthText)
#Damage bar
damageBar = TextBox(tileSize, tileSize*multiplyConstant + offset*2, font='Courier New',
                    fontSize=21, text="Damage", textColor=buttonText)
damageBar.setPaddingHeight(0)
buttonList.append(damageBar)
#Reload bar
reloadBar = TextBox(tileSize, tileSize*multiplyConstant + offset*3, font='Courier New',
                    fontSize=21, text="Reload", textColor=buttonText)
reloadBar.setPaddingHeight(0)
buttonList.append(reloadBar)
#Player 2 Statistics
speedText2 = TextBox(windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant,
                     font='Courier New',fontSize=21, text="Speed", textColor=buttonText)
speedText2.setPaddingHeight(0)
buttonList.append(speedText2)
#Health bar
healthText2 = TextBox(windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant + offset,
                      font='Courier New',fontSize=21, text="Health", textColor=buttonText)
healthText2.setPaddingHeight(0)
buttonList.append(healthText2)
#Damage bar
damageBar2 = TextBox(windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant + offset*2,
                     font='Courier New',fontSize=21, text="Damage", textColor=buttonText)
damageBar2.setPaddingHeight(0)
buttonList.append(damageBar2)
#Reload bar
reloadBar2 = TextBox(windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant + offset*3,
                     font='Courier New',fontSize=21, text="Reload", textColor=buttonText)
reloadBar2.setPaddingHeight(0)
buttonList.append(reloadBar2)

def checkButtons(mouse):
    #This function checks all the buttons of the mouse in the selection screen
    # Inputs: Mouse: The current location of the mouse
    # Outputs: None
    global p1I, p2I, p1J, p2J, p1K, p2K, gameMode
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
    global music, musicMax # Handling music
    if playButton.buttonClick(mouse):
        #Switch the the play screen
        print("Play")
        gameMode=GameMode.play
        music.stop()
        music = gameMusic
        musicMax = gameMusicMax
        music.play(-1)
    if homeButton.buttonClick(mouse):
        #Switch back to the home screen
        print("Back")
        gameMode = GameMode.home
        music.stop()
        # global music, musicMax
        music = lobbyMusic
        musicMax = lobbyMusicMax
        music.play(-1)

def checkHomeButtons(mouse):
    # This function checks all the buttons of the mouse in the home screen
    # Inputs: Mouse: The current location of the mouse
    # Outputs: None
    global gameMode
    if playButtonHome.buttonClick(mouse):
        #Switch to the selection screen
        gameMode = GameMode.selection
        global music, musicMax
        print("Selection")
        music.stop()
        music = selectionMusic
        musicMax = selectionMusicMax
        music.play(-1)
    if settingsButton.buttonClick(mouse):
        print("Unimplmented")
        # gameMode = GameMode.settings
    if quitButtonHome.buttonClick(mouse):
        global done
        done = True

#Menu screen
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

# Controls for the first tank
controlsTank1 = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'rotate_left': pygame.K_h,
    'rotate_right': pygame.K_k,
    'fire': pygame.K_j
}

# Controls for the second tank
controlsTank2 = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'rotate_left': pygame.K_COMMA,
    'rotate_right': pygame.K_PERIOD,
    'fire': pygame.K_SLASH
}

spawnTank1 = [tileList[spawnpoint[0]-1].x + tileSize//2, tileList[spawnpoint[0]-1].y + tileSize//2]
spawnTank2 = [tileList[spawnpoint[1]-1].x + tileSize//2, tileList[spawnpoint[1]-1].y + tileSize//2]

global tank1Health, tank2Health
tank1Health = 100
tank2Health = 100

global gun1Cooldown, gun2Cooldown
gun1Cooldown = 0
gun2Cooldown = 0

global tank1Dead, tank2Dead
tank1Dead = False
tank2Dead = False


# Create two tank instances with different controls
tank1 = Tank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
tank2 = Tank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName)
gun1 = Gun(tank1, controlsTank1, p1GunName)
gun2 = Gun(tank2, controlsTank2, p2GunName)

allSprites = pygame.sprite.Group()
allSprites.add(tank1, gun1, tank2, gun2)
bulletSprites = pygame.sprite.Group()

#Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                #Not left click
                break
            mouse = pygame.mouse.get_pos()
            if gameMode == GameMode.pause:
                #We are paused
                if (unPause.getCorners()[0] <= mouse[0] <= unPause.getCorners()[2] and
                    unPause.getCorners()[1] <= mouse[1] <= unPause.getCorners()[3]): #If we click the button
                    gameMode = GameMode.play # Return to game if button was clicked
                if (home.getCorners()[0] <= mouse[0] <= home.getCorners()[2] and
                    home.getCorners()[1] <= mouse[1] <= home.getCorners()[3]):
                    gameMode = GameMode.home
                    music.stop()
                    music = lobbyMusic
                    musicMax = lobbyMusicMax
                    music.play(-1)
                if (quitButton.getCorners()[0] <= mouse[0] <= quitButton.getCorners()[2]and
                    quitButton.getCorners()[1] <= mouse[1] <= quitButton.getCorners()[3]):
                    print("Quitting the game")
                    done = True # We quit the appplication
                if (mute.getCorners()[0] <= mouse[0] <= mute.getCorners()[2] and
                    mute.getCorners()[1] <= mouse[1] <= mute.getCorners()[3]):
                    mute.buttonClick()
                if (sfx.getCorners()[0] <= mouse[0] <= sfx.getCorners()[2] and
                    sfx.getCorners()[1] <= mouse[1] <= sfx.getCorners()[3]):
                    sfx.buttonClick()
            elif gameMode == GameMode.selection:
                textP1Turret.setText(turretList[p1I])
                textP2Turret.setText(turretList[p2I])
                textP1Hull.setText(hullList[p1J])
                textP2Hull.setText(hullList[p2J])
                checkButtons(pygame.mouse.get_pos())
            elif gameMode == GameMode.home:
                checkHomeButtons(pygame.mouse.get_pos())
        elif event.type == pygame.KEYDOWN: # Any key pressed
            if event.key == pygame.K_ESCAPE: # Escape hotkey to quit the window
                done = True
            if event.key == pygame.K_w:
                pass
            if event.key == pygame.K_e:
                pass
            if event.key == pygame.K_s:
                pass
            if event.key == pygame.K_d:
                pass
            if event.key == pygame.K_i:
                print("The current mouse position is: ", mouse)
            if event.key == pygame.K_o:
                pass
            if event.key == pygame.K_p:
                #Pause
                if gameMode == GameMode.pause:
                    gameMode = GameMode.play # Return to game if button was clicked
                elif gameMode == GameMode.play:
                    gameMode = GameMode.pause # Pause the game
            if event.key == pygame.K_l:
                lobbyMusicMax -= 0.01
                print("The current volume is: ", lobbyMusicMax)
            if event.key == pygame.K_k:
                lobbyMusicMax += 0.01
                print("The current volume is: ", lobbyMusicMax)
            if event.key == pygame.K_f:
                print("The current FPS is: ", clock.get_fps())
            if event.key == pygame.K_n:
                if gameMode == GameMode.play:
                    reset()
            if event.key == pygame.K_0:
                if gameMode == GameMode.play:
                    reset()
            if event.key == pygame.K_m:
                mute.mute()

    #Start the lobby music
    if not soundPlayed and pygame.time.get_ticks() - initialStartTime > 2000: # Delay by 1 second
        music.play(-1)
        soundPlayed = True

    music.set_volume(mute.getValue() * musicMax)
    tankShootSFX.set_volume(sfx.getValue() * tankShootMax)
    tankDeadSFX.set_volume(sfx.getValue() * tankDeadMax)
    turretRotateSFX.set_volume(sfx.getValue() * turretRotateMax)
    tankMoveSFX.set_volume(sfx.getValue() * tankMoveMax)
    mouse = pygame.mouse.get_pos() #Update the position

    screen.fill(bg) # This is the first line when drawing a new frame

    if gameMode == GameMode.play:
        playGame()
    elif gameMode == GameMode.pause:
        pauseScreen()
        if pygame.mouse.get_pressed()[0]:
            mute.updateSlider(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            sfx.updateSlider(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    elif gameMode == GameMode.selection:
        pygame.draw.rect(screen,(0,0,0), (tileSize, tileSize*multiplyConstant, rectX, rectY), 1)
        for button in buttonList:
            button.update_display(pygame.mouse.get_pos())
            button.draw(screen, outline = False)
        
        barBorder = 3
        #Blocks
        speedBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiplyConstant, rectX, rectY),barBorder)
        speedBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiplyConstant,
                                                             (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        speedOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiplyConstant,
                                                          rectX - speedText.getWidth(), rectY), barBorder)
        speedBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                                               tileSize*multiplyConstant, (rectX - speedText.getWidth())/3,rectY), barBorder)

        healthBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiplyConstant + offset, rectX, rectY),barBorder)
        healthBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiplyConstant + offset,
                                                              (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        healthOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiplyConstant + offset,
                                                           rectX - speedText.getWidth(), rectY), barBorder)
        healthBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                                                tileSize*multiplyConstant + offset, (rectX - speedText.getWidth())/3,rectY),
                                                                barBorder)

        damageBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiplyConstant + offset*2, rectX, rectY),barBorder)
        damageBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiplyConstant + offset*2,
                                                              (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        damageOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiplyConstant + offset*2,
                                                           rectX - speedText.getWidth(), rectY), barBorder)
        damageBlockOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                                                tileSize*multiplyConstant + offset*2, (rectX - speedText.getWidth())/3,rectY),
                                                                barBorder)

        reloadBarOutline = pygame.draw.rect(screen, c.geT("BLACK"), (tileSize, tileSize*multiplyConstant + offset*3, rectX, rectY),barBorder)
        reloadBar = pygame.draw.rect(screen, c.geT("GREEN"), (tileSize + speedText.getWidth(), tileSize*multiplyConstant + offset*3,
                                                              (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        reloadOutline = pygame.draw.rect(screen, (0,0,0), (tileSize + speedText.getWidth(), tileSize*multiplyConstant + offset*3,
                                                           rectX - speedText.getWidth(), rectY), barBorder)
        reloadBlockOutline = pygame.draw.rect(screen, (0,0,0),
                                              (tileSize + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                               tileSize*multiplyConstant + offset*3, (rectX - speedText.getWidth())/3,rectY), barBorder)

        speedBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant,
                                                                     rectX, rectY),barBorder)
        speedBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                              tileSize*multiplyConstant, (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        speedOutline2 = pygame.draw.rect(screen, (0,0,0), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                           tileSize*multiplyConstant, rectX - speedText.getWidth(), rectY), barBorder)
        speedBlockOutline2 = pygame.draw.rect(screen, (0,0,0), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth() +
                                                                (rectX - speedText.getWidth())/3, tileSize*multiplyConstant,
                                                                (rectX - speedText.getWidth())/3,rectY), barBorder)

        healthBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (windowWidth - tileSize*3 - forceWidth,
                                                                      tileSize*multiplyConstant + offset, rectX, rectY),barBorder)
        healthBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                               tileSize*multiplyConstant + offset,
                                                               (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        healthOutline2 = pygame.draw.rect(screen, (0,0,0), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                            tileSize*multiplyConstant + offset, rectX - speedText.getWidth(), rectY), barBorder)
        healthBlockOutline2 = pygame.draw.rect(screen, (0,0,0),
                                               (windowWidth - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                                tileSize*multiplyConstant + offset, (rectX - speedText.getWidth())/3,rectY), barBorder)

        damageBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant + offset*2,
                                                                      rectX, rectY),barBorder)
        damageBar2 = pygame.draw.rect(screen, c.geT("GREEN"), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                               tileSize*multiplyConstant + offset*2, (rectX - speedText.getWidth()) * tankValue/3,
                                                               rectY))
        #Outlines
        damageOutline2 = pygame.draw.rect(screen, (0,0,0), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                            tileSize*multiplyConstant + offset*2, rectX - speedText.getWidth(), rectY), barBorder)
        damageBlockOutline2 = pygame.draw.rect(screen, (0,0,0),
                                               (windowWidth - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                                tileSize*multiplyConstant + offset*2, (rectX - speedText.getWidth())/3,rectY), barBorder)

        reloadBarOutline2 = pygame.draw.rect(screen, c.geT("BLACK"), (windowWidth - tileSize*3 - forceWidth, tileSize*multiplyConstant + offset*3,
                                                                      rectX, rectY),barBorder)
        reloadBar2 = pygame.draw.rect(screen, c.geT("GREEN"),
                                      (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(), tileSize*multiplyConstant + offset*3,
                                       (rectX - speedText.getWidth()) * tankValue/3, rectY))
        #Outlines
        reloadOutline2 = pygame.draw.rect(screen, (0,0,0), (windowWidth - tileSize*3 - forceWidth + speedText.getWidth(),
                                                            tileSize*multiplyConstant + offset*3, rectX - speedText.getWidth(), rectY), barBorder)
        reloadBlockOutline2 = pygame.draw.rect(screen, (0,0,0),
                                               (windowWidth - tileSize*3 - forceWidth + speedText.getWidth() + (rectX - speedText.getWidth())/3,
                                                tileSize*multiplyConstant + offset*3, (rectX - speedText.getWidth())/3,rectY), barBorder)

        #Draw the tank image
        screen.blit(hullColors[p1K], (tileSize*2 + forceWidth//2-50, tileSize*2))
        screen.blit(hullColors[p2K], (windowWidth - tileSize*2 - forceWidth//2-50, tileSize*2))
        screen.blit(gunColors[p1K], (tileSize*2 + forceWidth//2, tileSize*2.5))
        screen.blit(gunColors[p2K], (windowWidth - tileSize*2 - forceWidth//2, tileSize*2.5))

    elif gameMode == GameMode.home:
        # Draw the tank image
        screen.blit(originalTankImage, (230, 65))  # Adjust the coordinates as needed

        # Draw the title text
        screen.blit(titleText, (windowWidth // 2 - titleText.get_width() // 2, 50))  # Centered horizontally, 50 pixels from top

        # Handle hover effect and draw buttons
        mouse_pos = pygame.mouse.get_pos()
        for button in homeButtonList:
            button.update_display(mouse_pos)
            button.draw(screen, outline=True)

    else:
        screen.fill(c.geT("WHITE"))
    clock.tick(240) # Set the FPS

    pygame.display.flip()# Update the screen

pygame.quit()