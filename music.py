import sys, os
import pygame
class Music:

    # This class will be used to handle all the music in the game
    # This class is built specifically for this project and generally will not work outside of the project

    lobbyMusicMax = 0.2

    selectionMusicMax = 1

    gameMusicMax = 0.2

    tankShootMax = 1
    tankDeadMax = 0.5
    turretRotateMax = 0.2
    tankMoveMax = 0.05

    currentTrack = None
    currentTrackString = 'lobby'
    nextTrack = None
    nextTrackString = 'lobby'
    fadeTrack = 0
    trigger = False

    def __init__(self):
        super().__init__()
        pygame.mixer.init() # Initialising music

        # Determine the correct base path
        if getattr(sys, 'frozen', False):  # Running as an .exe
            base_path = sys._MEIPASS
        else:  # Running as a .py script
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.tracks = {
            'lobby': pygame.mixer.Sound(os.path.join(base_path, 'Sounds/lobby_music.wav')),
            'selection': pygame.mixer.Sound(os.path.join(base_path, 'Sounds/selection_music.wav')),
            'game': pygame.mixer.Sound(os.path.join(base_path, 'Sounds/game_music.wav'))
        }

        self.volume = {
            'lobby': 0.2,
            'selection': 1,
            'game': 0.2,
        }

        self.hardVolume = {
            'lobby': 0.2,
            'selection': 1,
            'game': 0.2,
            }

        self.channels = {
            'lobby': pygame.mixer.Channel(0),
            'selection': pygame.mixer.Channel(1),
            'game': pygame.mixer.Channel(2)
        }

        self.busyChannels = {
            'tankShoot': pygame.mixer.Channel(3),
            'tankDead': pygame.mixer.Channel(4),
            'turretRotate': pygame.mixer.Channel(5),
            'tankMove': pygame.mixer.Channel(6)
        }

        self.playing = {
            'tankShoot': False,
            'tankDead': False,
            'turretRotate': False,
            'tankMove': False
        }

        self.currentTrack = self.tracks['lobby']

    def crossfade(self, nextTrack):
        if self.currentTrackString == nextTrack:
            return # Do nothing if the next track is the same as the current track
        self.trigger = True
        self.nextTrack = self.tracks[nextTrack]
        self.nextTrackString = nextTrack
        self.fadeTrack = 0

    def update(self, newVolumes=1):

        if self.trigger:
            self.channels[self.nextTrackString].set_volume(self.fadeTrack * self.volume[self.nextTrackString]*newVolumes)
            self.channels[self.currentTrackString].set_volume((1 - self.fadeTrack) * self.volume[self.currentTrackString]*newVolumes)
            for channel in self.channels:
                if channel != self.nextTrackString and channel != self.currentTrackString:
                    self.channels[channel].set_volume(0)
            self.fadeTrack += 0.01

            if self.fadeTrack >= 1: # This might need to be altered to better suit the music bug
                self.currentTrack = self.nextTrack
                self.currentTrackString = self.nextTrackString
                self.channels[self.nextTrackString].set_volume(self.volume[self.nextTrackString]*newVolumes) # Set the volume of the next track to 1
                self.trigger = False
                self.fadeTrack = 0
        else:
            self.channels[self.currentTrackString].set_volume(newVolumes*self.hardVolume[self.currentTrackString])

    def play(self):
        self.channels['lobby'].play(self.tracks['lobby'], loops=-1)
        self.currentTrack = self.tracks['lobby']
        self.channels['lobby'].set_volume(self.volume['lobby'])

        self.channels['selection'].play(self.tracks['selection'], loops=-1)
        self.channels['selection'].set_volume(self.volume['selection']*0)

        self.channels['game'].play(self.tracks['game'], loops=-1)
        self.channels['game'].set_volume(self.volume['game']*0)

    def stop(self):
        self.currentTrack.stop()
        self.playing = False
