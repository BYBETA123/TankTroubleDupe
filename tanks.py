import pygame
import math
import os, sys
# Main variables
TIMER_MAX = 19000 # The maximum time for the timer I think this is 10s?

def breathFirstSearchShort(tileList, choices, option):
    # This function will search the maze in a breath first manner to see if we can reach the second spawn
    # Inputs: tileList: The current list of tiles
    # Inputs: Choices: The locations of both spawns
    # Outputs: True if the second spawn is reachable, False otherwise

    #Setting up the BFS
    visitedQueue = []
    tracking = [False for _ in range(14*8+1)] # 14 is row amount and 8 is column amount
    queue = [choices[option]]
    predecessors = {}
    visitedQueue.append(choices[option])
    tracking[choices[option]] = True
    predecessors[choices[option]] = None
    while len(queue) > 0: # While there are still elements to check
        current = queue.pop(0)
        if current == choices[(option +1) % 2]:
            break
        for neighbour in tileList[current-1].getNeighbours():
            if not tracking[neighbour]:
                queue.append(neighbour)
                visitedQueue.append(neighbour)
                tracking[neighbour] = True
                predecessors[neighbour] = tileList[current-1].getIndex()  # Record the predecessor
    # Reconstruct the path from endNode to startNode
    path = []
    currentNode = choices[(option +1) % 2]
    while currentNode is not None:
        path.insert(0, currentNode)  # Insert at the beginning to avoid reversing later
        currentNode = predecessors[currentNode]
    # remove the first element
    path.pop(0)
    return path


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
        self.channelDict = {} # The dictionary that will store the sound effects
        self.AI = False
        self.lastTarget = x * 14 + y
        self.pseudoTargetarray = []
        self.BFSRefresh = True
        self.aimTime = 0
        self.changeX = 0
        self.changeY = 0
        self.soundDictionary = {} # The dictionary that will store the sound effects
        self.List = []
        self.deltaTime = 0
        self.effect = [0,0,0] # This is an array which carries timers for the effects being [damage, armor, speed] # we start with a speed boost
        self.weight = 1
        self.invincibility = TIMER_MAX * 2 / 9 # this is the invincibility period (~5sec)
        # Treads
        if getattr(sys, 'frozen', False):  # Running as an .exe
            base_path = sys._MEIPASS
        else:  # Running as a .py script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the correct path for the image file
        image_path = os.path.join(base_path, 'Assets', 'Treads.png')

        # Load the image with the corrected path
        self.tread_surface = pygame.image.load(image_path).convert_alpha()
        self.tread_surface = pygame.transform.scale(self.tread_surface, (8, self.originalTankImage.get_size()[1]))
        self.player = None

    def update(self):
        # This function updates the tank's position and rotation based on the controls detected
        # from the keyboard sound effects will be played as well as the sound effects
        # Inputs: None
        # Outputs: None
        self.invincibility = max(0, self.invincibility - self.deltaTime) # Decrease the invincibility timer
        if self.AI:
            #If the tank is an AI, it will move based on the AI's logic
            # current tile
            (currentTiley, currentTilex) = ((self.getCenter()[0]-50)//50 + 1, (self.getCenter()[1]-50)//50)
            currentTile = currentTilex * 14 + currentTiley
            currentTarget = self.lastTargetPackage[0]
            for t in self.tileList:
                t.setTarget(False)

            # visualising the BFS
            for tile in self.pseudoTargetarray:
                self.tileList[tile-1].setTarget(True)

            # set the current target tile
            self.tileList[currentTarget-1].setTarget(True)
            self.tileList[self.aim[0]-1].setTarget(True)
            targetTilex, targetTiley = self.lastTargetPackage[1], self.lastTargetPackage[2]

            if currentTile != self.aim[0] and self.BFSRefresh:

                self.BFSRefresh = False
                # we haven't reached the goal
                self.pseudoTargetarray = breathFirstSearchShort(self.tileList, [currentTile, self.aim[0]], 0)
                # needs to wait to be in center of tile
                if self.pseudoTargetarray==[] or self.pseudoTargetarray==None:
                    pass
                else:
                    currentTarget = self.pseudoTargetarray.pop(0) # we have an elemnt in the list
                self.lastTargetPackage = (currentTarget, currentTarget%14*50 + 50//2, ((currentTarget)//14 + 1)*50 + 50//2)

            # we are within the target tile
            if (abs(targetTilex - self.getCenter()[0]) < 10 and abs(targetTiley - self.getCenter()[1]) < 10):

                self.speed = 0
                self.rotationSpeed = 0
                self.BFSRefresh = True
                if self.pseudoTargetarray==[] or self.pseudoTargetarray==None:
                    pass
                else:
                    currentTarget = self.pseudoTargetarray.pop(0) # we have an elemnt in the list
                    #set the new target
                self.lastTargetPackage = (currentTarget, currentTarget%14*50 + 50//2, ((currentTarget)//14 + 1)*50 + 50//2)

            else:
                # we are not on the target tile

                # if we are below the target tile, turn the tank so it will face upwards
                vAngle = math.atan2(targetTilex - self.getCenter()[0], targetTiley - self.getCenter()[1])
                vAngle = math.degrees(vAngle)
                vAngle = (vAngle + 360 - 90) % 360 # we have a rotate coordinate system
                # make it so that the tank will go forward if it is facing the target
                # difference = (vAngle - self.angle) % 360

                #function
                #two inputs vAngle, self.angle
                #one output (+1, -1, 0)
                #The function should check both ways and return the faster method of travelling, this includes the knowledge about the 360 degree rotation
                #The function should return 1 if the tank should rotate clockwise, -1 if the tank should rotate counter clockwise and 0 if the tank should not rotate

                def getRotation(vAngle, angle):
                    deltaNum = 15
                    if vAngle == angle:
                        return 0
                    if vAngle > angle:
                        if vAngle - angle > 180:
                            #return the smaller angle between vAngle, angle and deltaNum
                            return max(-deltaNum, angle - vAngle)//1
                        else:
                            return min(deltaNum, vAngle - angle)//1
                    else:
                        if angle - vAngle > 180:
                            return min(deltaNum, angle - vAngle)//1
                        else:
                            return max(-deltaNum, vAngle - self.angle)//1

                self.rotationSpeed = getRotation(vAngle, self.angle)
                # if we are facing the target, go forward
                if abs(vAngle - self.angle) < 2: #if we are basically matching the target
                    self.speed = self.maxSpeed
                else:
                    self.speed = 0
                # self.speed = self.maxSpeed # I don't like this

        else:
            keys = pygame.key.get_pressed()
            #Movement keys
            if keys[self.controls['up']]:
                self.speed = self.maxSpeed # I don't like this
            elif keys[self.controls['down']]:
                self.speed = -self.maxSpeed # I don't like this
                
            else:
                self.speed = 0

            if keys[self.controls['left']]:
                self.rotationSpeed = self.getRotationalSpeed()
            elif keys[self.controls['right']]:
                self.rotationSpeed = -self.getRotationalSpeed()
            else:
                self.rotationSpeed = 0
            self.rotationSpeed *= self.deltaTime
        #This if statement checks to see if speed or rotation of speed is 0,
        #if so it will stop playing moving sound, otherwise, sound will play
        #indefinitely
        if self.speed != 0 or self.rotationSpeed != 0:
            if not self.channelDict["move"]["channel"].get_busy(): # if the sound isn't playing
                self.channelDict["move"]["channel"].play(self.soundDictionary["tankMove"], loops = -1)  # Play sound indefinitely
        else:
            if self.channelDict["move"]["channel"].get_busy(): # if the sound is playing
                self.channelDict["move"]["channel"].stop()  # Stop playin the sound

        self.angle += self.rotationSpeed
        # self.angle should always be between -360 and 360
        self.angle %= 360
        self.image = pygame.transform.rotate(self.originalTankImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        angleRad = math.radians(self.angle)

        self.changeX += math.cos(angleRad) * self._getSpeed() * self.deltaTime
        self.changeY += math.sin(angleRad) * self._getSpeed() * self.deltaTime

        # Update the tank effect
        for i in range(len(self.effect)):
            if self.effect[i] > 0:
                self.effect[i] -= self.deltaTime
                if self.effect[i] <= 0:
                    self.effect[i] = 0

    def draw(self, screen): # A manual entry of the draw screen so that we can update it with anything else we may need to draw
        if self.invincibility > 0:
            # Draw the tank with a transparent effect
            self.image.set_alpha(31)
        else:
            self.image.set_alpha(255)
        # Draw the tank image
        screen.blit(self.image, self.rect)

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

    def applyDoubleDamage(self):
        # This function will apply double damage to the tank
        # Inputs: None
        # Outputs: None
        self.effect[0] = TIMER_MAX
    
    def applyDoubleArmor(self):
        # This function will apply double armor to the tank
        self.effect[1] = TIMER_MAX
    
    def applySpeedBoost(self):
        self.effect[2] = TIMER_MAX / 3

    def setCoords(self, newx, newy):
        self.x, self.y = newx, newy

    def getCoords(self):
        return [self.rect.x, self.rect.y, self.rect.x + self.originalTankImage.get_size()[0], self.rect.y + self.originalTankImage.get_size()[1]]
    
    def setCentre(self, x, y):
        self.rect.center = (x, y)
        self.x = x # Update the x and y coordinate as well
        self.y = y

    def getCenter(self):
        return self.rect.center

    def isDrawable(self):
        return self.drawable

    def setHealth(self, health):
        self.health = health

    def getHealth(self):
        return self.health

    def setMaxHealth(self, health):
        self.maxHealth = health
        self.health = health

    def getMaxHealth(self):
        return self.maxHealth

    def setHealthStatistic(self, value):
        self.healthStatistic = value

    def getHealthStatistic(self):
        return self.healthStatistic
    
    def setSpeedStatistic(self, value):
        self.speedStatistic = value

    def getSpeedStatistic(self):
        return self.speedStatistic

    def setTankName(self, tankName):
        self.tankName = tankName

    def getTankName(self):
        return self.tankName
    
    def getName(self):
        return self.name
    
    def setRotationalSpeed(self, speed):
        self.rotationalSpeed = speed

    def getRotationalSpeed(self):
        return self.rotationalSpeed * (1.5 if (self.effect[2] != 0) else 1)

    def setTopRotationalSpeed(self, speed):
        self.topRotation = speed
        self.rotationalSpeed = speed

    def getTopRotationalSpeed(self):
        return self.topRotation
    
    def resetRotationalSpeed(self):
        self.rotationalSpeed = self.topRotation

    def setSpeed(self, speed):
        self.maxSpeed = speed

    def setTopSpeed(self, speed):
        self.topSpeed = speed
        self.maxSpeed = speed

    def resetMaxSpeed(self):
        self.maxSpeed = self.topSpeed

    def _getSpeed(self): # This is private
        return self.speed * (1.5 if (self.effect[2] != 0) else 1)

    def getSpeed(self):
        return self.topSpeed
    
    def setData(self, data):
        # This function will set up the tanks that are being used
        # Inputs: Data, all the data stored within the packages defined as global variables
        # Outputs: None
        self.controls = data[2]
        self.name = data[3]
        # self.rect = self.tankImage.get_rect(center=(data[0], data[1]))
        # self.x = float(self.rect.centerx)
        # self.y = float(self.rect.centery)
        self.x = data[0]
        self.y = data[1]
        self.rect = self.tankImage.get_rect(center=(self.x, self.y))

        # set up the audio channels
        self.channelDict = data[4]

    def setImage(self, name = 'tank', imageNum = 1):
        # Setup a new image if the selected one isn't the default
        # Inputs: imageNum: The index that points to the required image
        # Outputs: None
        # Load the tank image
        if getattr(sys, 'frozen', False):  # Running as an .exe
            currentDir = sys._MEIPASS
        else:  # Running as a .py script
            currentDir = os.path.dirname(os.path.abspath(__file__))
        tankPath = os.path.join(currentDir, 'Sprites', str(name) + str(imageNum) + '.png')
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

    def getEffect(self):
        return self.effect, [TIMER_MAX, TIMER_MAX, TIMER_MAX//3]

    def treads(self, treads):
        # This function will draw the treads of the tank
        # Inputs: None
        # Outputs: None
        # Determine the correct base path
        rotated_surface = pygame.transform.rotate(self.tread_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.x, self.y))

        treads.append((rotated_surface, rotated_rect.topleft))
        if (len(treads) > 30):
            treads.pop(0)

    def getCurrentTile(self):
        # This function will return the tile that the tank is currently on
        # Inputs: None
        # Outputs: The tile that the tank is currently on
        row = math.ceil((self.getCenter()[1] - 50)/50)
        col = math.ceil((self.getCenter()[0] - 50)/50)
        index = (row - 1)*14 + col
        return self.tileList[index-1]

    def getAngle(self):
        return self.angle

    def setAim(self, aim):
        self.aimTime = pygame.time.get_ticks()
        self.aim = aim
        self.BFSRefresh = True
        self.lastTargetPackage = aim
    
    def setAI(self, AI):
        self.AI = AI

    def setSoundDictionary(self, soundDictionary):
        self.soundDictionary = soundDictionary

    def settileList(self, tileList):
        self.tileList = tileList

    def setDelta(self, deltaTime):
        # set the delta time that occurs between each frame for refereneing elsewhere
        self.deltaTime = deltaTime

    def getCorners(self):
        # return the corners of the tank
        return self.corners

    def getAimTime(self):
        # This function is used to keep track of the time elapsed since the last aim update (see main.py)
        return self.aimTime

    def setWeight(self, weight):
        self.weight = weight

    def getWeight(self):
        return self.weight

    def getInvincibility(self):
        return self.invincibility

    def setPlayer(self, player):
        self.player = player
    
    def getPlayer(self):
        return self.player

#Hulls
class Bonsai(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(4500)
        self.setSpeedStatistic(2)
        self.setHealthStatistic(2)
        self.setTopSpeed(0.05)
        self.setTopRotationalSpeed(0.133)
        self.setTankName("Bonsai")
        self.setWeight(900)

    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), -5, 0, self.angle)
    
class Cicada(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(2100)
        self.setSpeedStatistic(3)
        self.setHealthStatistic(1)
        self.setTopSpeed(0.09)
        self.setTopRotationalSpeed(0.25)
        self.setTankName("Cicada")
        self.setWeight(233)


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
        self.setTopSpeed(0.08)
        self.setTopRotationalSpeed(0.17)
        self.setTankName("tank")
        self.setWeight(1)


class Fossil(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(5100)
        self.setSpeedStatistic(1)
        self.setHealthStatistic(3)
        self.setTopSpeed(0.04)
        self.setTopRotationalSpeed(0.08)
        self.setTankName("Fossil")
        self.setWeight(1275)


    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), 4, 0, self.angle)
    
class Gater(Tank):

    def __init__(self, x, y, controls, name):
        super().__init__(x, y, controls, name)
        self.setMaxHealth(3300)
        self.setSpeedStatistic(2)
        self.setHealthStatistic(2)
        self.setTopSpeed(0.07)
        self.setTopRotationalSpeed(0.16)
        self.setTankName("Gater")
        self.setWeight(471)


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
        self.setTopSpeed(0.1)
        self.setTopRotationalSpeed(0.22)
        self.setTankName("Panther")
        self.setWeight(150)


    def getGunCenter(self):
        #Since the point is not in the center of the tank, we need to adjust the gun position
        # Inputs: None
        # Outputs: The center of the gun
        return self.rotate_point((self.rect.centerx, self.rect.centery), -4, 0, self.angle)
