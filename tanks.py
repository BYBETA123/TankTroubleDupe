import pygame
import math
import os
# Main variables



#helper functions
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

    def update(self):
        # This function updates the tank's position and rotation based on the controls detected
        # from the keyboard sound effects will be played as well as the sound effects
        # Inputs: None
        # Outputs: None
        if self.AI:
            #If the tank is an AI, it will move based on the AI's logic
            # current tile
            (currentTiley, currentTilex) = ((self.getCenter()[0]-50)//50 + 1, (self.getCenter()[1]-50)//50)
            currentTile = currentTilex * 14 + currentTiley
            
            currentTarget = self.lastTargetPackage[0]

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

            if (targetTilex == self.getCenter()[0] and targetTiley == self.getCenter()[1]): # if we match our target tile
                self.speed = 0
                self.rotationSpeed = 0
                self.BFSRefresh = True
                if self.pseudoTargetarray==[] or self.pseudoTargetarray==None:
                    pass
                else:
                    currentTarget = self.pseudoTargetarray.pop(0) # we have an elemnt in the list
                self.lastTargetPackage = (currentTarget, currentTarget%14*50 + 50//2, ((currentTarget)//14 + 1)*50 + 50//2)
            else:
                # we are not on the target tile

                # if we are below the target tile, turn the tank so it will face upwards
                vAngle = math.atan2(targetTilex - self.getCenter()[0], targetTiley - self.getCenter()[1])
                vAngle = math.degrees(vAngle)
                vAngle = (vAngle + 360 - 90) % 360 # we have a rotate coordinate system
                
                # make it so that the tank will go forward if it is facing the target
                difference = (vAngle - self.angle) % 360
                if difference >180:
                    difference -= 360
                if difference < 0:
                    self.rotationSpeed = -1
                elif difference > 0:
                    self.rotationSpeed = 1
                else:
                    self.rotationSpeed = 0
                # if we are facing the target, go forward
                self.speed = self.topSpeed # we move
        else:
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
            if not self.channelDict["move"]["channel"].get_busy(): # if the sound isn't playing
                self.channelDict["move"]["channel"].play(self.soundDictionary["tankMove"], loops = -1)  # Play sound indefinitely
        else:
            if self.channelDict["move"]["channel"].get_busy(): # if the sound is playing
                self.channelDict["move"]["channel"].stop()  # Stop playin the sound

        self.angle += self.rotationSpeed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.originalTankImage, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))

        angleRad = math.radians(self.angle)
        self.changeX += math.cos(angleRad) * self.speed
        self.changeY += math.sin(angleRad) * self.speed

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
        # set up the audio channels
        self.channelDict = data[4]

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

    def treads(self, treads):
        # This function will draw the treads of the tank
        # Inputs: None
        # Outputs: None
        rect_surface = pygame.image.load("./Assets/Treads.png").convert_alpha()
        rect_surface = pygame.transform.scale(rect_surface, (self.originalTankImage.get_size()))


        rotated_surface = pygame.transform.rotate(rect_surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center = (self.x, self.y))

        treads.append((rotated_surface, rotated_rect.topleft))
        if (len(treads) > 15):
            treads.pop(0)

        # if num:
        #     treadsp1.append((rotated_surface, rotated_rect.topleft))
        #     if len(treadsp1) > 15:
        #         treadsp1.pop(0)
        # if not num:
        #     treadsp2.append((rotated_surface, rotated_rect.topleft))
        #     if len(treadsp2) > 15:
        #         treadsp2.pop(0)

    def getCurrentTile(self):
        # This function will return the tile that the tank is currently on
        # Inputs: None
        # Outputs: The tile that the tank is currently on
        row = math.ceil((self.getCenter()[1] - 50)/50)
        col = math.ceil((self.getCenter()[0] - 50)/50)
        index = (row-1)*8 + col
        return self.tileList[index-1]

    def getAngle(self):
        return self.angle

    def setAim(self, aim):
        self.aimTime = pygame.time.get_ticks()
        self.aim = aim
        self.BFSRefresh = True
        self.lastTargetPackage = aim

    def getAimTime(self):
        return self.aimTime
    
    def setAI(self, AI, currentTargetPackage):
        self.AI = AI
        self.lastTargetPackage = currentTargetPackage
        self.aim = currentTargetPackage

    def setSoundDictionary(self, soundDictionary):
        self.soundDictionary = soundDictionary

    def settileList(self, tileList):
        self.tileList = tileList
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
