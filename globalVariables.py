import pygame
import globalVariables as g
import constants as const
from otherClasses import Explosion, Flag
from DifficultyTypes import *

tankDead = [False, False, False, False, False, False, False, False] # This is to keep track of the tanks that are dead
tankList = [None for _ in range(8)] # list of all the current tanks in the game
gunList = [None for _ in range(8)] # list of all the current guns in the game

explosionGroup = pygame.sprite.Group() #All the explosions
bulletSprites = pygame.sprite.Group()
difficultyType = DifficultyType.NotInGame # difficulty Type
selectedMap = "Maps/flags.txt" # until we have other map options
tileList = [] #All the tiles in the game
team1Score = 0
team2Score = 0
playScreen = pygame.Surface((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

backgroundImage = pygame.image.load("Assets/image.png").convert() # Background image for the play screen
backgroundImage = pygame.transform.scale(backgroundImage, (const.WINDOW_WIDTH, const.WINDOW_HEIGHT))

flag = [Flag(0, (0,0)), Flag(1, (0,0))]

def spareChannels(sound):
    soundList = [pygame.mixer.Channel(i) for i in range(15, pygame.mixer.get_num_channels())]
    for channel in soundList:
        if not channel.get_busy():
            channel.play(sound) # attempt to play the sound
            return
    print("No available channels")
    return


def damage(tank, damage, owner):
    # This function will adjust the damage that the tank has taken
    # Inputs: damage: The amount of damage that the tank has taken
    # Outputs: None
    if tank.health <= 0: # if it was already dead
        return
    tank.health -= (damage * (0.55 if tank.effect[1] != 0 else 1)) if ((owner.getTeam() != tank.getTeam()) or (owner.getName() == tank.getPlayer().getName())) else 0 # if the tank is on the same team, don't do damage
    if tank.health > 0:
        if not tank.channelDict["death"]["channel"].get_busy(): # if the sound isn't playing
            tank.channelDict["death"]["channel"].play(const.SOUND_DICTIONARY["tankHurt"])  # Play sound indefinitely
        else:
            g.spareChannels(const.SOUND_DICTIONARY["tankHurt"])
    else: # if tank is dead
        # if the tank is dead everything should stop
        if owner.getName() != tank.getPlayer().getName(): # as long as it is not a self-kill
            owner.addKill()
        tank.getPlayer().addDeath()
        for channel in tank.channelDict:
            if tank.channelDict[channel]["channel"].get_busy():
                tank.channelDict[channel]["channel"].stop()
        # last sound to be played
        if not tank.channelDict["death"]["channel"].get_busy():
            tank.channelDict["death"]["channel"].play(const.SOUND_DICTIONARY["tankDeath"])
        else:
            spareChannels(const.SOUND_DICTIONARY["tankDeath"])
    updateTankHealth() # Manage the healthbar outside of the code


def updateTankHealth():
    # This function will update the tank health and check if the tank is dead
    # Inputs: None
    # Outputs: None
    global tankDead
    global allSprites, tankList, gunList
    #Update the tank health
    for i in range(difficultyType.playerCount):
        if not tankDead[i]:
            if tankList[i].getHealth() <= 0:
                # if the tank was holding a flag drop the flag
                if tankList[i].getFlag() is not None: # we have a flag
                    g.flag[tankList[i].getFlag()].drop()
                gunList[i].kill()
                tankList[i].kill()
                if not tankDead[i]:
                    tankDead[i] = True
                    g.explosionGroup.add(Explosion(tankList[i].getCenter()[0], tankList[i].getCenter()[1]))
                # try this
                gunList[i] = None
                tankList[i] = None
