import pygame
import sys, os
import math
import random
import constants as const
from bullets import *
import globalVariables as g
from ColorDictionary import ColourDictionary as c # colors
from DifficultyTypes import DifficultyType

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
        self.turretSpeed = 0.23 # This number * 30 for deg / tick
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
        self.player = None
        self.enemy = []
        self.dead = []
        self.target = None
        self.targetIndex = -1
        self.currentState = None

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
            # if the target is dead
            if self.AI_exitCondition(): # if the AI should exit
                self.getNewTarget() # find a new target
            if self.target is not None: # we have a target
                tank2x, tank2y = self.target.getCenter()# get the center
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

                self.angle = round(self.angle + temp) % 360
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
                            index = (row-1)*const.COLUMN_AMOUNT + col
                            tile = g.tileList[index-1]

                            if tile.border[0] and y - 1 <= tile.y:
                                break
                            if tile.border[1] and x + 1 >= tile.x + const.TILE_SIZE:
                                break
                            if tile.border[2] and y + 1 >= tile.y + const.TILE_SIZE:
                                break
                            if tile.border[3] and x - 1 <= tile.x:
                                break
                            if x <= const.MAZE_X or y <= const.MAZE_Y or x >= const.MAZE_WIDTH + const.MAZE_X or y >= const.MAZE_HEIGHT + const.MAZE_Y:
                                break
                        else:
                            self.fire() # huh
                            pass
            else: # if we don't have a target just come back to center
                if self.angle != self.tank.getAngle():
                    if self.angle < self.tank.getAngle():
                        self.angle += 1
                    else:
                        self.angle -= 1

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
                        self.channelDict["rotate"]["channel"].play(const.SOUND_DICTIONARY["turretRotate"], loops = -1)  # Play sound indefinitely
                else:
                    if self.channelDict["rotate"]["channel"].get_busy(): # if the sound is playing
                        self.channelDict["rotate"]["channel"].stop()  # Stop playing the sound

            if  keys[self.controls['left']]:
                self.rotationSpeed += self.tank.getRotationalSpeed() * self.deltaTime
            elif keys[self.controls['right']]:
                self.rotationSpeed += -self.tank.getRotationalSpeed() * self.deltaTime

            self.angle += self.rotationSpeed
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
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setDamage(self._getDamage())
        bullet.setName(self.getTank().getName())
        g.bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def AI_exitCondition(self, default = None):
        if default is None:
            default = g.difficultyType # if we didn't assign, we want to do what the game is currently set to

        if default == DifficultyType.NotInGame:
            return True
        if default == DifficultyType.OnePlayerYard:
            return self.dead[self.targetIndex]
        if default == DifficultyType.OnePlayerScrapYard:
            return self.dead[self.targetIndex]
        if default == DifficultyType.TwoPlayerYard:
            return self.dead[self.targetIndex]
        if default == DifficultyType.TwoPlayerScrapYard:
            return self.dead[self.targetIndex]
        if default == DifficultyType.OnePlayerBrawl:
            return self.dead[self.targetIndex]
        if default == DifficultyType.OnePlayerDeathMatch:
            return self.dead[self.targetIndex]
        if default == DifficultyType.TwoPlayerBrawl:
            return self.dead[self.targetIndex]
        if default == DifficultyType.TwoPlayerDeathMatch:
            return self.dead[self.targetIndex]
        if default == DifficultyType.OnePlayerTDM:
            return self.dead[self.targetIndex]
        if default == DifficultyType.TeamDeathMatch:
            return self.dead[self.targetIndex]
        if default == DifficultyType.OnePlayerCaptureTheFlag:
            if self.currentState == "enemyFlagAtHome": # enemy flag is at home
                # go and get it
                if not g.flag[(self.tank.getTeam())].isHome(): # if my flag is taken
                # if not g.flag[(self.tank.getTeam() + 1) % 2].isHome(): # This is our flag, but can't just flick constantly, we need a way to make a decision
                    self.currentState = None
                    # print("Enemy flag was taken, need a new target")
                    return True # we need a new target
                return False # we don't need a new target
            elif self.currentState == "enemyFlagNotAtHome": # enemy flag is not at home
                # if g.flag[(self.tank.getTeam())].isDropped() or not g.flag[(self.tank.getTeam() + 1) % 2].isHome(): # picked up or returned
                if g.flag[(self.tank.getTeam())].isHome() or g.flag[(self.tank.getTeam())].isDropped(): # the flag has been returned
                    self.currentState = None
                    # print("Enemy flag was picked up or returned, need a new target")
                    return True
                return False # we don't need a new target
            elif self.currentState == "enemyFlagDropped": # enemy flag is dropped
                # we should go and get it
                if not g.flag[(self.tank.getTeam())].isDropped(): # picked up or returned
                    self.currentState = None
                    # print("Enemy flag was picked up or returned after being dropped, need a new target")
                    return True
                return False # we don't need a new target
            elif self.currentState == "myFlagAtHome":
                # if either flag is missing, reconsider
                for f in g.flag:
                    if not f.isHome():
                        self.currentState = None
                        return True # we need a new target
                return False # we don't need a new target
            elif self.currentState == "myFlagNotAtHome":
                # when my flag is at home, we should switch
                if g.flag[(self.tank.getTeam() + 1) % 2].isHome():
                    # it's home so we can switch
                    self.currentState = None
                    # print("My flag was returned, need a new target")
                    return True # we need a new target
                return False # we don't need a new target
            elif self.currentState == "myFlagDropped":
                # we should go and return our flag
                # when my flag is at home, we should switch
                if g.flag[(self.tank.getTeam() + 1) % 2].isHome():
                    # it's home so we can switch
                    self.currentState = None
                    # print("My flag was returned after being dropped, need a new target")
                    return True # we need a new target
                return False # we don't need a new target
            else:
                # we don't have a target to choose
                self.currentState = None # we need a new target, something went wrong
                return True
        if default == DifficultyType.CaptureTheFlag:
            return self.AI_exitCondition(default=DifficultyType.OnePlayerCaptureTheFlag) # use the same logic as the one player mode
        return False

    def calculateDecision(self): # This function needs to be checked for impacting performance
        selectionDictionary = {
            "enemyFlagAtHome": 0,
            "enemyFlagNotAtHome": 0,
            "enemyFlagDropped": 0,
            "myFlagAtHome": 0,
            "myFlagNotAtHome": 0,
            "myFlagDropped": 0
        }

        # if the flag is at home, we should go for it
        if g.flag[self.tank.getTeam()].isHome():
            enemyFlag = g.flag[(self.tank.getTeam() + 1) % 2] # the enemy flag is always the next flag
            flagX, flagY = enemyFlag.getxy() # center of the enemy flag
            x,y = self.tank.getCenter() # center of the tank
            distance = math.hypot(flagX - x, flagY - y) / const.HYPOTENUSE # distance to the enemy flag
            selectionDictionary["enemyFlagAtHome"] = 1 + distance*1.25 # +1 to increase the priority of this state
            # ideally we should go and get it
        else:
            print("Enemy flag is not at home")
            selectionDictionary["enemyFlagNotAtHome"] = 1 # enemy flag is not at home
            # we don't really care if the enemy flag is not at home
        # if the flag is dropped, we should go for it
        if g.flag[self.tank.getTeam()].isDropped():
            # we should definitely look at getting it
            enemyFlag = g.flag[(self.tank.getTeam() + 1) % 2] # the enemy flag is always the next flag
            flagX, flagY = enemyFlag.getxy() # center of the enemy flag
            x,y = self.tank.getCenter() # center of the tank
            distance = math.hypot(flagX - x, flagY - y) / const.HYPOTENUSE # distance to the enemy flag
            selectionDictionary["enemyFlagDropped"] = 1 + distance # +1 to increase the priority of this state
        # if our flag is at home, we can go and attack the enemy
        if g.flag[(self.tank.getTeam() + 1) % 2].isHome():
            # we don't really care if our flag is at home
            selectionDictionary["myFlagAtHome"] = 0
        else:
            # we should go and hunt down the enemy with our flag
            # if we choose this we should also update the target constantly
            myFlag = g.flag[(self.tank.getTeam() + 1) % 2]
            flagX, flagY = myFlag.getxy() # center of the own flag
            x,y = self.tank.getCenter() # center of the tank
            distance = math.hypot(flagX - x, flagY - y) // const.HYPOTENUSE # distance to the own flag
            selectionDictionary["myFlagNotAtHome"] = 2 + distance*2 # +1 to increase the priority of this state, *2 to increase the priority of this state even more
        # if our flag is dropped, we should go and get it
        if g.flag[(self.tank.getTeam() + 1) % 2].isDropped():
            # we should definitely look at getting it
            myFlag = g.flag[self.tank.getTeam()]
            flagX, flagY = myFlag.getxy() # center of the own flag
            x,y = self.tank.getCenter() # center of the tank
            distance = math.hypot(flagX - x, flagY - y) // const.HYPOTENUSE # distance to the own flag
            selectionDictionary["myFlagDropped"] = 1 + distance # +1 to increase the priority of this state
        return selectionDictionary

    def getNewTarget(self, default = None):
        if default is None:
            default = g.difficultyType # if we didn't assign, we want to do what the game is currently set to

        if default == DifficultyType.NotInGame:
            return
        if default == DifficultyType.OnePlayerYard:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.OnePlayerScrapYard:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.TwoPlayerYard:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.TwoPlayerScrapYard:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.OnePlayerBrawl:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.OnePlayerDeathMatch:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.TwoPlayerBrawl:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target        if g.difficultyType == DifficultyType.TwoPlayerDeathMatch:
        if default == DifficultyType.OnePlayerTDM:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.TeamDeathMatch:
            # get available targets
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
                self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
            else: # we don't have a target to choose
                self.setGunTarget(None)
                self.setTankTarget(-1) # -1 is a special case for no target
        if default == DifficultyType.OnePlayerCaptureTheFlag:
            # get available targets
            # working out distances
            # how far is each tank from the tank

            # for gun only
            lst = [i for i in range(0, self.playerCount) if ((not self.dead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            # policy for selecting the next target
            distancelist = {} # This should be in the form of unit : distance
            for element in lst:
                # find the distance between the tank and the target
                x,y = self.tank.getCenter()
                targetX, targetY = self.enemy[element].getCenter() # center of the target
                distance = math.hypot(targetX - x, targetY - y)
                distancelist[element] = distance # add the distance to the list

            # find the closest target and set that as the gun target
            # we just focus on aiming at the nearest person
            if len(distancelist) != 0:
                closest = min(distancelist, key=distancelist.get) # get the closest target
                self.setGunTarget(self.enemy[closest])
            else: # we don't have a target to choose
                self.setGunTarget(None)

            # below here is the tank logic
            # enemy flag state -> at home / not at home / dropped
            # my flag state -> at home / not at home / dropped
            # currentState
            selectionDictionary = self.calculateDecision()
            self.currentState = max(selectionDictionary, key=selectionDictionary.get) # select the state with the highest priority

            # if we have the flag, our decision is much different
            if self.tank.getFlag() is None: # we don't have the flag
                # for the current state, do the following action
                if self.currentState == "enemyFlagAtHome": # enemy flag is at home
                    # go and get it
                    self.setTankTarget(g.flag[(self.tank.getTeam())].getTileIndex()) # set the tank target to get the own flag

                elif self.currentState == "enemyFlagNotAtHome": # enemy flag is not at home
                    # we can't go and get it, just go and find some other tank to kill
                    # prioritise the tank with the flag, but also consider the closest tank
                    closest = min(distancelist, key=distancelist.get) # get the closest target
                    self.setTankTarget(self.enemy[closest].getCurrentTile().getIndex())
                elif self.currentState == "enemyFlagDropped": # enemy flag is dropped
                    # we should go and get it
                    self.setTankTarget(g.flag[(self.tank.getTeam())].getTileIndex()) # set the tank target to get the own flag
                    # self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileIndex()) # set the tank target to the enemy flag
                elif self.currentState == "myFlagAtHome":
                    # we can go and attack the enemy
                    self.setTankTarget(g.flag[(self.tank.getTeam())].getTileIndex()) # set the tank target to get the own flag
                    # self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileIndex()) # go get the enemy flag
                elif self.currentState == "myFlagNotAtHome":
                    # since we don't have the flag, we should go and get it
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileIndex()) # set the tank target to the enemy flag
                    # self.setTankTarget(g.flag[(self.tank.getTeam())].getTileIndex()) # set the tank target to get the own flag
                elif self.currentState == "myFlagDropped":
                    # we should go and return our flag
                    # self.setTankTarget(g.flag[(self.tank.getTeam())].getTileIndex()) # set the tank target to get the own flag
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileIndex()) # set the tank target to the enemy flag
                else:
                    # we don't have a target to choose
                    self.setTankTarget(-1)
            else:
                # we have the flag
                # for the current state, do the following action
                if self.currentState == "enemyFlagAtHome": # enemy flag is at home
                    # impossible state, go home
                    print("Impossible state, enemy flag is at home but we have the flag")
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileHomeIndex()) # set the tank target to the enemy flag
                elif self.currentState == "enemyFlagNotAtHome": # enemy flag is not at home
                    # just get home because we have the flag
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileHomeIndex()) # set the tank target to the enemy flag
                elif self.currentState == "enemyFlagDropped": # enemy flag is dropped
                    # I'm dead
                    print("Impossible state, I'm dead")
                    self.setTankTarget(g.flag[(self.tank.getTeam())].getTileHomeIndex()) # set the tank target to the enemy flag
                elif self.currentState == "myFlagAtHome":
                    # get home
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileHomeIndex()) # set the tank target to the enemy flag
                elif self.currentState == "myFlagNotAtHome":
                    # prioritise getting home
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileHomeIndex()) # set the tank target to the enemy flag
                elif self.currentState == "myFlagDropped":
                    # we should preserve ourselves
                    self.setTankTarget(g.flag[(self.tank.getTeam() + 1) % 2].getTileHomeIndex()) # set the tank target to the enemy flag
                else:
                    # we don't have a target to choose
                    self.setTankTarget(-1)

        if default == DifficultyType.CaptureTheFlag:
            self.getNewTarget(default=DifficultyType.OnePlayerCaptureTheFlag)
        return

    def setGunTarget(self, target):
        """
        This function sets the target of the gun to the given target, this is in the form of a tank object.
        """
        self.target = target
    def setTankTarget(self, target):
        """
        This function sets the target of the tank to the given target, this is in the form of a tile index. (exclusively between 0 and 112)
        """
        if target < 0 or target > 112:
            return # don't set a target
        self.tank.setAim((target, target%14*const.TILE_SIZE + const.TILE_SIZE//2, ((target)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))


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
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Empty"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Empty"])

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
            self.channelDict["reload"]["channel"].play(const.SOUND_DICTIONARY["Reload"])

    def _getTurretSpeed(self):
        return self.turretSpeed * (1.5 if (self.tank.effect[2] != 0) else 1)
    
    def setDelta(self, delta):
        self.deltaTime = delta

    def setPlayer(self, player):
        self.player = player
    
    def getPlayer(self):
        return self.player

    def assignTeam(self, enemies, dead, players):
        self.enemy = enemies
        self.dead = dead
        self.playerCount = players
        lst = [i for i in range(0, self.playerCount) if ((not g.tankDead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
        self.targetIndex = random.choice(lst)
        self.target = self.enemy[self.targetIndex] # I think this works
        temp = self.target.getCurrentTile().getIndex() # for the most part we can guarantee this
        self.tank.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))

    def copy(self):
        return Gun(self.tank, self.controls, self.name)

    def getTeam(self):
        return self.player.getTeam()

    def updateAim(self):
        if g.difficultyType == DifficultyType.OnePlayerCaptureTheFlag or g.difficultyType == DifficultyType.CaptureTheFlag: # <!Help>
            # LEAVE
            if (self.currentState == "enemyFlagNotAtHome" or self.currentState == "myFlagNotAtHome") and self.tank.getFlag() is None: # we don't have the flag
                lst = [i for i in range(0, self.playerCount) if ((not g.tankDead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
                self.targetIndex = random.choice(lst)
                self.target = self.enemy[self.targetIndex] # I think this works
                temp = self.target.getCurrentTile().getIndex() # for the most part we can guarantee this
                self.tank.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))

            return
        if self.target is not None: # find a new target
            lst = [i for i in range(0, self.playerCount) if ((not g.tankDead[i]) and self.enemy[i].getName() != self.tank.name and self.enemy[i].getTeam() != self.tank.getTeam())]
            self.targetIndex = random.choice(lst)
            self.target = self.enemy[self.targetIndex] # I think this works
            temp = self.target.getCurrentTile().getIndex() # for the most part we can guarantee this
            self.tank.setAim((temp, temp%14*const.TILE_SIZE + const.TILE_SIZE//2, ((temp)//14 + 1)*const.TILE_SIZE + const.TILE_SIZE//2))

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
        bullet = ChamberBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setName(self.getTank().getName())
        bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(10)
        g.bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        #If either tank shoots, play this sound effect.
        self.playSFX()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Chamber"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Chamber"])

    def copy(self):
        return Chamber(self.getTank(), self.controls, self.getTank().getName())

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
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setDamage(self._getDamage())
        bullet.setBounce(5)
        bullet.setName(self.getTank().getName())
        g.bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def copy(self):
        return DefaultGun(self.getTank(), self.controls, self.getTank().getName())

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
        bullet = Bullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setName(self.getTank().getName())
        if random.random() <= 0.4:  # 40% chance
            bullet.setDamage(self._getDamage() * 2)
        else:
            bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(15)
        g.bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Huntsman"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Huntsman"])

    def copy(self):
        return Huntsman(self.getTank(), self.controls, self.getTank().getName())

class Judge(Gun):

    def __init__(self, tank, controls, name):
        super().__init__(tank, controls, name)
        self.setCooldown(800)  # 800 ms
        self.setDamage(40)
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
        bullet = JudgeBullet(bulletX + random.uniform(-3, 3), bulletY + random.uniform(-3, 3), bulletAngle, self.gunLength, self.tipOffSet, self)
        bullet.setName(self.getTank().getName())
        bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(8)
        g.bulletSprites.add(bullet)

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Judge"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Judge"])

    def getReloadPercentage(self):
        # The bar has 3 segments, each segment is 1/3 of the reload time
        # cooldownDuration = 800 ms
        if self.currentUses == self.maxUses:
            temp = self.shootCooldown / (self.cooldownDuration * self.maxUses)
        else:
            temp = 1 - (self.currentUses % self.maxUses + self.shootCooldown / self.cooldownDuration) / self.maxUses
        return temp

    def copy(self):
        return Judge(self.getTank(), self.controls, self.getTank().getName())

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
        bullet = SidewinderBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setName(self.getTank().getName())
        bullet.setBulletSpeed(10)
        bullet.setDamage(self._getDamage())
        g.bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.playSFX()

    def playSFX(self):
        # This function will play the sound effect of the gun firing
        # Inputs: None
        # Outputs: None
        if not self.channelDict["fire"]["channel"].get_busy(): # if the sound isn't playing
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Sidewinder"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Sidewinder"])

    def copy(self):
        return Sidewinder(self.getTank(), self.controls, self.getTank().getName())

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
                self.channelDict["rotate"]["channel"].play(const.SOUND_DICTIONARY["turretRotate"], loops = -1)  # Play sound indefinitely
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
        bullet = SilencerBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setDamage(self._getDamage())
        bullet.setBulletSpeed(50)
        bullet.setName(self.getTank().getName())
        bullet.drawable = True
        bullet.trail = True
        g.bulletSprites.add(bullet)
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
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Silencer"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Silencer"])

    def copy(self):
        return Silencer(self.getTank(), self.controls, self.getTank().getName())

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
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Tempest"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Tempest"])

    def copy(self):
        return Tempest(self.getTank(), self.controls, self.getTank().getName())
    
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
                self.channelDict["rotate"]["channel"].play(const.SOUND_DICTIONARY["turretRotate"], loops = -1)  # Play sound indefinitely
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
        bullet = WatcherBullet(bulletX, bulletY, self.angle, self.gunLength, self.tipOffSet, self)
        bullet.setDamage(self.getDamage())
        bullet.setBulletSpeed(50)
        bullet.setName(self.getTank().getName())
        bullet.drawable = True
        g.bulletSprites.add(bullet)
        self.canShoot = False
        self.shootCooldown = self.cooldownDuration
        self.scopeDamage = 350 # Reset the damage
        self.playSFX()

    def getDamage(self):
        return self.scopeDamage * (self._getDamage() / self.damage) # reverting any change made

    def customDraw(self, screen):

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
                if tempX <= const.MAZE_X or tempY <= const.MAZE_Y or tempX >= const.MAZE_WIDTH + const.MAZE_X or tempY >= const.MAZE_HEIGHT + const.MAZE_Y:
                    found = True
                    break
                # Recalculate row and column based on the smaller steps
                row = math.ceil((tempY - const.MAZE_Y) / const.TILE_SIZE)
                col = math.ceil((tempX - const.MAZE_X) / const.TILE_SIZE)
                index = (row - 1) * const.COLUMN_AMOUNT + col

                # Handle wall collision
                if (index < 0) or (index >= len(g.tileList)):
                    found = True
                    break
                tile = g.tileList[index-1]
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
            self.channelDict["fire"]["channel"].play(const.SOUND_DICTIONARY["Watcher"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["Watcher"])

    def copy(self):
        return Watcher(self.getTank(), self.controls, self.getTank().getName())
