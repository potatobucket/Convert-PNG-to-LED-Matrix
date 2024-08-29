"""
Handles logic for converting individual images to frames for the Arduino Uno R4 Wifi LED matrix.
"""

import exceptions
import gif_conversion
from PIL import Image

manditoryWidth = 12
manditoryHeight = 8

def format_for_matrix(first: str, second: str, third: str, name: str):
    """
Formats the three hexidecimal numbers (first, second, third) into a variable declaration for C++.
    """
    return f"""
const uint32_t {name}[] = {{
    {first},
    {second},
    {third}
}};"""

class Picture:
    """
Used to convert a picture to a format for an LED matrix on an Arduino Uno R4 Wifi board.
    """
    def __init__(self, imagePath: str, nameOfFrame: str):
        self.imagePath = imagePath
        self.nameOfFrame = nameOfFrame
    
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
            return format_for_matrix(hexOne, hexTwo, hexThree, self.nameOfFrame)

def convert_picture(picturePath: str, frameName: str):
    picture = Picture(picturePath, frameName)
    return picture.convert_to_matrix()

def convert_gif(gifPath: str):
    """
Converts a given GIF to a series of frames for the Arduino Uno R4 Wifi LED matrix and appends a C++ array of the frames at the end.
    """
    frameList = []
    if gifPath.split(".")[-1] != "gif":
        raise exceptions.NotAGif("File is not a gif")
    else:
        gif_conversion.extract_frames(gifPath, "Temporary")
    for index, frame in enumerate(gif_conversion.get_files("Temporary")):
        index = str(index).zfill(2)
        frame = Picture(f"Temporary/{frame}", f"frame{index}")
        frameList.append(f"frame{index}")
        print(frame.convert_to_matrix())
    print(gif_conversion.create_frame_array(frameList))
    gif_conversion.delete_folder("Temporary")

if __name__ == "__main__":
    #-- Example code to convert single image
    print(convert_picture("example.png", "heart"))

    #-- Example code to convert gif to series of single images
    convert_gif("example_gif.gif")
