import pygame
import tkinter as tk
from tkinter import filedialog
import os
import random
from tile import Tile  # Assuming Tile is defined in Tile.py
from ColorDictionary import ColourDictionary as c # colors

pygame.init()

root = tk.Tk()
root.withdraw()  # Hide the root window

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
    print(f"Starting BFS from {choices[option]} to {choices[(option +1) % 2]}")
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
        # currentNode = predecessors[currentNode]
        try:
            currentNode = predecessors[currentNode]
        except KeyError:
            currentNode = None  # If the key is not found, we set it to None
            print(f"KeyError: {currentNode} not found in predecessors")  # Debugging line
            break # if the key is not found, we break out of the loop
    # remove the first element
    # path.pop(0)
    return path

# tkinter functions
def saveFile():
    path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir = os.path.dirname(os.path.abspath(__file__)), filetypes=[("Text files", "*.txt")])
    # verify the maze is correct
    if not generate(squares):
        # we are in trouble
        print("Error: File not saved")
        return False
    if path:
        with open(path, 'w') as f:
            # Save the data to the file
            for s in squares:
                f.write(f"{s.x}||{s.y}||{s.color}||{s.width}||{s.height}||{s.index}||{s.borderindex}||{s.getSpecialCode()}\n")
        print("File saved successfully!")

def loadFile():
    path = filedialog.askopenfilename(initialdir = os.path.dirname(os.path.abspath(__file__)), filetypes=[("Text files", "*.txt")])
    if path:
        with open(path, 'r') as f:
            # Load the data from the file
            # we'll make this part up later
            global squares
            squares = []
            for line in f:
                l = line.strip().split("||")
                # cast the string to a tuple

                t = l[2][1:-1].split(",")

                temp = makerTile(int(l[0]), int(l[1]), int(l[5]), (int(t[0]),int(t[1]),int(t[2])), int(l[3]), int(l[4]))
                temp.borderindex = int(l[6])
                temp.setSpecial(int(l[7]))
                squares.append(temp)

        print("File loaded successfully!")

class makerTile(Tile):
    def __init__(self, x, y, index, color = (198, 198, 198), height = 50, width = 50):
        super().__init__(int(index), x, y, color)
        self.height = height
        self.width = width
        self.spawnpoint = 0
        
    def update(self, squares): # idk if this needs to be changed
        # update the current borders
        print("Updating borders for tile", self.index)
        # we only care about the current borders
        neighbours = [self.index - 1, self.index + 14, self.index + 1, self.index - 14] # revered because its weird
        for idx, neighbour in enumerate(neighbours):
            if neighbour < 1 or neighbour > 8*12:
                #We do not want this
                continue
            neighbor = squares[neighbour - 1]
            opposite_idx = (idx + 2) % 4
            opposite_bit = 1 << opposite_idx

            neighbor.borderindex &= ~opposite_bit
            if self.borderindex & (1 << idx):
                # print(f"Setting border for tile {self.index} to {neighbor.index} at index {idx}")
                neighbor.borderindex |= opposite_bit
                neighbor.setBorderIndex((neighbor.borderindex | opposite_bit))
            else:
                # print(f"Removing border for tile {self.index} to {neighbor.index} at index {idx}")
                neighbor.borderindex &= ~opposite_bit
                neighbor.setBorderIndex((neighbor.borderindex & ~opposite_bit))
        self.neighbours, self.bordering = self.neighbourCheck()
        print(f"Tile {self.index} neighbours: {self.neighbours}, bordering: {self.bordering}")
    
    def draw(self, screen): # I think we need to override this method
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.height, self.width])

        match self.borderindex: # 0 - 15
            case 0:
                # nothing
                pass
            case 1:
                # West (0001)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x, self.y+self.width - 1], 1) # West
            case 2:
                # South (0010)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y + self.width - 1], [self.x+self.height - 1, self.y+self.width - 1], 1) # South
            case 3:
                # South West (0011)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x, self.y + self.width - 1], [self.x + self.height - 1, self.y + self.width - 1]], 1) # South West
            case 4:
                # East (0100)
                pygame.draw.line(screen, (0,0,0), [self.x + self.height - 1, self.y], [self.x+self.height - 1, self.y+self.width - 1], 1) # East
            case 5:
                # East West (0101)
                pygame.draw.line(screen, (0,0,0), [self.x + self.height - 1, self.y], [self.x+self.height - 1, self.y+self.width - 1], 1) # East
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x, self.y+self.width - 1], 1) # West
            case 6:
                # South East (0110)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y + self.width - 1], [self.x+self.height - 1, self.y+self.width - 1], [self.x + self.height - 1, self.y]], 1) # South East
            case 7:
                # South East West (0111)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x, self.y + self.width-1], [self.x + self.height - 1, self.y + self.width-1], [self.x + self.height - 1, self.y]], 1)
            case 8:
                # North (1000)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x+self.height - 1, self.y], 1) # North
            case 9:
                # North West (1001)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x + self.height - 1, self.y], [self.x, self.y], [self.x, self.y+self.width - 1]], 1) # North West
            case 10:
                # North South (1010)
                pygame.draw.line(screen, (0,0,0), [self.x, self.y], [self.x+self.height - 1, self.y], 1) # North
                pygame.draw.line(screen, (0,0,0), [self.x, self.y + self.width - 1], [self.x+self.height - 1, self.y+self.width - 1], 1) # South
            case 11:
                # North South West (1011)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x + self.height - 1, self.y], [self.x, self.y], [self.x, self.y+self.width-1], [self.x + self.height - 1, self.y + self.width-1]], 1) # North South West
            case 12:
                # North East (1100)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x+self.height - 1, self.y], [self.x + self.height - 1, self.y + self.width - 1]], 1)
            case 13:
                # North East West (1101)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y+self.width], [self.x, self.y], [self.x + self.height - 1, self.y], [self.x + self.height - 1, self.y + self.width]], 1) # North East West
            case 14:
                # North South East (1110)
                pygame.draw.lines(screen, (0,0,0), False, [[self.x, self.y], [self.x+self.height -1, self.y], [self.x + self.height -1, self.y + self.width -1], [self.x, self.y + self.width -1]], 1) # North South East
            case 15:
                # North South East West (1111)
                pygame.draw.rect(screen, (0,0,0), [self.x, self.y, self.height, self.width], 1) # all

        # special draw
        if self.spawnpoint: # automatically filters 0
            pygame.draw.rect(screen, self.spawnColor(), [self.x + self.height // 2 - 10, self.y + self.width // 2 - 10, 20, 20])

        if self.flag: # automatically filters 0
            pygame.draw.polygon(screen, self.spawnColor(), [[self.x + 35, self.y + 25], [self.x + 20, self.y + 35], [self.x + 20, self.y + 15]])

        if self.AITarget:
            pygame.draw.rect(screen, (0, 0, 255), [self.x + self.height//2 - 5, self.y + self.width//2 - 5, 10, 10]) # draw a green square in the center)

    def drawUpdate(self, screen):
        # if we are a debug tile, draw a small square in the center

        if self.flag: # automatically filters 0
            # if self.flagPicked:
            pygame.draw.polygon(screen, (self.spawnColor()), [[self.x + 35, self.y + 25], [self.x + 20, self.y + 35], [self.x + 20, self.y + 15]])

    def broder(self, move = 1):
        print(self.border) # why does this already have something
        self.setBorderIndex((self.borderindex + move) % 16)
        # go through the neighbours and update them
        self.update(squares)  # update the borders for this tile
        # for each of the neighbours, we need to update the borders

    def setSpawnpoint(self):
        self.flag = 0
        self.spawnpoint = (self.spawnpoint+1) % 3 # 0 = no spawn 1 = blue 2 = red
        print(f"Set spawnpoint as {self.spawnpoint}")

    def setFlag(self): # if the flag is set we can't have a spawnpoint
        self.spawnpoint = 0
        self.flag = (self.flag+1) % 3 # 0 = no spawn 1 = blue 2 = red
        print(f"Set spawnpoint as {self.flag}")

    def reset(self):
        self.color = (198, 198, 198) # for the eraser tool
        self.borderindex = 0
        self.border = [False, False, False, False]
        self.update(squares)
        self.spawnpoint = 0
        self.flag = 0

    def debug(self):
        print(f"Tile {self.index}")
        print(r"{0:04b}".format(self.borderindex))
    
    def setSpecial(self, num):
        if num == 1:
            self.spawnpoint = 1
        if num == 2:
            self.spawnpoint = 2
        if num == 3:
            self.flag = 1
        if num == 4:
            self.flag = 2

    def spawnColor(self):
        if self.flag == 1 or self.spawnpoint == 1:
            return c.geT("RED")
        if self.flag == 2 or self.spawnpoint == 2:
            return c.geT("BLUE")
        return c.geT("BLACK")

    def getSpecialCode(self):

        if self.spawnpoint == 1:
            return 1 # 1 is for red team spawnpoint
        if self.spawnpoint == 2:
            return 2 # 2 is for blue team spawnpoint
        if self.flag == 1:
            return 3 # 3 is for red team flag
        if self.flag == 2:
            return 4 # 4 is for blue team flag

        return 0 # nothing

screen = pygame.display.set_mode((800,600))  # Windowed (safer/ superior)

def getIndex(i,j):
    # calcualte the respective position that i and j are in
    i_calc = i/50-1
    j_calc = j/50-1
    result = i_calc * 14 + j_calc + 1
    return result

def randomGen(tiles):
    def rg():
        return random.choices([True, False], weights = (0.16, 1-0.16))[0]
    for t in tiles:
        t.reset()
    for t in tiles:
        t.setBorderIndex((t.borderindex | (rg()*8 + rg() * 4 + rg() * 2 + rg())))

def generate(tiles):
    # check that everything is good to go
    # go around the edge and make the borders true
    spawnRed = []
    spawnBlue = []
    returnType = True
    for t in tiles:
        if t.index in range(1,112, 14):
            t.setBorderIndex((t.borderindex | 1))
        if t.index in range(99, 113):
            t.setBorderIndex((t.borderindex | 2))
        if t.index in range(14, 113, 14):
            t.setBorderIndex((t.borderindex | 4))
        if t.index in range(1, 15):
            t.setBorderIndex((t.borderindex | 8))

        # count the number of tiles with spanpoints
        if t.spawnpoint == 1:
            spawnRed.append(t)
        if t.spawnpoint == 2:
            spawnBlue.append(t)
    # verification
    # we need to make sure that the spawnpoints are far apart from each other

    # if the amount of spawnpoints is not 8 then we need to flag it
    if len(spawnRed) != 4 and len(spawnBlue) != 4: # if we have 4 slots for each team
        print(f"Error: Spawnpoints are not correct: Red: {spawnRed} {len(spawnRed)} Blue: {spawnBlue} {len(spawnBlue)}")
        returnType = False

    return returnType

def findBetween(tiles, start, end):
    # This function will find the tiles between the two spawnpoints
    # Inputs: tiles: The current list of tiles
    # Inputs: start: The first spawnpoint
    # Inputs: end: The second spawnpoint
    # Outputs: A list of tiles between the two spawnpoints

    choices = [start, end]
    print(f"Finding path between {start} and {end}")
    if start is None or end is None:
        print("Exit early: None Type")
        return []
    path = breathFirstSearchShort(tiles, choices, 0)
    # we have a path?
    if path is None or len(path) == 0:
        print("Exit early: No path found")
        return []
    # we have a path, now we need to set the borders
    for s in squares:
        s.setTarget(False)  # reset all targets
    for p in path:
        squares[p-1].setTarget(True)
    print(f"Path found: {path}")
    return path

# draw a 14 x 8 grid of 50 x 50 squares
squares = []
start_x = 50
start_y = 50
for j in range(start_y, 450, 50):
    for i in range(start_x, 750, 50):
        squares.append(makerTile(i,j, getIndex(j,i), (198, 198, 198), 50, 50))

for s in squares:
    # wipe all borders
    s.borderindex = 0
    s.border = [False, False, False, False] # [North, East, South, West]

currentTool = 1 # eraser
done = False
t1 = None
t2 = None

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if event.button == 1:
                # find which tile the mouse is in
                for s in squares:
                    if s.isWithin(mouse):
                        # since we did something in the file, we need to set the correct thing based on the currently selected tool
                        if currentTool == 1: # eraser
                            s.reset()
                        elif currentTool == 2: # pen tool
                            s.broder(1)
                            s.update(squares)
                            s.drawUpdate(screen)
                        elif currentTool == 3: # spawnpoints
                            s.setSpawnpoint()
                        elif currentTool == 4: # flag
                            s.setFlag()
                        else:
                            s.setColor((255, 0, 0))

            elif event.button == 3: # right click

                # find which tile the mouse is in
                for s in squares:
                    if s.isWithin(mouse):
                        # we are in this tile
                        t1 = t2
                        t2 = int(s.index)
                findBetween(squares, t1, t2)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print("Setting to Eraser")
                currentTool = 1
            elif event.key == pygame.K_2:
                print("Setting to pen")
                currentTool = 2
            elif event.key == pygame.K_3:   
                print("Setting to add spawnpoints")
                currentTool = 3
            elif event.key == pygame.K_4:
                print("Setting to add flags")
                currentTool = 4
            elif event.key == pygame.K_5:
                print("Key 5 pressed")
            elif event.key == pygame.K_6:
                print("Key 6 pressed")
            elif event.key == pygame.K_7:
                print("Key 7 pressed")
            elif event.key == pygame.K_8:
                print("Key 8 pressed")
            elif event.key == pygame.K_9:
                print("Key 9 pressed")
            elif event.key == pygame.K_0:
                print("Key 0 pressed")
            elif event.key == pygame.K_ESCAPE:
                done = True # end
            elif event.key == pygame.K_i:
                # info
                for s in squares:
                    if s.isWithin(pygame.mouse.get_pos()):
                        s.printDebug()
            elif event.key == pygame.K_g:
                generate(squares) # make it ready
            elif event.key == pygame.K_s:
                saveFile()
            elif event.key == pygame.K_l:
                l = loadFile()
                if l:
                    # load the file
                    squares = l
            elif event.key == pygame.K_r:
                randomGen(squares)

    screen.fill((217,217,217))
    # draw the grid of squres
    for s in squares:
        s.draw(screen)
        s.drawUpdate(screen)

    # draw the options at the bottom
    pygame.display.flip()

pygame.quit()
