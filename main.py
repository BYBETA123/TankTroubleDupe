import pygame
import random
import math
import time
import os, sys
from ColorDictionary import ColourDictionary as c # colors
from enum import Enum
from UIUtility import Button, ButtonSlider, TextBox
from music import Music
import copy
from tanks import *
from Screen import *
import constants as const

# Safety Checks
if getattr(sys, 'frozen', False):  # Running as an .exe
    tempList = os.listdir(os.path.join(sys._MEIPASS, 'Sprites'))
else:  # Running as a .py script
    tempList = os.listdir('Sprites')

comparisonList = [] # This list is to contain all of the different types of sprites that are involved
nameList = ["Bonsai", "Chamber", "Cicada", "Fossil", "Gater", "gun", "Hull", "Huntsman", "Judge", "Panther", "playerGunSprite", "playerTankSprite", "Sidewinder", "Silencer", "tank", "Tempest", "Turret", "Watcher"]
for i in range(len(nameList)):
    for j in range(8): # There are 8 different types of sprites
        comparisonList.append(nameList[i] + str(j+1) + ".png")

# Check that all the sprites are present
found = False
anyMissing = False
for j in comparisonList:
    found = False # Reset the found variable
    for i in tempList:
        if i == j:
            # If they are the same then the sprite is present
            found = True
            break
    if not found:
        print(f"Error: {j} is missing")
        anyMissing = True

# Check the asssets folder
if getattr(sys, 'frozen', False):  # Running as an .exe
    tempList = os.listdir(os.path.join(sys._MEIPASS, 'Assets'))
else:  # Running as a .py script
    tempList = os.listdir('Assets')
comparisonList = ['bullet.png', 'explosion.png', 'tank_menu_logo.png', 'Tile.png', 'TileDebug.png', 'TileE.png', 'TileES.png', 'TileESW.png', 'TileEW.png', 'TileN.png', 'TileNE.png', 'TileNES.png', 'TileNESW.png', 'TileNEW.png', 'TileNS.png', 'TileNSW.png', 'TileNW.png', 'TileS.png', 'TileSW.png', 'TileW.png', 'Treads.png']

for i in comparisonList:
    found = False # Reset the found variable
    for j in tempList:
        if j == i:
            found = True
            break
    if not found:
        print(f"Error: {i} is missing")
        anyMissing = True


if (anyMissing):
    # In case there are missing sprites
    print("Error: Missing sprites")
    exit()
else:
    print("All sprites are present")

# check the audio
if getattr(sys, 'frozen', False):  # Running as an .exe
    tempList = os.listdir(os.path.join(sys._MEIPASS, 'Sounds'))
else:  # Running as a .py script
    tempList = os.listdir('Sounds')
comparisonList = ["Chamber.wav", "Empty.wav", "game_music.wav", "Huntsman.wav", "Judge.wav", "lobby_music.wav", "Reload.wav", "selection_music.wav", "Sidewinder.wav", "Silencer.wav", "tank_dead.wav", "tank_moving.wav", "tank_shoot.wav", "tank_turret_rotate.wav", "Tempest.wav", "Watcher.wav"]
print("Checking audio files")
for i in comparisonList:
    found = False # Reset the found variable
    for j in tempList:
        if j == i:
            found = True
            break
    if not found:
        print(f"Error: {i} is missing")
        anyMissing = True

if (anyMissing):
    # In case there are missing sprites
    print("Error: Missing audio files")
    exit()
else:
    print("All audio files are present")

#Verification done
global timerClock
timerClock = 0
#init
pygame.init()


# setup font dictionary
if getattr(sys, 'frozen', False):  # Running as an .exe
    base_path = sys._MEIPASS
else:  # Running as a .py script
    base_path = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(base_path, 'fonts', 'LondrinaSolid-Regular.otf')

#Classes
class UpDownTimer():
    def __init__(self, duration = 0, up = True):
        self.duration = duration * 1e9 # duration in nano seconds
        self.startTime = time.time_ns()
        self.timer = self.startTime
        self.up = up
        self.expired = False
        self.paused = False
        self.pausedTime = 0

    def tick(self):
        if self.paused:
            return # exit early
        if self.isExpired():
            return # exit early
        # we are counting up
        if self.timer < self.duration + self.startTime:
            self.timer = time.time_ns()
        if self.timer >= self.duration + self.startTime:
            self.timer = self.duration + self.startTime
            self.expired = True
            
    def reset(self):
        self.timer = time.time_ns()
        self.startTime = time.time_ns()
        self.expired = False
        self.paused = False
    
    def setDirection(self, up):
        # up is True and down is False
        self.up = up
        self.startTime = time.time_ns()

    def setDuration(self, duration):
        # set the duration of the timer in seconds
        self.duration = duration * 1e9
        self.startTime = time.time_ns()

    def start(self):
        self.startTime = time.time_ns()
        self.timer = self.startTime if self.up else self.duration
        self.expired = False

    def pause(self):
        self.pausedTime = time.time_ns()
        self.paused = True

    def resume(self):
        self.paused = False
        cTime = time.time_ns()
        self.timer -= (cTime - self.pausedTime) # capture
        self.startTime += (cTime - self.pausedTime)

    def getElapsed(self):
        return self.timer - self.startTime if self.up else self.duration - self.timer + self.startTime

    def getElapsedAsSeconds(self):
        return self.getElapsed()/1e9

    def isExpired(self):
        return self.expired

    def getTime(self):
        return int(self.getElapsed()//1e9)

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

        if getattr(sys, 'frozen', False):  # Running as an .exe
            currentDir = sys._MEIPASS
        else:  # Running as a .py script
            currentDir = os.path.dirname(os.path.abspath(__file__))
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
        self.turretSpeed = 0.27
        self.drawable = False
        self.topTurretSpeed = self.turretSpeed
        self.gunH = 7
        self.imgScaler = 1.5
        self.channelListBusy = [False, False, False, False] # The channels that the sound effects will be played on
        self.channelDict = {} # The dictionary that will store the sound effects
        angleRad = math.radians(self.angle)
        gunEndX, gunEndY = self.tank.getGunCenter()
        self.rect = self.image.get_rect(center=(gunEndX + self.gunH * math.cos(angleRad), gunEndY - self.gunH * math.sin(angleRad)))
        self.AI = False
        self.hard = False
        self.default = False
        self.reload = False
        self.deltaTime = 0

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
        if self.AI:
            tank2x, tank2y = tank2.getCenter() # get the center
            
            c = self.tank.getCorners() # Our center

            tank1x, tank1y = (c[0][0] + c[1][0])//2, (c[0][1] + c[2][1])//2
            dx, dy = tank2x - tank1x, tank2y - tank1y
            a = math.degrees(math.atan2(dx, dy))//1
            a = (a + 360 - 90) % 360
            temp = 0
            if self.hard:
                # make it find the shortest path and store in self.angle
                if abs(a - self.angle) > 180:
                    temp = self.angle - a
                else:
                    temp = a - self.angle
                #limit the change to a max of 15 degrees
                if (temp>0):
                    temp = min(temp, 15)
                else:
                    temp = max(temp, -15)
            else:
                temp =self.tank.getAngle() - self.angle

            self.angle = (self.angle + temp)
            self.angle = round(self.angle)
            self.angle %= 360
            # Line of sight for the tank to shoot

            lowerlimit = ((self.angle + 5) + 360) % 360
            upperlimit = ((self.angle - 5) + 360) % 360

            if self.canShoot:
                if ((a <=lowerlimit and a >= upperlimit) or ((lowerlimit <= 5) and (upperlimit >= 355) and (a >= 355 or a <= 5))):
                    distance = math.hypot(dx, dy)
                    steps = int(distance)
                    for i in range(steps):
                        x = tank1x + (dx/distance) * i
                        y = tank1y + (dy/distance) * i
                        #check the tile it is in
                        row = math.ceil((y - const.MAZE_Y)/const.TILE_SIZE)
                        col = math.ceil((x - const.MAZE_X)/const.TILE_SIZE)
                        index = (row-1)*colAmount + col
                        tile = tileList[index-1]

                        if tile.border[0] and y - 1 <= tile.y:
                            break
                        if tile.border[1] and x + 1 >= tile.x + const.TILE_SIZE:
                            break
                        if tile.border[2] and y + 1 >= tile.y + const.TILE_SIZE:
                            break
                        if tile.border[3] and x - 1 <= tile.x:
                            break
                        if x <= const.MAZE_X or y <= const.MAZE_Y or x >= mazeWidth + const.MAZE_X or y >= mazeHeight + const.MAZE_Y:
                            break
                    if i == steps - 1:
                        self.fire()
                        # print("Boom")

        else:

            keys = pygame.key.get_pressed()
            #Checks what keys are pressed, and changes speed accordingly
            #If tank hull moves left or right, the gun will also move simultaneously
            #with the tank hull at the same speed and direction.
            self.rotationSpeed = 0
            if not self.default:
                if keys[self.controls['rotate_left']]:
                    self.rotationSpeed += self._getTurretSpeed() * self.deltaTime
                elif keys[self.controls['rotate_right']]:
                    self.rotationSpeed += -self._getTurretSpeed() * self.deltaTime  
                
                #This if statement checks to see if speed or rotation of speed is 0,
                #if so it will stop playing moving sound, otherwise, sound will play
                #indefinitely

                if self.rotationSpeed != 0: # This should be made so that it doesn't rotate if the hull is turning
                    if not self.channelDict["rotate"]["channel"].get_busy(): # if the sound isn't playing
                        self.channelDict["rotate"]["channel"].play(soundDictionary["turretRotate"], loops = -1)  # Play sound indefinitely
                else:
                    if self.channelDict["rotate"]["channel"].get_busy(): # if the sound is playing
                        self.channelDict["rotate"]["channel"].stop()  # Stop playing the sound

            if  keys[self.controls['left']]:
                self.rotationSpeed += self.tank.getRotationalSpeed() * self.deltaTime
            elif keys[self.controls['right']]:
                self.rotationSpeed += -self.tank.getRotationalSpeed() * self.deltaTime

            self.angle += self.rotationSpeed
            # self.angle = round(self.angle)
            self.angle %= 360

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
            self.tryReload()
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
        bullet.setDamage(self._getDamage())
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
    
    def _getDamage(self):
        return self.damage * (1.5 if (self.tank.effect[0] != 0) else 1)

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

    def setData(self, tank, controls, name, channel):
        # This function will set up the gun that is being used
        # Inputs: tank: The tank object that the gun is attached to
        #         controls: The controls that are being used to control the gun
        #         name: The name of the gun
        # Outputs: None
        self.tank = tank
        self.controls = controls
        self.name = name
        self.rect = self.gunImage.get_rect(center=(tank.rect.center))
        self.channelDict = channel
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

    def draw(self, screen):
        if self.tank.getInvincibility() > 0:
            # Draw the tank with a transparent effect
            self.image.set_alpha(31)
        else:
            self.image.set_alpha(255)
        # Draw the tank image
        screen.blit(self.image, self.rect)

    def setImage(self, name = 'gun', imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imagePath: The filepath the points to the required image
        # Outputs: None
        if getattr(sys, 'frozen', False):  # Running as an .exe
            currentDir = sys._MEIPASS
        else:  # Running as a .py script
            currentDir = os.path.dirname(os.path.abspath(__file__))
        gunPath = os.path.join(currentDir,'Sprites', str(name) + str(imageNum) + '.png')
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
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Empty"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Empty"])

    def setReload(self, b = False):
        self.reload = b

    def setAI(self, AI):
        self.AI = AI

    def setHard(self, hard = True):
        self.hard = hard

    def setDefault(self, default = True):
        self.default = default

    def tryReload(self):
        if self.reload == False or self.canShoot == True:
            return
        if not self.channelDict["reload"]["channel"].get_busy():
            self.channelDict["reload"]["channel"].play(soundDictionary["Reload"])

    def _getTurretSpeed(self):
        return self.tank.getRotationalSpeed() * (1.2 if (self.tank.effect[2] != 0) else 1)
    
    def setDelta(self, delta):
        self.deltaTime = delta

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
        if getattr(sys, 'frozen', False):  # Running as an .exe
            currentDir = sys._MEIPASS
        else:  # Running as a .py script
            currentDir = os.path.dirname(os.path.abspath(__file__))
            
        bulletPath = os.path.join(currentDir, './Assets/bullet.png')
        self.originalBulletImage = pygame.image.load(bulletPath).convert_alpha()
        self.bulletImage = self.originalBulletImage
        self.image = self.bulletImage
        self.angle = angle
        self.speed = 12
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
        self.deltaTime = 0

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
        # Calculate angle in radians
        angleRad = math.radians(self.angle)

        # Calculate the change in x and y
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)

        # Set the maximum step size
        max_step = 0.1

        # Track the progress along dx and dy
        remaining_dx = dx
        remaining_dy = dy
        # Continue while there's still distance to cover in either direction
        while abs(remaining_dx) > 0 or abs(remaining_dy) > 0:
            # Determine the step size, which should be limited to max_step
            step_dx = max(-max_step, min(max_step, remaining_dx))
            step_dy = max(-max_step, min(max_step, remaining_dy))
            # Update temp positions based on step size
            tempX = self.x + step_dx
            tempY = self.y + step_dy

            # Check if the bullet goes outside of the maze
            if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= mazeWidth + const.MAZE_X or tempY >= mazeHeight + const.MAZE_Y:
                self.kill()
                return
            
            # Recalculate row and column based on the smaller steps
            row = math.ceil((self.getCenter()[1] - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((self.getCenter()[0] - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * colAmount + col

            # Check for collisions with tanks
            tank1Collision = self.getCollision(tank1.getCorners(), (tempX, tempY))
            tank2Collision = self.getCollision(tank2.getCorners(), (tempX, tempY))

            if self.name == tank1.getName() and tank2Collision and tank2.getInvincibility() == 0:
                damage(tank2, self.damage)
                self.kill()
                return
            if self.name == tank2.getName() and tank1Collision and tank1.getInvincibility() == 0:
                damage(tank1, self.damage)
                self.kill()
                return
            # Checking for self damage
            if self.bounce != self.originalBounce:
                self.selfCollision = True

            if self.selfCollision:
                if tank1Collision and tank1.getInvincibility()==0:
                    damage(tank1, self.damage)
                    self.kill()
                    return
                if tank2Collision and tank2.getInvincibility()==0:
                    damage(tank2, self.damage)
                    self.kill()
                    return

            # Handle wall collision
            tile = tileList[index-1]
            wallCollision = False
            if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y: # Top border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + const.TILE_SIZE: # Right border
                wallCollision = True
                self.angle = 360 - self.angle
            if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + const.TILE_SIZE: # Bottom border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x: # Left border
                wallCollision = True
                self.angle = 360 - self.angle
            if wallCollision:
                self.bounce -= 1
                self.speed *= -1
                if self.bounce == 0:
                    self.kill()
                return
            # After checking, update the current position
            self.x = tempX
            self.y = tempY

            # Subtract the amount we moved this step from the remaining distance
            remaining_dx -= step_dx
            remaining_dy -= step_dy

        # Once done with the loop, update the bullet's position and state
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
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
            offset = 5
            tX, tY = self.trailX, self.trailY
            if abs(self.trailX - self.x) < offset:
                tY += offset
            if abs(self.trailY - self.y) < offset:
                tX += offset
            pygame.draw.line(screen, c.geT("NEON_PURPLE"), (tX, tY), (self.x, self.y), 10)
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
    
    def setDelta(self, delta):
        self.deltaTime = delta

    def getCollision(self, corners, point):
        # return point[0] >= corners[0][0] and point[0] <= corners[1][0] and point[1] >= corners[0][1] and point[1] <= corners[1][1]
        x,y = point
        inside = False
        for i in range(len(corners)):
            x1, y1 = corners[i]
            x2, y2 = corners[(i+1) % len(corners)]
            if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
                inside = not inside
        return inside

class SidewinderBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.setBounce(5)

class JudgeBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.setBounce(2)

class SilencerBullet(Bullet):

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.speed = 0.13
    
    def update(self):
        """
        Updates the bullet's position using ray tracing for precise collision detection.
        """
        # Convert angle to radians
        angleRad = math.radians(self.angle)

        # Calculate total movement in x and y
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)

        # Store initial position
        start_x, start_y = self.x, self.y

        # Track the path along the ray pixel by pixel
        steps = int(math.hypot(dx, dy))  # Number of pixels to check
        for i in range(steps + 1):  # Include the endpoint
            tempX = start_x + (dx * (i / steps))
            tempY = start_y + (dy * (i / steps))

            # Check if the bullet goes outside of the maze
            if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= mazeWidth + const.MAZE_X or tempY >= mazeHeight + const.MAZE_Y:
                self.kill()
                return

            # Determine current tile based on precise position
            row = math.ceil((tempY - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((tempX - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * colAmount + col

            # Checking for self-damage
            if self.bounce != self.originalBounce:
                self.selfCollision = True

            # Handle wall collision
            tile = tileList[index - 1]
            wallCollision = False

            # Check borders (ray-traced collision detection)
            if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y:  # Top border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + const.TILE_SIZE:  # Right border
                wallCollision = True
                self.angle = 360 - self.angle
            if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + const.TILE_SIZE:  # Bottom border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x:  # Left border
                wallCollision = True
                self.angle = 360 - self.angle

            if wallCollision:
                self.bounce -= 1
                if self.bounce == 0:
                    self.kill()
                    return
                # Stop at collision point
                break

        # Update bullet position to the last valid point before collision
        self.x, self.y = tempX, tempY

        # Update bullet state
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.pleaseDraw = True

class WatcherBullet(Bullet):

    trailColor = (255, 0, 0)

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.speed = 0.2

    def update(self):
        """
        Updates the bullet's position using ray-tracing for precise collision detection with walls and tanks.

        This method calculates the new position of the bullet, handles collisions with tanks and walls,
        and updates the bullet's state accordingly.
        """

        # Convert angle to radians for movement calculation
        angle_rad = math.radians(self.angle)

        # Calculate movement in x and y directions
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)

        # Determine the number of steps for fine-grained movement (ray tracing)
        steps = int(max(abs(dx), abs(dy)) * 10)  # Increase for more precision
        for step in range(steps + 1):
            temp_x = self.x + (dx * step / steps)
            temp_y = self.y + (dy * step / steps)

            # Check if the bullet goes outside the maze boundaries
            if temp_x <= const.MAZE_X or temp_y <= const.MAZE_Y or temp_x >= mazeWidth + const.MAZE_X or temp_y >= mazeHeight + const.MAZE_Y:
                self.kill()
                return

            # Determine the current tile based on bullet position
            row = math.ceil((temp_y - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((temp_x - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * colAmount + col

            # Check for collisions with tanks

            tank1_collision = (self.getCollision(tank1.getCorners(), (temp_x, temp_y)))
            tank2_collision = (self.getCollision(tank2.getCorners(), (temp_x, temp_y)))

            if self.name == tank1.getName() and tank2_collision and tank2.getInvincibility() == 0:
                damage(tank2, self.damage)
                self.kill()
                return
            if self.name == tank2.getName() and tank1_collision and tank1.getInvincibility() == 0:
                damage(tank1, self.damage)
                self.kill()
                return

            if self.bounce != self.originalBounce:
                self.selfCollision = True

            if self.selfCollision:
                if tank1_collision:
                    damage(tank1, self.damage)
                    self.kill()
                    return
                if tank2_collision:
                    damage(tank2, self.damage)
                    self.kill()
                    return

            # Handle wall collisions and bouncing
            tile = tileList[index - 1]
            bullet_size = self.image.get_size()[1]
            wall_collision = False

            # Check each wall (Top, Right, Bottom, Left)
            if tile.border[0] and temp_y - bullet_size <= tile.y:  # Top wall
                wall_collision = True
                self.angle = 180 - self.angle
            if tile.border[1] and temp_x + bullet_size >= tile.x + const.TILE_SIZE:  # Right wall
                wall_collision = True
                self.angle = 360 - self.angle
            if tile.border[2] and temp_y + bullet_size >= tile.y + const.TILE_SIZE:  # Bottom wall
                wall_collision = True
                self.angle = 180 - self.angle
            if tile.border[3] and temp_x - bullet_size <= tile.x:  # Left wall
                wall_collision = True
                self.angle = 360 - self.angle

            if wall_collision:
                self.bounce -= 1
                if self.bounce == 0:
                    self.kill()
                    return
            

        # After all steps, update the bullet's final position
        self.x = temp_x
        self.y = temp_y
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

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

    splash = True

    def __init__(self, x, y, angle, gunLength, tipOffSet):
        super().__init__(x, y, angle, gunLength, tipOffSet)
        self.speed = 0.5
        self.drawable = True

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
        # Calculate angle in radians
        angleRad = math.radians(self.angle)

        # Calculate the change in x and y
        dx = self.speed * math.cos(angleRad)
        dy = -self.speed * math.sin(angleRad)

        # Set the maximum step size
        max_step = 0.1

        # Track the progress along dx and dy
        remaining_dx = dx
        remaining_dy = dy
        # Continue while there's still distance to cover in either direction
        while abs(remaining_dx) > 0 or abs(remaining_dy) > 0:
            # Determine the step size, which should be limited to max_step
            step_dx = max(-max_step, min(max_step, remaining_dx))
            step_dy = max(-max_step, min(max_step, remaining_dy))
            # Update temp positions based on step size
            tempX = self.x + step_dx
            tempY = self.y + step_dy

            # Check if the bullet goes outside of the maze
            if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= mazeWidth + const.MAZE_X or tempY >= mazeHeight + const.MAZE_Y:
                self.explode()
                return
            
            # Recalculate row and column based on the smaller steps
            row = math.ceil((self.getCenter()[1] - const.MAZE_Y) / const.TILE_SIZE)
            col = math.ceil((self.getCenter()[0] - const.MAZE_X) / const.TILE_SIZE)
            index = (row - 1) * colAmount + col

            # use the old collision
            tank1Collision = pygame.sprite.collide_rect(self, tank1)
            tank2Collision = pygame.sprite.collide_rect(self, tank2)
            
            if self.name == tank1.getName() and tank2Collision and tank2.getInvincibility() == 0:
                damage(tank2, self.damage)
                self.explode()
                return
            if self.name == tank2.getName() and tank1Collision and tank1.getInvincibility() == 0:
                damage(tank1, self.damage)
                self.explode()
                return

            if self.selfCollision:
                if tank1Collision and tank1.getInvincibility() == 0:
                    damage(tank1, self.damage)
                    self.explode()
                    return
                if tank2Collision and tank2.getInvincibility() == 0:
                    damage(tank2, self.damage)
                    self.explode()
                    return

            # Checking for self damage
            if self.bounce != self.originalBounce:
                self.selfCollision = True

            # Handle wall collision
            tile = tileList[index-1]
            wallCollision = False
            if tile.border[0] and tempY - self.image.get_size()[1] <= tile.y: # Top border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[1] and tempX + self.image.get_size()[1] >= tile.x + const.TILE_SIZE: # Right border
                wallCollision = True
                self.angle = 360 - self.angle
            if tile.border[2] and tempY + self.image.get_size()[1] >= tile.y + const.TILE_SIZE: # Bottom border
                wallCollision = True
                self.angle = 180 - self.angle
            if tile.border[3] and tempX - self.image.get_size()[1] <= tile.x: # Left border
                wallCollision = True
                self.angle = 360 - self.angle
            if wallCollision:
                if self.name == tank1.getName() and tank1Collision and tank1.getInvincibility() == 0:
                    damage(tank1, self.damage)
                    self.explode()
                    return
                if self.name == tank2.getName() and tank2Collision and tank2.getInvincibility() == 0:
                    damage(tank2, self.damage)
                    self.explode()
                    return
                self.bounce -= 1
                self.speed *= -1
                if self.bounce == 0:
                    self.explode()
                    return

            # After checking, update the current position
            self.x = tempX
            self.y = tempY

            # Subtract the amount we moved this step from the remaining distance
            remaining_dx -= step_dx
            remaining_dy -= step_dy

        # Once done with the loop, update the bullet's position and state
        self.updateCorners()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
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
            splash1.setBulletSpeed(0.1)
            splash1.update()
            splash1.kill()
            # Outer radius
            splash2 = ChamberBullet(self.x, self.y, 0, 0, 0)
            splash2.sizeImage(20)
            splash2.updateCorners()
            splash2.setSplash(False)
            splash2.setDamage(self.damage)
            splash2.setName(self.name)
            splash2.setBulletSpeed(0.1)
            splash2.update()
            splash2.kill()
        self.kill()

    def draw(self,screen):
        # This function will only draw if the bullet is a splash and not a radius
        # Inputs: screen: The screen that the bullet will be drawn on
        # Outputs: None
        if self.splash:
            screen.blit(self.image, self.rect)

class Tile(pygame.sprite.Sprite):
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
        self.AITarget = False
        self.supply = None
        self.timer = 8372 # Roughly one minute?
        self.supplyTimer = self.timer # This is the timer for the supply
        self.picked = False
        self.supplyIndex = None # The index of the supply that is on the tile

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
        
        # if tank1 or tank 2 is within the tile, then we want to grant the effect
        if self.supply is not None and not self.picked:
            if self.isWithin(tank1.getCenter()):
                if self.supplyIndex == 0:
                    tank1.applyDoubleDamage()
                elif self.supplyIndex == 1:
                    tank1.applyDoubleArmor()
                elif self.supplyIndex == 2:
                    tank1.applySpeedBoost()
                self.picked = True
                self.supplyTimer = self.timer
            if self.isWithin(tank2.getCenter()):
                if self.supplyIndex == 0:
                    tank2.applyDoubleDamage()
                elif self.supplyIndex == 1:
                    tank2.applyDoubleArmor()
                elif self.supplyIndex == 2:
                    tank2.applySpeedBoost()
                self.picked = True
                self.supplyTimer = self.timer

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
                border[i] = random.choices([True, False], weights = (weightTrue, 1-weightTrue))[0]

        return border

    def drawText(self, screen):
        # access the "tileFont" key from the dictionary
        text = const.FONT_DICTIONARY["tileFont"].render(str(self.index), True, c.geT("BLACK"))
        screen.blit(text, [self.x + const.TILE_SIZE/2 - text.get_width()/2, self.y + const.TILE_SIZE/2 - text.get_height()/2])

    def draw(self, screen):
        # if self.AITarget:
        #     screen.blit(self.debug, self.rect)
        # else:
        #     screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect)

        if self.supply is not None:
            # draw the supply icon
            if self.picked:
                screen.blit(self.supply[0], (self.x + const.TILE_SIZE//2 - self.supply[0].get_width()//2, self.y + const.TILE_SIZE//2 - self.supply[0].get_height()//2))
            else:
                screen.blit(self.supply[1], (self.x + const.TILE_SIZE//2 - self.supply[1].get_width()//2, self.y + const.TILE_SIZE//2 - self.supply[1].get_height()//2))
        # self.drawText(screen)
    
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

    def printDebug(self):
        print("Index: ", self.index, end = " ")
        print(self.index%14, self.index//14)
        print("Neighbours: ", self.neighbours, end = " ")
        print("Bordering: ", self.bordering)

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
    credit = 5
    info = 6

class DifficultyType(Enum):
    # format is <Number> <Respawn> <AI>
    NotInGame = (0, False, False)
    OnePlayerYard = (1, False, True)
    OnePlayerScrapYard = (2, False, True)
    TwoPlayerYard = (3, False, False)
    TwoPlayerScrapYard = (4, False, False)
    OnePlayerBrawl = (5, True, True)
    OnePlayerDeathMatch = (6, True, True)
    TwoPlayerBrawl = (7, True, False)
    TwoPlayerDeathMatch = (8, True, False)

    def __init__(self, number, respawn, ai):
        self._value_ = number
        self.respawn = respawn
        self.ai = ai

    @classmethod
    def from_index(cls, index):
        for mode in cls:
            if mode.value == index:
                return mode
        raise ValueError(f"No GameMode with index {index}")

#Turrets

class Chamber(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(1500) # 200 ms
        self.setDamage(247) # Should be 900 but because of the 3 step effect it will be split into 3x 300
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setGunBackDuration(500)
        self.setGunCenter(0, -4)
        self.setReload(True)

    def fire(self):
        # This function is responsible for all the firing mechanics of the gun
        # The Bullet is custom here as it is tailored for the Chamber
        # Inputs: None
        # Outputs: None

        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = ChamberBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(10)
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        #If either tank shoots, play this sound effect.
        self.playSFX()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Chamber"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Chamber"])

class DefaultGun(Gun):
    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(400) # 500 ms
        self.setDamage(1) # 10000
        self.setDefault(True)

    def fire(self):
        # This function completely handles the bullet generation when firing a bullet
        # Inputs: None
        # Outputs: None

        # Calculating where the bullet should spawn
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setDamage(self._getDamage())
        bullet.setBounce(5)
        bullet.setName(self.getTank().getName())
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

class Huntsman(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(1000) # 1000 ms
        self.setDamage(600)
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setGunBackDuration(300)
        self.setReload(True)

    def fire(self):
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        if random.random() <= 0.4:  # 40% chance
            bullet.setDamage(self._getDamage() * 2)
        else:
            bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(15)
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Huntsman"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Huntsman"])

class Judge(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(800)  # 800 ms
        self.setDamage(80)
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setGunBackDuration(300)
        self.setTipOffset(28)
        self.bulletInterval = 15
        self.maxUses = 3
        self.currentUses = self.maxUses
        self.reloadTime = 2  # 2 seconds
        self.setGunCenter(0, -3)
        self.setReload(True)
        
    def fire(self):
        if self.currentUses != 0:
            self.canShoot = False
            self.currentUses -= 1
            if (self.currentUses): # if there are still uses left
                self.shootCooldown = self.cooldownDuration
            else:
                self.shootCooldown = self.cooldownDuration * 3
                self.currentUses = self.maxUses

            # <!Optimize>
            for _ in range(20): # 20 bullets
                self.fireBullet()

            self.playSFX()

    def fireBullet(self):
        scatterAngle = random.uniform(-7.5, 7.5) # cone of 10 degrees
        bulletAngle = self.angle + scatterAngle
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = JudgeBullet(bulletX + random.uniform(-3, 3), bulletY + random.uniform(-3, 3), bulletAngle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(8)
        bulletSprites.add(bullet)

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Judge"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Judge"])

    def getReloadPercentage(self):
        # The bar has 3 segments, each segment is 1/3 of the reload time
        # cooldownDuration = 800 ms
        if self.currentUses == self.maxUses:
            temp = self.shootCooldown / (self.cooldownDuration * self.maxUses)
        else:
            temp = 1 - (self.currentUses % self.maxUses + self.shootCooldown / self.cooldownDuration) / self.maxUses
        return temp

class Sidewinder(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(500)  # 500 ms
        self.setDamage(300)
        self.setDamageStatistic(1)
        self.setReloadStatistic(2)
        self.setGunBackDuration(300)
        self.setGunCenter(0, 1)
        
    def fire(self):
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = SidewinderBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setName(self.getTank().getName())
        bullet.setBulletSpeed(10)
        bullet.setDamage(self._getDamage())
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Sidewinder"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Sidewinder"])

class Silencer(Gun):

    wind_up = 1200
    delay = True
    lastRegister = 0
    sound = True
    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(2400) #2400 ms
        self.setDamage(1300)
        self.setDamageStatistic(3)
        self.setReloadStatistic(1)
        self.drawable = True
        self.setGunCenter(0, -3)
        self.setReload(True)
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
        self.rotationSpeed = 0
        
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed += self._getTurretSpeed() * self.deltaTime
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed += -self._getTurretSpeed() * self.deltaTime
      
        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if self.rotationSpeed != 0:
            if not self.channelDict["rotate"]["channel"].get_busy(): # if the sound isn't playing
                self.channelDict["rotate"]["channel"].play(soundDictionary["turretRotate"], loops = -1)  # Play sound indefinitely
        else:
            if self.channelDict["rotate"]["channel"].get_busy(): # if the sound is playing
                self.channelDict["rotate"]["channel"].stop()  # Stop playing the sound

        if  keys[self.controls['left']]:
            self.rotationSpeed += self.tank.getRotationalSpeed() * self.deltaTime
        elif keys[self.controls['right']]:
            self.rotationSpeed += -self.tank.getRotationalSpeed() * self.deltaTime

        self.angle += self.rotationSpeed
        self.angle = round(self.angle)
        self.angle %= 360

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
            self.tryReload()
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
        bullet.setBulletSpeed(50)
        bullet.setName(self.getTank().getName())
        bullet.drawable = True
        bullet.trail = True
        bulletSprites.add(bullet)
        # Real bullet
        bullet1 = WatcherBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet1.setDamage(self._getDamage())
        bullet1.setBulletSpeed(50)
        bullet1.setName(self.getTank().getName())
        bullet1.drawable = True
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

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Silencer"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Silencer"])

class Tempest(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(200) # 200 ms
        self.setDamage(150)
        self.setDamageStatistic(1)
        self.setReloadStatistic(3)
        self.setGunBackDuration(50)
        self.setGunCenter(0, -2)

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Tempest"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Tempest"])

class Watcher(Gun):

    scoping = False
    scopeDamage = 700
    scopeStartTime = 0
    speed = 0.1

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(1500) #1500 ms
        self.setDamage(3000)
        self.setDamageStatistic(2)
        self.setReloadStatistic(2)
        self.setTipOffset(25)
        self.drawable = True
        self.setGunCenter(0, -3)
        self.setReload(True)

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
        self.rotationSpeed = 0

        if keys[self.controls['rotate_left']]:
            self.rotationSpeed += self._getTurretSpeed() * self.deltaTime
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed += -self._getTurretSpeed() * self.deltaTime
        
        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if self.rotationSpeed != 0:
            if not self.channelDict["rotate"]["channel"].get_busy(): # if the sound isn't playing
                self.channelDict["rotate"]["channel"].play(soundDictionary["turretRotate"], loops = -1)  # Play sound indefinitely
        else:
            if self.channelDict["rotate"]["channel"].get_busy(): # if the sound is playing
                self.channelDict["rotate"]["channel"].stop()  # Stop playing the sound
        
        if  keys[self.controls['left']]:
            self.rotationSpeed += self.tank.getRotationalSpeed() * self.deltaTime
        elif keys[self.controls['right']]:
            self.rotationSpeed += -self.tank.getRotationalSpeed() * self.deltaTime
    
        self.angle += self.rotationSpeed
        #Reload cooldown of bullet and determines the angle to fire the bullet,
        #which is relative to the posistion of the tank gun.
        if keys[self.controls['fire']] and self.canShoot:
            self.scoping = True
            self.scopeStartTime = pygame.time.get_ticks()

        if self.scoping:
            self.setTurretSpeed(self.getTurretSpeed()/20)
            self.getTank().setSpeed(self.getTank().getSpeed()/2)
            self.getTank().setRotationalSpeed(self.getTank().getTopRotationalSpeed()/10)
            #Scale the damage of the bullet
            self.scopeDamage += 60
            if self.scopeDamage >= self.damage: # Max damage
                self.scopeDamage = self.damage

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
            self.tryReload()
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

    def fire(self):
        # This function is responsible for all the firing mechanics of the gun
        # The Bullet is custom here as it is tailored for the Watcher
        # Inputs: None
        # Outputs: None
        # Setup bullet
        bulletX, bulletY = self.getTank().getGunCenter()
        bullet = WatcherBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet)
        bullet.setDamage(self.getDamage())
        bullet.setBulletSpeed(50)
        bullet.setName(self.getTank().getName())
        bullet.drawable = True
        bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.scopeDamage = 350 # Reset the damage
        self.playSFX()

    def getDamage(self):
        return self.scopeDamage * (self._getDamage() / self.damage) # reverting any change made

    def customDraw(self, _):

        def getColor():
            # This function will return the color of the bullet based on the damage
            # Inputs: None
            # Outputs: The color of the bullet
            if self.scopeDamage >= self.damage:
                return c.geT("GREEN")
            else:
                return c.geT("RED")

        #This function will draw the gun on the tank
        # Inputs: None
        # Outputs: None
        if self.scoping:
            #Draw a line that is dotted which ends when it collides with something
            #The line will be drawn from the gun to the end of the screen
            #find the location of the nearest obstacle
            found = False
            currentX = self.getTank().getGunCenter()[0]
            currentY = self.getTank().getGunCenter()[1]
            step_dx, step_dy = math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle))
            tempX, tempY = currentX, currentY
            while not found:
                # Determine the step size, which should be limited to max_step
                # Update temp positions based on step size
                tempX += step_dx
                tempY += step_dy

                # Check if the bullet goes outside of the maze
                if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= mazeWidth + const.MAZE_X or tempY >= mazeHeight + const.MAZE_Y:
                    found = True
                    break
                # Recalculate row and column based on the smaller steps
                row = math.ceil((tempY - const.MAZE_Y) / const.TILE_SIZE)
                col = math.ceil((tempX - const.MAZE_X) / const.TILE_SIZE)
                index = (row - 1) * colAmount + col

                # Handle wall collision
                if (index < 0) or (index >= len(tileList)):
                    found = True
                    break
                tile = tileList[index-1]
                wallCollision = False
                if tile.border[0] and tempY - 1 <= tile.y: # Top border
                    wallCollision = True
                if tile.border[1] and tempX + 1 >= tile.x + const.TILE_SIZE: # Right border
                    wallCollision = True
                if tile.border[2] and tempY + 1 >= tile.y + const.TILE_SIZE: # Bottom border
                    wallCollision = True
                if tile.border[3] and tempX - 1 <= tile.x: # Left border
                    wallCollision = True
                if wallCollision:
                    found = True
                    break
            SPACING = 25
            count = int(math.sqrt((tempX - currentX)**2 + (tempY - currentY)**2) / SPACING)
            #tempX and tempY are our "going to" location
            while count != 0:
                currentX += step_dx * SPACING
                currentY += step_dy * SPACING
                pygame.draw.circle(screen, getColor(), (int(currentX), int(currentY)), 1)
                count -= 1

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(soundDictionary["Watcher"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["Watcher"])

#Functions
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

def spareChannels(sound):
    soundList = [pygame.mixer.Channel(i) for i in range(15, pygame.mixer.get_num_channels())]
    for channel in soundList:
        if not channel.get_busy():
            channel.play(sound) # attempt to play the sound
            return
    print("No available channels")
    return

def tileGen():
    # This function is responsible for generating the tiles for the maze
    # Inputs: No inputs
    # Outputs: A list of tiles that make up the maze
    #

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
        for j in range(const.MAZE_Y, mazeHeight + 1, const.TILE_SIZE): # Assign the tiles and spawns once everything is found
            for i in range(const.MAZE_X, mazeWidth + 1, const.TILE_SIZE):
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
    # supplies

    if getattr(sys, 'frozen', False):  # Running as an .exe
        currentDir = sys._MEIPASS
    else:  # Running as a .py script
        currentDir = os.path.dirname(os.path.abspath(__file__))

    tileList[98].setSupply([os.path.join(currentDir, 'Assets', 'Armor_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Armor_Floor.png')], 1)
    tileList[74].setSupply([os.path.join(currentDir, 'Assets', 'Damage_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Damage_Floor.png')], 0)
    tileList[105].setSupply([os.path.join(currentDir, 'Assets', 'Speed_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Speed_Floor.png')], 2)

    tileList[95].setSupply([os.path.join(currentDir, 'Assets', 'Armor_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Armor_Floor.png')], 1)
    tileList[54].setSupply([os.path.join(currentDir, 'Assets', 'Damage_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Damage_Floor.png')], 0)
    tileList[10].setSupply([os.path.join(currentDir, 'Assets', 'Speed_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Speed_Floor.png')], 2)

    tileList[2].setSupply([os.path.join(currentDir, 'Assets', 'Armor_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Armor_Floor.png')], 1)
    tileList[33].setSupply([os.path.join(currentDir, 'Assets', 'Damage_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Damage_Floor.png')], 0)
    tileList[42].setSupply([os.path.join(currentDir, 'Assets', 'Speed_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Speed_Floor.png')], 2)

    return tileList

def setUpTank1(dType = 0):
    global tileList, spawnpoint, tank1, gun1, allSprites, bulletSprites
    global p1I, p1J, p1K, p1L, spawnTank1
    global player1PackageTank, player1PackageGun
    global player1Channels, p1TankName, p1GunName, DifficultyType

    match dType:
        case DifficultyType.OnePlayerYard:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Simple Tanks
            tank1 = DefaultTank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
            tank1.setAI(True, currentTargetPackage)
            tank1.setData(player1PackageTank)
            tank1.setImage('tank', p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]

            gun1 = DefaultGun(tank1, controlsTank1, p1GunName) # Gun 1 setup
            gun1.setAI(True)
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage('gun', p1K + 1)
        
        case DifficultyType.OnePlayerScrapYard:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank1 = copy.copy(hullList[p1J]) # Tank 1 setup
            tank1.setAI(True, currentTargetPackage)
            tank1.setData(player1PackageTank)
            tank1.setImage(hullList[p1J].getName(), p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]
            
            #Because silencer and watcher aren't made yet, skip them
            if p1I == 1 or p1I == 2:
                print("Skipping Silencer or Watcher, selecting Chamber")
                gun1 = copy.copy(turretList[3]) # Gun 1 setup
            else:
                gun1 = copy.copy(turretList[p1I]) # Gun 1 setup
            gun1.setAI(True)
            gun1.setHard()
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage(turretList[p1I].getGunName(), p1K + 1)

        case DifficultyType.TwoPlayerYard:
            # Scrapyard, Player vs Player Simple Tanks
            tank1 = DefaultTank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
            tank1.setData(player1PackageTank)
            tank1.setImage('tank', p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]

            gun1 = DefaultGun(tank1, controlsTank1, p1GunName) # Gun 1 setup
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage('gun', p1K + 1)

        case DifficultyType.TwoPlayerScrapYard:
            # Scrapyard, Player vs Player Normal Tanks
            tank1 = copy.copy(hullList[p1J]) # Tank 1 setup
            tank1.setData(player1PackageTank)
            tank1.setImage(hullList[p1J].getName(), p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]

            gun1 = copy.copy(turretList[p1I]) # Gun 1 setup
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage(turretList[p1I].getGunName(), p1K + 1)

        case DifficultyType.OnePlayerBrawl:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Simple Tanks
            tank1 = DefaultTank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
            tank1.setAI(True, currentTargetPackage)
            tank1.setData(player1PackageTank)
            tank1.setImage('tank', p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]

            gun1 = DefaultGun(tank1, controlsTank1, p1GunName) # Gun 1 setup
            gun1.setAI(True)
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage('gun', p1K + 1)
        
        case DifficultyType.OnePlayerDeathMatch:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank1 = copy.copy(hullList[p1J]) # Tank 1 setup
            tank1.setAI(True, currentTargetPackage)
            tank1.setData(player1PackageTank)
            tank1.setImage(hullList[p1J].getName(), p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]
            
            #Because silencer and watcher aren't made yet, skip them
            if p1I == 1 or p1I == 2:
                print("Skipping Silencer or Watcher, selecting Chamber")
                gun1 = copy.copy(turretList[3]) # Gun 1 setup
            else:
                gun1 = copy.copy(turretList[p1I]) # Gun 1 setup
            gun1.setAI(True)
            gun1.setHard()
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage(turretList[p1I].getGunName(), p1K + 1)

        case DifficultyType.TwoPlayerBrawl:
            # Scrapyard, Player vs Player Simple Tanks
            tank1 = DefaultTank(spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName)
            tank1.setData(player1PackageTank)
            tank1.setImage('tank', p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]

            gun1 = DefaultGun(tank1, controlsTank1, p1GunName) # Gun 1 setup
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage('gun', p1K + 1)

        case DifficultyType.TwoPlayerDeathMatch:
            # Scrapyard, Player vs Player Normal Tanks
            tank1 = copy.copy(hullList[p1J]) # Tank 1 setup
            tank1.setData(player1PackageTank)
            tank1.setImage(hullList[p1J].getName(), p1L + 1)
            tank1.setSoundDictionary(soundDictionary)
            tank1.settileList(tileList)
            tank1.effect = [0,0,0]

            gun1 = copy.copy(turretList[p1I]) # Gun 1 setup
            gun1.setData(tank1, player1PackageGun[0], player1PackageGun[1], player1Channels)
            gun1.setImage(turretList[p1I].getGunName(), p1K + 1)

def setUpTank2(dType = 0):
    global tileList, spawnpoint, tank2, gun2, allSprites, bulletSprites
    global p2I, p2J, p2K, p2L, spawnTank2, DifficultyType
    global player2PackageTank, player2PackageGun
    global player2Channels, p2TankName, p2GunName


    match dType:
        case DifficultyType.OnePlayerYard:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Simple Tanks
            tank2 = DefaultTank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage('tank', p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = DefaultGun(tank2, controlsTank2, p2GunName) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage('gun', p2K + 1)

        case DifficultyType.OnePlayerScrapYard:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks

            tank2 = copy.copy(hullList[p2J]) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage(hullList[p2J].getName(), p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = copy.copy(turretList[p2I]) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage(turretList[p2I].getGunName(), p2K + 1)

        case DifficultyType.TwoPlayerYard:
            # Scrapyard, Player vs Player Simple Tanks
            tank2 = DefaultTank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage('tank', p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = DefaultGun(tank2, controlsTank2, p2GunName) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage('gun', p2K + 1)

        case DifficultyType.TwoPlayerScrapYard:
            # Scrapyard, Player vs Player Normal Tanks
            tank2 = copy.copy(hullList[p2J]) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage(hullList[p2J].getName(), p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = copy.copy(turretList[p2I]) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage(turretList[p2I].getGunName(), p2K + 1)

        case DifficultyType.OnePlayerBrawl:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Simple Tanks
            tank2 = DefaultTank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage('tank', p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = DefaultGun(tank2, controlsTank2, p2GunName) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage('gun', p2K + 1)

        case DifficultyType.OnePlayerDeathMatch:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks

            tank2 = copy.copy(hullList[p2J]) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage(hullList[p2J].getName(), p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = copy.copy(turretList[p2I]) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage(turretList[p2I].getGunName(), p2K + 1)

        case DifficultyType.TwoPlayerBrawl:
            # Scrapyard, Player vs Player Simple Tanks
            tank2 = DefaultTank(spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage('tank', p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = DefaultGun(tank2, controlsTank2, p2GunName) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage('gun', p2K + 1)

        case DifficultyType.TwoPlayerDeathMatch:
            # Scrapyard, Player vs Player Normal Tanks
            tank2 = copy.copy(hullList[p2J]) # Tank 2 setup
            tank2.setData(player2PackageTank)
            tank2.setImage(hullList[p2J].getName(), p2L + 1)
            tank2.setSoundDictionary(soundDictionary)
            tank2.settileList(tileList)
            tank2.effect = [0,0,0]

            gun2 = copy.copy(turretList[p2I]) # Gun 2 setup
            gun2.setData(tank2, player2PackageGun[0], player2PackageGun[1], player2Channels)
            gun2.setImage(turretList[p2I].getGunName(), p2K + 1)

def setUpPlayers():
    # This function sets up the players for the game including reseting the respective global veriables
    #This function has no real dependencies on things outside of its control
    # Inputs: None
    # Outputs: None
    global tileList, spawnpoint, tank1, tank2, gun1, gun2, allSprites, bulletSprites
    global p1I, p1J, p2I, p2J, p1K, p2K, p1L, p2L, difficultyType, DifficultyType, spawnTank1, spawnTank2
    global player1PackageTank, player1PackageGun, player2PackageTank, player2PackageGun
    global player1Channels, player2Channels, p1TankName, p2TankName, p1GunName, p2GunName
    tileList = tileGen() # Get a new board
    spawnTank1 = [tileList[spawnpoint[0]-1].x + const.TILE_SIZE//2, tileList[spawnpoint[0]-1].y + const.TILE_SIZE//2]
    spawnTank2 = [tileList[spawnpoint[1]-1].x + const.TILE_SIZE//2, tileList[spawnpoint[1]-1].y + const.TILE_SIZE//2]
    player1Channels = {"move": {"channel": pygame.mixer.Channel(3), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(4), "volume": 0.2}, "death": {"channel" : pygame.mixer.Channel(5), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(6), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(7), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(8), "volume": 0.5}}
    player2Channels = {"move": {"channel": pygame.mixer.Channel(9), "volume": 0.05}, "rotate": {"channel": pygame.mixer.Channel(10), "volume": 0.3}, "death": {"channel" : pygame.mixer.Channel(11), "volume": 0.5}, "fire": {"channel": pygame.mixer.Channel(12), "volume": 1}, "hit": {"channel": pygame.mixer.Channel(13), "volume": 1}, "reload": {"channel": pygame.mixer.Channel(14), "volume": 0.5}}
    #Updating the packages
    player1PackageTank = [spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName, player1Channels]
    player1PackageGun = [controlsTank1, p1GunName, player1Channels]
    player2PackageTank = [spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName, player2Channels]
    player2PackageGun = [controlsTank2, p2GunName, player2Channels]
    # setup the tanks and guns
    setUpTank1(difficultyType)
    setUpTank2(difficultyType)


    # setup the tanks
    match difficultyType:
        case DifficultyType.OnePlayerYard:
            # # easy AI, 1 Player
            temp = tank2.getCurrentTile().getIndex()
            tank1.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))
            # scrapyard
            timer.setDirection(True)
        case DifficultyType.OnePlayerScrapYard:
            temp = tank2.getCurrentTile().getIndex()
            tank1.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))
            # scrapyard
            timer.setDirection(True)
        case DifficultyType.TwoPlayerYard:
            timer.setDirection(True)
        case DifficultyType.TwoPlayerScrapYard:
            timer.setDirection(True)
        case DifficultyType.OnePlayerBrawl:
            temp = tank2.getCurrentTile().getIndex()
            tank1.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.OnePlayerDeathMatch:
            temp = tank2.getCurrentTile().getIndex()
            tank1.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.TwoPlayerBrawl:
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.TwoPlayerDeathMatch:
            timer.setDirection(False)
            timer.setDuration(301)
        case _:
            print("Unknown state")
            return
    #Updating the groups
    
    for sprite in allSprites:
        sprite.kill()
    allSprites = pygame.sprite.Group() # Wipe the current Sprite Group   

    allSprites.add(tank1, gun1, tank2, gun2) # Add the new sprites
    for bullet in bulletSprites:
        bullet.kill()
    bulletSprites = pygame.sprite.Group()
    timer.reset() # Reset the timer

def constantHomeScreen():
    #This funciton handles the constant elements of the home screen
    # Inputs: None
    # Outputs: None
    screen.fill(bg) # This is the first line when drawing a new frame
    screen.blit(lpng, (const.WINDOW_WIDTH // 2 - lpng.get_width() // 2, 15))
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
    screen.blit(gun1.getSprite(True), (const.TILE_SIZE, 0.78*const.WINDOW_HEIGHT)) # Gun 2
    screen.blit(tank1.getSprite(True), (const.TILE_SIZE, 0.78*const.WINDOW_HEIGHT)) # Tank 2

    screen.blit(gun2.getSprite(), (const.WINDOW_WIDTH - const.TILE_SIZE*3, 0.78*const.WINDOW_HEIGHT)) # Gun 2
    screen.blit(tank2.getSprite(), (const.WINDOW_WIDTH - const.TILE_SIZE*3, 0.78*const.WINDOW_HEIGHT)) # Tank 2
    print("Switching to game music")
    mixer.crossfade('game')

    # Load the custom font
    fontString = "PLAYER 1             SCORE              PLAYER 2" # This is a bad way to write a string
    controlString = "WASD                            ↑↓→←" # This is a bad way to write a string
    textp2Name = const.FONT_DICTIONARY["playerStringFont"].render(fontString, True, c.geT("BLACK"))
    controls = const.FONT_DICTIONARY["ctrlFont"].render(controlString, True, c.geT("BLACK"))
    screen.blit(textp2Name,[const.WINDOW_WIDTH//2 - textp2Name.get_width()//2, 0.78*const.WINDOW_HEIGHT]) # This is the name on the right
    screen.blit(controls,[const.WINDOW_WIDTH//2 - controls.get_width()//2, const.WINDOW_HEIGHT*5/6]) # This is the name on the right

    HealthBox = TextBox(const.TILE_SIZE*7/8-1, 0.88*const.WINDOW_HEIGHT, "Londrina", "HEALTH", 20, c.geT("BLACK"))
    HealthBox.setPaddingHeight(0)
    HealthBox.setPaddingWidth(0)
    HealthBox.setBoxColor(bg)
    HealthBox.draw(screen)

    ReloadBox = TextBox(const.TILE_SIZE*7/8-1, 0.88*const.WINDOW_HEIGHT + const.MAZE_Y//2, "Londrina", "RELOAD", 20, c.geT("BLACK"))
    ReloadBox.setPaddingHeight(0)
    ReloadBox.setPaddingWidth(0)
    ReloadBox.setBoxColor(bg)
    ReloadBox.draw(screen)

    HealthBox2 = TextBox(const.WINDOW_WIDTH-const.TILE_SIZE*2.2-1, 0.88*const.WINDOW_HEIGHT, "Londrina", "HEALTH", 20, c.geT("BLACK"))
    HealthBox2.setPaddingHeight(0)
    HealthBox2.setPaddingWidth(0)
    HealthBox2.setBoxColor(bg)
    HealthBox2.draw(screen)

    ReloadBox2 = TextBox(const.WINDOW_WIDTH-const.TILE_SIZE*2.2-1, 0.88*const.WINDOW_HEIGHT + const.MAZE_Y//2, "Londrina", "RELOAD", 20, c.geT("BLACK"))
    ReloadBox2.setPaddingHeight(0)
    ReloadBox2.setPaddingWidth(0)
    ReloadBox2.setBoxColor(bg)
    ReloadBox2.draw(screen)

def fixMovement(tanks):
    # This function will fix the movements of the tanks so that they aren't colliding with each other
    # Inputs: An array of the tanks that need to be processed
    #force to only have 2 tanks

    for idx, t in enumerate(tanks):

        tempX = t.x + t.changeX
        tempY = t.y - t.changeY

        if tempX <= const.MAZE_X + t.originalTankImage.get_size()[0]/2:
            tempX = const.MAZE_X + t.originalTankImage.get_size()[0]/2
        if tempY <= const.MAZE_Y + t.originalTankImage.get_size()[0]/2:
            tempY = const.MAZE_Y + t.originalTankImage.get_size()[0]/2
        if tempX > mazeWidth + const.MAZE_X - t.originalTankImage.get_size()[0]/2:
            tempX = mazeWidth + const.MAZE_X - t.originalTankImage.get_size()[0]/2
        if tempY > mazeHeight + const.MAZE_Y - t.originalTankImage.get_size()[0]/2:
            tempY = mazeHeight + const.MAZE_Y - t.originalTankImage.get_size()[0]/2

        t1 = tanks[(idx+2)%2]
        t2 = tanks[(idx+1+2)%2]
        # between tanks
        if pygame.sprite.collide_rect(t1, t2):

            # Calculate the direction vector between the tanks
            deltaX = t2.x - t1.x
            deltaY = t2.y - t1.y

            # Get the distance between the two tanks
            distance = (deltaX**2 + deltaY**2)**0.5

            # Define a minimum distance threshold (how far apart the tanks should be)
            minDistance = 15  # Adjust this value as needed

            # Only push the tanks apart if they are within the threshold distance
            if distance < minDistance:
                # Calculate the overlap (how much the tanks are colliding)
                overlap = minDistance - distance

                # Normalize the direction vector to get a unit vector
                if distance != 0:
                    directionX = deltaX / distance
                    directionY = deltaY / distance
                else:
                    directionX = 0
                    directionY = 0

                # Calculate the total weight of both tanks
                totalWeight = t1.getWeight() + t2.getWeight()

                # Calculate the push-back proportionally to the weight
                pushAmountT1 = (t2.getWeight() / totalWeight) * overlap  # t1's pushback based on its weight
                pushAmountT2 = (t1.getWeight() / totalWeight) * overlap  # t2's pushback based on its weight

                # Apply the push-back to both tanks
                t1.setCoords(t1.x - directionX * pushAmountT1, t1.y - directionY * pushAmountT1)
                t2.setCoords(t2.x + directionX * pushAmountT2, t2.y + directionY * pushAmountT2)
        
        # Check for collision with walls
        row = math.ceil((t.getCenter()[1] - const.MAZE_Y) / const.TILE_SIZE)
        col = math.ceil((t.getCenter()[0] - const.MAZE_X) / const.TILE_SIZE)
        index = (row - 1) * colAmount + col

        if index in range(1, rowAmount * colAmount + 1):
            tile = tileList[index - 1]
            tank_width = t.originalTankImage.get_size()[0]
            tank_height = t.originalTankImage.get_size()[1]

            # Calculate tank's future position (without correction)
            futureX = tempX
            futureY = tempY

            # Check top, bottom, left, and right borders
            if tile.border[0] and tempY - tank_height <= tile.y:  # Top border
                futureY = tile.y + tank_height
            if tile.border[1] and tempX + tank_width / 2 >= tile.x + const.TILE_SIZE:  # Right border
                futureX = tile.x + const.TILE_SIZE - tank_width / 2
            if tile.border[2] and tempY + tank_height > tile.y + const.TILE_SIZE:  # Bottom border
                futureY = tile.y + const.TILE_SIZE - tank_height
            if tile.border[3] and tempX - tank_width / 2 < tile.x:  # Left border
                futureX = tile.x + tank_width / 2

            # Corner detection (top-left, top-right, bottom-left, bottom-right)
            if tile.border[0] and tile.border[3]:  # Top-left corner
                if tempX - tank_width / 2 < tile.x and tempY - tank_height <= tile.y:
                    futureX = tile.x + tank_width / 2
                    futureY = tile.y + tank_height
            elif tile.border[0] and tile.border[1]:  # Top-right corner
                if tempX + tank_width / 2 >= tile.x + const.TILE_SIZE and tempY - tank_height <= tile.y:
                    futureX = tile.x + const.TILE_SIZE - tank_width / 2
                    futureY = tile.y + tank_height
            elif tile.border[2] and tile.border[3]:  # Bottom-left corner
                if tempX - tank_width / 2 < tile.x and tempY + tank_height > tile.y + const.TILE_SIZE:
                    futureX = tile.x + tank_width / 2
                    futureY = tile.y + const.TILE_SIZE - tank_height
            elif tile.border[2] and tile.border[1]:  # Bottom-right corner
                if tempX + tank_width / 2 >= tile.x + const.TILE_SIZE and tempY + tank_height > tile.y + const.TILE_SIZE:
                    futureX = tile.x + const.TILE_SIZE - tank_width / 2
                    futureY = tile.y + const.TILE_SIZE - tank_height

            # Apply the corrected positions
            tempX, tempY = futureX, futureY

        t.setCentre(tempX, tempY)

        t.changeX = 0
        t.changeY = 0
    
def damage(tank, damage):
    # This function will adjust the damage that the tank has taken
    # Inputs: damage: The amount of damage that the tank has taken
    # Outputs: None
    # if tank.getInvincibility() != 0: # we are still invincible
    #     return
    tank.health -= (damage * (0.5 if tank.effect[1] != 0 else 1))
    if tank.health > 0:
        if not tank.channelDict["death"]["channel"].get_busy(): # if the sound isn't playing
            tank.channelDict["death"]["channel"].play(soundDictionary["tankHurt"])  # Play sound indefinitely
        else:
            spareChannels(soundDictionary["tankHurt"])
    else: # if tank is dead
        # if the tank is dead everything should stop
        for channel in tank.channelDict:
            if tank.channelDict[channel]["channel"].get_busy():
                tank.channelDict[channel]["channel"].stop()
        # last sound to be played
        if not tank.channelDict["death"]["channel"].get_busy():
            tank.channelDict["death"]["channel"].play(soundDictionary["tankDeath"])
        else:
            spareChannels(soundDictionary["tankDeath"])
    updateTankHealth() # Manage the healthbar outside of the code

def playGame():

    def checkGameOver(t):
        global tank1Dead, tank2Dead, DifficultyType, difficultyType
        match t:
            case DifficultyType.OnePlayerYard:
                return tank1Dead or tank2Dead
            case DifficultyType.OnePlayerScrapYard:
                return tank1Dead or tank2Dead
            case DifficultyType.TwoPlayerYard:
                return tank1Dead or tank2Dead
            case DifficultyType.TwoPlayerScrapYard:
                return tank1Dead or tank2Dead
            case DifficultyType.OnePlayerBrawl:
                return timer.isExpired()
            case DifficultyType.OnePlayerDeathMatch:
                return timer.isExpired()
            case DifficultyType.TwoPlayerBrawl:
                return timer.isExpired()
            case DifficultyType.TwoPlayerDeathMatch:
                return timer.isExpired()
    # This function controls the main execution of the game
    # Inputs: None
    # Outputs: None
    # Because of the way the game is structured, these global variables can't be avoided
    global gameOverFlag, cooldownTimer, systemTime, p1Score, p2Score, startTreads
    global tank1Dead, tank2Dead, tileList, spawnpoint, player1Channels, player2Channels
    global tank1, tank2, gun1, gun2, allSprites, bulletSprites
    global currentTime, deltaTime, lastUpdateTime, difficultyType
    global upplyAssets, timerClock
    if checkGameOver(t = difficultyType) and not cooldownTimer:
        #The game is over
        systemTime = time.time() #Start a 3s timer
        cooldownTimer = True
        timer.pause()
    if cooldownTimer:
        #movement sound
        pygame.mixer.Channel(3).stop()
        pygame.mixer.Channel(9).stop()
        #rotation sound
        pygame.mixer.Channel(4).stop()
        pygame.mixer.Channel(10).stop()
        if time.time() - systemTime >= 3: # 3 seconds
            #Reset the game
            reset()
            constantPlayGame()
            timer.reset() # rest the clock

    seconds = timer.getTime()
    textString = f"{seconds // 60:02d}:{seconds % 60:02d}"
    text = const.FONT_DICTIONARY["scoreFont"].render(textString, True, c.geT("BLACK"))

    #UI Elements
    pauseButton.update_display(pygame.mouse.get_pos())
    pauseButton.draw(screen, outline = True)

    pygame.draw.rect(screen, bg, [const.TILE_SIZE*0.72, const.TILE_SIZE*0.72, const.WINDOW_WIDTH - const.TILE_SIZE*1.4, const.TILE_SIZE*8.5]) # Draw a box for the maze
    
    #Making the string for score
    p1ScoreText = str(p1Score)
    p2ScoreText = str(p2Score)
    #Setting up the tex

    # Load the custom font
    pygame.draw.rect(screen, bg, [const.TILE_SIZE*2.1, 0.87*const.WINDOW_HEIGHT, const.WINDOW_WIDTH-const.TILE_SIZE*1.2-barWidth, const.WINDOW_HEIGHT*0.15]) # The bottom bar

    text3 = const.FONT_DICTIONARY["playerScore"].render(p1ScoreText + ":" + p2ScoreText, True, c.geT("BLACK"))
    screen.blit(text3, [const.WINDOW_WIDTH/2 - text3.get_width()/2, 0.85*const.WINDOW_HEIGHT])

    #Box around the bottom of the screen for the health and reload bars


    pygame.draw.rect(screen, c.geT("RED"), [const.TILE_SIZE*2.2, 0.88*const.WINDOW_HEIGHT, barWidth*(tank1.getHealthPercentage()),
                                            barHeight]) # Bar
    pygame.draw.rect(screen, c.geT("BLACK"), [const.TILE_SIZE*2.2, 0.88*const.WINDOW_HEIGHT, barWidth, barHeight], 2) # Outline
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [const.TILE_SIZE*2.2, 0.88*const.WINDOW_HEIGHT + const.MAZE_Y//2, barWidth*(min(1,1-gun1.getReloadPercentage())),
                                             barHeight]) # The 25 is to space from the health bar

    pygame.draw.rect(screen, c.geT("BLACK"), [const.TILE_SIZE*2.2, 0.88*const.WINDOW_HEIGHT + const.MAZE_Y//2, barWidth, barHeight], 2) # Outline


    #Health bars
    pygame.draw.rect(screen, c.geT("RED"), [const.WINDOW_WIDTH - const.TILE_SIZE*2.2 - barWidth, 0.88*const.WINDOW_HEIGHT, barWidth*(tank2.getHealthPercentage()),
                                            barHeight])
    pygame.draw.rect(screen, c.geT("BLACK"), [const.WINDOW_WIDTH - const.TILE_SIZE*2.2 - barWidth, 0.88*const.WINDOW_HEIGHT, barWidth, barHeight], 2)
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [const.WINDOW_WIDTH - const.TILE_SIZE*2.2 - barWidth, 0.88*const.WINDOW_HEIGHT + const.MAZE_Y//2,
                                             barWidth*(min(1,1-gun2.getReloadPercentage())),
                                             barHeight]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, c.geT("BLACK"), [const.WINDOW_WIDTH - const.TILE_SIZE*2.2 - barWidth, 0.88*const.WINDOW_HEIGHT + const.MAZE_Y//2, barWidth, barHeight], 2) # Outline

    #draw the supplies # Draw more on top of them

    ef, mx = tank1.getEffect()

    # Dynamic updating of the current supply status
    screen.blit(supplyAssets[0][min(int(((ef[0]/mx[0])*10)//1) + 1, 10) if ef[0] != 0 else 0], [270, 550])
    screen.blit(supplyAssets[1][min(int(((ef[1]/mx[1])*10)//1) + 1, 10) if ef[1] != 0 else 0], [300, 550])
    screen.blit(supplyAssets[2][min(int(((ef[2]/mx[2])*10)//1) + 1, 10) if ef[2] != 0 else 0], [270, 520])

    ef2, mx2 = tank2.getEffect()

    screen.blit(supplyAssets[0][min(int(((ef2[0]/mx2[0])*10)//1) + 1, 10) if ef2[0] != 0 else 0], [510, 550])
    screen.blit(supplyAssets[1][min(int(((ef2[1]/mx2[1])*10)//1) + 1, 10) if ef2[1] != 0 else 0], [480, 550])
    screen.blit(supplyAssets[2][min(int(((ef2[2]/mx2[2])*10)//1) + 1, 10) if ef2[2] != 0 else 0], [510, 520])

    # Draw the border
    for tile in tileList:
        tile.update()
        tile.draw(screen)

    # Draw the edge of themaze
    pygame.draw.rect(screen, c.geT("BLACK"), [const.MAZE_X, const.MAZE_Y, mazeWidth, mazeHeight], 2)
    #Anything below here will be drawn on top of the maze and hence is game updates

    if pygame.time.get_ticks() - startTreads > 50:
        if tank1Dead:
            treadsp1.clear()
        else:
            if tank1.invincibility==0:
                tank1.treads(treadsp1)

        if tank2Dead:
            treadsp2.clear()
        else:
            if tank2.invincibility==0:
                tank2.treads(treadsp2)
        startTreads = pygame.time.get_ticks() # Reset the timer

    for pos in treadsp1:
        screen.blit(pos[0], pos[1])
    for pos in treadsp2:
        screen.blit(pos[0], pos[1])

    # fill up the area covered by the tank with the background color
    pygame.draw.rect(screen, bg, [const.WINDOW_WIDTH//2 - (text.get_width()//2) * 1.1, 8, text.get_width()* 1.1, text.get_height()])
    # draw the text again
    screen.blit(text, [const.WINDOW_WIDTH//2 - text.get_width()//2, 8])

    # pygame.draw.polygon(screen, c.geT("GREEN"), tank1.getCorners(), 2) #Hit box outline
    # pygame.draw.polygon(screen, c.geT("GREEN"), tank2.getCorners(), 2) #Hit box outline
    # if we are using AI we need to set the target to go to the other tank
    if difficultyType.ai and pygame.time.get_ticks() - tank1.getAimTime() > 2000:
        # AI difficulty
        if not tank2Dead: # if the tank is still alive
            temp = tank2.getCurrentTile().getIndex()
            tank1.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))

    currentTime = time.time()
    deltaTime = currentTime - lastUpdateTime
    if deltaTime >= 1/TPS:
        #Update the location of the corners
        if not tank1Dead:
            tank1.updateCorners()
            tank1.setDelta(TPS)
            gun1.setDelta(TPS)
        else:
            if difficultyType.respawn:
                # easy
                setUpTank1(difficultyType)
                tank1.setCentre(spawnTank1[0], spawnTank1[1])
                tank1Dead = False
                allSprites.add(tank1, gun1) # Add the new sprites

        if not tank2Dead:
            tank2.updateCorners()
            tank2.setDelta(TPS)
            gun2.setDelta(TPS)
        else:
            if difficultyType.respawn:
                setUpTank2(difficultyType)
                tank2Dead = False
                allSprites.add(tank2, gun2) # Add the new sprites
            
        for bullet in bulletSprites:
            bullet.setDelta(TPS)

        #Fixing tank movement
        # don't update the bullets if the game is over
        if not cooldownTimer:
            allSprites.update()
            fixMovement([tank1, tank2])
            bulletSprites.update()
        explosionGroup.update()
        lastUpdateTime = currentTime

    for sprite in allSprites:
        sprite.draw(screen)
        if sprite.isDrawable():
            sprite.customDraw(screen)

    for sprite in bulletSprites:
        sprite.draw(screen)
        if sprite.isDrawable():
            sprite.customDraw(screen)

    explosionGroup.draw(screen)
    if timerClock == 0:
        timer.tick()
    # 125 is the reference for the FPS
    timerClock = (timerClock + 1) % 120 # This is to make sure that the timer doesn't go too fast

def reset():
    # This function is to reset the board everytime we want to restart the game
    # Inputs: None
    # Outputs: None
    # Because of the way it's coded, these global declarations can't be avoided
    global gameOverFlag, cooldownTimer, systemTime, p1Score, p2Score
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
    systemTime = 0
    tank1Dead = False
    tank2Dead = False
    treadsp1.clear()
    treadsp2.clear()
    setUpPlayers()

def updateTankHealth():
    # This function will update the tank health and check if the tank is dead
    # Inputs: None
    # Outputs: None
    global explosionGroup, tank1Dead, tank2Dead
    global p1Score, p2Score
    global allSprites, tank1, tank2, gun1, gun2
    #Update the tank health
    if tank1.getHealth() <= 0:
        if not tank1Dead:
            p2Score = (p2Score + 1) % 99 # Fix the maximum to 99
            tank1Dead = True
            explosionGroup.add(Explosion(tank1.getCenter()[0], tank1.getCenter()[1]))
        tank1.setCentre(2000, 2000)
        gun1.kill()
        tank1.kill()
        if tank2.getHealth() <= 0:
            for sprite in allSprites:
                sprite.kill()
            allSprites = pygame.sprite.Group()
    if tank2.getHealth() <= 0:
        if not tank2Dead:
            p1Score = (p1Score + 1) % 99 # Fix the maximum to 99
            tank2Dead = True
            explosionGroup.add(Explosion(tank2.getCenter()[0], tank2.getCenter()[1]))
        tank2.setCentre(-2000, -2000)
        gun2.kill()
        tank2.kill()
        if tank1.getHealth() <= 0:
            for sprite in allSprites:
                sprite.kill()            
            allSprites = pygame.sprite.Group()

timer = UpDownTimer(1000, True)

#Game setup
#Start the game setup
mixer = Music()
mixer.play()
pygame.display.set_caption("Flanki") # Name the window
clock = pygame.time.Clock() # Start the clock

initialStartTime = pygame.time.get_ticks()
soundPlayed = False
global animationCool
animationCool = 12

global explosionGroup
explosionGroup = pygame.sprite.Group() #All the explosions

resetFlag = True
systemTime = 0
cooldownTimer = False

global startTreads
startTreads = 0
global gameOverFlag
gameOverFlag = False
#Constants
done = False
const.WINDOW_WIDTH = 800
const.WINDOW_HEIGHT = 600

TPS = 30 #Ticks per second

global currentTime, deltaTime, lastUpdateTime
currentTime = 0
deltaTime = 0
lastUpdateTime = 0

screen = pygame.display.set_mode((const.WINDOW_WIDTH,const.WINDOW_HEIGHT))  # Windowed (safer/ superior)

# Fullscreen but it renders your computer useless otherwise
supplyAssets = ["Assets/Double_Armor.png", "Assets/Speed_Boost.png"]
if getattr(sys, 'frozen', False):  # Running as an .exe
    currentDir = sys._MEIPASS
else:  # Running as a .py script
    currentDir = os.path.dirname(os.path.abspath(__file__))

supplyAssets = [[None]*11 for _ in range(3)] # 3 for the supply, 3 for the picked up supply
names = ["Damage", "Armor", "Speed"]
for i in range(3):
    for j in range(11): # each version of the supply
        supplyAssets[i][j] = pygame.image.load(os.path.join(currentDir, 'Assets', f"{names[i]}_{j}.png")).convert_alpha()
        supplyAssets[i][j] = pygame.transform.scale(supplyAssets[i][j], (20, 20))


#safe full screen
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # For fullscreen enjoyers
# const.WINDOW_WIDTH, const.WINDOW_HEIGHT = pygame.display.get_surface().get_size()
# print(const.WINDOW_WIDTH, const.WINDOW_HEIGHT)

weightTrue = 0.16 # The percentage change that side on a tile will have a border
rowAmount = 14
colAmount = 8
# Keeping track of score
p1Score = 0
p2Score = 0

p1NameIndent = 25
p2NameIndent = const.WINDOW_WIDTH - 25

#Defining the variables that make up the main maze screen
mazeWidth = const.WINDOW_WIDTH - const.MAZE_X*2 # We want it to span most of the screen
mazeHeight = const.WINDOW_HEIGHT - const.MAZE_Y*4
rowAmount = mazeHeight//const.TILE_SIZE # Assigning the amount of rows
colAmount = mazeWidth//const.TILE_SIZE # Assigning the amount of columns
barWidth = 150
barHeight = 20
bg = c.geT('SOFT_WHITE')
gameMode = GameMode.home
difficultyType = DifficultyType.NotInGame
#Changing variables
p1TankName = "Plwasd1"
p2TankName = "Plarro2"

p1GunName = "Gun1"
p2GunName = "Gun2"

tileList = tileGen()

selectionBackground = c.geT("SOFT_WHITE")
monoFont = 'Courier New'

#Selection Screen
buttonList = []

homeButton = TextBox(const.TILE_SIZE//4, const.TILE_SIZE//4, font=const.SELECTION_FONT,fontSize=26, text="BACK", textColor=c.geT("BLACK"))
homeButton.setBoxColor(selectionBackground)
homeButton.setOutline(True, 5)
homeButton.selectable(True)
buttonList.append(homeButton)

#How to play button
howToPlayButton = TextBox(const.WINDOW_WIDTH - 150, const.TILE_SIZE//4, font=const.SELECTION_FONT,fontSize=26, text="HOW TO PLAY", textColor=c.geT("BLACK"))
howToPlayButton.setBoxColor(selectionBackground)
howToPlayButton.setOutline(True, 5)
howToPlayButton.selectable(True)
buttonList.append(howToPlayButton)

playButton = TextBox(const.WINDOW_WIDTH//2-84, 95, font=const.SELECTION_FONT,fontSize=52, text="PLAY", textColor=c.geT("BLACK"))
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

turretListLength = len(turretList)
hullListLength = len(hullList)

hullColors = []
gunColors = []

treadsp1 = []
treadsp2 = []
treadslen = 10

# Load all the images
if getattr(sys, 'frozen', False):  # Running as an .exe
    currentDir = sys._MEIPASS
else:  # Running as a .py script
    currentDir = os.path.dirname(os.path.abspath(__file__))

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

verticalSpacing = 40
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

textP1 = TextBox(playerX, playerY, font=const.SELECTION_FONT,fontSize=38, text="PLAYER 1", textColor=c.geT("BLACK"))
textP1.setBoxColor(selectionBackground)
textP1.setOutline(True, outlineWidth = 5)
buttonList.append(textP1)

textP2 = TextBox(const.WINDOW_WIDTH - playerX*2.5, playerY, font=const.SELECTION_FONT,fontSize=38, text="PLAYER 2", textColor=c.geT("BLACK"))
textP2.setBoxColor(selectionBackground)
textP2.setOutline(True, outlineWidth = 5)
buttonList.append(textP2)

offset = 35
speedBarX = 250

healthBarX = speedBarX + offset
damageBarX = healthBarX + offset
reloadBarX = damageBarX + offset


#Other constants
rectX = 280
rectY = 25
barFontSize = 36

speedText = TextBox(50, speedBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="SPEED", textColor=c.geT("BLACK"))
speedText.setPaddingHeight(0)
speedText.setPaddingWidth(0)
speedText.setCharacterPad(7)
speedText.setBoxColor(selectionBackground)
speedText.setText("SPEED", 'right')
buttonList.append(speedText)

healthText = TextBox(42, healthBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Health", textColor=c.geT("BLACK"))
healthText.setPaddingHeight(0)
healthText.setPaddingWidth(0)
healthText.setCharacterPad(7)
healthText.setBoxColor(selectionBackground)
healthText.setText("HEALTH", "right")
buttonList.append(healthText)

damageBar = TextBox(31, damageBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Damage", textColor=c.geT("BLACK"))
damageBar.setPaddingHeight(0)
damageBar.setPaddingWidth(0)
damageBar.setCharacterPad(7)
damageBar.setBoxColor(selectionBackground)
damageBar.setText("DAMAGE", "right")
buttonList.append(damageBar)

reloadBar = TextBox(37, reloadBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Reload", textColor=c.geT("BLACK"))
reloadBar.setPaddingHeight(0)
reloadBar.setPaddingWidth(0)
reloadBar.setCharacterPad(7)
reloadBar.setBoxColor(selectionBackground)
reloadBar.setText("RELOAD", "right")
buttonList.append(reloadBar)

speedText2 = TextBox(650, speedBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Speed", textColor=c.geT("BLACK"))
speedText2.setPaddingHeight(0)
speedText2.setPaddingWidth(0)
speedText2.setCharacterPad(7)
speedText2.setBoxColor(selectionBackground)
speedText2.setText("SPEED", "left")
buttonList.append(speedText2)

healthText2 = TextBox(650, healthBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Health", textColor=c.geT("BLACK"))
healthText2.setPaddingHeight(0)
healthText2.setPaddingWidth(0)
healthText2.setCharacterPad(7)
healthText2.setBoxColor(selectionBackground)
healthText2.setText("HEALTH", "left")
buttonList.append(healthText2)

damageBar2 = TextBox(650, damageBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Damage", textColor=c.geT("BLACK"))
damageBar2.setPaddingHeight(0)
damageBar2.setPaddingWidth(0)
damageBar2.setCharacterPad(7)
damageBar2.setBoxColor(selectionBackground)
damageBar2.setText("DAMAGE", "left")
buttonList.append(damageBar2)

reloadBar2 = TextBox(650, reloadBarX, font=const.SELECTION_FONT,fontSize=barFontSize, text="Reload", textColor=c.geT("BLACK"))
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
        gameMode = GameMode.info # Switch to the info screen
        infoScreen.draw(screen)

def checkHomeButtons(mouse):
    # This function checks all the buttons of the mouse in the home screen
    # Inputs: Mouse: The current location of the mouse
    # Outputs: None
    global gameMode, difficultyType, pageNum

    if HomeButton1.buttonClick(mouse):
        difficultyType = DifficultyType.from_index(1 + pageNum)
        setUpPlayers()
        gameMode=GameMode.play
        #Switch the the play screen
        print("One Player Easy")
        constantPlayGame()
    if HomeButton2.buttonClick(mouse):
        difficultyType = DifficultyType.from_index(2 + pageNum)
        print("One Player Hard")
        gameMode = GameMode.selection
        constantSelectionScreen()
    if HomeButton3.buttonClick(mouse):
        difficultyType = DifficultyType.from_index(3 + pageNum)
        setUpPlayers()
        gameMode=GameMode.play
        #Switch the the play screen
        print("Two Player Easy")
        constantPlayGame()
    if HomeButton4.buttonClick(mouse):
        difficultyType = DifficultyType.from_index(4 + pageNum)
        print("Two Player Hard")
        gameMode = GameMode.selection
        constantSelectionScreen()
    if homeLeftButton.buttonClick(mouse):
        pageNum = (pageNum - 4) % len(homeButtonNameArray)
        HomeButton1.setText(homeButtonNameArray[(pageNum) % len(homeButtonNameArray)])
        HomeButton2.setText(homeButtonNameArray[(pageNum + 1) % len(homeButtonNameArray)])
        HomeButton3.setText(homeButtonNameArray[(pageNum + 2) % len(homeButtonNameArray)])
        HomeButton4.setText(homeButtonNameArray[(pageNum + 3) % len(homeButtonNameArray)])
    if homeRightButton.buttonClick(mouse):
        pageNum = (pageNum + 4) % len(homeButtonNameArray)
        HomeButton1.setText(homeButtonNameArray[(pageNum) % len(homeButtonNameArray)])
        HomeButton2.setText(homeButtonNameArray[(pageNum + 1) % len(homeButtonNameArray)])
        HomeButton3.setText(homeButtonNameArray[(pageNum + 2) % len(homeButtonNameArray)])
        HomeButton4.setText(homeButtonNameArray[(pageNum + 3) % len(homeButtonNameArray)])

    if settingsButton.buttonClick(mouse):
        print("Settings")
        gameMode = GameMode.settings
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
    screen.blit(tankImage2, (const.WINDOW_WIDTH - hullImageX - 4 * 20, hullImageY))

    gunPath2 = os.path.join(currentDir, 'Sprites', turretList[p2I].getGunName() + str(p2K+1) + '.png')
    originalGunImage2 = pygame.image.load(gunPath2).convert_alpha()
    centerX, centerY = hullList[p2J].getGunCenter()
    gX, _ = turretList[p2I].getGunCenter()

    gunImage2 = pygame.transform.scale(originalGunImage2, (15*gunScale, 15*gunScale))
    gunImage2 = pygame.transform.flip(gunImage2, True, False) # Flipped
    screen.blit(gunImage2, (const.WINDOW_WIDTH - gunImageX - gunScale * 15 - (centerX - gX)*gunScale, gunImageY + centerY*gunScale - 6*gunScale))

# UI Screens
creditsScreen = CreditScreen()
settingsScreen = SettingsScreen()
pauseScreen = PauseScreen()
infoScreen = InfoScreen()
homeScreen = HomeScreen()

#Menu screen
homeButtonList = []

# Load the tank image
if getattr(sys, 'frozen', False):  # Running as an .exe
    currentDir = sys._MEIPASS
else:  # Running as a .py script
    currentDir = os.path.dirname(os.path.abspath(__file__))
tankPath = os.path.join(currentDir, './Assets/tank_menu_logo.png')
originalTankImage = pygame.image.load(tankPath).convert_alpha()
originalTankImage = pygame.transform.scale(originalTankImage, (originalTankImage.get_size()[0]/2.25, originalTankImage.get_size()[1]//2.25))

# Load the logo image
lpng = pygame.image.load(os.path.join(currentDir, "Assets", "logo.png")).convert_alpha()
lpng = pygame.transform.scale(lpng, (lpng.get_size()[0]//15, lpng.get_size()[1]//15))

# number to keep track of which page we are on
global pageNum
pageNum = 0

# homeButtonNameArray = ["1P Easy", "1P Hard", "2P Easy", "2P Hard"] #<!>
homeButtonNameArray = ["1P Yard", "1P Scrapyard", "2P Yard", "2P Scrapyard", "1p Brawl", "1P DeathMatch", "2P Brawl", "2P DeathMatch"] #<!>

# Create buttons with specified positions and text
homeLeftButton = Button(c.geT("BLACK"), c.geT("BLACK"), 30, 490, 40, 80, '←', (255, 255, 255), 25, hoverColor=(100, 100, 255))
HomeButton1 = Button(c.geT("BLACK"),c.geT("BLACK"), 106, 490, 120, 80, homeButtonNameArray[0], (255, 255, 255), 15, hoverColor=(100, 100, 255))
HomeButton2 = Button(c.geT("BLACK"),c.geT("BLACK"), 262, 490, 120, 80, homeButtonNameArray[1], (255, 255, 255), 15, hoverColor=(100, 100, 255))
HomeButton3 = Button(c.geT("BLACK"),c.geT("BLACK"), 418, 490, 120, 80, homeButtonNameArray[2], (255, 255, 255), 15, hoverColor=(100, 100, 255))
HomeButton4 = Button(c.geT("BLACK"),c.geT("BLACK"), 574, 490, 120, 80, homeButtonNameArray[3], (255, 255, 255), 15, hoverColor=(100, 100, 255))
homeRightButton = Button(c.geT("BLACK"), c.geT("BLACK"), 730, 490, 40, 80, '→', (255, 255, 255), 25, hoverColor=(100, 100, 255))

quitButtonHome = Button(c.geT("BLACK"), c.geT("BLACK"), 30, 30, 140, 80, 'Quit', (255, 255, 255), 25, hoverColor=(100, 100, 255))
settingsButton = Button(c.geT("BLACK"), c.geT("BLACK"), 570, 30, 210, 80, 'Settings', (255, 255, 255), 25, hoverColor=(100, 100, 255))

homeButtonList.append(homeLeftButton)
homeButtonList.append(HomeButton1)
homeButtonList.append(HomeButton3)
homeButtonList.append(HomeButton2)
homeButtonList.append(HomeButton4)
homeButtonList.append(homeRightButton)
homeButtonList.append(settingsButton)
homeButtonList.append(quitButtonHome)

# Define title text properties
titleText = const.FONT_DICTIONARY["titleFont"].render('FLANKI', True, (0, 0, 0))  # Render the title text

pauseButton = Button(bg ,bg, const.WINDOW_WIDTH-const.TILE_SIZE*3, const.TILE_SIZE//5,const.TILE_SIZE*2,const.TILE_SIZE//2, "PAUSE", c.geT("BLACK"), 20, c.geT("OFF_WHITE"))
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
    'tankShoot': 0.5,
    'tankDeath': 0.5,
    'tankHurt': 0.5,
    'turretRotate': 0.2,
    'tankMove': 0.05,
    'Chamber': 0.5,
    'Empty': 1,
    'Huntsman': 1,
    'Judge': 0.38,
    'Reload': 0.2,
    'Silencer': 0.25,
    'Sidewinder': 1,
    'Tempest': 1,
    'Watcher': 0.5
}
# Determine the correct base path
if getattr(sys, 'frozen', False):  # Running as an .exe
    currentDir = sys._MEIPASS
else:  # Running as a .py script
    currentDir = os.path.dirname(os.path.abspath(__file__))

# Construct the correct path for the sound
# sound_path = os.path.join(base_path, "Sounds", "tank_dead.wav")

soundDictionary = {
    'tankDeath' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "tank_dead.wav")),
    'tankHurt' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "tank_dead.wav")), # replace
    'tankMove' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "tank_moving.wav")),
    'tankShoot' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "tank_shoot.wav")),
    'turretRotate' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "tank_turret_rotate.wav")),
    'Chamber' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Chamber.wav")),
    'Empty' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Empty.wav")),
    'Huntsman' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Huntsman.wav")),
    'Judge' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Judge.wav")),
    'Reload' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Reload.wav")),
    'Silencer' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Silencer.wav")),
    'Sidewinder' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Sidewinder.wav")), # replace
    'Tempest' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Tempest.wav")),
    'Watcher' : pygame.mixer.Sound(os.path.join(currentDir, "Sounds", "Watcher.wav")),
}

pygame.mixer.set_num_channels(32)

for sound in soundDictionary:
    soundDictionary[sound].set_volume(volume[sound])

global spawnpoint
spawnTank1 = [tileList[spawnpoint[0]-1].x + const.TILE_SIZE//2, tileList[spawnpoint[0]-1].y + const.TILE_SIZE//2]
spawnTank2 = [tileList[spawnpoint[1]-1].x + const.TILE_SIZE//2, tileList[spawnpoint[1]-1].y + const.TILE_SIZE//2]
global tank1Dead, tank2Dead
tank1Dead = False
tank2Dead = False
currentTargetPackage = (spawnpoint[1]-1, tileList[spawnpoint[1]-1].x + const.TILE_SIZE//2, tileList[spawnpoint[1]-1].y + const.TILE_SIZE//2)
player1PackageTank = [spawnTank1[0], spawnTank1[1], controlsTank1, p1TankName]
player1PackageGun = [controlsTank1, p1GunName]
player2PackageTank = [spawnTank2[0], spawnTank2[1], controlsTank2, p2TankName]
player2PackageGun = [controlsTank2, p2GunName]

allSprites = pygame.sprite.Group()
bulletSprites = pygame.sprite.Group()

constantHomeScreen()

def main():
    global done, gameMode, iIndex
    #Main loop
    while not done:
        # Early define probably not a good idea, but will help with reducing function calls
        mouse = pygame.mouse.get_pos() #Update the position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos() # Update on button press
                if event.button == 1:
                    #If it is left click
                    #If we are in the play screen
                    if gameMode == GameMode.play:
                        #If the mouse is within the maze, make the tile the target
                        for tile in tileList:
                            tile.isWithin() # If the mouse is within the tile
                        if pauseButton.buttonClick(mouse):
                            gameMode = GameMode.pause
                    elif gameMode == GameMode.pause:
                        #We are paused
                        if pauseScreen.isWithinUnpauseButton(mouse):
                            constantPlayGame()
                            gameMode = GameMode.play # Return to game if button was clicked
                        if pauseScreen.isWithinHomeButton(mouse):
                            for i in range(3, pygame.mixer.get_num_channels()): # Stop all sounds
                                pygame.mixer.Channel(i).stop()
                            constantHomeScreen()
                            gameMode = GameMode.home
                        if pauseScreen.isWithinQuitButton(mouse):
                            print("Quitting the game")
                            done = True # We quit the appplication
                        if pauseScreen.isWithinMuteButton(mouse):
                            pauseScreen.volume.mute.buttonClick()
                        if pauseScreen.isWithinSFXButton(mouse):
                            pauseScreen.volume.sfx.buttonClick()
                        if pauseButton.buttonClick(mouse):
                            constantPlayGame()
                            gameMode = GameMode.play
                    elif gameMode == GameMode.selection: # Selection screen
                        textP1Turret.setText(turretList[p1I].getGunName())
                        textP2Turret.setText(turretList[p2I].getGunName())
                        textP1Hull.setText(hullList[p1J].getTankName())
                        textP2Hull.setText(hullList[p2J].getTankName())
                        checkButtons(mouse)
                    elif gameMode == GameMode.home: # Home screen
                        checkHomeButtons(mouse)
                        global p1Score, p2Score
                        p1Score, p2Score = 0, 0 # reset the player scores

                    elif gameMode == GameMode.play:
                        if pauseButton.buttonClick(mouse):
                            print("Hi")
                            for i in range(3, pygame.mixer.get_num_channels()): # Stop all sounds
                                pygame.mixer.Channel(i).stop()
                            gameMode = GameMode.pause
                    elif gameMode == GameMode.credit:
                        if creditsScreen.isWithinBackButton(mouse):
                            print("Returning to the settings menu")
                            gameMode = GameMode.settings
                    elif gameMode == GameMode.info:
                        # L/R/ buttons

                        if infoScreen.isWithinBackButton(mouse):
                            gameMode = GameMode.selection
                            constantSelectionScreen()
                        if infoScreen.isWithinLArrowButton(mouse):
                            # Update the list
                            infoScreen.updateBox(-1)
                        if infoScreen.isWithinRArrowButton(mouse):
                            # Update the list
                            infoScreen.updateBox(1)
                    elif gameMode == GameMode.settings:
                        if settingsScreen.isWithinCreditButton(mouse):
                            creditsScreen.draw(screen = screen)
                            gameMode = GameMode.credit
                        if settingsScreen.isWithinHomeButton(mouse):
                            gameMode = GameMode.home
                            constantHomeScreen()
                        if settingsScreen.isWithinQuitButton(mouse):
                            print("Quitting the game")
                            done = True # We quit the appplication
                        if settingsScreen.isWithinMuteButton(mouse):
                            settingsScreen.volume.mute.buttonClick()
                        if settingsScreen.isWithinSFXButton(mouse):
                            settingsScreen.volume.sfx.buttonClick()

            elif event.type == pygame.KEYDOWN: # Any key pressed
                if event.key == pygame.K_ESCAPE: # Escape hotkey to quit the window
                    done = True
                if event.key == pygame.K_i:
                    print("The current mouse position is: ", mouse)
                if event.key == pygame.K_p:
                    #Pause
                    if gameMode == GameMode.pause:
                        constantPlayGame()
                        gameMode = GameMode.play # Return to game if button was clicked
                        timer.resume()
                    elif gameMode == GameMode.play:
                        for i in range(3, pygame.mixer.get_num_channels()): # Stop all sounds
                            pygame.mixer.Channel(i).stop()
                        gameMode = GameMode.pause # Pause the game
                        timer.pause()
                if event.key == pygame.K_f:
                    #Calculate and track the average FPS
                    print("The FPS is: ", clock.get_fps())
                if event.key == pygame.K_m:
                    settingsScreen.volume.mute.mute()
                    settingsScreen.volume.sfx.mute()
                    for sound in soundDictionary:
                        soundDictionary[sound].set_volume(volume[sound] * settingsScreen.volume.sfx.getValue())
        if gameMode == GameMode.play:
            playGame() # Play the game
        elif gameMode == GameMode.pause:
            pauseScreen.draw(screen = screen) # Pause screen
            if mouse[0] and pygame.mouse.get_pressed()[0]:
                pauseScreen.updateMute(mouse)
                pauseScreen.updateSFX(mouse)
                for sound in soundDictionary:
                    soundDictionary[sound].set_volume(volume[sound] * pauseScreen.getSFXValue())
        elif gameMode == GameMode.selection:
            screen.fill(selectionBackground) # This is the first line when drawing a new frame
            for button in buttonList:
                button.update_display(mouse)
                button.draw(screen, outline = False)
            selectionScreen()
        elif gameMode == GameMode.home:
            # # Draw the tank image
            screen.blit(originalTankImage, (const.WINDOW_WIDTH//2 - originalTankImage.get_width()//2, const.WINDOW_HEIGHT//2 - originalTankImage.get_height()//2))  # Centered horizontally

            # Draw the title text
            screen.blit(titleText, (const.WINDOW_WIDTH // 2 - titleText.get_width() // 2, 110))  # Centered horizontally, 50 pixels from top

            # Handle hover effect and draw buttons
            for button in homeButtonList:
                button.update_display(mouse)
                button.draw(screen, outline=True)
            homeScreen.draw(screen, mouse) # we need the mouse argument in order to update the hover effect

        elif gameMode == GameMode.credit:
            pass # Do nothing
        elif gameMode == GameMode.info:
            infoScreen.draw(screen) # Info screen
            # we need to update the info screen if the user changes the input # however there may be the case where we don't need to do it and only update once ever click
        elif gameMode == GameMode.settings:
            # pauseScreen() # Pause screen
            settingsScreen.draw(screen = screen)
            if mouse[0] and pygame.mouse.get_pressed()[0]:
                settingsScreen.updateMute(mouse)
                settingsScreen.updateSFX(mouse)
                for sound in soundDictionary:
                    soundDictionary[sound].set_volume(volume[sound] * settingsScreen.getSFXValue())
        else:
            screen.fill(c.geT("WHITE")) # Errornous state
        clock.tick(240) # Set the FPS
        mixer.update(settingsScreen.getMuteValue()) # Update the mixer
        # print(spawnTank1, spawnTank2)
        pygame.display.flip()# Update the screen

    pygame.quit()

main()