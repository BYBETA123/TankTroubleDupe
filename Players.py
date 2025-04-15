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
    
    def movePlayer2TurretColourIndex(self, move):
        self.p2K = (self.p2K + move) % len(self.ColorIndex)
        if self.p2K == self.p1K:
            self.p2K = (self.p2K + move) % len(self.ColorIndex)
    
    def movePlayer1HullColourIndex(self, move):
        self.p1L = (self.p1L + move) % len(self.ColorIndex)
        if self.p1L == self.p2L:
            self.p1L = (self.p1L + move) % len(self.ColorIndex)

    def movePlayer2HullColourIndex(self, move):
        self.p2L = (self.p2L + move) % len(self.ColorIndex)
        if self.p2L == self.p1L:
            self.p2L = (self.p2L + move) % len(self.ColorIndex)

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

class Player(): # This is a class that is being reported to
    def __init__(self, name):
        self.name = name
        self.kills = 0
        self.deaths = 0

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