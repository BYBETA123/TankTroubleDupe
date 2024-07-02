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