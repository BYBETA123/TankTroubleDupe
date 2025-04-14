import time
class UpDownTimer():
    def __init__(self, duration = 0, up = True):
        self.duration = duration * 1e9 # duration in nano seconds
        self.startTime = time.time_ns()
        self.timer = self.startTime
        self.up = up
        self.expired = False
        self.paused = False
        self.pausedTime = 0

    def tick(self):
        if self.paused:
            return # exit early
        if self.isExpired():
            return # exit early
        # we are counting up
        if self.timer < self.duration + self.startTime:
            self.timer = time.time_ns()
        if self.timer >= self.duration + self.startTime:
            self.timer = self.duration + self.startTime
            self.expired = True
            
    def reset(self):
        self.timer = time.time_ns()
        self.startTime = time.time_ns()
        self.expired = False
        self.paused = False
    
    def setDirection(self, up):
        # up is True and down is False
        self.up = up
        self.startTime = time.time_ns()

    def setDuration(self, duration):
        # set the duration of the timer in seconds
        self.duration = duration * 1e9
        self.startTime = time.time_ns()

    def start(self):
        self.startTime = time.time_ns()
        self.timer = self.startTime if self.up else self.duration
        self.expired = False

    def pause(self):
        self.pausedTime = time.time_ns()
        self.paused = True

    def resume(self):
        self.paused = False
        cTime = time.time_ns()
        self.timer -= (cTime - self.pausedTime) # capture
        self.startTime += (cTime - self.pausedTime)

    def getElapsed(self):
        return self.timer - self.startTime if self.up else self.duration - self.timer + self.startTime

    def getElapsedAsSeconds(self):
        return self.getElapsed()/1e9

    def isExpired(self):
        return self.expired

    def getTime(self):
        return int(self.getElapsed()//1e9)