import pygame
import random
#Classes
tileSize = 50
weightTrue = 0.27
rowamount = 14
colamount = 8


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
        neighbours = [self.index - colamount, self.index + 1, self.index + colamount, self.index - 1]
        #Check if there are any invalid neighbours
        newlist = []
        for idx, neighbour in enumerate(neighbours):
            if neighbour < 1 or neighbour > rowamount*colamount:
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
        if localIndex in range(1, colamount+1):
            border[0] = True
        # Right Row
        if localIndex in range(colamount, rowamount*colamount+1, colamount):
            border[1] = True
        # Bottom Row
        if localIndex in range(99, rowamount*colamount + 1):
            border[2] = True
        #Left Row
        if localIndex in range(1, rowamount*colamount, colamount):
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
        self.drawText(screen)

    def getNeighbours(self):
        return self.neighbours

    def getIndex(self):
        return self.index

    def setBorder(self, borderidx):
        self.border[borderidx] = True
        self.neighbours = self.neighbourCheck() # Update the neighbours list

#Functions
def TileGen():
    # This function is responsible for generating the tiles for the maze
    # Inputs: No inputs
    # Outputs: A list of tiles that make up the maze
    #



    def ValidateChoice(option, choices):
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
            # print("Rowamount: ", rowamount, "Colamount: ", colamount)
            row1, col1 = choices[0]//colamount, choices[0]%colamount
            row2, col2 = option//colamount, option%colamount

            if abs(col1-col2) < columnOffset:
                print("Column Check Failed, ", col1, col2, "Difference: ", abs(col1-col2), "Offset: ", columnOffset)
                return False
            if abs(row1-row2) < rowOffset:
                print("Row Check Failed, ", row1, row2, "Difference: ", abs(row1-row2), "Offset: ", rowOffset)
                return False
            #If they are edge cases, try the other side
            if col1 == 0:
                col1 = rowamount
            if col2 == 0:
                col2 = rowamount
            if row1 == 0:
                row1 = colamount
            if row2 == 0:
                row2 = colamount

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

    def BreathFirstSearch(tileList, choices):
        # This function will search the maze in a breath first manner to see if we can reach the second spawn
        # Inputs: tileList: The current list of tiles
        # Inputs: Choices: The locations of both spawns
        # Outputs: True if the second spawn is reachable, False otherwise


        #Setting up the BFS
        visitedQueue = []
        tracking = [False for i in range(rowamount*colamount+1)]
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
        choice = [i for i in range(1,rowamount*colamount+1)] # Make all the choices
        choices = []
        option = random.choice(choice) # Select the spawn zones
        failsafe = 0
        while len(choices) < 2 and failsafe < 10: # We only 2 spawns
            if ValidateChoice(option, choices):
                choices.append(option)
                tempchoice = choices.copy()
                #Remove close choices that are invalid so that we can choose a valid one more easily
                for i in range(2, len(choice)):
                    row1, col1 = choices[0]//colamount, choices[0]%colamount
                    row2, col2 = i//colamount, i%colamount
                    if abs(col1-col2) >= 6 and abs(row1-row2) >= 3:
                        tempchoice.append(i)
            option = random.choice(tempchoice) # Try again
            failsafe += 1
        if failsafe == 10: # In case we are running for too long
            print("Failsafe activated")
            choices = [1,rowamount*colamount]
        for j in range(mazeY, mazeHeight + 1, tileSize): # Assign the tiles and spawns once everything is found
            for i in range(mazeX, mazeWidth + 1, tileSize):
                if index in choices:
                    spawn = True
                else:
                    spawn = False

                tileList.append(Tile(index, i,j,RED, spawn))
                index += 1

        #Validate the tileList
        validMaze = BreathFirstSearch(tileList, choices)


    #Now that we have a valid maze, update all the neighbors so that the walls are double bordered
    for tile in tileList:
        neighboringTiles = tile.getNeighbours()
        #Write a list of the neighbors which need to be double bordered
        doubleBorder = []
        allNeighbours = [tile.getIndex() - colamount, tile.getIndex() + 1, tile.getIndex() + colamount, tile.getIndex() - 1]

        for i in range(len(allNeighbours)):
            if allNeighbours[i] not in neighboringTiles:
                doubleBorder.append(allNeighbours[i])
            else:
                doubleBorder.append(None)
        #Validate the data
        for i in range(len(doubleBorder)):
            if doubleBorder[i] is not None and (doubleBorder[i] < 1 or doubleBorder[i] > rowamount*colamount):
                doubleBorder[i] = None
        #Can be optimised out?
        for i in range(len(doubleBorder)):
            if doubleBorder[i] is not None:
                tileList[doubleBorder[i]-1].setBorder(i)

    return tileList

#Constants
done = False
windowWidth = 800
windowHeight = 600

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


rowamount = mazeHeight//tileSize # Assigning the amount of rows
colamount = mazeWidth//tileSize # Assigning the amount of columns


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

tileList = TileGen()

#Main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN: # Any key pressed
            if event.key == pygame.K_ESCAPE: # Escape hotkey to quit the window
                done = True
            if event.key == pygame.K_w:
                p1Score += 5
            if event.key == pygame.K_e:
                p2Score += 5
            if event.key == pygame.K_s:
                p1Score -= 5
            if event.key == pygame.K_d:
                p2Score -= 5
            if event.key == pygame.K_i:
                print("The current mouse position is: ", mouse)
            if event.key == pygame.K_o:
                pass
            if event.key == pygame.K_j:
                pass
            if event.key == pygame.K_k:
                pass
            if event.key == pygame.K_n:
                tileList = TileGen()


    mouse = pygame.mouse.get_pos() #Update the position

    screen.fill(GREY) # This is the first line when drawing a new frame

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

    pygame.display.flip()# Update the screen

pygame.quit()