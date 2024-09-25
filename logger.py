import time

class Logger():
    # This class will be used to log any messages to a file
    filename = "log.txt" # default filename
    def __init__(self):
        pass # Empty constructor until needed
        self.clear() # Clear the log file on startup

    def log(self, msg):
        # This will be used to log any message to the log file
        # Inputs: msg: string, the message to be logged
        # Outputs: None
        #
        with open(self.filename, "a") as f:
            f.write(msg + "\n")

    def set_filename(self, filename):
        self.filename = filename
    
    def get_filename(self):
        return self.filename
    
    def clear(self):
        # This function will clear the file when run
        # Inputs: None
        # Outputs: None

        f = open(self.filename, "w")
        f.close() # Wipe the file and create a new one
        print("The log file has been cleared")

class SpeedTimer():
    def __init__(self, filename="speedtimer.txt", note="No note provided"):
        self.start_time = None
        self.end_time = None
        self.note  = note
        self.filename = "speedtimer.txt"
        self.split = None
        #wipe the file
        f= open(self.filename, "w")
        f.close()

    def start(self): # Starts the timer
            self._write_to_file("Timer started")
            self.start_time = time.time()
            self.split = self.start_time

    def stop(self): # Stops the timer
            self.end_time = time.time()
            self._write_to_file("Timer stopped")

    def elapsed(self): # Calculates the elapsed time
            if self.start_time is None:
                return 0
            elif self.end_time is None:
                return time.time() - self.start_time
            else:
                return self.end_time - self.start_time

    def split_time(self): # Splits the time
        self.split = time.time()
        self._write_to_file("Split time")

    def peek(self, note = ""): # Prints the elapsed time
        self._write_to_file(f"Peek: {note} : {time.time() - self.split :.4f}")
        self.split = time.time()

    def logTime(self): # log the time briefly (most helpful for small timing debugging)
        self._write_to_file("Time logged")

    def _write_to_file(self, message): # Write the message to the file
        starting_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time))
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        elapsed_time = self.elapsed()
        with open(self.filename, "a") as f:
            f.write(f"{starting_time} : {current_time} - {elapsed_time:.4f} - Note: {self.note} - {message}\n")