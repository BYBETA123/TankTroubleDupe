import pygame
import random
import math
import time
import os
from ColorDictionary import ColorDicionary
from threading import Timer
from enum import Enum
from UIUtility import Button, ButtonSlider, TextBox
from music import Music
import copy
#Classes

# Tank sprite class
class Tank(pygame.sprite.Sprite):
    topSpeed = 0
    topRotation = 0
    spriteImage = None
    def __init__(self, x, y, controls, name = "Default"):

        super().__init__()
        try:
            # Load the tank image
            currentDir = os.path.dirname(__file__)
            tankPath = os.path.join(currentDir, 'Sprites', 'tank1.png')
            self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

            # Scale the tank image to a smaller size
            self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        except pygame.error as e: # In case there is an issue opening the file
            print(f"Failed to load image: {e}")
            pygame.quit()
            exit()

        # Setting variables
        self.angle = 0
        self.center = (x, y)
        self.controls = controls
        self.health = 3000
        self.maxHealth = 3000
        self.name = name
        self.rotationSpeed = 0
        self.rotationalSpeed = 0.5
        self.speed = 0
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(x, y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        self.updateCorners() #Set the corners
        self.soundPlaying = False
        self.speedStatistic = 1
        self.healthStatistic = 1
        self.maxSpeed = 0.15
        self.tankName = "Default"
        self.drawable = False
        self.topSpeed = self.maxSpeed
        self.topRotation = self.rotationalSpeed

    def updateCorners(self):
        # This function will update the corners of the tank based on the new position
        # This is to make sure that the coliisions detection is accurate
        # Inputs: None
        # Outputs: None
        cx, cy = self.rect.center
        w, h = self.width / 2, self.height / 2
        rad = math.radians(self.angle)
        rad = math.pi * 2 - rad
        cosA = math.cos(rad)
        sinA = math.sin(rad)
        # assign the new corners
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

    



        # if pygame.sprite.collide_rect(tank1, tank2):

        if satCollision(tank1, tank2): #If the tanks are colliding
            if self.name == p1TankName:
                #If there is a collision here, move the other tank
                    #This player is being pushed
                    tank2.setCoords(tank2.x + dx, tank2.y - dy)
                    tempX = self.x - dx * 1.5
                    tempY = self.y + dy * 1.5
            elif self.name == p2TankName:
                #If there is a collision here, move the other tank
                    #This player is being pushed
                    tank1.setCoords(tank1.x + dx, tank1.y - dy)
                    tempX = self.x - dx * 1.5
                    tempY = self.y + dy * 1.5
            else:
                print("Error: Invalid tank name")

        #Check for collision with walls
        #We are going to calculate the row and column
        row = math.ceil((self.getCenter()[1] - mazeY)/tileSize)
        col = math.ceil((self.getCenter()[0] - mazeX)/tileSize)
        #Find the file at the exact index
        index = (row-1)*colAmount + col

        #Check if the tank is colliding with the walls
        if index not in range(1, rowAmount*colAmount+1): #If we are outside of the maze
            return self.x, self.y
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
        # This function updates the tank's position and rotation based on the controls detected
        # from the keyboard sound effects will be played as well as the sound effects
        # Inputs: None
        # Outputs: None

        keys = pygame.key.get_pressed()
        #Movement keys
        if keys[self.controls['up']]:
            self.speed = self.maxSpeed
        elif keys[self.controls['down']]:
            self.speed = -self.maxSpeed
        else:
            self.speed = 0
        if keys[self.controls['left']]:
            self.rotationSpeed = self.rotationalSpeed
        elif keys[self.controls['right']]:
            self.rotationSpeed = -self.rotationalSpeed
        else:
            self.rotationSpeed = 0

        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if self.speed != 0 or self.rotationSpeed != 0:
            if not self.soundPlaying:
                soundDictionary["tankMove"].play(-1)  # Play sound indefinitely
                self.soundPlaying = True
        else:
            if self.soundPlaying:
                soundDictionary["tankMove"].stop()  # Play sound indefinitely
                self.soundPlaying = False

        self.angle += self.rotationSpeed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.originalTankImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        angleRad = math.radians(self.angle)
        dx = math.cos(angleRad) * self.speed
        dy = math.sin(angleRad) * self.speed
        self.x, self.y = self.fixMovement(dx,dy) # Adjust the movement

    def damage(self, damage):
        # This function will adjust the damage that the tank has taken
        # Inputs: damage: The amount of damage that the tank has taken
        # Outputs: None
        self.health -= damage
        updateTankHealth() # Manage the healthbar outside of the code

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
        self.x = x # Update the x and y coordinate as well
        self.y = y

    def isDrawable(self):
        return self.drawable

    def getHealth(self):
        return self.health
    
    def setHealth(self, health):
        self.health = health

    def setMaxHealth(self, health):
        self.maxHealth = health
        self.health = health

    def getMaxHealth(self):
        return self.maxHealth

    def getHealthStatistic(self):
        return self.healthStatistic
    
    def setHealthStatistic(self, value):
        self.healthStatistic = value

    def getSpeedStatistic(self):
        return self.speedStatistic
    
    def setSpeedStatistic(self, value):
        self.speedStatistic = value

    def setTankName(self, tankName):
        self.tankName = tankName

    def setRotationalSpeed(self, speed):
        self.rotationalSpeed = speed

    def setTopRotationalSpeed(self, speed):
        self.topRotation = speed
        self.rotationalSpeed = speed

    def resetRotationalSpeed(self):
        self.rotationalSpeed = self.topRotation

    def getRotationalSpeed(self):
        return self.rotationalSpeed

    def getTopRotationalSpeed(self):
        return self.topRotation

    def setSpeed(self, speed):
        self.maxSpeed = speed

    def setTopSpeed(self, speed):
        self.topSpeed = speed
        self.maxSpeed = speed

    def resetMaxSpeed(self):
        self.maxSpeed = self.topSpeed

    def getSpeed(self):
        return self.topSpeed

    def getTankName(self):
        return self.tankName
    
    def setData(self, data):
        # This function will set up the tanks that are being used
        # Inputs: Data, all the data stored within the packages defined as global variables
        # Outputs: None
        self.controls = data[2]
        self.name = data[3]
        self.rect = self.tankImage.get_rect(center=(data[0], data[1]))
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def draw(self, screen): # A manual entry of the draw screen so that we can update it with anything else we may need to draw
        screen.blit(self.image, self.rect)

    def getName(self):
        return self.name

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'tank' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getHealthPercentage(self):
        return min((self.health/self.maxHealth),1)

    def getSprite(self, flipped = False):
        return pygame.transform.flip(self.spriteImage, flipped, False)
    
    def getGunCenter(self):
        return (self.x, self.y)

    def rotate_point(self, pivot, distance, initial_angle, rotation_angle):
        """
        Rotate a point around a given pivot point by a certain angle.
        
        :param pivot: Tuple of (x, y) for the pivot point
        :param distance: Distance of the point from the pivot
        :param initial_angle: Initial angle of the point from the pivot in degrees
        :param rotation_angle: Rotation angle in degrees
        :return: Tuple of (x', y') for the rotated point
        """
        initial_angle_rad = math.radians(initial_angle)  # Convert initial angle to radians
        rotation_angle_rad = math.radians(rotation_angle)  # Convert rotation angle to radians
        # Calculate the new angle after rotation
        new_angle_rad = initial_angle_rad + rotation_angle_rad
        new_angle_rad = 2 * math.pi - new_angle_rad

        # Calculate new coordinates
        x_p, y_p = pivot
        x_prime = x_p + distance * math.cos(new_angle_rad)
        y_prime = y_p + distance * math.sin(new_angle_rad)
        
        return x_prime, y_prime

    def treads(self, num):
        # This function will draw the treads of the tank
        # Inputs: None
        # Outputs: None
        rect_surface = pygame.image.load("Sprites/ZTreads.png").convert_alpha()
        rect_surface = pygame.transform.scale(rect_surface, (self.originalTankImage.get_size()))


        rotated_surface = pygame.transform.rotate(rect_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.x, self.y))

        if num:
            treadsp1.append((rotated_surface, rotated_rect.topleft))
            if len(treadsp1) > 15:
                treadsp1.pop(0)
        if not num:
            treadsp2.append((rotated_surface, rotated_rect.topleft))
            if len(treadsp2) > 15:
                treadsp2.pop(0)


class Gun(pygame.sprite.Sprite):

    topTurretSpeed = 0
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
        self.angle = 0
        self.rotationSpeed = 0
        self.tank = tank
        self.gunLength = -24
        self.gunRotationDirection = 0
        self.tipOffSet = 30
        self.controls = controls
        self.name = name
        self.originalGunLength = self.gunLength
        self.gunBackDuration = 200
        self.canShoot = True
        self.shootCooldown = 0
        self.soundPlaying=False
        self.lastUpdateTime = pygame.time.get_ticks()
        self.cooldownDuration = 500
        self.damage = 700
        self.damageStatistic = 1
        self.reloadStatistic = 1
        self.turretSpeed = 0.8
        self.drawable = False
        self.topTurretSpeed = self.turretSpeed
        self.gunH = 7
        self.imgScaler = 1.5
        angleRad = math.radians(self.angle)
        gunEndX, gunEndY = self.tank.getGunCenter()
        self.rect = self.image.get_rect(center=(gunEndX + self.gunH * math.cos(angleRad), gunEndY - self.gunH * math.sin(angleRad)))

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
        self.rotationSpeed = 0
        
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed += self.turretSpeed
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed += -self.turretSpeed
        if  keys[self.controls['left']]:
            self.rotationSpeed += self.tank.getRotationalSpeed()
        elif keys[self.controls['right']]:
            self.rotationSpeed += -self.tank.getRotationalSpeed()                
    
        self.angle += self.rotationSpeed
        self.angle %= 360
        
        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        # <SOUND REWORK>
        if keys[self.controls['rotate_left']] or keys[self.controls['rotate_right']]:
            if self.rotationSpeed != 0:
                if not self.soundPlaying:
                    soundDictionary["turretRotate"].play(loops = -1, fade_ms = 100)  # Play sound indefinitely
                    self.soundPlaying = True
            else:
                if self.soundPlaying:
                    soundDictionary["turretRotate"].stop()
                    self.soundPlaying = False
        else:
            if self.soundPlaying:
                soundDictionary["turretRotate"].stop()
                self.soundPlaying = False

        #Reload cooldown of bullet and determines the angle to fire the bullet,
        #which is relative to the posistion of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            self.fire()

        angleRad = math.radians(self.angle)
        gunEndX, gunEndY = self.tank.getGunCenter()

        rotatedGunImage = pygame.transform.rotate(self.originalGunImage, self.angle)
        self.image = rotatedGunImage
        self.rect = self.image.get_rect(center=(gunEndX + self.gunH * math.cos(angleRad), gunEndY - self.gunH * math.sin(angleRad)))
        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.shootCooldown = 0
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

    def fire(self):
        # This function completely handles the bullet generation when firing a bullet
        # Inputs: None
        # Outputs: None

        # Calculating where the bullet should spawn
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setDamage(self.damage)
        bullet.setName(self.getTank().getName())
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def setCooldown(self, value = 0):
        #This function sets the cooldown of the gun
        #Inputs: value: The value of the cooldown
        #Outputs: None
        self.cooldownDuration = value

    def getCooldown(self):
        return self.shootCooldown

    def getCooldownMax(self):
        return self.cooldownDuration

    def setDamageStatistic(self, value):
        self.damageStatistic = value

    def setDamage(self, damage):
        self.damage = damage

    def setReloadStatistic(self, value):
        self.reloadStatistic = value

    def getDamageStatistic(self):
        return self.damageStatistic

    def getReloadStatistic(self):
        return self.reloadStatistic
    
    def getGunName(self):
        return self.name

    def setGunBackDuration(self, duration):
        self.gunBackDuration = duration

    def getReloadStatistic(self):
        return self.reloadStatistic
    
    def getDamageStatistic(self):
        return self.damageStatistic
    
    def setTurretSpeed(self, speed):
        self.turretSpeed = speed

    def resetTurrtSpeed(self):
        self.turretSpeed = self.topTurretSpeed

    def getTurretSpeed(self):
        return self.topTurretSpeed

    def getTank(self):
        return self.tank

    def isDrawable(self):
        return self.drawable

    def setData(self, tank, controls, name):
        # This function will set up the gun that is being used
        # Inputs: tank: The tank object that the gun is attached to
        #         controls: The controls that are being used to control the gun
        #         name: The name of the gun
        # Outputs: None
        self.tank = tank
        self.controls = controls
        self.name = name
        self.rect = self.gunImage.get_rect(center=(tank.rect.center))
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'gun' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getReloadPercentage(self):
        return min((self.shootCooldown/self.cooldownDuration),1)

    def getSprite(self, flipped = False):
        return pygame.transform.flip(self.spriteImage, flipped, False)

    def setTipOffset(self, tip):
        self.tipOffSet = tip

    def setGunCenter(self, x, y):
        self.gunH = (x**2 + y**2)**0.5 # hypotenuse
    
    def getGunCenter(self):
        return self.rect.center

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Empty"].play()

class Bullet(pygame.sprite.Sprite):

    originalCollision = True
    name = "Default"
    initialX = 0
    initialY = 0
    selfCollision = False
    originalBounce = 1
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
        self.speed = 0.5
        self.drawable = False
        self.trail = False
        angleRad = math.radians(self.angle)

        dx = (gunLength + tipOffSet) * math.cos(angleRad)
        dy = -(gunLength + tipOffSet) * math.sin(angleRad)

        self.rect = self.bulletImage.get_rect(center=(x + dx, y + dy))
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.trailX =  self.rect.centerx
        self.trailY = self.rect.centery
        self.bounce = 1
        self.originalBounce = self.bounce
        self.corners = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y),
                        (self.rect.x + self.rect.width, self.rect.y + self.rect.height), (self.rect.x, self.rect.y + self.rect.height)]
        self.damage = 700
        self.pleaseDraw = False
        self.initialX = x
        self.initialY = y
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

        if self.name == tank1.getName() and tank2Collision:
                soundDictionary["tankDeath"].play()
                tank2.damage(self.damage)
                self.kill()
        if self.name == tank2.getName() and tank1Collision:
                soundDictionary["tankDeath"].play()
                tank1.damage(self.damage)
                self.kill()

        if self.selfCollision:
            if tank1Collision:
                soundDictionary["tankDeath"].play()
                tank1.damage(self.damage)
                self.kill()
            if tank2Collision:
                soundDictionary["tankDeath"].play()
                tank2.damage(self.damage)
                self.kill()

        # Checking for self damage
        if self.bounce != self.originalBounce:
            self.selfCollision = True

        tile = tileList[index-1]
        wallCollision = False
        if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y: #If the top border is present
            wallCollision = True
            self.angle = 180 - self.angle
        if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + tileSize: #If the right border is present
            wallCollision = True
            self.angle = 360 - self.angle
        if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + tileSize: #If the bottom border is present
            wallCollision = True
            self.angle = 180 - self.angle
        if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x: #If the left border is present
            wallCollision = True
            self.angle = 360 - self.angle
        if wallCollision:
            self.bounce -= 1
            self.speed *= -1
            if self.bounce == 0:
                self.kill() # delete the bullet
        self.updateCorners()
        # Store the updated values
        self.rect.x = int(tempX)
        self.rect.y = int(tempY)
        self.x = tempX
        self.y = tempY
        self.pleaseDraw = True

    def setBulletSpeed(self, speed):
        self.speed = speed

    def isDrawable(self):
        return self.drawable

    def getCenter(self):
        return (self.x, self.y)

    def updateCorners(self):
        # This function will update the corners of the tank based on the new position
        # Inputs: None
        # Outputs: None
        self.corners = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y),
                        (self.rect.x + self.rect.width, self.rect.y + self.rect.height), (self.rect.x, self.rect.y + self.rect.height)]

    def setDamage(self, damage):
        self.damage = damage

    def customDraw(self, screen):
        # This function will draw the bullet on the screen and any additional features that may be needed
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.pleaseDraw and self.trail:
            pygame.draw.line(screen, c.geT("NEON_PURPLE"), (self.trailX, self.trailY), (self.x, self.y), 3)
            self.pleaseDraw = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def setName(self, name):
        self.name = name

    def setOriginalCollision(self, value):
        self.originalCollision = value

    def setBounce(self, bounceValue):
        self.bounce = bounceValue
        self.originalBounce = bounceValue

class SidewinderBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.setBounce(5)
        self.setDamage(350)

class JudgeBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet, initialDamage=76, minDamage=50):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.damage = initialDamage
        self.setBounce(2)

class SilencerBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.speed = 0.4
        self.damage = 1400
    
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
        if abs(self.x- self.trailX) >= 1 and abs(tempY-self.trailY) >= 1:
            self.pleaseDraw = True

class WatcherBullet(Bullet):

    trailColor = (255, 0, 0)

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.speed = 0.2
        self.damage = 3300
        
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

        if self.name == tank1.getName() and tank2Collision:
                soundDictionary["tankDeath"].play()
                tank2.damage(self.damage)
                self.kill()
        if self.name == tank2.getName() and tank1Collision:
                soundDictionary["tankDeath"].play()
                tank1.damage(self.damage)
                self.kill()

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

    def customDraw(self, screen):
        # This function will draw the bullet on the screen and any additional features that may be needed
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.trail:
            pygame.draw.circle(screen, self.trailColor, (self.x, self.y), 1)
            self.pleaseDraw = False

    def setTrailColor(self, color):
        self.trailColor = color

    def draw(self,_):
        return # We don't want to draw the bullet

class ChamberBullet(Bullet):

    gunLength = -24
    tipOffSet = 30
    splash = True

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.speed = 0.5
        self.damage = 1000
        self.drawable = True
        self.gunLength = gunLength
        self.tipOffSet = tipOffSet

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
            self.explode()
            return
        
        #If we hit a tank
        tank1Collision = satCollision(self, tank1)
        tank2Collision = satCollision(self, tank2)

        if self.name == tank1.getName() and tank2Collision:
                soundDictionary["tankDeath"].play()
                tank2.damage(self.damage)
                self.explode()
        if self.name == tank2.getName() and tank1Collision:
                soundDictionary["tankDeath"].play()
                tank1.damage(self.damage)
                self.explode()



        tile = tileList[index-1]
        wallCollision = False
        if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y: #If the top border is present
            wallCollision = True
            self.angle = 180 - self.angle
        if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + tileSize: #If the right border is present
            wallCollision = True
            self.angle = 360 - self.angle
        if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + tileSize: #If the bottom border is present
            wallCollision = True
            self.angle = 180 - self.angle
        if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x: #If the left border is present
            wallCollision = True
            self.angle = 360 - self.angle
        if wallCollision:
            if self.name == tank1.getName() and tank1Collision:
                soundDictionary["tankDeath"].play()
                tank1.damage(self.damage)
                self.explode()
                return
            if self.name == tank2.getName() and tank2Collision:
                soundDictionary["tankDeath"].play()
                tank2.damage(self.damage)
                self.explode()
                return

            self.bounce -= 1
            self.speed *= -1
            if self.bounce == 0:
                self.explode() # delete the bullet
                return
        self.updateCorners()

        self.rect.x = int(tempX)
        self.rect.y = int(tempY)
        self.x = tempX
        self.y = tempY
        if abs(self.x- self.trailX) >= 1 and abs(tempY-self.trailY) >= 1:
            self.pleaseDraw = True

    def sizeImage(self, scale):
        # This function will resize the image
        # Inputs: Scale: The scale that the image will be resized to
        # Outputs: None
        originalCenter = self.rect.center
        originalCenter = copy.copy(originalCenter)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height()* scale))
        self.rect = self.image.get_rect()
        self.rect.center = originalCenter

    def setSplash(self, value):
        self.splash = value

    def explode(self):
        # This function will handle the explosion of the bullet and the respective splash damage
        # Inputs: None
        # Outputs: None
        if self.splash:
            #Middle radius
            splash1 = ChamberBullet(self.x, self.y, 0, 0, 0)
            splash1.sizeImage(10)
            splash1.updateCorners()
            splash1.setSplash(False)
            splash1.setDamage(self.damage)
            splash1.setName(self.name)
            splash1.setBulletSpeed(0)
            splash1.update()
            splash1.kill()
            # Outer radius
            splash2 = ChamberBullet(self.x, self.y, 0, 0, 0)
            splash2.sizeImage(5)
            splash2.updateCorners()
            splash2.setSplash(False)
            splash2.setDamage(self.damage)
            splash2.setName(self.name)
            splash2.setBulletSpeed(0)
            splash2.update()
            splash2.kill()

        self.kill()

    def draw(self,screen):
        # This function will only draw if the bullet is a splash and not a radius
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.splash:
            screen.blit(self.image, self.rect)

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
            self.images.append(self.getImage(SpriteSheetImage, i, 128, 128, 0.5))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lastUpdate = pygame.time.get_ticks()
        global animationCool
        self.animationCooldown = animationCool

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

class GameMode(Enum):
    #This class is responsible for the game mode
    # This class doesn't have other function as they are not needed
    pause = 0
    play = 1
    home = 2
    settings = 3
    selection = 4

#Turrets

class Chamber(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(1500) # 200 ms
        self.setDamage(270) # Should be 900 but because of the 3 step effect it will be split into 3x 300
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setGunBackDuration(500)
        self.setGunCenter(0, -4)

    def fire(self):
        # This function is responsible for all the firing mechanics of the gun
        # The Bullet is custom here as it is tailored for the Chamber
        # Inputs: None
        # Outputs: None

        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = ChamberBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        bullet.setDamage(self.damage)
        bullet.setBulletSpeed(5)
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        #If either tank shoots, play this sound effect.
        self.playSFX()

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None        
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Chamber' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Chamber"].play()

class DefaultGun(Gun):
    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(400) # 500 ms
        self.setDamage(10000) # 10000

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None        
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'gun' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

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
        self.rotationSpeed = 0
        if  keys[self.controls['left']]:
            self.rotationSpeed += self.tank.getRotationalSpeed()
        elif keys[self.controls['right']]:
            self.rotationSpeed += -self.tank.getRotationalSpeed()                
    
        self.angle += self.rotationSpeed
        self.angle %= 360
        
        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        # <SOUND REWORK>
        if keys[self.controls['rotate_left']] or keys[self.controls['rotate_right']]:
            if self.rotationSpeed != 0:
                if not self.soundPlaying:
                    soundDictionary["turretRotate"].play(loops = -1, fade_ms = 100)  # Play sound indefinitely
                    self.soundPlaying = True
            else:
                if self.soundPlaying:
                    soundDictionary["turretRotate"].stop()
                    self.soundPlaying = False
        else:
            if self.soundPlaying:
                soundDictionary["turretRotate"].stop()
                self.soundPlaying = False

        #Reload cooldown of bullet and determines the angle to fire the bullet,
        #which is relative to the posistion of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            self.fire()

        angleRad = math.radians(self.angle)
        gunEndX, gunEndY = self.tank.getGunCenter()

        rotatedGunImage = pygame.transform.rotate(self.originalGunImage, self.angle)
        self.image = rotatedGunImage
        self.rect = self.image.get_rect(center=(gunEndX + self.gunH * math.cos(angleRad), gunEndY - self.gunH * math.sin(angleRad)))
        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.shootCooldown = 0
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

    def fire(self):
        # This function completely handles the bullet generation when firing a bullet
        # Inputs: None
        # Outputs: None

        # Calculating where the bullet should spawn
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setDamage(self.damage)
        bullet.setBounce(5)
        bullet.setName(self.getTank().getName())
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

class Judge(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(800)  # 800 ms
        self.setDamage(76)
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setGunBackDuration(300)
        self.setTipOffset(28)
        self.bulletInterval = 15
        self.scatterRange = 13
        self.maxUses = 3
        self.currentUses = 0
        self.reloadTime = 2  # 2 seconds
        self.setGunCenter(0, -3)

    def fire(self):
        if self.currentUses < self.maxUses:
            self.canShoot = False
            self.shootCooldown = self.cooldownDuration

            for i in range(1, 11):
                Timer(self.bulletInterval * i / 1000.0, self.fireBullet).start() # Threaded???
            self.playSFX()
            self.currentUses += 1
            if self.currentUses >= self.maxUses:
                self.currentUses = 0
                #This needs to be fixed a little bit
                # self.canShoot = False
                # Timer(self.reloadTime, self.reload).start()

    def fireBullet(self):
        scatterAngle = random.uniform(-self.scatterRange, self.scatterRange)
        bulletAngle = self.angle + scatterAngle
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = JudgeBullet(bulletX, bulletY, bulletAngle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        bullet.setDamage(self.damage)
        bullet.setBulletSpeed(0.5)
        bulletSprites.add(bullet)
        Timer(2, lambda: bullet.kill()).start() # Dies after a while

    def reload(self):
        self.currentUses = 0
        self.canShoot = True

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None        
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Judge' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Judge"].play()

class Huntsman(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(1000) # 1000 ms
        self.setDamage(600)
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setGunBackDuration(300)

    def fire(self):
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        if random.random() < 0.05:  # 5% chance
            bullet.setDamage(self.damage * 2)
        else:
            bullet.setDamage(self.damage)
        bullet.setBulletSpeed(2)
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Huntsman' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Huntsman"].play()

class Sidewinder(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(500)  # 500 ms
        self.setDamage(350)
        self.setDamageStatistic(1)
        self.setReloadStatistic(2)
        self.setGunBackDuration(300)
        self.setGunCenter(0, 1)
        
    def fire(self):
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = SidewinderBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        bullet.setBulletSpeed(1)
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None        
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Sidewinder' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        print("No sound effect smh")
        soundDictionary["Empty"].play()

class Silencer(Gun):

    wind_up = 1200
    delay = True
    lastRegister = 0
    sound = True
    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(2400) #2400 ms
        self.setDamage(1400)
        self.setDamageStatistic(3)
        self.setReloadStatistic(1)
        self.drawable = True
        self.setGunCenter(0, -3)

    def update(self):
        """
        Updates the gun's position, rotation, and shooting state based on the current controls and time.

        Because the Silencer has a custom shot, it needs to own special update method.
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
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed = self.turretSpeed
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed = -self.turretSpeed
        elif  keys[self.controls['left']]:
            self.rotationSpeed = self.tank.getRotationalSpeed()
        elif keys[self.controls['right']]:
            self.rotationSpeed = -self.tank.getRotationalSpeed()
        else:
            self.rotationSpeed = 0                
    
        self.angle += self.rotationSpeed
        self.angle %= 360

        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if keys[self.controls['rotate_left']] or keys[self.controls['rotate_right']]:
            if self.rotationSpeed != 0:
                if not self.soundPlaying:
                    soundDictionary["turretRotate"].play(loops = -1, fade_ms = 100)  # Play sound indefinitely
                    self.soundPlaying = True
            else:
                if self.soundPlaying:
                    soundDictionary["turretRotate"].stop()
                    self.soundPlaying = False
        else:
            if self.soundPlaying:
                soundDictionary["turretRotate"].stop()
                self.soundPlaying = False

        #Reload cooldown of bullet and determines the angle to fire the bullet,
        #which is relative to the posistion of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            if self.sound:
                self.playSFX()
                self.sound = False

            if self.delay:
                self.lastRegister = pygame.time.get_ticks()
                self.delay = False


        if not self.delay:
            wait = pygame.time.get_ticks()
            if wait - self.lastRegister >= self.wind_up:
                self.fire()
                self.delay = True

        angleRad = math.radians(self.angle)
        gunEndX, gunEndY = self.tank.getGunCenter()

        rotatedGunImage = pygame.transform.rotate(self.originalGunImage, self.angle)
        self.image = rotatedGunImage
        self.rect = self.image.get_rect(center=(gunEndX + self.gunH * math.cos(angleRad), gunEndY - self.gunH * math.sin(angleRad)))
        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.shootCooldown = 0
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

    def fire(self):
        # This function is responsible for all the firing mechanics of the gun
        # The Bullet is custom here as it is tailored for the Silencer
        # Inputs: None
        # Outputs: None
        #Setup bullet (Trailed/ Temp)
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = SilencerBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setDamage(0)
        bullet.setBulletSpeed(5)
        bullet.setName(self.getTank().getName())
        bullet.drawable = True
        bullet.trail = True
        bulletSprites.add(bullet)
        # Real bullet
        bullet1 = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet1.setDamage(self.damage)
        bullet1.setBulletSpeed(5)
        bullet1.setName(self.getTank().getName())
        bullet1.drawable = True
        bullet1.trail = True
        bulletSprites.add(bullet1)
        self.sound = True
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration

    def customDraw(self, screen):
        #This function will draw the gun on the tank and any additional features that may be needed
        # Inputs: Screen - The screen that the gun will be drawn on
        # Outputs: None
        if self.wind_up - (pygame.time.get_ticks() - self.lastRegister) >= 0:
            gunEndX, gunEndY = self.tank.getGunCenter()
            angleRad = math.radians(self.angle)
            pygame.draw.circle(screen, c.geT("NEON_PURPLE"),
                               (gunEndX + (self.gunH + 7) * math.cos(angleRad), gunEndY - (self.gunH + 7) * math.sin(angleRad)),
                                (pygame.time.get_ticks() - self.lastRegister)/self.wind_up * 5)

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None        
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Silencer' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Silencer"].play()

class Tempest(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(200) # 200 ms
        self.setDamage(200)
        self.setDamageStatistic(1)
        self.setReloadStatistic(3)
        self.setGunBackDuration(50)
        self.setGunCenter(0, -2)

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Tempest' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Tempest"].play()

class Watcher(Gun):

    scoping = False
    scopeDamage = 700
    scopeStartTime = 0
    speed = 0.1

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(1500) #1500 ms
        self.setDamage(3300)
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setTipOffset(25)
        self.drawable = True
        self.setGunCenter(0, -3)

    def update(self):
        """
        Updates the gun's position, rotation, and shooting state based on the current controls and time.

        Because the Silencer has a custom shot, it needs to own special update method.
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
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed = self.turretSpeed
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed = -self.turretSpeed
        elif  keys[self.controls['left']]:
            self.rotationSpeed = self.tank.getRotationalSpeed()
        elif keys[self.controls['right']]:
            self.rotationSpeed = -self.tank.getRotationalSpeed()
        else:
            self.rotationSpeed = 0               
    
        self.angle += self.rotationSpeed
        self.angle %= 360
        
        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if keys[self.controls['rotate_left']] or keys[self.controls['rotate_right']]:
            if self.rotationSpeed != 0:
                if not self.soundPlaying:
                    soundDictionary["turretRotate"].play(loops = -1, fade_ms = 100)  # Play sound indefinitely
                    self.soundPlaying = True
            else:
                if self.soundPlaying:
                    soundDictionary["turretRotate"].stop()
                    self.soundPlaying = False
        else:
            if self.soundPlaying:
                soundDictionary["turretRotate"].stop()
                self.soundPlaying = False


        #Reload cooldown of bullet and determines the angle to fire the bullet,
        #which is relative to the posistion of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            self.scoping = True
            self.scopeStartTime = pygame.time.get_ticks()

        if self.scoping:
            self.setTurretSpeed(self.getTurretSpeed()/20)
            self.getTank().setSpeed(self.getTank().getSpeed()/2)
            self.getTank().setRotationalSpeed(self.getTank().getTopRotationalSpeed()/25)
            #Scale the damage of the bullet
            self.scopeDamage += 10
            if self.scopeDamage >= 3300: # Max damage
                self.scopeDamage = 3300

            if not keys[self.controls['fire']]:
                self.scoping = False
                self.canShoot = False
                self.shootCooldown = self.cooldownDuration
                self.fire()
        else:
            self.resetTurrtSpeed()
            self.getTank().resetMaxSpeed()
            self.getTank().resetRotationalSpeed()

        angleRad = math.radians(self.angle)
        gunEndX, gunEndY = self.tank.getGunCenter()

        rotatedGunImage = pygame.transform.rotate(self.originalGunImage, self.angle)
        self.image = rotatedGunImage
        self.rect = self.image.get_rect(center=(gunEndX + self.gunH * math.cos(angleRad), gunEndY - self.gunH * math.sin(angleRad)))
        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.shootCooldown = 0
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

    def fire(self):
        # This function is responsible for all the firing mechanics of the gun
        # The Bullet is custom here as it is tailored for the Watcher
        # Inputs: None
        # Outputs: None
        # Setup bullet
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setDamage(self.getDamage())
        bullet.setBulletSpeed(5)
        bullet.setName(self.getTank().getName())
        bullet.drawable = True
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.scopeDamage = 700 # Reset the damage
        self.playSFX()

    def getDamage(self):
        return self.scopeDamage

    def customDraw(self, _):
        #This function will draw the gun on the tank
        # Inputs: None
        # Outputs: None
        if self.scoping:
            bulletX, bulletY = self.getTank().getGunCenter()
            bullet = WatcherBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
            bullet.setDamage(0)
            bullet.setBulletSpeed(25)
            if self.scopeDamage >= 3300:
                bullet.setTrailColor(c.geT("GREEN"))
            bullet.drawable = True
            bullet.trail = True
            bulletSprites.add(bullet)

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None        
        currentDir = os.path.dirname(__file__)
        gunPath = os.path.join(currentDir,'Sprites', 'Watcher' + str(imageNum) + '.png')
        self.originalGunImage = pygame.image.load(gunPath).convert_alpha()
        width, height = self.originalGunImage.get_size()
        self.originalGunImage = pygame.transform.scale(self.originalGunImage, (int(width*self.imgScaler), int(height*self.imgScaler)))
        self.gunImage = self.originalGunImage
        self.image = self.gunImage

        spritePath = os.path.join(currentDir, 'Sprites', 'Turret' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        soundDictionary["Watcher"].play()

#Hulls
class Bonsai(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(3500)
        self.setSpeedStatistic(2)
        self.setHealthStatistic(2)
        self.setTopSpeed(0.15)
        self.setTopRotationalSpeed(0.5)
        self.setTankName("Bonsai")

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'Bonsai' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), -5, 0, self.angle)
    
class Cicada(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(2000)
        self.setSpeedStatistic(3)
        self.setHealthStatistic(1)
        self.setTopSpeed(0.25)
        self.setTopRotationalSpeed(0.75)
        self.setTankName("Cicada")

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'Cicada' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), -4, 0, self.angle)

class DefaultTank(Tank):
    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(1)
        self.setSpeedStatistic(2)
        self.setHealthStatistic(2)
        self.setTopSpeed(0.25)
        self.setTopRotationalSpeed(0.5)
        self.setTankName("tank")

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'tank' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

class Fossil(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(4000)
        self.setSpeedStatistic(1)
        self.setHealthStatistic(3)
        self.setTopSpeed(0.1)
        self.setTopRotationalSpeed(0.25)
        self.setTankName("Fossil")

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'Fossil' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), 4, 0, self.angle)
    
class Gater(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(3000)
        self.setSpeedStatistic(2)
        self.setHealthStatistic(2)
        self.setTopSpeed(0.2)
        self.setTopRotationalSpeed(0.5)
        self.setTankName("Gater")

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'Gater' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), 0, 0, self.angle)

class Panther(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(1500)
        self.setSpeedStatistic(3)
        self.setHealthStatistic(1)
        self.setTopSpeed(0.3)
        self.setTopRotationalSpeed(0.8)
        self.setTankName("Panther")

    def setImage(self, imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        currentDir = os.path.dirname(__file__)
        tankPath = os.path.join(currentDir, 'Sprites', 'Panther' + str(imageNum) + '.png')
        self.originalTankImage = pygame.image.load(tankPath).convert_alpha()

        # Scale the tank image to a smaller size
        self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))
        self.width, self.height = self.originalTankImage.get_size() # Setting dimensions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        spritePath = os.path.join(currentDir, 'Sprites', 'Hull' + str(imageNum) + '.png')
        self.spriteImage = pygame.image.load(spritePath).convert_alpha()

    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), -4, 0, self.angle)

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

def setUpPlayers():
    global tileList, spawnpoint, tank1, tank2, gun1, gun2, allSprites, bulletSprites
    global p1I, p1J, p2I, p2J, p1K, p2K, p1L, p2L, DifficultyType
    # This function sets up the players for the game including reseting the respective global veriables
    #This function has no real dependencies on things outside of its control
    # Inputs: None
    # Outputs: None
    tileList = tileGen() # Get a new board
    spawnTank1 = [tileList[spawnpoint[0]-1].x + tileSize//2, tileList[spawnpoint[0]-1].y + tileSize//2]
    spawnTank2 = [tileList[spawnpoint[1]-1].x + tileSize//2, tileList[spawnpoint[1]-1].y + tileSize//2]
    #Updating the packages
    player1PackageTank = [spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName]
    player1PackageGun = [controlsTank1, p1GunName]
    player2PackageTank = [spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName]
    player2PackageGun = [controlsTank2, p2GunName]
    #Setup the tanks
    print(f"Difficulty Type: {DifficultyType}")
    if DifficultyType:
        # easy
        # tank1 = copy.copy(hullList[p1J]) # Tank 1 setup
        tank1 = DefaultTank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
        tank1.setData(player1PackageTank)
        tank1.setImage(p1L + 1)

        tank2 = DefaultTank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName) # Tank 2 setup
        tank2.setData(player2PackageTank)
        tank2.setImage(p2L + 1)

        gun1 = DefaultGun(tank1, controlsTank1, p1GunName) # Gun 1 setup
        gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1])
        gun1.setImage(p1K + 1)

        gun2 = DefaultGun(tank2, controlsTank2, p2GunName) # Gun 2 setup
        gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1])
        gun2.setImage(p2K + 1)
    else:
        #normal
        tank1 = copy.copy(hullList[p1J]) # Tank 1 setup
        tank1.setData(player1PackageTank)
        tank1.setImage(p1L + 1)

        tank2 = copy.copy(hullList[p2J]) # Tank 2 setup
        tank2.setData(player2PackageTank)
        tank2.setImage(p2L + 1)

        gun1 = copy.copy(turretList[p1I]) # Gun 1 setup
        gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1])
        gun1.setImage(p1K + 1)

        gun2 = copy.copy(turretList[p2I]) # Gun 2 setup
        gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1])
        gun2.setImage(p2K + 1)
    #Updating the groups
    for sprite in allSprites:
        sprite.kill()
    allSprites = pygame.sprite.Group() # Wipe the current Sprite Group

    allSprites.add(tank1, gun1, tank2, gun2) # Add the new sprites
    for bullet in bulletSprites:
        bullet.kill()
    bulletSprites = pygame.sprite.Group()

def constantHomeScreen():
    #This funciton handles the constant elements of the home screen
    # Inputs: None
    # Outputs: None
    screen.fill(bg) # This is the first line when drawing a new frame
    print("Switching to lobby music")
    mixer.crossfade('lobby')

def constantSelectionScreen():
    #This function handles the constant elements of the selection screen
    # Inputs: None
    # Outputs: None
    print("Switching to selection music")
    mixer.crossfade('selection')

def constantPlayGame():
    #This function handles the constant elements of the game screen
    # Inputs: None
    # Outputs: None
    screen.fill(bg) # This is the first line when drawing a new frame
    screen.blit(gun1.getSprite(True), (tileSize, 0.78*windowHeight)) # Gun 2
    screen.blit(tank1.getSprite(True), (tileSize, 0.78*windowHeight)) # Tank 2

    screen.blit(gun2.getSprite(), (windowWidth - tileSize*3, 0.78*windowHeight)) # Gun 2
    screen.blit(tank2.getSprite(), (windowWidth - tileSize*3, 0.78*windowHeight)) # Tank 2
    print("Switching to game music")
    mixer.crossfade('game')
    fontName = pygame.font.Font('fonts/LondrinaSolid-Regular.otf', 30)
    fontName2 = pygame.font.SysFont('Courier New', 20, True, False)
    fontString = "PLAYER 1             SCORE              PLAYER 2" # This is a bad way to write a string
    controlString = "WASD                            ↑↓→←" # This is a bad way to write a string
    textp2Name = fontName.render(fontString, True, c.geT("BLACK"))
    controls = fontName2.render(controlString, True, c.geT("BLACK"))
    screen.blit(textp2Name,[windowWidth//2 - textp2Name.get_width()//2, 0.78*windowHeight]) # This is the name on the right
    screen.blit(controls,[windowWidth//2 - controls.get_width()//2, windowHeight*5/6]) # This is the name on the right

    HealthBox = TextBox(tileSize*7/8-1, 0.88*windowHeight, "Londrina", "HEALTH", 20, c.geT("BLACK"))
    HealthBox.setPaddingHeight(0)
    HealthBox.setPaddingWidth(0)
    HealthBox.setBoxColor(bg)
    HealthBox.draw(screen)

    ReloadBox = TextBox(tileSize*7/8-1, 0.88*windowHeight + mazeY//2, "Londrina", "RELOAD", 20, c.geT("BLACK"))
    ReloadBox.setPaddingHeight(0)
    ReloadBox.setPaddingWidth(0)
    ReloadBox.setBoxColor(bg)
    ReloadBox.draw(screen)

    HealthBox2 = TextBox(windowWidth-tileSize*2.2-1, 0.88*windowHeight, "Londrina", "HEALTH", 20, c.geT("BLACK"))
    HealthBox2.setPaddingHeight(0)
    HealthBox2.setPaddingWidth(0)
    HealthBox2.setBoxColor(bg)
    HealthBox2.draw(screen)

    ReloadBox2 = TextBox(windowWidth-tileSize*2.2-1, 0.88*windowHeight + mazeY//2, "Londrina", "RELOAD", 20, c.geT("BLACK"))
    ReloadBox2.setPaddingHeight(0)
    ReloadBox2.setPaddingWidth(0)
    ReloadBox2.setBoxColor(bg)
    ReloadBox2.draw(screen)

def playGame():
    # This function controls the main execution of the game
    # Inputs: None
    # Outputs: None
    # Because of the way the game is structured, these global variables can't be avoided
    global gameOverFlag, cooldownTimer, startTime, p1Score, p2Score, startTreads
    global tank1Dead, tank2Dead, tileList, spawnpoint
    global tank1, tank2, gun1, gun2, allSprites, bulletSprites
    if gameOverFlag:
        #The game is over
        startTime = time.time() #Start a 5s timer
        gameOverFlag = False
        cooldownTimer = True
    if cooldownTimer:
        if time.time() - startTime >= 3: # 3 seconds
            #Reset the game
            reset()
            constantPlayGame()

    #UI Elements
    pauseButton.update_display(pygame.mouse.get_pos())
    pauseButton.draw(screen, outline = True)

    pygame.draw.rect(screen, bg, [tileSize*0.72, tileSize*0.72, windowWidth - tileSize*1.4, tileSize*8.5]) # Draw a box for the maze
    
    #Making the string for score
    p1ScoreText = str(p1Score)
    p2ScoreText = str(p2Score)
    #Setting up the text
    fontScore = pygame.font.SysFont('Londrina', 90, True, False)
    fontScore = pygame.font.Font('fonts/LondrinaSolid-Regular.otf', 70)
    pygame.draw.rect(screen, bg, [tileSize*2.1, 0.87*windowHeight, windowWidth-tileSize*1.2-barWidth, windowHeight*0.15]) # The bottom bar

    text3 = fontScore.render(p1ScoreText + ":" + p2ScoreText, True, c.geT("BLACK"))
    screen.blit(text3, [windowWidth/2 - text3.get_width()/2, 0.87*windowHeight])

    #Box around the bottom of the screen for the health and reload bars


    pygame.draw.rect(screen, c.geT("RED"), [tileSize*2.2, 0.88*windowHeight, barWidth*(tank1.getHealthPercentage()),
                                            barHeight]) # Bar
    pygame.draw.rect(screen, c.geT("BLACK"), [tileSize*2.2, 0.88*windowHeight, barWidth, barHeight], 2) # Outline
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [tileSize*2.2, 0.88*windowHeight + mazeY//2, barWidth*(min(1,1-gun1.getReloadPercentage())),
                                             barHeight]) # The 25 is to space from the health bar

    pygame.draw.rect(screen, c.geT("BLACK"), [tileSize*2.2, 0.88*windowHeight + mazeY//2, barWidth, barHeight], 2) # Outline




    #Health bars
    pygame.draw.rect(screen, c.geT("RED"), [windowWidth - tileSize*2.2 - barWidth, 0.88*windowHeight, barWidth*(tank2.getHealthPercentage()),
                                            barHeight])
    pygame.draw.rect(screen, c.geT("BLACK"), [windowWidth - tileSize*2.2 - barWidth, 0.88*windowHeight, barWidth, barHeight], 2)
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [windowWidth - tileSize*2.2 - barWidth, 0.88*windowHeight + mazeY//2,
                                             barWidth*(min(1,1-gun2.getReloadPercentage())),
                                             barHeight]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, c.geT("BLACK"), [windowWidth - tileSize*2.2 - barWidth, 0.88*windowHeight + mazeY//2, barWidth, barHeight], 2) # Outline

    # Draw the border

    for tile in tileList:
        tile.draw(screen)




    #Anything below here will be drawn on top of the maze and hence is game updates

    #Update the location of the corners
    tank1.updateCorners()
    tank2.updateCorners()

    if pygame.time.get_ticks() - startTreads > 50:
        tank1.treads(1)
        tank2.treads(2)
        startTreads = pygame.time.get_ticks() # Reset the timer

    for pos in treadsp1:
        screen.blit(pos[0], pos[1])
    for pos in treadsp2:
        screen.blit(pos[0], pos[1])
    # pygame.draw.polygon(screen, GREEN, tank1.getCorners(), 2) #Hit box outline
    # pygame.draw.polygon(screen, GREEN, tank2.getCorners(), 2) #Hit box outline
    allSprites.update()
    bulletSprites.update()
    explosionGroup.update()
    for sprite in allSprites:
        sprite.draw(screen)
        if sprite.isDrawable():
            sprite.customDraw(screen)

    for sprite in bulletSprites:
        sprite.draw(screen)
        if sprite.isDrawable():
            sprite.customDraw(screen)    


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

def reset():
    # This function is to reset the board everytime we want to restart the game
    # Inputs: None
    # Outputs: None
    # Because of the way it's coded, these global declarations can't be avoided
    global gameOverFlag, cooldownTimer, startTime, p1Score, p2Score
    global tank1Dead, tank2Dead
    global allSprites, bulletSprites
    gameOverFlag = False
    cooldownTimer = False
    #Remove all the sprites
    for sprite in allSprites:
        sprite.kill()
    allSprites = pygame.sprite.Group() # Wipe the current Sprite Group
    for sprite in bulletSprites:
        sprite.kill()
    bulletSprites = pygame.sprite.Group()
    #Nautural constants
    startTime = 0
    tank1Dead = False
    tank2Dead = False
    treadsp1.clear()
    treadsp2.clear()
    setUpPlayers()

def updateTankHealth():
    # This function will update the tank health and check if the tank is dead
    # Inputs: None
    # Outputs: None
    global explosionGroup, tank1Dead, tank2Dead, gameOverFlag
    global p1Score, p2Score
    global allSprites, tank1, tank2, gun1, gun2
    #Update the tank health
    if tank1.getHealth() <= 0:
        if not tank1Dead:
            print("Player 2 Wins")
            p2Score += 1
            tank1Dead = True
            explosionGroup.add(Explosion(tank1.getCenter()[0], tank1.getCenter()[1]))
        tank1.setCentre(2000, 2000)
        gun1.kill()
        tank1.kill()
        if tank2.getHealth() <= 0:
            for sprite in allSprites:
                sprite.kill()
            allSprites = pygame.sprite.Group()
        gameOverFlag = True #The game is over
    if tank2.getHealth() <= 0:
        if not tank2Dead:
            print("Player 1 Wins")
            p1Score += 1
            tank2Dead = True
            explosionGroup.add(Explosion(tank2.getCenter()[0], tank2.getCenter()[1]))
        tank2.setCentre(-2000, -2000)
        gun2.kill()
        tank2.kill()
        if tank1.getHealth() <= 0:
            for sprite in allSprites:
                sprite.kill()            
            allSprites = pygame.sprite.Group()
        gameOverFlag = True #The game is over


#Game setup
#Start the game setup
pygame.init()
mixer = Music()
mixer.play()
pygame.display.set_caption("TankTroubleDupe") # Name the window
clock = pygame.time.Clock() # Start the clock

initialStartTime = pygame.time.get_ticks()
soundPlayed = False

global animationCool
animationCool = 12

global explosionGroup
explosionGroup = pygame.sprite.Group() #All the explosions

resetFlag = True
startTime = 0
cooldownTimer = False
global startTreads
startTreads = 0
global gameOverFlag
gameOverFlag = False

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
mazeY = 50
mazeWidth = windowWidth - mazeX*2 # We want it to span most of the screen
mazeHeight = windowHeight - mazeY*4
rowAmount = mazeHeight//tileSize # Assigning the amount of rows
colAmount = mazeWidth//tileSize # Assigning the amount of columns
barWidth = 150
barHeight = 20
bg = c.geT('SOFT_WHITE')
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

selectionBackground = c.geT("SOFT_WHITE")
selectionFont = 'Londrina Solid'
monoFont = 'Courier New'


#Selection Screen
buttonList = []
homeButton = TextBox(tileSize//4, tileSize//4, font=selectionFont,fontSize=26, text="BACK", textColor=c.geT("BLACK"))
homeButton.setBoxColor(selectionBackground)
homeButton.setOutline(True, 5)
homeButton.selectable(True)
buttonList.append(homeButton)

#How to play button
howToPlayButton = TextBox(windowWidth - 150, tileSize//4, font=selectionFont,fontSize=26, text="HOW TO PLAY", textColor=c.geT("BLACK"))
howToPlayButton.setBoxColor(selectionBackground)
howToPlayButton.setOutline(True, 5)
howToPlayButton.selectable(True)
buttonList.append(howToPlayButton)

playButton = TextBox(windowWidth//2-84, 95, font=selectionFont,fontSize=52, text="PLAY", textColor=c.geT("BLACK"))
playButton.setBoxColor(selectionBackground)
playButton.setOutline(True, 5)
playButton.selectable(True)
buttonList.append(playButton)

buttonPrimary = c.geT("BLACK")
buttonSecondary = c.geT("WHITE")
buttonText = c.geT("WHITE")
optionText = c.geT("GREY")
#Hull and turret list
turretList = [Tempest(Tank(0,0,None, "Default"), None, "Tempest"), Silencer(Tank(0,0,None, "Default"), None, "Silencer"),
              Watcher(Tank(0,0,None, "Default"), None, "Watcher"), Chamber(Tank(0,0,None, "Default"), None, "Chamber"),
              Huntsman(Tank(0,0,None,"Default"),None,"Huntsman"), Judge(Tank(0,0,None,"Default"),None,"Judge"),
              Sidewinder(Tank(0,0,None,"Default"),None,"Sidewinder")]

hullList = [Panther(0, 0, None, "Panther"), Cicada(0, 0, None, "Cicada"), Gater(0, 0, None, "Gater"), Bonsai(0, 0, None, "Bonsai"),
            Fossil(0, 0, None, "Fossil")]

DifficultyType = 0

turretListLength = len(turretList)
hullListLength = len(hullList)

hullColors = []
gunColors = []

treadsp1 = []
treadsp2 = []
treadslen = 10

# Load all the images
currentDir = os.path.dirname(__file__)

ColorIndex = ["TANK_GREEN", "BURGUNDY", "ORANGE", "YELLOW", "SKY_BLUE", "LIGHT_BROWN", "DARK_LILAC", "BRIGHT_PINK"]

tankMultiple = 4
gunMultiple = 4
for i in range(8): # Generate all the tanks, this needs to be removed as it's not needed anymore
    tankPath = os.path.join(currentDir, 'Sprites', 'tank' + str(i+1) + '.png')
    originalTankImage = pygame.image.load(tankPath).convert_alpha()
    tankImage = pygame.transform.scale(originalTankImage, (20*tankMultiple, 13*tankMultiple))
    hullColors.append(tankImage)
    gunPath = os.path.join(currentDir, 'Sprites', 'gun' + str(i+1) + '.png')
    originalGunImage = pygame.image.load(gunPath).convert_alpha()
    gunImage = pygame.transform.scale(originalGunImage, (15*gunMultiple, 2*gunMultiple))
    gunColors.append(gunImage)    


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

p1L = 1
p2L = 0
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
textP1Turret = TextBox(cBoX, TurretX, font=monoFont,fontSize=textFontSize, text=turretList[p1I].getGunName(), textColor=buttonText)
textP1Turret.setBoxColor(optionText)
textP1Turret.selectable(False)
textP1Turret.setPaddingHeight(0)
buttonList.append(textP1Turret)
rArrowP1Turret = Button(buttonPrimary, buttonPrimary, rArrowX, TurretX, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP1Turret.selectable(False)
buttonList.append(rArrowP1Turret)

lArrowP1Hull = Button(buttonPrimary, buttonPrimary, lArrowX, HullX, buttonSize, buttonSize, '<', buttonText, buttonFontSize)
lArrowP1Hull.selectable(False)
buttonList.append(lArrowP1Hull)
textP1Hull = TextBox(cBoX, HullX, font=monoFont,fontSize=textFontSize, text=hullList[p1J].getTankName(), textColor=buttonText)
textP1Hull.setBoxColor(optionText)
textP1Hull.selectable(False)
textP1Hull.setPaddingHeight(0)
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
textP1Colour2.setBoxColor(c.geT(ColorIndex[p1L]))
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
textP2Turret = TextBox(cBo2X, TurretX, font=monoFont,fontSize=textFontSize, text=turretList[p2I].getGunName(), textColor=buttonText)
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
textP2Hull = TextBox(cBo2X, HullX, font=monoFont,fontSize=textFontSize, text=hullList[p2J].getTankName(), textColor=buttonText)
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
textP2Colour2.setBoxColor(c.geT(ColorIndex[p2L]))
textP2Colour2.selectable(False)
textP2Colour2.setPaddingHeight(0)
buttonList.append(textP2Colour2)
rArrowP2Colour2 = Button(buttonPrimary, buttonPrimary,  rArrow2X, ColourX2, buttonSize, buttonSize, '>', buttonText, buttonFontSize)
rArrowP2Colour2.selectable(False)
buttonList.append(rArrowP2Colour2)

# Player names
playerX = 100
playerY = 100

textP1 = TextBox(playerX, playerY, font=selectionFont,fontSize=38, text="PLAYER 1", textColor=c.geT("BLACK"))
textP1.setBoxColor(selectionBackground)
textP1.setOutline(True, outlineWidth = 5)
buttonList.append(textP1)

textP2 = TextBox(windowWidth - playerX*2.5, playerY, font=selectionFont,fontSize=38, text="PLAYER 2", textColor=c.geT("BLACK"))
textP2.setBoxColor(selectionBackground)
textP2.setOutline(True, outlineWidth = 5)
buttonList.append(textP2)

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
    #This function checks all the buttons of the mouse in the selection screen
    # Inputs: Mouse: The current location of the mouse
    # Outputs: None
    global p1I, p2I, p1J, p2J, p1K, p2K, p1L, p2L, gameMode
    global tank1, tank2, gun1, gun2

    if lArrowP1Turret.buttonClick(mouse):
        p1I = (p1I - 1) % turretListLength
        textP1Turret.setText(turretList[p1I].getGunName())
    if rArrowP1Turret.buttonClick(mouse):
        p1I = (p1I + 1) % turretListLength
        textP1Turret.setText(turretList[p1I].getGunName())
    if lArrowP1Hull.buttonClick(mouse):
        p1J = (p1J - 1) % hullListLength
        textP1Hull.setText(hullList[p1J].getTankName())
    if rArrowP1Hull.buttonClick(mouse):
        p1J = (p1J + 1) % hullListLength
        textP1Hull.setText(hullList[p1J].getTankName())
    if lArrowP2Turret.buttonClick(mouse):
        p2I = (p2I - 1) % turretListLength
        textP2Turret.setText(turretList[p2I].getGunName())
    if rArrowP2Turret.buttonClick(mouse):
        p2I = (p2I + 1) % turretListLength
        textP2Turret.setText(turretList[p2I].getGunName())
    if lArrowP2Hull.buttonClick(mouse):
        p2J = (p2J - 1) % hullListLength
        textP2Hull.setText(hullList[p2J].getTankName())
    if rArrowP2Hull.buttonClick(mouse):
        p2J = (p2J + 1) % hullListLength
        textP2Hull.setText(hullList[p2J].getTankName())
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
    if lArrowP1Colour2.buttonClick(mouse):
        p1L = (p1L - 1) % len(hullColors)
        if p1L == p2L:
            p1L = (p1L - 1) % len(hullColors)
        textP1Colour2.setBoxColor(c.geT(ColorIndex[p1L]))
    if rArrowP1Colour2.buttonClick(mouse):
        p1L = (p1L + 1) % len(hullColors)
        if p1L == p2L:
            p1L = (p1L + 1) % len(hullColors)
        textP1Colour2.setBoxColor(c.geT(ColorIndex[p1L]))
    if lArrowP2Colour2.buttonClick(mouse):
        p2L = (p2L - 1) % len(hullColors)
        if p2L == p1L:
            p2L = (p2L - 1) % len(hullColors)
        textP2Colour2.setBoxColor(c.geT(ColorIndex[p2L]))
    if rArrowP2Colour2.buttonClick(mouse):
        p2L = (p2L + 1) % len(hullColors)
        if p2L == p1L:
            p2L = (p2L + 1) % len(hullColors)
        textP2Colour2.setBoxColor(c.geT(ColorIndex[p2L]))

    if playButton.buttonClick(mouse):
        setUpPlayers()
        #Switch the the play screen
        print("Play")
        constantPlayGame()
        gameMode=GameMode.play
    if homeButton.buttonClick(mouse):
        #Switch back to the home screen
        constantHomeScreen()
        print("Back")
        gameMode = GameMode.home
    if howToPlayButton.buttonClick(mouse):
        print("How to Play")

def checkHomeButtons(mouse):
    # This function checks all the buttons of the mouse in the home screen
    # Inputs: Mouse: The current location of the mouse
    # Outputs: None
    global gameMode, DifficultyType

# homeButtonList.append(onePlayerButtonHomeN)
# homeButtonList.append(onePlayerButtonHomeH)
# homeButtonList.append(twoPlayerButtonHomeN)
# homeButtonList.append(twoPlayerButtonHomeH)
    if onePlayerButtonHomeN.buttonClick(mouse):
        DifficultyType = 1
        setUpPlayers()
        gameMode=GameMode.play
        #Switch the the play screen
        print("One Player Easy")
        constantPlayGame()
    if twoPlayerButtonHomeN.buttonClick(mouse):
        DifficultyType = 1
        setUpPlayers()
        gameMode=GameMode.play
        #Switch the the play screen
        print("Two Player Easy")
        constantPlayGame()
    if onePlayerButtonHomeH.buttonClick(mouse):
        print("One Player Hard")
        gameMode = GameMode.selection
        DifficultyType = 0
        constantSelectionScreen()
    if twoPlayerButtonHomeH.buttonClick(mouse):
        print("Two Player Hard")
        gameMode = GameMode.selection
        DifficultyType = 0
        constantSelectionScreen()



    # if playButtonHome.buttonClick(mouse):
    #     #Switch to the selection screen
    #     gameMode = GameMode.selection
    #     print("Selection")
    #     constantSelectionScreen()
    if settingsButton.buttonClick(mouse):
        print("Unimplmented")
        # gameMode = GameMode.settings
    if quitButtonHome.buttonClick(mouse):
        global done
        done = True

def selectionScreen():
    barBorder = 3
    
    #Blocks
    BarLevelX = 157
    cellWidth = 50
    # Player 1 Speed
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, speedBarX, cellWidth * hullList[p1J].getSpeedStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, speedBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, speedBarX, cellWidth, rectY), barBorder) # Thirding

    #Player 1 Health
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, healthBarX, cellWidth * hullList[p1J].getHealthStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, healthBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, healthBarX, cellWidth,rectY), barBorder) # Thirding

    # Player 1 damage
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, damageBarX, cellWidth * turretList[p1I].getDamageStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, damageBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, damageBarX, cellWidth,rectY), barBorder) # Thirding

    # Player 1 reload
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelX, reloadBarX, cellWidth * turretList[p1I].getReloadStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX, reloadBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelX + cellWidth, reloadBarX, cellWidth,rectY), barBorder) # Thirding


    BarLevelRX = 493

    #Player 2 Speed
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, speedBarX, cellWidth * hullList[p2J].getSpeedStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, speedBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, speedBarX, cellWidth,rectY), barBorder) # Thirding

    # Player 2 Health
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, healthBarX, cellWidth * hullList[p2J].getHealthStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, healthBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, healthBarX, cellWidth,rectY), barBorder) # Thirding

    # Player 2 Damage
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, damageBarX,cellWidth * turretList[p2I].getDamageStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, damageBarX, cellWidth*3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, damageBarX, cellWidth, rectY), barBorder) # Thirding

    # Player 2 Reload
    pygame.draw.rect(screen, c.geT("GREEN"), (BarLevelRX, reloadBarX, cellWidth * turretList[p2I].getReloadStatistic(), rectY)) # Green bar
    #Outlines
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX, reloadBarX, cellWidth * 3, rectY), barBorder) # Green bar outline
    pygame.draw.rect(screen, c.geT("BLACK"), (BarLevelRX + cellWidth, reloadBarX, cellWidth,rectY), barBorder) # Thirding

    #Draw the tank image
    # Update display

    hullImageX = 130
    hullImageY = 174
    gunImageX = 170
    gunImageY = 194

    gunScale = 5

    #Draw the tank image

    tankPath = os.path.join(currentDir, 'Sprites', hullList[p1J].getTankName() + str(p1L + 1) + '.png')
    originalTankImage = pygame.image.load(tankPath).convert_alpha()
    tankImage = pygame.transform.scale(originalTankImage, (20*4, 13*4))
    screen.blit(tankImage, (hullImageX, hullImageY))

    gunPath = os.path.join(currentDir, 'Sprites', turretList[p1I].getGunName() + str(p1K+1) + '.png')
    originalGunImage = pygame.image.load(gunPath).convert_alpha()
    centerX, centerY = hullList[p1J].getGunCenter()
    gX, _ = turretList[p1I].getGunCenter()
    gunImage = pygame.transform.scale(originalGunImage, (15*gunScale, 15*gunScale))
    screen.blit(gunImage, (gunImageX + (centerX - gX) * gunScale, gunImageY - (centerY + 6) * gunScale))
    
    tankPath2 = os.path.join(currentDir, 'Sprites', hullList[p2J].getTankName() + str(p2L + 1) + '.png')
    originalTankImage2 = pygame.image.load(tankPath2).convert_alpha()
    tankImage2 = pygame.transform.scale(originalTankImage2, (20*4, 13*4))
    tankImage2 = pygame.transform.flip(tankImage2, True, False) # Flipped    
    screen.blit(tankImage2, (windowWidth - hullImageX - 4 * 20, hullImageY))

    gunPath2 = os.path.join(currentDir, 'Sprites', turretList[p2I].getGunName() + str(p2K+1) + '.png')
    originalGunImage2 = pygame.image.load(gunPath2).convert_alpha()
    centerX, centerY = hullList[p2J].getGunCenter()
    gX, _ = turretList[p2I].getGunCenter()

    gunImage2 = pygame.transform.scale(originalGunImage2, (15*gunScale, 15*gunScale))
    gunImage2 = pygame.transform.flip(gunImage2, True, False) # Flipped
    screen.blit(gunImage2, (windowWidth - gunImageX - gunScale * 15 - (centerX - gX)*gunScale, gunImageY + centerY*gunScale - 6*gunScale))

#Menu screen
homeButtonList = []

# Load the tank image
currentDir = os.path.dirname(__file__)
tankPath = os.path.join(currentDir, 'tank_menu_logo.png')
originalTankImage = pygame.image.load(tankPath).convert_alpha()



# Create buttons with specified positions and text
onePlayerButtonHomeN = Button(c.geT("BLACK"),c.geT("BLACK"), 30, 470, 140, 80, '1P Easy', (255, 255, 255), 15, hoverColor=(100, 100, 255))
onePlayerButtonHomeH = Button(c.geT("BLACK"),c.geT("BLACK"), 230, 470, 140, 80, '1P Hard', (255, 255, 255), 15, hoverColor=(100, 100, 255))
twoPlayerButtonHomeN = Button(c.geT("BLACK"),c.geT("BLACK"), 430, 470, 140, 80, '2P Easy', (255, 255, 255), 15, hoverColor=(100, 100, 255))
twoPlayerButtonHomeH = Button(c.geT("BLACK"),c.geT("BLACK"), 630, 470, 140, 80, '2P Hard', (255, 255, 255), 15, hoverColor=(100, 100, 255))
quitButtonHome = Button(c.geT("BLACK"), c.geT("BLACK"), 30, 30, 140, 80, 'Quit', (255, 255, 255), 25, hoverColor=(100, 100, 255))
settingsButton = Button(c.geT("BLACK"), c.geT("BLACK"), 600, 30, 210, 80, 'Settings', (255, 255, 255), 25, hoverColor=(100, 100, 255))

homeButtonList.append(onePlayerButtonHomeN)
homeButtonList.append(onePlayerButtonHomeH)
homeButtonList.append(twoPlayerButtonHomeN)
homeButtonList.append(twoPlayerButtonHomeH)
homeButtonList.append(settingsButton)
homeButtonList.append(quitButtonHome)

# Define title text properties
titleFont = pygame.font.SysFont('Arial', 60)
titleText = titleFont.render('Tank Game Menu', True, (0, 0, 0))  # Render the title text

pauseButton = Button(bg ,bg, windowWidth-tileSize*3, tileSize//5,tileSize*2,tileSize//2, "PAUSE", c.geT("BLACK"), 20, c.geT("OFF_WHITE"))
pauseButton.setOutline(True, 2)

# Controls for the first tank
controlsTank1 = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'rotate_left': pygame.K_r,
    'rotate_right': pygame.K_t,
    'fire': pygame.K_y
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

volume = {
    'lobby': 0.2,
    'selection': 1,
    'game': 0.2,
    'tankShoot': 1,
    'tankDeath': 0.5,
    'turretRotate': 0.2,
    'tankMove': 0.05,
    'Chamber': 0.5,
    'Empty': 1,
    'Huntsman': 1,
    'Judge': 0.38,
    'Silencer': 0.25,
    'Sidewinder': 1,
    'Tempest': 1,
    'Watcher': 0.5
}

soundDictionary = {
    'tankDeath' : pygame.mixer.Sound('Sounds/tank_dead.wav'),
    'tankMove' : pygame.mixer.Sound('Sounds/tank_moving.wav'),
    'tankShoot' : pygame.mixer.Sound('Sounds/tank_shoot.wav'),
    'turretRotate' : pygame.mixer.Sound('Sounds/tank_turret_rotate.wav'),
    'Chamber' : pygame.mixer.Sound('Sounds/Empty.wav'),
    'Empty' : pygame.mixer.Sound('Sounds/Empty.wav'),
    'Huntsman' : pygame.mixer.Sound('Sounds/Huntsman.wav'),
    'Judge' : pygame.mixer.Sound('Sounds/Judge.wav'),
    'Silencer' : pygame.mixer.Sound('Sounds/Silencer.wav'),
    'Sidewinder' : pygame.mixer.Sound('Sounds/Empty.wav'),
    'Tempest' : pygame.mixer.Sound('Sounds/Empty.wav'),
    'Watcher' : pygame.mixer.Sound('Sounds/Watcher.wav'),
}



for sound in soundDictionary:
    soundDictionary[sound].set_volume(volume[sound])

spawnTank1 = [tileList[spawnpoint[0]-1].x + tileSize//2, tileList[spawnpoint[0]-1].y + tileSize//2]
spawnTank2 = [tileList[spawnpoint[1]-1].x + tileSize//2, tileList[spawnpoint[1]-1].y + tileSize//2]

global tank1Dead, tank2Dead
tank1Dead = False
tank2Dead = False

player1PackageTank = [spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName]
player1PackageGun = [controlsTank1, p1GunName]
player2PackageTank = [spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName]
player2PackageGun = [controlsTank2, p2GunName]

allSprites = pygame.sprite.Group()
bulletSprites = pygame.sprite.Group()

constantHomeScreen()
totalfps = 0
fpsCounter = 0


#Main loop
while not done:
    # Early define probably not a good idea, but will help with reducing function calls
    mouse = pygame.mouse.get_pos() #Update the position

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse = pygame.mouse.get_pos() # Update on button press
            if event.button != 1:
                #Not left click
                break
            if gameMode == GameMode.pause:
                #We are paused
                if (unPause.getCorners()[0] <= mouse[0] <= unPause.getCorners()[2] and
                    unPause.getCorners()[1] <= mouse[1] <= unPause.getCorners()[3]): #If we click the return to game button
                    constantPlayGame()
                    gameMode = GameMode.play # Return to game if button was clicked
                if (home.getCorners()[0] <= mouse[0] <= home.getCorners()[2] and
                    home.getCorners()[1] <= mouse[1] <= home.getCorners()[3]): # Home button
                    constantHomeScreen()
                    gameMode = GameMode.home
                if (quitButton.getCorners()[0] <= mouse[0] <= quitButton.getCorners()[2]and
                    quitButton.getCorners()[1] <= mouse[1] <= quitButton.getCorners()[3]): # If we hit the quit butotn
                    print("Quitting the game")
                    done = True # We quit the appplication
                if (mute.getCorners()[0] <= mouse[0] <= mute.getCorners()[2] and
                    mute.getCorners()[1] <= mouse[1] <= mute.getCorners()[3]): # If we hit the mute button
                    mute.buttonClick()
                if (sfx.getCorners()[0] <= mouse[0] <= sfx.getCorners()[2] and 
                    sfx.getCorners()[1] <= mouse[1] <= sfx.getCorners()[3]): # If we hit the sfx button
                    sfx.buttonClick()
                if pauseButton.buttonClick(mouse):
                    constantPlayGame()
                    gameMode = GameMode.play
                    print("Pause button clicked")
            elif gameMode == GameMode.selection: # Selection screen
                textP1Turret.setText(turretList[p1I].getGunName())
                textP2Turret.setText(turretList[p2I].getGunName())
                textP1Hull.setText(hullList[p1J].getTankName())
                textP2Hull.setText(hullList[p2J].getTankName())
                checkButtons(mouse)
            elif gameMode == GameMode.home: # Home screen
                checkHomeButtons(mouse)
            elif gameMode == GameMode.play:
                if pauseButton.buttonClick(mouse):
                    gameMode = GameMode.pause
                    print("Pause button clicked")
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
                    constantPlayGame()
                    gameMode = GameMode.play # Return to game if button was clicked
                elif gameMode == GameMode.play:
                    gameMode = GameMode.pause # Pause the game
            if event.key == pygame.K_l:
                pass
            if event.key == pygame.K_k:
                pass
            if event.key == pygame.K_f:
                #Calculate and track the average FPS
                totalfps += clock.get_fps()
                fpsCounter += 1
                print("The average FPS is: ", totalfps/fpsCounter)
                totalfps = 0
                fpsCounter = 0

            if event.key == pygame.K_n:
                if gameMode == GameMode.play:
                    constantPlayGame()
                    reset()
            if event.key == pygame.K_0:
                if gameMode == GameMode.play:
                    constantPlayGame()
                    reset()
            if event.key == pygame.K_m:
                mute.mute()

    if gameMode == GameMode.play:
        playGame() # Play the game
    elif gameMode == GameMode.pause:
        pauseScreen() # Pause screen
        if mouse[0]:
            mute.updateSlider(mouse[0], mouse[1])
            sfx.updateSlider(mouse[0], mouse[1])
            for sound in soundDictionary:
                soundDictionary[sound].set_volume(volume[sound] * sfx.getValue())
    elif gameMode == GameMode.selection:
        screen.fill(selectionBackground) # This is the first line when drawing a new frame
        for button in buttonList:
            button.update_display(mouse)
            button.draw(screen, outline = False)
        selectionScreen()


    elif gameMode == GameMode.home:
        # Draw the tank image
        screen.blit(originalTankImage, (230, 65))  # Adjust the coordinates as needed

        # Draw the title text
        screen.blit(titleText, (windowWidth // 2 - titleText.get_width() // 2, 50))  # Centered horizontally, 50 pixels from top

        # Handle hover effect and draw buttons
        for button in homeButtonList:
            button.update_display(mouse)
            button.draw(screen, outline=True)
    
    else:
        screen.fill(c.geT("WHITE")) # Errornous state
    clock.tick(240) # Set the FPS
    mixer.update(mute.getValue()) # Update the mixer

    pygame.display.flip()# Update the screen

pygame.quit()