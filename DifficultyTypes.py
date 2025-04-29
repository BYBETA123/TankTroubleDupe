from enum import Enum


class DifficultyType(Enum):
    # format is <Number> <Respawn> <AI> <No. of Players>, <humanCount>, <teamCount>
    NotInGame = (0, False, False, 0, 0, 0)
    OnePlayerYard = (1, False, True, 2, 1, 2)
    OnePlayerScrapYard = (2, False, True, 2, 1, 2)
    TwoPlayerYard = (3, False, False, 2, 2, 2)
    TwoPlayerScrapYard = (4, False, False, 2, 2, 2)
    OnePlayerBrawl = (5, True, True, 2, 1, 2)
    OnePlayerDeathMatch = (6, True, True, 2, 1, 2)
    TwoPlayerBrawl = (7, True, False, 2, 2, 2)
    TwoPlayerDeathMatch = (8, True, False, 2, 2, 2)
    OnePlayerTDM = (9, True, True, 8, 1, 2)
    TeamDeathMatch = (10, True, True, 8, 2, 2)
    OnePlayerCaptureTheFlag = (11, True, True, 2, 1, 2)
    CaptureTheFlag = (12, True, False, 2, 2, 2)

    def __init__(self, number, respawn, ai, playerCount, human, teamCount):
        self._value_ = number
        self.respawn = respawn
        self.ai = ai
        self.playerCount = playerCount
        self.humanCount = human
        self.teamCount = teamCount

    @classmethod
    def from_index(cls, index):
        for mode in cls:
            if mode.value == index:
                return mode
        raise ValueError(f"No GameMode with index {index}")