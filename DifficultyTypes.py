from enum import Enum


class DifficultyType(Enum):
    # format is <Number> <Respawn> <AI> <No. of Players>, <humanCount>, <teamCount>, <Map>
    NotInGame = (0, False, False, 0, 0, 0, False)
    OnePlayerYard = (1, False, True, 2, 1, 2, False)
    OnePlayerScrapYard = (2, False, True, 2, 1, 2, False)
    TwoPlayerYard = (3, False, False, 2, 2, 2, False)
    TwoPlayerScrapYard = (4, False, False, 2, 2, 2, False)
    OnePlayerBrawl = (5, True, True, 2, 1, 2, False)
    OnePlayerDeathMatch = (6, True, True, 2, 1, 2, False)
    TwoPlayerBrawl = (7, True, False, 2, 2, 2, False)
    TwoPlayerDeathMatch = (8, True, False, 2, 2, 2, False)
    OnePlayerTDM = (9, True, True, 4, 1, 2, False)
    TeamDeathMatch = (10, True, True, 4, 2, 2, False)
    OnePlayerCaptureTheFlag = (11, True, True, 2, 1, 2, False)
    CaptureTheFlag = (12, True, True, 4, 2, 2, True)

    def __init__(self, number, respawn, ai, playerCount, human, teamCount, hasMap):
        self._value_ = number
        self.respawn = respawn
        self.ai = ai
        self.playerCount = playerCount
        self.humanCount = human
        self.teamCount = teamCount
        self.map = hasMap

    @classmethod
    def from_index(cls, index):
        for mode in cls:
            if mode.value == index:
                return mode
        raise ValueError(f"No GameMode with index {index}")