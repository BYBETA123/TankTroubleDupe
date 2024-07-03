class ColorDicionary:
    
    COLORS = {
        "BLACK": '#000000',
        "WHITE": '#FFFFFF',
        "RED": '#FF0000',
        "GREEN": '#00FF00',
        "BLUE": '#0000FF',
    }
    
    def __init__(self):
        print("Using Beta's Color class")
        pass # Empty constructor as we are holding colors only

    def getHex(self, color):
        if color.upper() not in self.COLORS:
            print("The requested color isn't in the dictionary")
            return '#000000'
        # Return the HEX value of the color
        return self.COLORS[color.upper()]
    
    def getRGB(self, color):
        if color.upper() not in self.COLORS:
            print("The requested color isn't in the dictionary")
            return (0, 0, 0)
        # Return the RGB value of the color
        hex_value = self.COLORS[color.upper()].lstrip('#')
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    

