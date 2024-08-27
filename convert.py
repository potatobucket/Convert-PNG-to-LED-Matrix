import exceptions
from PIL import Image

manditoryWidth = 12
manditoryHeight = 8

def format_for_matrix(first: str, second: str, third: str):
    """
Formats the three hexidecimal numbers (first, second, third) into a variable declaration for C++.
    """
    curlyOpen = "{"   # -- a hacky way to get the f-string to work
    curlyClosed = "}" # -- nothing else I tried worked. I'm sorry
    return f"""
const uint32_t frame[] = {curlyOpen}
    {first},
    {second},
    {third}
{curlyClosed};
                """

class Picture:
    """
Used to convert a picture to a format for an LED matrix on an Arduino Uno R4 Wifi board.
    """
    def __init__(self, imagePath: str):
        self.imagePath = imagePath
    
    def convert_to_matrix(self):
        """
    Handles the conversion process.
        """
        with Image.open(self.imagePath) as img:
            img = img.convert("1")
            width, height = img.size
            if width > manditoryWidth or height > manditoryHeight:
                raise exceptions.TooBig("Image too large. Must be 12x8")
            elif width < manditoryWidth or height < manditoryHeight:
                raise exceptions.TooSmall("Image too small. Must be 12x8")
            pixelData = ["0" if img.getpixel((column, row)) == 0 else "1" for row in range(height) for column in range(width)]
            firstSet = pixelData[:32]
            secondSet = pixelData[32:64]
            thirdSet = pixelData[64:]
            hexOne = hex(int("".join(firstSet), 2))
            hexTwo = hex(int("".join(secondSet), 2))
            hexThree = hex(int("".join(thirdSet), 2))
            return format_for_matrix(hexOne, hexTwo, hexThree)

if __name__ == "__main__":
    picture = Picture("example.png")
    print(picture.convert_to_matrix())
