import pygame
class Music:
    # global tankShootSFX, tankDeadSFX, turretRotateSFX, tankMoveSFX
    # tankShootSFX = pygame.mixer.Sound("Sounds/tank_shoot.mp3")
    # tankShootMax = 1

    # tankDeadSFX = pygame.mixer.Sound("Sounds/tank_dead.mp3")
    # tankDeadMax = 0.5

    # turretRotateSFX = pygame.mixer.Sound("Sounds/tank_turret_rotate.wav")
    # turretRotateMax = 0.2

    # tankMoveSFX = pygame.mixer.Sound("Sounds/tank_moving.mp3")
    # tankMoveMax = 0.05

    # lobbyMusic = pygame.mixer.Sound("Sounds/lobby_music.wav")
    # lobbyMusicMax = 0.2

    # selectionMusic = pygame.mixer.Sound("Sounds/selection_music.mp3")
    # selectionMusicMax = 1

    # gameMusic = pygame.mixer.Sound("Sounds/game_music.mp3")
    # gameMusicMax = 0.2

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
        pygame.mixer.set_num_channels(16) # Setting the number of channels to 16

        self.tracks = {
            'lobby': pygame.mixer.Sound('Sounds/lobby_music.wav'),
            'selection': pygame.mixer.Sound('Sounds/selection_music.mp3'),
            'game': pygame.mixer.Sound('Sounds/game_music.mp3')
        }

        self.volume = {
            'lobby': 0.2,
            'selection': 1,
            'game': 0.2,
            'tankShoot': 1,
            'tankDead': 0.5,
            'turretRotate': 0.2,
            'tankMove': 0.05
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

        self.customSoundVolume = {
            'tankShoot': 0,
            'tankDead': 0,
            'turretRotate': 0,
            'tankMove': 0
        }

        self.currentTrack = self.tracks['lobby']

    def crossfade(self, nextTrack):
        if self.currentTrackString == nextTrack:
            return # Do nothing if the next track is the same as the current track
        self.trigger = True


        self.nextTrack = self.tracks[nextTrack]
        self.nextTrackString = nextTrack
        self.fadeTrack = 0

    def update(self):
        if self.trigger:
            self.channels[self.nextTrackString].set_volume(self.fadeTrack * self.volume[self.nextTrackString])
            self.channels[self.currentTrackString].set_volume((1 - self.fadeTrack) * self.volume[self.currentTrackString])
            self.fadeTrack += 0.01

            if self.fadeTrack >= 1:
                self.currentTrack = self.nextTrack
                self.currentTrackString = self.nextTrackString
                self.channels[self.nextTrackString].set_volume(self.volume[self.nextTrackString]*1) # Set the volume of the next track to 1
                self.trigger = False
                self.fadeTrack = 0

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
