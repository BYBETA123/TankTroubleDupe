class ColorDicionary:
    
    COLORS = {
        "BLACK": '#000000',
        "WHITE": '#FFFFFF',
        "RED": '#FF0000',
        "GREEN": '#00FF00',
        "BLUE": '#0000FF',
        "GREY": '#808080',
        "GRAY": '#808080',
        "LIGHT_GREY": '#C6C6C6',
        "OFF_WHITE": '#F0F0F0',
        "OWHITE": '#FFFAF0',
    }

    def __init__(self):
        # Empty constructor as we are holding colors only
        print("Using Beta's Color class")

    def getHex(self, color = "BLACK"):
        # This function returns the HEX value of the color
        # Inputs: color (string) This should match with one of the colors in the dictionary
        # Outputs: HEX value of the color

        if color.upper() not in self.COLORS:
            print("The requested color isn't in the dictionary")
            return '#000000'
        # Return the HEX value of the color
        return self.COLORS[color.upper()]
    
    def getRGB(self, color="BLACK"):
        #This function returns the RGB value of the color
        # Inputs: color (string) This should match with one of the colors in the dictionary
        # Outputs: Tuple of 3 integers (R, G, B)
        if color.upper() not in self.COLORS:
            print("The requested color isn't in the dictionary")
            return (0, 0, 0)
        # Return the RGB value of the color
        hex_value = self.COLORS[color.upper()].lstrip('#')
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    
    def geT(self, color="BLACK"):
        # This function is just a faster way of returning the tuple
        # Inputs: color (string) This should match with one of the colors in the dictionary
        # Outputs: Tuple of 3 integers (R, G, B)
        return self.getRGB(color)