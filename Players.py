import constants as const
import random

class PlayerInformation:
    # This class will hold the turret / hulls for each of the players


    ColorIndex = ["TANK_GREEN", "BURGUNDY", "ORANGE", "YELLOW", "SKY_BLUE", "LIGHT_BROWN", "DARK_LILAC", "BRIGHT_PINK"]

    #Hull and turret list

    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PlayerInformation, cls).__new__(cls)
        return cls._instance

    def __init__(self, tList, hList):
        # To prevent re-initialization on every call
        if not hasattr(self, 'initialized'):
            self.turretList = tList
            self.hullList = hList
            self.initialized = True

            #List indexes for player selection
            #Turret index
            self.p1I = 0
            self.p2I = 0
            #Hull index
            self.p1J = 0
            self.p2J = 0
            #Colour index
            self.p1K = 0
            self.p2K = 1

            self.p1L = 1
            self.p2L = 0

            self.TurretColors = [i for i in range(len(self.ColorIndex))]
            self.HullColors = [i for i in range(len(self.ColorIndex))]
            self.updateColors()

    def getTurretList(self):
        return self.turretList
    
    def getHullList(self):
        return self.hullList
    
    def getTurretListLength(self):
        return self.turretListLength
    
    def getHullListLength(self):
        return self.hullListLength
    
    def Player1TurretIndex(self):
        return self.p1I
    
    def Player2TurretIndex(self):
        return self.p2I
    
    def Player1HullIndex(self):
        return self.p1J
    
    def Player2HullIndex(self):
        return self.p2J
    
    def Player1TurretColourIndex(self):
        return self.p1K
    
    def Player2TurretColourIndex(self):
        return self.p2K
    
    def Player1HullColourIndex(self):
        return self.p1L
    
    def Player2HullColourIndex(self):
        return self.p2L

    def movePlayer1TurretIndex(self, move):
        self.p1I = (self.p1I + move) % len(self.turretList)

    def movePlayer2TurretIndex(self, move):
        self.p2I = (self.p2I + move) % len(self.turretList)

    def movePlayer1HullIndex(self, move):
        self.p1J = (self.p1J + move) % len(self.hullList)

    def movePlayer2HullIndex(self, move):
        self.p2J = (self.p2J + move) % len(self.hullList)

    def movePlayer1TurretColourIndex(self, move):
        self.p1K = (self.p1K + move) % len(self.ColorIndex)
        if self.p1K == self.p2K:
            self.p1K = (self.p1K + move) % len(self.ColorIndex)
        self.updateColors()
    
    def movePlayer2TurretColourIndex(self, move):
        self.p2K = (self.p2K + move) % len(self.ColorIndex)
        if self.p2K == self.p1K:
            self.p2K = (self.p2K + move) % len(self.ColorIndex)
        self.updateColors()
    
    def movePlayer1HullColourIndex(self, move):
        self.p1L = (self.p1L + move) % len(self.ColorIndex)
        if self.p1L == self.p2L:
            self.p1L = (self.p1L + move) % len(self.ColorIndex)
        self.updateColors()

    def movePlayer2HullColourIndex(self, move):
        self.p2L = (self.p2L + move) % len(self.ColorIndex)
        if self.p2L == self.p1L:
            self.p2L = (self.p2L + move) % len(self.ColorIndex)
        self.updateColors()

    def updateColors(self):
        temp = [i for i in range(len(self.ColorIndex))]
        self.TurretColors[0] = self.p1K
        temp.remove(self.p1K)
        self.TurretColors[1] = self.p2K
        temp.remove(self.p2K)
        for i in range(2, len(self.turretList)):
            item = random.choice(temp)
            self.TurretColors[i] = item
            temp.remove(item)
        temp = [i for i in range(len(self.ColorIndex))]
        self.HullColors[0] = self.p1L
        temp.remove(self.p1L)
        self.HullColors[1] = self.p2L
        temp.remove(self.p2L)
        for i in range(2, len(self.hullList)):
            item = random.choice(temp)
            self.HullColors[i] = item
            temp.remove(item)

    def getPlayerTurret(self, index):
        if index == 0:
            return self.turretList[self.p1I]
        elif index == 1:
            return self.turretList[self.p2I]
        else: # no more players, just AI
            vChoice = [i for i in range(0, len(self.turretList) - 1) if i != 1 and i != 2]
            return random.choice(vChoice)

    def getPlayerHull(self, index):
        if index == 0:
            return self.hullList[self.p1J]
        elif index == 1:
            return self.hullList[self.p2J]
        else: # no more players, just AI
            return self.hullList[random.randint(0, len(self.hullList) - 1)]

    def getPlayerTurretColour(self, index):
        return self.TurretColors[index]
    
    def getPlayerHullColour(self, index):
        return self.HullColors[index]

    def getPlayer1Turret(self):
        return self.turretList[self.p1I]
    
    def getPlayer2Turret(self):
        return self.turretList[self.p2I]
    
    def getPlayer1Hull(self):
        return self.hullList[self.p1J]
    
    def getPlayer2Hull(self):
        return self.hullList[self.p2J]
    
    def getPlayer1TurretColour(self):
        return self.ColorIndex[self.p1K]
    
    def getPlayer2TurretColour(self):
        return self.ColorIndex[self.p2K]
    
    def getPlayer1HullColour(self):
        return self.ColorIndex[self.p1L]
    
    def getPlayer2HullColour(self):
        return self.ColorIndex[self.p2L]
    
    def specificTurret(self, index):
        return self.turretList[index]
    
    def specificHull(self, index):
        return self.hullList[index]

    def setPlayer1Turret(self, index):
        self.p1I = index % len(self.turretList) # for safety

class Player(): # This is a class that is being reported to
    def __init__(self, name, CONTROLS = const.CONTROLS_TANK1, TANK_NAME = const.PLAYER_1_TANK_NAME, TANK_CHANNELS = const.PLAYER_1_CHANNELS, GUN_NAME = const.PLAYER_1_GUN_NAME, SPAWN = [(0,0)]):
        self.name = name
        self.kills = 0
        self.deaths = 0
        self.controls = CONTROLS
        self.tankName = TANK_NAME
        self.tankChannels = TANK_CHANNELS
        self.gunName = GUN_NAME
        self.spawn = SPAWN
    def getTableEntry(self):
        return [self.name, self.kills, self.deaths, self.kills / max(self.deaths, 1)]
    
    def addKill(self):
        self.kills += 1

    def addDeath(self):
        self.deaths += 1

    def addShoot(self):
        self.shoot += 1

    def addHit(self):
        self.hit += 1

    def getName(self):
        return self.name
    
    def resetPlayer(self):
        self.kills = 0
        self.deaths = 0

    def getControls(self):
        return self.controls
    
    def getTankName(self):
        return self.tankName
    
    def getTankChannels(self):
        return self.tankChannels
    
    def getGunName(self):
        return self.gunName
    
    def getSpawn(self):
        return self.spawn