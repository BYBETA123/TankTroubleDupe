import pygame
import random
import math
import time
import os
#Classes

# Tank sprite class
class Tank(pygame.sprite.Sprite):
    prin = True
    def __init__(self, x, y, controls, name = "Default"):
        super().__init__()
        try:
            # Load the tank image
            currentDir = os.path.dirname(__file__)
            
            tank_path = os.path.join(currentDir,'Sprites','tank1.png')
            self.originalTankImage = pygame.image.load(tank_path).convert_alpha()
            print(f"Original tank image size: {self.originalTankImage.get_size()}")

            # Scale the tank image to a smaller size
            self.tankImage = pygame.transform.scale(self.originalTankImage, (200, 100))
            print(f"Scaled tank image size: {self.tankImage.get_size()}")
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            pygame.quit()
            exit()

        self.image = self.tankImage
        self.rect = self.tankImage.get_rect(center=(x, y))
        self.name = name
        self.angle = 0
        self.speed = 0
        self.rotationSpeed = 0
        self.controls = controls
        self.center = (x, y)
        self.width, self.height = self.originalTankImage.get_size()
        self.updateCorners()

    def updateCorners(self):
        cx, cy = self.rect.center
        w, h = self.width / 2, self.height / 2
        rad = math.radians(self.angle)
        rad = math.pi * 2 - rad
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        self.corners = [
            (cx + cos_a * -w - sin_a * -h, cy + sin_a * -w + cos_a * -h),
            (cx + cos_a * w - sin_a * -h, cy + sin_a * w + cos_a * -h),
            (cx + cos_a * w - sin_a * h, cy + sin_a * w + cos_a * h),
            (cx + cos_a * -w - sin_a * h, cy + sin_a * -w + cos_a * h),
        ]

    def fixMovement(self, dx, dy):
        # This function checks if the tank is moving out of the maze and corrects it
        # Inputs: dx, dy: The change in x and y coordinates
        # Outputs: The corrected x and y coordinates

        tempX = self.rect.x + dx
        tempY = self.rect.y - dy


        #We are outside of the maze
        if tempX < mazeX:
            tempX = mazeX
        if tempY < mazeY:
            tempY = mazeY
        if tempX > mazeWidth + mazeX - self.originalTankImage.get_size()[0]:
            tempX = mazeWidth + mazeX - self.originalTankImage.get_size()[0]
        if tempY > mazeHeight + mazeY - self.originalTankImage.get_size()[0]:
            tempY = mazeHeight + mazeY - self.originalTankImage.get_size()[0]

        global resetFlag
        if sat_collision(tank1, tank2):
            if self.name == "Player1":
                #If there is a collision here, move the other tank
                    #This player is being pushed
                    tank2.setCoords(tank2.rect.x + dx, tank2.rect.y - dy)
                    tempX = self.rect.x - dx
                    tempY = self.rect.y + dy
            elif self.name == "Player2":
                #If there is a collision here, move the other tank
                    #This player is being pushed
                    tank1.setCoords(tank1.rect.x + dx, tank1.rect.y - dy)
                    tempX = self.rect.x - dx
                    tempY = self.rect.y + dy
            else:
                print("Error: Invalid tank name")

        return tempX, tempY

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[self.controls['up']]:
            self.speed = 1
        elif keys[self.controls['down']]:
            self.speed = -1
        else:
            self.speed = 0

        if keys[self.controls['left']]:
            self.rotationSpeed = 4
        elif keys[self.controls['right']]:
            self.rotationSpeed = -4
        else:
            self.rotationSpeed = 0

        self.angle += self.rotationSpeed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.originalTankImage, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        angleRad = math.radians(self.angle)
        dx = math.cos(angleRad) * self.speed
        dy = math.sin(angleRad) * self.speed
        self.rect.x, self.rect.y = self.fixMovement(dx,dy)


    def getCoords(self):
        return [self.rect.x, self.rect.y, self.rect.x + self.originalTankImage.get_size()[0], self.rect.y + self.originalTankImage.get_size()[1]]

    def getCorners(self):
        return self.corners
    
    def getCenter(self):
        return self.rect.center
    
    def setCoords(self, newx, newy):
        self.center = (newx, newy)
        self.rect.center = self.center


class Gun(pygame.sprite.Sprite):
    def __init__(self, tank, controls):
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
        self.gunLength = -17
        self.gunRotationDirection = 0
        self.tipOffSet = 30
        self.controls = controls

        self.originalGunLength = self.gunLength
        self.gunBackStartTime = 0
        self.gunBackDuration = 200
        self.canShoot = True
        self.shootCooldown = 0
        self.cooldownDuration = 3000
        self.lastUpdateTime = pygame.time.get_ticks()

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
        if keys[self.controls['rotate_left']]:
            self.rotationSpeed = 2
        elif keys[self.controls['rotate_right']]:
            self.rotationSpeed = -2
        elif  keys[self.controls['left']]:
            self.rotationSpeed = 4
        elif keys[self.controls['right']]:
            self.rotationSpeed = -4
        else:
            self.rotationSpeed = 0

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

        if self.shootCooldown > 0:
            self.shootCooldown -= pygame.time.get_ticks() - self.lastUpdateTime
        else:
            self.canShoot = True

        self.lastUpdateTime = pygame.time.get_ticks()

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
        self.speed = 10

        angleRad = math.radians(self.angle)

        dx = (gunLength + tipOffSet - 32) * math.cos(angleRad)
        dy = -(gunLength + tipOffSet - 32) * math.sin(angleRad)

        self.rect = self.bulletImage.get_rect(center=(x + dx, y + dy))
        self.startX = self.rect.centerx
        self.startY = self.rect.centery

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
        self.rect.x += dx
        self.rect.y += dy

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
            self.color = GREEN
        self.border = self.borderControl()
        self.neighbours = self.neighbourCheck()

    def neighbourCheck(self):
        #This function will return a list of the indexes of the neighbours based on the current list of border
        # No inputs are needed
        # The output will be an updated list of neighbours
        #
        neighbours = [self.index - colAmount, self.index + 1, self.index + colAmount, self.index - 1]
        #Check if there are any invalid neighbours
        newlist = []
        for idx, neighbour in enumerate(neighbours):
            if neighbour < 1 or neighbour > rowAmount*colAmount:
                #We do not want this
                pass
            elif self.border[idx] == True:
                #We do not want this
                pass
            else:
                newlist.append(neighbour)
        return newlist

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
        #If the tile is surrounded by walls then it should be black
        true_count = 0
        for b in border:
            if b:
                true_count += 1
        if true_count == 4:
            self.color = BLACK

        return border


    def drawText(self, screen):
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(str(self.index), True, BLACK)
        screen.blit(text, [self.x + tileSize/2 - text.get_width()/2, self.y + tileSize/2 - text.get_height()/2])

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.x, self.y, tileSize, tileSize])
        #Draw the border
        if self.border[0]:
            pygame.draw.line(screen, BLACK, [self.x, self.y], [self.x+tileSize, self.y], self.borderWidth)
        if self.border[1]:
            pygame.draw.line(screen, BLACK, [self.x + tileSize, self.y], [self.x+tileSize, self.y+tileSize], self.borderWidth)
        if self.border[2]:
            pygame.draw.line(screen, BLACK, [self.x, self.y + tileSize], [self.x+tileSize, self.y+tileSize], self.borderWidth)
        if self.border[3]:
            pygame.draw.line(screen, BLACK, [self.x, self.y], [self.x, self.y+tileSize], self.borderWidth)

        #Draw the index
        # self.drawText(screen)

    def getNeighbours(self):
        return self.neighbours

    def getIndex(self):
        return self.index

    def setBorder(self, borderidx):
        self.border[borderidx] = True
        self.neighbours = self.neighbourCheck() # Update the neighbours list

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

    def breathFirstSearch(tileList, choices):
        # This function will search the maze in a breath first manner to see if we can reach the second spawn
        # Inputs: tileList: The current list of tiles
        # Inputs: Choices: The locations of both spawns
        # Outputs: True if the second spawn is reachable, False otherwise


        #Setting up the BFS
        visitedQueue = []
        tracking = [False for i in range(rowAmount*colAmount+1)]
        queue = [choices[0]]
        visitedQueue.append(choices[0])
        tracking[choices[0]] = True
        while len(queue) > 0: # While there are still elements to check
            current = queue.pop(0)
            for neighbour in tileList[current-1].getNeighbours():
                if not tracking[neighbour]:
                    queue.append(neighbour)
                    visitedQueue.append(neighbour)
                    tracking[neighbour] = True

        if choices[1] in visitedQueue: # If the second spawn is reachable
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

                tileList.append(Tile(index, i,j,RED, spawn))
                index += 1

        #Validate the tileList
        validMaze = breathFirstSearch(tileList, choices)
        global spawnpoint
        spawnpoint = []
        spawnpoint = choices
    return tileList


# Helper functions for SAT
def get_edges(corners):
    edges = []
    for i in range(len(corners)):
        edge = (corners[i][0] - corners[i - 1][0], corners[i][1] - corners[i - 1][1])
        edges.append(edge)
    return edges

def get_perpendicular_vector(edge):
    return (-edge[1], edge[0])

def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def project_polygon(corners, axis):
    min_proj = dot_product(corners[0], axis)
    max_proj = min_proj
    for corner in corners[1:]:
        projection = dot_product(corner, axis)
        if projection < min_proj:
            min_proj = projection
        if projection > max_proj:
            max_proj = projection
    return min_proj, max_proj

def overlap(proj1, proj2):
    return proj1[0] < proj2[1] and proj2[0] < proj1[1]

def sat_collision(rect1, rect2):
    for rect in [rect1, rect2]:
        edges = get_edges(rect.corners)
        for edge in edges:
            axis = get_perpendicular_vector(edge)
            proj1 = project_polygon(rect1.corners, axis)
            proj2 = project_polygon(rect2.corners, axis)
            if not overlap(proj1, proj2):
                return False
    return True


#Constants
done = False
windowWidth = 800
windowHeight = 600
tileSize = 50
weightTrue = 0.33
rowAmount = 14
colAmount = 8
#Colors
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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


eventFlag = False # This flag is just for debugging purposes

barWidth = 150
barHeight = 20

#Start the game setup
pygame.init()
pygame.display.set_caption("TankTroubleDupe") # Name the window
#Keeping the mouse and its location
mouse = pygame.mouse.get_pos()

#Setting up the window
screen = pygame.display.set_mode((windowWidth,windowHeight))

tileList = tileGen()
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

# Create two tank instances with different controls
tank1 = Tank(spawnTank1[0], spawnTank1[1], controlsTank1, "Player1")
tank2 = Tank(spawnTank2[0], spawnTank2[1], controlsTank2, "Player2")
gun1 = Gun(tank1, controlsTank1)
gun2 = Gun(tank2, controlsTank2)

allSprites = pygame.sprite.Group()
allSprites.add(tank1, gun1, tank2, gun2)
bulletSprites = pygame.sprite.Group()


bg = GREY
resetFlag = True

#Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
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
                weightTrue += 0.01
                print("The current weight is: ", weightTrue)
            if event.key == pygame.K_j:
                weightTrue -= 0.01
                print("The current weight is: ", weightTrue)
            if event.key == pygame.K_k:
                print(get_edges(tank1.corners))
                print(get_edges(tank2.corners))
            if event.key == pygame.K_n:
                tileList = tileGen()
                spawnTank1 = [tileList[spawnpoint[0]-1].x + tileSize//2, tileList[spawnpoint[0]-1].y + tileSize//2]
                spawnTank2 = [tileList[spawnpoint[1]-1].x + tileSize//2, tileList[spawnpoint[1]-1].y + tileSize//2]
                tank1.setCoords(spawnTank1[0], spawnTank1[1])
                tank2.setCoords(spawnTank2[0], spawnTank2[1])
            if event.key == pygame.K_0:
                tileList = tileGen()
                spawnTank1 = [tileList[spawnpoint[0]-1].x + tileSize//2, tileList[spawnpoint[0]-1].y + tileSize//2]
                spawnTank2 = [tileList[spawnpoint[1]-1].x + tileSize//2, tileList[spawnpoint[1]-1].y + tileSize//2]
                tank1.setCoords(spawnTank1[0], spawnTank1[1])
                tank2.setCoords(spawnTank2[0], spawnTank2[1])

    mouse = pygame.mouse.get_pos() #Update the position

    screen.fill(bg) # This is the first line when drawing a new frame

    # Draw the score

    #Making the string for score
    p1ScoreText = str(p1Score)
    p2ScoreText = str(p2Score)
    
    #Setting up the text
    fontScore = pygame.font.SysFont('Calibri', 100, True, False)
    fontName = pygame.font.SysFont('Calibri', 35, True, False)
    # Player 1 Text
    textp1 = fontScore.render(p1ScoreText, True, WHITE)
    textp1Name = fontName.render("Player 1", True, WHITE)

    # Player 2 Text
    textp2 = fontScore.render(p2ScoreText, True, WHITE)
    textp2Name = fontName.render("Player 2", True, WHITE)

    #Misc Text
    text3 = fontScore.render("-",True,WHITE)

    #Visualing player 1
    screen.blit(textp1,[windowWidth/2 - textp1.get_width()-text3.get_width()/2, 0.8*windowHeight]) # This is the score on the left
    screen.blit(textp1Name,[p1NameIndent, 0.783*windowHeight]) # This is the name on the left
    #Health bars outline
    #Health bar
    pygame.draw.rect(screen, RED, [p1NameIndent, 0.8*windowHeight + textp1Name.get_height(), barWidth*((100-p1Score)/100), barHeight]) # Bar
    pygame.draw.rect(screen, BLACK, [p1NameIndent, 0.8*windowHeight + textp1Name.get_height(), barWidth, barHeight], 2) # Outline
    #Reload bars
    pygame.draw.rect(screen, BLUE, [p1NameIndent, 0.8*windowHeight + textp1Name.get_height() + 25, barWidth, barHeight]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, BLACK, [p1NameIndent, 0.8*windowHeight + textp1Name.get_height() + 25, barWidth, barHeight], 2) # Outline
    #Visualising player 2
    screen.blit(textp2,[windowWidth/2 + text3.get_width()*1.5, 0.8*windowHeight]) # This is the score on the right
    screen.blit(textp2Name,[p2NameIndent - textp2Name.get_width(), 0.783*windowHeight]) # This is the name on the left
    #Health bars
    pygame.draw.rect(screen, RED, [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height(), barWidth, barHeight])
    pygame.draw.rect(screen, GREY, [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height(), barWidth*(1-(100-p2Score)/100), barHeight])
    pygame.draw.rect(screen, BLACK, [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height(), barWidth, barHeight], 2)
    #Reload bars
    pygame.draw.rect(screen, BLUE, [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height() + 25, barWidth, barHeight]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, BLACK, [p2NameIndent - barWidth, 0.8*windowHeight + textp2Name.get_height() + 25, barWidth, barHeight], 2) # Outline

    # Misc text and other little pieces
    screen.blit(text3,[windowWidth/2,0.79*windowHeight])

    # Draw the border
    pygame.draw.rect(screen, BLACK, [mazeX, mazeY, mazeWidth,mazeHeight], 1) # The maze border


    for tile in tileList:
        tile.draw(screen)

    #Anything below here will be drawn on top of the maze

    #Update the location of the corners
    tank1.updateCorners()
    tank2.updateCorners()

    allSprites.update()
    bulletSprites.update()
    allSprites.draw(screen)
    bulletSprites.draw(screen)

    pygame.time.Clock().tick(120)

    pygame.display.flip()# Update the screen

pygame.quit()