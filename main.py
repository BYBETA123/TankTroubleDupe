import pygame
import random
import math
import time
import os, sys
from ColorDictionary import ColourDictionary as c # colors
from enum import Enum
from UIUtility import Button, TextBox
from music import Music
import copy
from tanks import *
from Screen import *
import constants as const
from timer import UpDownTimer
from Players import Player # maybe this is needed
import globalVariables as g
from guns import *
from bullets import *
from tile import Tile
from DifficultyTypes import *

global timerClock
timerClock = 0
# final set up of the players

global playerlist
playerlist = [Player("Player 1", const.CONTROLS_TANK1, const.PLAYER_1_TANK_NAME, const.PLAYER_1_CHANNELS, const.PLAYER_1_GUN_NAME),
              Player("Player 2", const.CONTROLS_TANK2, const.PLAYER_2_TANK_NAME, const.PLAYER_2_CHANNELS, const.PLAYER_2_GUN_NAME),
              Player("Player 3", None, const.PLAYER_3_TANK_NAME, const.PLAYER_3_CHANNELS, const.PLAYER_3_GUN_NAME),
              Player("Player 4", None, const.PLAYER_4_TANK_NAME, const.PLAYER_4_CHANNELS, const.PLAYER_4_GUN_NAME),
              Player("Player 5", None, const.PLAYER_5_TANK_NAME, const.PLAYER_5_CHANNELS, const.PLAYER_5_GUN_NAME),
              Player("Player 6", None, const.PLAYER_6_TANK_NAME, const.PLAYER_6_CHANNELS, const.PLAYER_6_GUN_NAME),
              Player("Player 7", None, const.PLAYER_7_TANK_NAME, const.PLAYER_7_CHANNELS, const.PLAYER_7_GUN_NAME),
              Player("Player 8", None, const.PLAYER_8_TANK_NAME, const.PLAYER_8_CHANNELS, const.PLAYER_8_GUN_NAME)]

# quick adjustment
for i in range(len(playerlist)):
    playerlist[i].setTeam(i%2) # temporarily set all the players to either team 0 or team 1

treads = [[] for _ in range(8)]

healthColor = ['#330000', '#990000', '#CC0000', '#FF3300', '#FF6600', '#FF9900', '#FFCC00', '#CCFF00', '#99FF33', '#66FF66']

pygame.init()

#Classes
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
    end = 7
    unimplemented = 8

def breathFirstSearch(tileLst, choices, option):
    """
    This function will search the maze in a breadth-first manner to see if we can reach the second spawn
    Inputs: tileLst: The current list of tiles
    Inputs: choices: The locations of both spawns
    Outputs: True if the second spawn is reachable, False otherwise
    """

    #Setting up the BFS
    visitedQueue = []
    tracking = [False for _ in range(const.ROW_AMOUNT*const.COLUMN_AMOUNT+1)]
    queue = [choices[option]]
    visitedQueue.append(choices[option])
    tracking[choices[option]] = True
    while len(queue) > 0: # While there are still elements to check
        current = queue.pop(0)
        for neighbour in tileLst[current-1].getNeighbours():
            if not tracking[neighbour]:
                queue.append(neighbour)
                visitedQueue.append(neighbour)
                tracking[neighbour] = True

    if choices[(option +1) % 2] in visitedQueue: # If the second spawn is reachable
        return True
    else:
        return False

def tileGen(numSpawns = 2): # Default is 2 spawns
    """
    This function generates the tiles for the maze and sets up the spawn points
    Inputs: numSpawns: The number of spawn points to generate
    Outputs: A list of tiles that make up the maze
    """

    def gen():
        """
        This function generates the tiles for the maze
        Inputs: None
        Outputs: A list of tiles that make up the maze with borders randomly generated
        """
        # This function will randomly generate the tiles that make up the background
        # Inputs: None
        # Outputs: A list of tiles that make up the maze
        tempTiles = []
        index = 1
        for j in range(const.MAZE_Y, const.MAZE_HEIGHT + 1, const.TILE_SIZE_Y): # Assign the tiles and spawns once everything is found
            for i in range(const.MAZE_X, const.MAZE_WIDTH + 1, const.TILE_SIZE_X):
                tempTiles.append(Tile(index, i, j, c.geT("LIGHT_GREY"), False))
                index += 1

        # #We need to make sure that all the borders are bordered on both sides
        for tile in tempTiles:
            bordering = tile.getBordering()
            for border in bordering:
                if border != -1:
                    tempTiles[border-1].setBorder((bordering.index(border)+2)%4, tile.border[bordering.index(border)])
        for tile in tempTiles:
            tile.updateBorder()

        return tempTiles

    choices = []
    side = 0 # start with the right

    g.tileList = gen()

    cArrL = [1, 2, 3, 15, 16, 17, 29, 30, 31, 43, 44, 45, 57, 58, 59, 71, 72, 73, 85, 86, 87, 99, 100, 101]
    cArrR = [12, 13, 14, 26, 27, 28, 40, 41, 42, 54, 55, 56, 68, 69, 70, 82, 83, 84, 96, 97, 98, 110, 111, 112]
    option = random.choice(cArrL) # Select the spawn zones
    cArrL.remove(option) # Remove the spawn zone from the list of choices
    choices.append(option) # Add the spawn zone to the list of choices

    while len(choices) < numSpawns:
        while len(cArrL) != 0 and len(cArrR) != 0:
            # we need to generate enough spawns to fill the maximum amount of spawns
            if side:
                # Left
                option = random.choice(cArrL) # Select the spawn zones
                cArrL.remove(option)
            else:
                # Right
                option = random.choice(cArrR) # Select the spawn zones
                cArrR.remove(option)

            # verify that this can reach another choice within the maze
            if breathFirstSearch(g.tileList, [choices[-1], option], 0):
                # if success we can break this while
                choices.append(option)
                # validate that the spawn is valid
                break 

        side = (side+1)%2 # now we switch to the other
        # have we run out of options?
        if (len(cArrL) == 0 or len(cArrR) == 0): # just in case we actually passed
            # reset and try again
            print(f"Failed to generate at {len(choices)}")
            choices = []
            side = 0 # start with the right
            # maze generated

            g.tileList = gen()

            # get 2 choices
            cArrL = [1, 2, 3, 15, 16, 17, 29, 30, 31, 43, 44, 45, 57, 58, 59, 71, 72, 73, 85, 86, 87, 99, 100, 101]
            cArrR = [12, 13, 14, 26, 27, 28, 40, 41, 42, 54, 55, 56, 68, 69, 70, 82, 83, 84, 96, 97, 98, 110, 111, 112]
            option = random.choice(cArrL) # Select the spawn zones
            cArrL.remove(option) # Remove the spawn zone from the list of choices
            choices.append(option) # Add the spawn zone to the list of choices

    # turn the spawnpoints into something usable
    choices_remaster = []
    for i in range(len(choices)):
        choices_remaster.append([g.tileList[choices[i] - 1].x + const.TILE_SIZE_X // 2, g.tileList[choices[i] - 1].y + const.TILE_SIZE_Y // 2])

    # supplies
    global spawnpoint
    spawnpoint = []
    spawnpoint = choices_remaster

    if getattr(sys, 'frozen', False):  # Running as an .exe
        currentDir = sys._MEIPASS
    else:  # Running as a .py script
        currentDir = os.path.dirname(os.path.abspath(__file__))

    g.tileList[98].setSupply([os.path.join(currentDir, 'Assets', 'Armor_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Armor_Floor.png')], 1)
    g.tileList[74].setSupply([os.path.join(currentDir, 'Assets', 'Damage_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Damage_Floor.png')], 0)
    g.tileList[105].setSupply([os.path.join(currentDir, 'Assets', 'Speed_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Speed_Floor.png')], 2)

    g.tileList[95].setSupply([os.path.join(currentDir, 'Assets', 'Armor_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Armor_Floor.png')], 1)
    g.tileList[54].setSupply([os.path.join(currentDir, 'Assets', 'Damage_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Damage_Floor.png')], 0)
    g.tileList[10].setSupply([os.path.join(currentDir, 'Assets', 'Speed_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Speed_Floor.png')], 2)

    g.tileList[2].setSupply([os.path.join(currentDir, 'Assets', 'Armor_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Armor_Floor.png')], 1)
    g.tileList[33].setSupply([os.path.join(currentDir, 'Assets', 'Damage_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Damage_Floor.png')], 0)
    g.tileList[42].setSupply([os.path.join(currentDir, 'Assets', 'Speed_Floor_Picked.png'), os.path.join(currentDir, 'Assets', 'Speed_Floor.png')], 2)

    return g.tileList

def nextType():
    """
    Setup the gamemode based on the selected difficulty type
    """
    global gameMode

    # quickly assign the game sprites
    match g.difficultyType:
        case DifficultyType.OnePlayerYard:
            reset()
            gameMode=GameMode.play
            #Switch the the play screen
            constantPlayGame()
        case DifficultyType.OnePlayerScrapYard:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.TwoPlayerYard:
            reset()
            gameMode=GameMode.play
            #Switch the the play screen
            constantPlayGame()
        case DifficultyType.TwoPlayerScrapYard:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.OnePlayerBrawl:
            reset()
            gameMode=GameMode.play
            #Switch the the play screen
            constantPlayGame()
        case DifficultyType.OnePlayerDeathMatch:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.TwoPlayerBrawl:
            reset()
            gameMode=GameMode.play
            #Switch the the play screen
            constantPlayGame()
        case DifficultyType.TwoPlayerDeathMatch:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.OnePlayerTDM:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.TeamDeathMatch:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.OnePlayerCaptureTheFlag:
            reset()
            gameMode = GameMode.selection
            constantSelectionScreen()
        case DifficultyType.CaptureTheFlag:
            reset()
            gameMode = GameMode.unimplemented
            # gameMode = GameMode.selection
            constantSelectionScreen()
        case _:
            print("Invalid difficulty type")
            gameMode = GameMode.unimplemented

def setUpTank(dType = -1, AI = False, spawn = [0,0], player = None, index = 0):
    """
    Based on the dififculty type, setup the players
    Inputs: dType: The difficulty type
    Inputs: AI: If the player is an AI or not
    Inputs: spawn: The spawn point for the player
    Inputs: player: The player object
    Inputs: index: The index of player's chosen color
    """
    global DifficultyType
    match dType:
        
        case DifficultyType.OnePlayerYard:
            # Scrapyard, Player vs AI (AI is player 1 and Player is p2) Simple Tanks
            tank = DefaultTank(0, 0, player.getControls(), player.getTankName())
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage('tank', playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.setAI(AI)
            tank.effect = [0,0,0]
            tank.setPlayer(player)

            gun = DefaultGun(tank, player.getTankName(), player.getGunName()) # Gun 1 setup
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setImage('gun', playerInformation.getPlayerTurretColour(index) + 1)
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.OnePlayerScrapYard:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank = copy.copy(playerInformation.getPlayerHull(index)) # Tank 1 setup
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)
            
            #Because silencer and watcher aren't made yet, skip them
            if playerInformation.Player2TurretIndex() == 1 or playerInformation.Player2TurretIndex() == 2:
                playerInformation.setPlayer2Turret(3)
                print("Skipping Silencer or Watcher, selecting Chamber")

            gun = copy.copy(playerInformation.getPlayerTurret(index)) # Gun 1 setup
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.TwoPlayerYard:
            # Scrapyard, Player vs Player Simple Tanks
            tank = DefaultTank(0, 0, player.getControls(), player.getTankName())
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage('tank', playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.setAI(AI)
            tank.effect = [0,0,0]
            tank.setPlayer(player)

            gun = DefaultGun(tank, player.getTankName(), player.getGunName()) # Gun 1 setup
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setImage('gun', playerInformation.getPlayerTurretColour(index) + 1)
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.TwoPlayerScrapYard:
            # Scrapyard, Player vs Player Normal Tanks
            tank = copy.copy(playerInformation.getPlayerHull(index)) # Tank 1 setup
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)

            gun = copy.copy(playerInformation.getPlayerTurret(index)) # Gun 1 setup
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.OnePlayerBrawl:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Simple Tanks
            tank = DefaultTank(0, 0, player.getControls(), player.getTankName())
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage('tank', playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.setAI(AI)
            tank.effect = [0,0,0]
            tank.setPlayer(player)

            gun = DefaultGun(tank, player.getTankName(), player.getGunName()) # Gun 1 setup
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setImage('gun', playerInformation.getPlayerTurretColour(index) + 1)
            gun.setAI(AI)
            gun.setPlayer(player)
        
        case DifficultyType.OnePlayerDeathMatch:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank = copy.copy(playerInformation.getPlayerHull(index)) # Tank 1 setup
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)
            
            #Because silencer and watcher aren't made yet, skip them
            if playerInformation.Player2TurretIndex() == 1 or playerInformation.Player2TurretIndex() == 2:
                playerInformation.setPlayer2Turret(3)
                print("Skipping Silencer or Watcher, selecting Chamber")

            gun = copy.copy(playerInformation.getPlayerTurret(index)) # Gun 1 setup
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.TwoPlayerBrawl:
            # Scrapyard, Player vs Player Simple Tanks
            tank = DefaultTank(0, 0, player.getControls(), player.getTankName())
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage('tank', playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.setAI(AI)
            tank.effect = [0,0,0]
            tank.setPlayer(player)

            gun = DefaultGun(tank, player.getTankName(), player.getGunName()) # Gun 1 setup
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setImage('gun', playerInformation.getPlayerTurretColour(index) + 1)
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.TwoPlayerDeathMatch:
            # Scrapyard, Player vs Player Normal Tanks
            tank = copy.copy(playerInformation.getPlayerHull(index)) # Tank 1 setup
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)
            
            gun = copy.copy(playerInformation.getPlayerTurret(index)) # Gun 1 setup
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.OnePlayerTDM:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            # tank = copy.copy(playerInformation.getPlayerHull(index)) # Tank 1 setup
            tank = playerInformation.getPlayerHull(index).copy()
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)
            
            #Because silencer and watcher aren't made yet, skip them
            if playerInformation.Player2TurretIndex() == 1 or playerInformation.Player2TurretIndex() == 2:
                playerInformation.setPlayer2Turret(3)
                print("Skipping Silencer or Watcher, selecting Chamber")

            gun = playerInformation.getPlayerTurret(index).copy()
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.TeamDeathMatch:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank = playerInformation.getPlayerHull(index).copy()
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)

            gun = playerInformation.getPlayerTurret(index).copy()
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.OnePlayerCaptureTheFlag:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank = playerInformation.getPlayerHull(index).copy()
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)

            gun = playerInformation.getPlayerTurret(index).copy()
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

        case DifficultyType.CaptureTheFlag:
            # Scrapyard, Player vs AI (AI is plpayer 1 and Player is p2) Normal Tanks
            tank = playerInformation.getPlayerHull(index).copy()
            tank.setData([spawn[0], spawn[1], player.getControls(), player.getTankName(), player.getTankChannels()])
            tank.setImage(playerInformation.getPlayerHull(index).getName(), playerInformation.getPlayerHullColour(index) + 1)
            tank.setSoundDictionary(const.SOUND_DICTIONARY)
            tank.settileList(g.tileList)
            tank.effect = [0,0,0]
            tank.setAI(AI)
            tank.setPlayer(player)

            gun = playerInformation.getPlayerTurret(index).copy()
            gun.setImage(playerInformation.getPlayerTurret(index).getGunName(), playerInformation.getPlayerTurretColour(index) + 1)
            gun.setHard()
            gun.setData(tank, player.getControls(), player.getGunName(), player.getTankChannels())
            gun.setAI(AI)
            gun.setPlayer(player)

    return gun, tank

def getMap(mapPath):
    """
    This is a function that will read the map from a file and return the tiles and spawn points
    The map file should be made by using the map editor provided in mapMaker.py
    Inputs: mapPath: The path to the map file
    Outputs: A list of tiles and a list of spawn points read from the file
    """

    if getattr(sys, 'frozen', False):  # Running as an .exe
        currentDir = sys._MEIPASS
    else:  # Running as a .py script
        currentDir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(currentDir, mapPath), "r") as f:
        # opening the path
        tList = []
        choices = [0 for _ in range(8)]
        rIndex = 0
        bIndex = 1
        for line in f.readlines(): # for each line, we can extract the information
            l = line.strip().split("||")
            # cast the string to a tuple
            t = l[2][1:-1].split(",")
            # let's auto assign tiles

            temp = Tile(int(l[5]), int(int(l[0])/50*const.TILE_SIZE_X), int(int(l[1])/50*const.TILE_SIZE_Y), (int(t[0]), int(t[1]), int(t[2])), False)
            temp.setBorderIndex(int(l[6]))
            temp.updateBorder()
            temp.setSpecial(int(l[7]))
            tList.append(temp)
            if l[7] == "1":
                # blue spawnpoint
                choices[bIndex] = int(l[5])
                bIndex += 2
            if l[7] == "2":
                # red spawnpoint
                choices[rIndex] = int(l[5])
                rIndex += 2
    spwn = []

    for i in range(len(choices)):
        spwn.append([tList[choices[i] - 1].x + const.TILE_SIZE_X // 2, tList[choices[i] - 1].y + const.TILE_SIZE_Y // 2])

    return tList, spwn

def setUpPlayers():
    """
    This function sets up the players for the game based on the selected difficulty type, this function will setup all the players
    Inputs: None
    Outputs: None
    """
    global spawnpoint, allSprites
    global DifficultyType

    if g.difficultyType.map:
        # if we need a predefined map
        global spawnpoint
        g.tileList, spawnpoint = getMap(g.selectedMap)
    else:
        g.tileList = tileGen(g.difficultyType.playerCount) # Get a new board
    for sprite in allSprites:
        sprite.kill()
    allSprites = pygame.sprite.Group() # Wipe the current Sprite Group
    # setup the tanks
    for i in range(g.difficultyType.playerCount):
        if i < g.difficultyType.humanCount:
            g.gunList[i], g.tankList[i] = setUpTank(g.difficultyType, AI = False, spawn = spawnpoint[i], player = playerlist[i], index = i)
        else:
            g.gunList[i], g.tankList[i] = setUpTank(g.difficultyType, AI = True, spawn = spawnpoint[i], player = playerlist[i], index = i)
        playerlist[i].setTeam(i%g.difficultyType.teamCount) # This team assignment is temporary, it will need to be updated to allow 2p on the same team
        allSprites.add(g.tankList[i], g.gunList[i])

    for i in range(g.difficultyType.playerCount):
        g.gunList[i].assignTeam(g.tankList, g.tankDead, g.difficultyType.playerCount) # Assign the teams

    match g.difficultyType:
        # The code used here is to set the end conditions of the game
        case DifficultyType.OnePlayerYard: 
            timer.setDirection(True)
        case DifficultyType.OnePlayerScrapYard:
            timer.setDirection(True)
        case DifficultyType.TwoPlayerYard:
            timer.setDirection(True)
        case DifficultyType.TwoPlayerScrapYard:
            timer.setDirection(True)
        case DifficultyType.OnePlayerBrawl:
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.OnePlayerDeathMatch:
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.TwoPlayerBrawl:
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.TwoPlayerDeathMatch:
            timer.setDirection(False)
            timer.setDuration(301)
        case DifficultyType.OnePlayerTDM:
            timer.setDirection(False)
            timer.setDuration(61)
        case DifficultyType.TeamDeathMatch:
            timer.setDirection(False)
            timer.setDuration(61)
        case DifficultyType.OnePlayerCaptureTheFlag:
            timer.setDirection(False)
            timer.setDuration(600) # 10 min
        case DifficultyType.CaptureTheFlag:
            timer.setDirection(False)
            timer.setDuration(1) # 10 min #<!FIXME (61)>
        case _:
            print("Unknown state")
            return
    #Updating the groups
    
    for bullet in g.bulletSprites:
        bullet.kill()
    g.bulletSprites = pygame.sprite.Group()   

    timer.reset() # Reset the timer

def constantHomeScreen():
    """
    The constant elements of the home screen (Which at this point is just resetting players and background music)
    Parameters: None
    Returns: None
    """
    for p in playerlist:
        p.resetPlayer(hard = True) # Reset the players
    homeScreen.draw(screen, pygame.mouse.get_pos())
    print("Switching to lobby music")
    mixer.crossfade('lobby')

def constantSelectionScreen():
    """
    The constant elements of the selection screen (Which at this point is just changing background music)
    Parameters: None
    Returns: None
    """
    print("Switching to selection music")
    mixer.crossfade('selection')

def constantPlayGame():
    """
    This function handles the constant elements of the game screen.
    It blits the background such that it can be drawn quickly in every frame
    Inputs: None
    Outputs: None
    """
    g.playScreen.fill(const.BACKGROUND_COLOR)
    g.playScreen.blit(g.gunList[0].getSprite(True), (const.TILE_SIZE_X, 0.78*const.WINDOW_HEIGHT))
    g.playScreen.blit(g.tankList[0].getSprite(True), (const.TILE_SIZE_X, 0.78*const.WINDOW_HEIGHT))
    g.playScreen.blit(g.gunList[1].getSprite(), (const.WINDOW_WIDTH - const.TILE_SIZE_X*3, 0.78*const.WINDOW_HEIGHT)) # Gun 2
    g.playScreen.blit(g.tankList[1].getSprite(), (const.WINDOW_WIDTH - const.TILE_SIZE_X*3, 0.78*const.WINDOW_HEIGHT)) # Tank 2
    for tile in g.tileList:
        tile.draw(g.playScreen)
    pygame.draw.rect(g.playScreen, c.geT("BLACK"), [const.MAZE_X, const.MAZE_Y, const.MAZE_WIDTH, const.MAZE_HEIGHT], 2)
    
    if timer.isPaused():
        timer.resume()

    print("Switching to game music")
    mixer.crossfade('game')

    # Load the custom font
    fontString = "PLAYER 1             SCORE              PLAYER 2"
    controlString = "WASD                            ↑↓←→" 
    textp2Name = const.FONT_DICTIONARY["playerStringFont"].render(fontString, True, c.geT("BLACK"))
    controls = const.FONT_DICTIONARY["ctrlFont"].render(controlString, True, c.geT("BLACK"))
    g.playScreen.blit(textp2Name,[const.WINDOW_WIDTH//2 - textp2Name.get_width()//2, 0.78*const.WINDOW_HEIGHT]) # This is the name on the right
    g.playScreen.blit(controls,[const.WINDOW_WIDTH//2 - controls.get_width()//2, const.WINDOW_HEIGHT*5/6]) # This is the name on the right

    LplayerstatLeft = const.TILE_SIZE_X*7/8-1
    playerstatTop = 0.88*const.WINDOW_HEIGHT
    RplayerstatLeft = const.WINDOW_WIDTH - const.TILE_SIZE_X*2.2-1
    
    HealthBox = TextBox(LplayerstatLeft, playerstatTop, "Londrina", "HEALTH", 20, c.geT("BLACK"))
    HealthBox.setPaddingHeight(0)
    HealthBox.setPaddingWidth(0)
    HealthBox.setBoxColor(const.BACKGROUND_COLOR)
    HealthBox.draw(g.playScreen)

    ReloadBox = TextBox(LplayerstatLeft, playerstatTop + const.MAZE_Y//2, "Londrina", "RELOAD", 20, c.geT("BLACK"))
    ReloadBox.setPaddingHeight(0)
    ReloadBox.setPaddingWidth(0)
    ReloadBox.setBoxColor(const.BACKGROUND_COLOR)
    ReloadBox.draw(g.playScreen)

    HealthBox2 = TextBox(RplayerstatLeft, playerstatTop, "Londrina", "HEALTH", 20, c.geT("BLACK"))
    HealthBox2.setPaddingHeight(0)
    HealthBox2.setPaddingWidth(0)
    HealthBox2.setBoxColor(const.BACKGROUND_COLOR)
    HealthBox2.draw(g.playScreen)

    ReloadBox2 = TextBox(RplayerstatLeft, playerstatTop + const.MAZE_Y//2, "Londrina", "RELOAD", 20, c.geT("BLACK"))
    ReloadBox2.setPaddingHeight(0)
    ReloadBox2.setPaddingWidth(0)
    ReloadBox2.setBoxColor(const.BACKGROUND_COLOR)
    ReloadBox2.draw(g.playScreen)

def fixMovement():
    """
    This function will fix the movements of the tanks such that they don't collide with each other, or with the walls or boundaries of the maze.
    Inputs: None
    Outputs: None
    """

    for i in range(g.difficultyType.playerCount):
        if not g.tankDead[i]: # if the tank is dead, skip it
            t = g.tankList[i]

            tempX = t.x + t.changeX
            tempY = t.y - t.changeY

            if tempX <= const.MAZE_X + t.tankImage.get_size()[0]/2:
                tempX = const.MAZE_X + t.tankImage.get_size()[0]/2
            if tempY <= const.MAZE_Y + t.tankImage.get_size()[0]/2:
                tempY = const.MAZE_Y + t.tankImage.get_size()[0]/2
            if tempX > const.MAZE_WIDTH + const.MAZE_X - t.tankImage.get_size()[0]/2:
                tempX = const.MAZE_WIDTH + const.MAZE_X - t.tankImage.get_size()[0]/2
            if tempY > const.MAZE_HEIGHT + const.MAZE_Y - t.tankImage.get_size()[0]/2:
                tempY = const.MAZE_HEIGHT + const.MAZE_Y - t.tankImage.get_size()[0]/2

            for j in range(i+1, g.difficultyType.playerCount):
                t1 = t
                if not g.tankDead[j]: # if the tank is alive
                    t2 = g.tankList[j]
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
            row = math.ceil((t.getCenter()[1] - const.MAZE_Y) / const.TILE_SIZE_Y)
            col = math.ceil((t.getCenter()[0] - const.MAZE_X) / const.TILE_SIZE_X)
            index = (row - 1) * const.COLUMN_AMOUNT + col

            if index in range(1, const.ROW_AMOUNT * const.COLUMN_AMOUNT + 1):
                tile = g.tileList[index - 1]
                tank_width = t.tankImage.get_size()[0]
                tank_height = t.tankImage.get_size()[1]

                # Calculate tank's future position (without correction)
                futureX = tempX
                futureY = tempY

                # Check top, bottom, left, and right borders
                if tile.border[0] and tempY - tank_height <= tile.y:  # Top border
                    futureY = tile.y + tank_height
                if tile.border[1] and tempX + tank_width / 2 >= tile.x + const.TILE_SIZE_X:  # Right border
                    futureX = tile.x + const.TILE_SIZE_X - tank_width / 2
                if tile.border[2] and tempY + tank_height > tile.y + const.TILE_SIZE_Y:  # Bottom border
                    futureY = tile.y + const.TILE_SIZE_Y - tank_height
                if tile.border[3] and tempX - tank_width / 2 < tile.x:  # Left border
                    futureX = tile.x + tank_width / 2

                # Corner detection (top-left, top-right, bottom-left, bottom-right)
                if tile.border[0] and tile.border[3]:  # Top-left corner
                    if tempX - tank_width / 2 < tile.x and tempY - tank_height <= tile.y:
                        futureX = tile.x + tank_width / 2
                        futureY = tile.y + tank_height
                elif tile.border[0] and tile.border[1]:  # Top-right corner
                    if tempX + tank_width / 2 >= tile.x + const.TILE_SIZE_X and tempY - tank_height <= tile.y:
                        futureX = tile.x + const.TILE_SIZE_X - tank_width / 2
                        futureY = tile.y + tank_height
                elif tile.border[2] and tile.border[3]:  # Bottom-left corner
                    if tempX - tank_width / 2 < tile.x and tempY + tank_height > tile.y + const.TILE_SIZE_Y:
                        futureX = tile.x + tank_width / 2
                        futureY = tile.y + const.TILE_SIZE_Y - tank_height
                elif tile.border[2] and tile.border[1]:  # Bottom-right corner
                    if tempX + tank_width / 2 >= tile.x + const.TILE_SIZE_X and tempY + tank_height > tile.y + const.TILE_SIZE_Y:
                        futureX = tile.x + const.TILE_SIZE_X - tank_width / 2
                        futureY = tile.y + const.TILE_SIZE_Y - tank_height

                # Apply the corrected positions
                tempX, tempY = futureX, futureY

            t.setCentre(tempX, tempY)

            t.changeX = 0
            t.changeY = 0
        
def getColor(color):
    """
    For a team's color, return the color of the team
    """
    if color == 0:
        return c.geT("BLUE")
    elif color == 1:
        return c.geT("RED")
    else:
        return c.geT("GREY")

def playGame():
    """
    This function is the main game loop, it will handle the game logic and the rendering of the game
    """
    def checkGameOver(t):
        """
        This function checks the ending conditions of the game based on the difficulty type
        Inputs: t: The difficulty type
        Outputs: True if the game is over, False otherwise
        """
        global DifficultyType
        match t:
            case DifficultyType.OnePlayerYard:
                return g.tankDead[:g.difficultyType.playerCount].count(False) == 1
            case DifficultyType.OnePlayerScrapYard:
                return g.tankDead[:g.difficultyType.playerCount].count(False) == 1
            case DifficultyType.TwoPlayerYard:
                return g.tankDead[:g.difficultyType.playerCount].count(False) == 1
            case DifficultyType.TwoPlayerScrapYard:
                return g.tankDead[:g.difficultyType.playerCount].count(False) == 1
            case DifficultyType.OnePlayerBrawl:
                return timer.isExpired()
            case DifficultyType.OnePlayerDeathMatch:
                return timer.isExpired()
            case DifficultyType.TwoPlayerBrawl:
                return timer.isExpired()
            case DifficultyType.TwoPlayerDeathMatch:
                return timer.isExpired()
            case DifficultyType.OnePlayerTDM:
                return timer.isExpired()
            case DifficultyType.TeamDeathMatch:
                return timer.isExpired()
            case DifficultyType.OnePlayerCaptureTheFlag:
                return timer.isExpired()
            case DifficultyType.CaptureTheFlag:
                return timer.isExpired()
    
    def updateScore():
        """
        Based on the difficulty type, update the score of the game
        """
        match g.difficultyType:
            case DifficultyType.OnePlayerYard:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills

            case DifficultyType.OnePlayerScrapYard:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.TwoPlayerYard:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.TwoPlayerScrapYard:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.OnePlayerBrawl:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.OnePlayerDeathMatch:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.TwoPlayerBrawl:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.TwoPlayerDeathMatch:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.OnePlayerTDM:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.TeamDeathMatch:
                g.team1Score = 0
                g.team2Score = 0
                for i in range(g.difficultyType.playerCount):
                    if playerlist[i].getTeam() == 0:
                        g.team1Score += playerlist[i].kills
                    else:
                        g.team2Score += playerlist[i].kills
            case DifficultyType.OnePlayerCaptureTheFlag:
                g.team1Score = g.flag[1].getScore()
                g.team2Score = g.flag[0].getScore()
            case DifficultyType.CaptureTheFlag:
                g.team1Score = g.flag[1].getScore()
                g.team2Score = g.flag[0].getScore()

    def makeTable():
        """
        Generate the end screen table based on the players' scores and kills
        """
        endScreen.makeTable(*[player.getTableEntry() for player in playerlist[:g.difficultyType.playerCount]])

    def getHealthIndicator(health):
        """
        This function returns the color of the health bar based on the health of the tank
        """
        return healthColor[max(int((health*10-1)//1),0)]
        
    global gameOverFlag, cooldownTimer, systemTime, startTreads
    global spawnpoint
    global allSprites
    global currentTime, deltaTime, lastUpdateTime
    global timerClock, gameMode
    if checkGameOver(t = g.difficultyType) and not cooldownTimer:
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
            match g.difficultyType:
                case DifficultyType.OnePlayerYard:
                    if g.team1Score == 21 or g.team2Score == 21:
                        makeTable()
                        gameMode = GameMode.end
                    else:
                        reset()
                        constantPlayGame()
                        timer.reset() # rest the clock
                case DifficultyType.OnePlayerScrapYard:
                    if g.team1Score == 21 or g.team2Score == 21:
                        makeTable()
                        gameMode = GameMode.end
                    else:
                        reset()
                        constantPlayGame()
                        timer.reset() # rest the clock
                case DifficultyType.TwoPlayerYard:
                    if g.team1Score == 21 or g.team2Score == 21:
                        makeTable()
                        gameMode = GameMode.end
                    else:
                        reset()
                        constantPlayGame()
                        timer.reset() # rest the clock
                case DifficultyType.TwoPlayerScrapYard:
                    if g.team1Score == 21 or g.team2Score == 21:
                        makeTable()
                        gameMode = GameMode.end
                    else:
                        reset()
                        constantPlayGame()
                        timer.reset() # rest the clock
                case DifficultyType.OnePlayerBrawl:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.OnePlayerDeathMatch:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.TwoPlayerBrawl:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.TwoPlayerDeathMatch:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.OnePlayerTDM:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.TeamDeathMatch:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.OnePlayerCaptureTheFlag:
                    makeTable()
                    gameMode = GameMode.end
                case DifficultyType.CaptureTheFlag:
                    makeTable()
                    gameMode = GameMode.end
    seconds = timer.getTime()
    textString = f"{seconds // 60:02d}:{seconds % 60:02d}"
    text = const.FONT_DICTIONARY["scoreFont"].render(textString, True, c.geT("BLACK"))
    screen.blit(g.playScreen, (0,0))
    updateScore()
    #UI Elements
    pauseButton.update_display(pygame.mouse.get_pos())
    pauseButton.draw(screen, outline = True)

    # Load the custom font
    pygame.draw.rect(screen, const.BACKGROUND_COLOR, [const.TILE_SIZE_X*2.1, 0.87*const.WINDOW_HEIGHT, const.WINDOW_WIDTH-const.TILE_SIZE_X*1.2-150*const.UNIVERSAL_SCALER_WIDTH, const.WINDOW_HEIGHT*0.15]) # The bottom bar

    text3 = const.FONT_DICTIONARY["playerScore"].render(str(g.team1Score) + ":" + str(g.team2Score), True, c.geT("BLACK"))
    screen.blit(text3, [const.WINDOW_WIDTH/2 - text3.get_width()/2, 0.85*const.WINDOW_HEIGHT])

    #Box around the bottom of the screen for the health and reload bars

    LplayerStatupdateLeft = const.TILE_SIZE_X*2.2
    playerStatupdateTop = 0.88*const.WINDOW_HEIGHT
    RplayerStatupdateLeft = const.WINDOW_WIDTH - const.TILE_SIZE_X*2.2 - 150 * const.UNIVERSAL_SCALER_WIDTH

    pygame.draw.rect(screen, c.geT("RED"), [LplayerStatupdateLeft, playerStatupdateTop, const.UNIVERSAL_SCALER_WIDTH*150*(g.tankList[0].getHealthPercentage() if not g.tankDead[0] else 0),
                                            20]) # Bar
    pygame.draw.rect(screen, c.geT("BLACK"), [LplayerStatupdateLeft, playerStatupdateTop, 150 * const.UNIVERSAL_SCALER_WIDTH, 20], 2) # Outline
    # #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [LplayerStatupdateLeft, playerStatupdateTop + const.MAZE_Y//2, const.UNIVERSAL_SCALER_WIDTH* 150*(min(1,1-g.gunList[0].getReloadPercentage() if not g.tankDead[0] else 0)),
                                             20]) # The 25 is to space from the health bar

    pygame.draw.rect(screen, c.geT("BLACK"), [LplayerStatupdateLeft, playerStatupdateTop + const.MAZE_Y//2, 150 * const.UNIVERSAL_SCALER_WIDTH, 20], 2) # Outline


    # Health bars
    pygame.draw.rect(screen, c.geT("RED"), [RplayerStatupdateLeft, playerStatupdateTop, 150*const.UNIVERSAL_SCALER_WIDTH*(g.tankList[1].getHealthPercentage() if not g.tankDead[1] else 0),
                                            20])
    pygame.draw.rect(screen, c.geT("BLACK"), [RplayerStatupdateLeft, playerStatupdateTop, 150*const.UNIVERSAL_SCALER_WIDTH, 20], 2)
    #Reload bars
    pygame.draw.rect(screen, c.geT("BLUE"), [RplayerStatupdateLeft, playerStatupdateTop + const.MAZE_Y//2,
                                             150*const.UNIVERSAL_SCALER_WIDTH*(min(1,1-g.gunList[1].getReloadPercentage()) if not g.tankDead[1] else 0),
                                             20]) # The 25 is to space from the health bar
    pygame.draw.rect(screen, c.geT("BLACK"), [RplayerStatupdateLeft, playerStatupdateTop + const.MAZE_Y//2, 150*const.UNIVERSAL_SCALER_WIDTH, 20], 2) # Outline

    #draw the supplies # Draw more on top of them
    ef, mx = g.tankList[0].getEffect() if not g.tankDead[0] else ([0,0,0], [19000, 19000, 19000//3])

    # # Dynamic updating of the current supply status

    # ef0 is damage
    # ef1 is armor
    # ef2 is speed
    row1Height = 550*const.UNIVERSAL_SCALER_HEIGHT
    row2Height = 520*const.UNIVERSAL_SCALER_HEIGHT
    col1Left = 270*const.UNIVERSAL_SCALER_WIDTH
    col1Right = 300*const.UNIVERSAL_SCALER_WIDTH
    col2Left = 510*const.UNIVERSAL_SCALER_WIDTH
    col2Right = 480*const.UNIVERSAL_SCALER_WIDTH

    screen.blit(const.SUPPLY_ASSETS[0][min(int(((ef[0]/mx[0])*10)//1) + 1, 10) if ef[0] != 0 else 0], [col1Left, row1Height])
    screen.blit(const.SUPPLY_ASSETS[1][min(int(((ef[1]/mx[1])*10)//1) + 1, 10) if ef[1] != 0 else 0], [col1Right, row1Height])
    screen.blit(const.SUPPLY_ASSETS[2][min(int(((ef[2]/mx[2])*10)//1) + 1, 10) if ef[2] != 0 else 0], [col1Left, row2Height])

    ef2, mx2 = g.tankList[1].getEffect() if not g.tankDead[1] else ([0,0,0], [19000, 19000, 19000//3])

    screen.blit(const.SUPPLY_ASSETS[0][min(int(((ef2[0]/mx2[0])*10)//1) + 1, 10) if ef2[0] != 0 else 0], [col2Left, row1Height])
    screen.blit(const.SUPPLY_ASSETS[1][min(int(((ef2[1]/mx2[1])*10)//1) + 1, 10) if ef2[1] != 0 else 0], [col2Right, row1Height])
    screen.blit(const.SUPPLY_ASSETS[2][min(int(((ef2[2]/mx2[2])*10)//1) + 1, 10) if ef2[2] != 0 else 0], [col2Left, row2Height])

    # Draw the border
    for tile in g.tileList:
        tile.update() # This should be a togglable feature because it impacts performance
        # tile.draw(screen)
        tile.drawUpdate(screen) # on top of the constant

    #Anything below here will be drawn on top of the maze and hence is game updates
    if pygame.time.get_ticks() - startTreads > 50:
        for i in range(g.difficultyType.playerCount):
            if g.tankDead[i]:
                treads[i].clear()
            else:
                if g.tankList[i].invincibility==0:
                    g.tankList[i].treads(treads[i])
        startTreads = pygame.time.get_ticks() # Reset the timer
    for i in range(g.difficultyType.playerCount):
        for p in treads[i]:
            screen.blit(p[0], p[1])

    # # fill up the area covered by the tank with the background color
    # # draw the text again
    screen.blit(text, [const.WINDOW_WIDTH//2 - text.get_width()//2, 8])

    # # temp solution while the AI needs to be improved
    if g.difficultyType.ai:
        for i in range(1, g.difficultyType.playerCount):
            if not g.tankDead[i]: # if the tank is alive
                if pygame.time.get_ticks() - g.tankList[i].getAimTime() > 2000:
                    if not g.tankDead[0]:
                        g.gunList[i].updateAim()

    currentTime = time.time()
    deltaTime = currentTime - lastUpdateTime
    if deltaTime >= 1/const.TPS:
        #Update the location of the corners

        for i in range(g.difficultyType.playerCount):
            if not g.tankDead[i]:
                g.tankList[i].updateCorners()
                g.tankList[i].setDelta(const.TPS)
                g.gunList[i].setDelta(const.TPS)
            else:
                if g.difficultyType.respawn:
                    if i < g.difficultyType.humanCount:
                        g.gunList[i], g.tankList[i] = setUpTank(g.difficultyType, AI = False, spawn = spawnpoint[i], player = playerlist[i], index = i)
                    else:
                        g.gunList[i], g.tankList[i] = setUpTank(g.difficultyType, AI = True, spawn = spawnpoint[i], player = playerlist[i], index = i)
                        g.gunList[i].assignTeam(g.tankList, g.tankDead, g.difficultyType.playerCount) # Assign the teams
                    allSprites.add(g.tankList[i], g.gunList[i])
                    g.tankDead[i] = False
            
        for bullet in g.bulletSprites:
            bullet.setDelta(const.TPS)

        #Fixing tank movement
        # don't update the bullets if the game is over
        if not cooldownTimer:
            allSprites.update()
            fixMovement()
            g.bulletSprites.update()
        g.explosionGroup.update()
        lastUpdateTime = currentTime
    for sprite in allSprites:
        sprite.draw(screen)
        if sprite.isDrawable():
            sprite.customDraw(screen)

    for sprite in g.bulletSprites:
        sprite.draw(screen)
        if sprite.isDrawable():
            sprite.customDraw(screen)

    for i in range(g.difficultyType.playerCount):
        if not g.tankDead[i]:
            pygame.draw.polygon(screen, getColor(g.tankList[i].getTeam()), g.tankList[i].getCornersInflated(3), 2) #Hit box outline

    # # # we are drawing a surface to stick the health bars on top of the tanks # this should be a togglable feature because it impacts performance
    for i in range(g.difficultyType.playerCount):
        if not g.tankDead[i]:
            pygame.draw.rect(screen, getHealthIndicator(g.tankList[i].getHealthPercentage()), [g.tankList[i].getCenter()[0] - 10, g.tankList[i].getCenter()[1], 20, 5])

    if (g.difficultyType == DifficultyType.CaptureTheFlag) or (g.difficultyType == DifficultyType.OnePlayerCaptureTheFlag):
        for f in g.flag:
            f.update()
            f.draw(screen)

    g.explosionGroup.draw(screen)
    if timerClock == 0:
        timer.tick()
    # 125 is the reference for the FPS
    timerClock = (timerClock + 1) % 120 # This is to make sure that the timer doesn't go too fast

def reset():
    """
    This function is responsible for resetting the game state.
    Inputs: None
    Outputs: None
    """
    global gameOverFlag, cooldownTimer, systemTime
    global playerlist
    global allSprites
    gameOverFlag = False
    cooldownTimer = False
    for p in playerlist:
        p.resetPlayer()
    #Remove all the sprites
    for sprite in allSprites:
        sprite.kill()
    allSprites = pygame.sprite.Group() # Wipe the current Sprite Group
    for sprite in g.bulletSprites:
        sprite.kill()
    g.bulletSprites = pygame.sprite.Group()
    #Nautural constants
    systemTime = 0
    for i in range(g.difficultyType.playerCount):
        g.tankDead[i] = False
        treads[i].clear()
    setUpPlayers()

timer = UpDownTimer(1000, True)

#Game setup
#Start the game setup
mixer = Music()
mixer.play()
pygame.display.set_caption("Flanki") # Name the window
clock = pygame.time.Clock() # Start the clock

systemTime = 0
cooldownTimer = False

global startTreads
startTreads = 0
global gameOverFlag
gameOverFlag = False
done = False

global currentTime, deltaTime, lastUpdateTime
currentTime = 0
deltaTime = 0
lastUpdateTime = 0

screen = pygame.display.set_mode((const.WINDOW_WIDTH,const.WINDOW_HEIGHT), pygame.RESIZABLE)  # Windowed (safer/ superior)
# full screen
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)  # Full screen




gameMode = GameMode.home

turretList = [Tempest(Tank(0,0,None, "Default"), None, "Tempest"), Silencer(Tank(0,0,None, "Default"), None, "Silencer"),
        Watcher(Tank(0,0,None, "Default"), None, "Watcher"), Chamber(Tank(0,0,None, "Default"), None, "Chamber"),
        Huntsman(Tank(0,0,None,"Default"),None,"Huntsman"), Judge(Tank(0,0,None,"Default"),None,"Judge"),
        Sidewinder(Tank(0,0,None,"Default"),None,"Sidewinder")]

hullList = [Panther(0, 0, None, "Panther"), Cicada(0, 0, None, "Cicada"), Gater(0, 0, None, "Gater"), Bonsai(0, 0, None, "Bonsai"),
        Fossil(0, 0, None, "Fossil")]

endScreen = EndScreen()
creditsScreen = CreditScreen()
settingsScreen = SettingsScreen()
pauseScreen = PauseScreen()
infoScreen = InfoScreen()
homeScreen = HomeScreen()
playerInformation = PlayerInformation(turretList, hullList)
selectionScreen = SelectionScreen(turretList, hullList, mousePos = pygame.mouse.get_pos())
broken = NotImplmented()

# number to keep track of which page we are on
global pageNum
pageNum = 0

pauseButton = Button(const.BACKGROUND_COLOR ,const.BACKGROUND_COLOR, const.WINDOW_WIDTH-const.TILE_SIZE_X*3, const.TILE_SIZE_Y//5,const.TILE_SIZE_X*2,const.TILE_SIZE_Y//2, "PAUSE", c.geT("BLACK"), 20, c.geT("OFF_WHITE"))
pauseButton.setOutline(True, 2)

pygame.mixer.set_num_channels(64) #MORE

for sound in const.SOUND_DICTIONARY:
    const.SOUND_DICTIONARY[sound].set_volume(const.VOLUME[sound])

allSprites = pygame.sprite.Group()

constantHomeScreen()

def main():
    global done, gameMode
    #Main loop
    while not done:
        # Early define probably not a good idea, but will help with reducing function calls
        mouse = pygame.mouse.get_pos() #Update the position of the mouse (This might actually be a bad call)
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
                        for tile in g.tileList:
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

                    elif gameMode == GameMode.selection: # Selection screen

                        if selectionScreen.isWithinPlayButton(mouse):
                            reset()
                            #Switch the the play screen
                            print("Play")
                            constantPlayGame()
                            gameMode=GameMode.play
                        if selectionScreen.isWithinHomeButton(mouse):
                            #Switch back to the home screen
                            constantHomeScreen()
                            print("Back")
                            gameMode = GameMode.home
                        if selectionScreen.isWithinHowToPlayButton(mouse):
                            print("How to Play")
                            gameMode = GameMode.info # Switch to the info screen
                            infoScreen.draw(screen)
                        selectionScreen.update(mouse)

                    elif gameMode == GameMode.home: # Home screen

                        global pageNum
                        g.team1Score, g.team2Score = 0, 0 # reset the player scores

                        if homeScreen.isWithinHomeButton1(mouse):
                            g.difficultyType = DifficultyType.from_index(1 + pageNum)
                            nextType()

                        if homeScreen.isWithinHomeButton2(mouse):
                            g.difficultyType = DifficultyType.from_index(2 + pageNum)
                            nextType()

                        if homeScreen.isWithinHomeButton3(mouse):
                            g.difficultyType = DifficultyType.from_index(3 + pageNum)
                            nextType()

                        if homeScreen.isWithinHomeButton4(mouse):
                            g.difficultyType = DifficultyType.from_index(4 + pageNum)
                            nextType()

                        if homeScreen.isWithinHomeLeftButton(mouse):
                            pageNum = (pageNum - 4) % homeScreen.getLenNameArray()
                            homeScreen.setTextHomeButton1(pageNum)
                            homeScreen.setTextHomeButton2(pageNum + 1)
                            homeScreen.setTextHomeButton3(pageNum + 2)
                            homeScreen.setTextHomeButton4(pageNum + 3)

                        if homeScreen.isWithinHomeRightButton(mouse):
                            pageNum = (pageNum + 4) % homeScreen.getLenNameArray()
                            homeScreen.setTextHomeButton1(pageNum)
                            homeScreen.setTextHomeButton2(pageNum + 1)
                            homeScreen.setTextHomeButton3(pageNum + 2)
                            homeScreen.setTextHomeButton4(pageNum + 3)

                        if homeScreen.isWithinSettingsButton(mouse):
                            print("Settings")
                            gameMode = GameMode.settings

                        if homeScreen.isWithinQuitButton(mouse):
                            done = True # We quit the appplication

                    elif gameMode == GameMode.play:
                        if pauseButton.buttonClick(mouse):
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
                            infoScreen.updateBox(-1)

                        if infoScreen.isWithinRArrowButton(mouse):
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

                    elif gameMode == GameMode.end:
                        if endScreen.isWithinPlayAgainButton(mouse):
                            print("Play Again")
                            g.team1Score, g.team2Score = 0, 0 # reset the player scores
                            reset()
                            constantPlayGame()
                            gameMode = GameMode.play
                        if endScreen.isWithinHomeButton(mouse):
                            print("Home")
                            constantHomeScreen()
                            gameMode = GameMode.home

                    elif gameMode == GameMode.unimplemented:
                        if broken.isWithinBackButton(mouse):
                            gameMode = GameMode.home
                            constantHomeScreen()

            elif event.type == pygame.KEYDOWN: # Any key pressed

                if event.key == pygame.K_ESCAPE: # Escape hotkey to quit the window

                    if gameMode == GameMode.play:
                        for i in range(3, pygame.mixer.get_num_channels()): # Stop all sounds
                            pygame.mixer.Channel(i).stop()
                        gameMode = GameMode.pause # Pause the game
                        timer.pause()
                    elif gameMode == GameMode.pause:
                        # Do nothing
                        pass
                    else:
                        done = True

                if event.key == pygame.K_i:
                    print("The current mouse position is: ", mouse)
                    print(const.MAZE_X, const.MAZE_Y, const.MAZE_WIDTH, const.MAZE_HEIGHT)

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
                    for sound in const.SOUND_DICTIONARY:
                        const.SOUND_DICTIONARY[sound].set_volume(const.VOLUME[sound] * settingsScreen.volume.sfx.getValue())

        if gameMode == GameMode.play:
            playGame() # Play the game

        elif gameMode == GameMode.pause:
            pauseScreen.draw(screen = screen) # Pause screen
            if mouse[0] and pygame.mouse.get_pressed()[0]:
                pauseScreen.updateMute(mouse)
                pauseScreen.updateSFX(mouse)
                for sound in const.SOUND_DICTIONARY:
                    const.SOUND_DICTIONARY[sound].set_volume(const.VOLUME[sound] * pauseScreen.getSFXValue())

        elif gameMode == GameMode.selection:

            selectionScreen.draw(screen, mouse)

        elif gameMode == GameMode.home:
            # # Draw the tank image
            homeScreen.draw(screen, mouse) # Home screen

        elif gameMode == GameMode.credit:
            pass # Do nothing

        elif gameMode == GameMode.info:
            infoScreen.draw(screen) # Info screen

        elif gameMode == GameMode.settings:
            settingsScreen.draw(screen = screen)
            if mouse[0] and pygame.mouse.get_pressed()[0]:
                settingsScreen.updateMute(mouse)
                settingsScreen.updateSFX(mouse)
                for sound in const.SOUND_DICTIONARY:
                    const.SOUND_DICTIONARY[sound].set_volume(const.VOLUME[sound] * settingsScreen.getSFXValue())
        
        elif gameMode == GameMode.end:
            endScreen.draw(screen)
        
        elif gameMode == GameMode.unimplemented:
            broken.draw(screen)
        
        else:
            screen.fill(c.geT("WHITE")) # Errornous state

        clock.tick(240) # Set the FPS
        mixer.update(settingsScreen.getMuteValue()) # Update the mixer
        pygame.display.flip()# Update the screen

    pygame.quit()

main()
