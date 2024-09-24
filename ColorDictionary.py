class ColourDictionary:

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
        "TANK_GREEN" : '#22B14D',
        "BURGUNDY" : '#880015',
        "ORANGE" : '#FF7D27',
        "YELLOW" : '#FFC90E',
        "SKY_BLUE" : '#00A2E8',
        "LIGHT_BROWN" : '#B97A57',
        "DARK_LILAC" : '#A349A4',
        "BRIGHT_PINK" : '#FF00FF',
        "NEON_PURPLE" : '#BC13FE',
        "SOFT_WHITE" : '#D9D9D9',
        "BEIGE" : '#F5F5DC',
        "SAND_BEIGE" : '#F4A460',
    }

    def __init__(self):
        # Empty constructor as we are holding colors only
        print("Using Beta's Color class")
        raise ValueError("Dont use this class")

    @staticmethod
    def getHex(color = "BLACK"):
        # This function returns the HEX value of the color
        # Inputs: color (string) This should match with one of the colors in the dictionary
        # Outputs: HEX value of the color

        if color.upper() not in ColourDictionary.COLORS:
            print("The requested color isn't in the dictionary")
            return '#000000'
        # Return the HEX value of the color
        return ColourDictionary.COLORS[color.upper()]
    
    @staticmethod
    def getRGB(color="BLACK"):
        #This function returns the RGB value of the color
        # Inputs: color (string) This should match with one of the colors in the dictionary
        # Outputs: Tuple of 3 integers (R, G, B)
        if color.upper() not in ColourDictionary.COLORS:
            print("The requested color isn't in the dictionary")
            return (0, 0, 0)
        # Return the RGB value of the color
        hex_value = ColourDictionary.COLORS[color.upper()].lstrip('#')
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def geT(color="BLACK"):
        # This function is just a faster way of returning the tuple
        # Inputs: color (string) This should match with one of the colors in the dictionary
        # Outputs: Tuple of 3 integers (R, G, B)
        return ColourDictionary.getRGB(color)