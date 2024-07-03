class ColorDicionary:
    
    colors = {
        "black": '#000000',
        "white": '#FFFFFF',
        "red": '#FF0000',
        "green": '#00FF00',
        "blue": '#0000FF',
    }
    
    def __init__(self):
        print("Using Beta's Color class")
        pass # Empty constructor as we are holding colors only

    def getHex(self, color):
        if color.lower() not in self.colors:
            print("The requested color isn't in the dictionary")
            return '#000000'
        # Return the HEX value of the color
        return self.colors[color.lower()]
    
    def getRGB(self, color):
        if color.lower() not in self.colors:
            print("The requested color isn't in the dictionary")
            return (0, 0, 0)
        # Return the RGB value of the color
        hex_value = self.colors[color.lower()].lstrip('#')
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    

