# Assorted methods to help convert emojis into images, and paste them onto images
from PIL import Image, ImageDraw
import os
import math
import numpy

# Find Code Point for Emoji. Returns false if there isn't one.
def findCodePoint(arg: str):
    line = findAssociatedLine(arg)
    if (line == False):
        return False
    else:
        # Make line into just a substring
        line = line[0:20].strip().replace(" ","-")
        return(line)

# Returns the line associated with the Emoji passed to this function
def findAssociatedLine(arg: str):
    # ToDo: Make this path relative
    dirname = os.path.dirname(__file__)
    file = open(f"{dirname}\\emoji-mapping.txt","r",encoding="utf8")
    for line in file:
        if arg in line:
            ans = line
            file.close()
            print(ans)
            return(ans)      
    return False

# Pastes images (sticker) onto another image (base) in the corner randomly based on the possible positions, and based on placement type. Returns final image.
async def pasteEmotes(base: Image, sticker: Image, positionsMatrix: numpy.ndarray, placementType : str):
    sticker.thumbnail((72,72)) # Resize to 72x72. Default emotes are always 72x72, so this is just for custom ones.
    sticker = sticker.convert('RGBA')
    posX = range(base.width)
    posY = range(base.height)
    # Count the number of 1s in the positionsMatrix
    count = numpy.sum(positionsMatrix)

    # Paste the desired number of emotes
    for i in range(5):
        # A do while loop: ends when we find a position in the matrix with a 1
        while True:
            position = (numpy.random.choice(posX),numpy.random.choice(posY))
            if (positionsMatrix[position[0],position[1]]==1):
                break
        position = (position[0]-15,position[1]-15) # Slightly adjust position so left and top sides of the border have some emotes clipping through
        # Paste sticker onto base image
        base.paste(sticker,position,sticker)
    base.show()
    return base

# Generates posible positions for emojis to be pasted on the border. The border is 1/10 of the width/height. Returns a matrix with 1s where images can be placed, 0s where they can't.
def generatePossibleBorderPositions(base: Image, canGoOffBorder: bool):
    # Create an array representing pixels
    positionsMatrix = numpy.ones((base.width,base.height))
    borderWidth = base.width//12
    borderHeight = base.height//12

    if (canGoOffBorder):
        adjust = 40
    else:
        adjust = 0

    # Set the inside of the picture to 0s, where emotes shouldn't be placed
    for y in range(borderHeight,base.height-borderHeight-adjust):
        for x in range(borderWidth,base.width-borderWidth-adjust):
            positionsMatrix[x,y] = 0

    # Set right and bottom borders to 0s so it looks better when pasting
    # Bottom Border
    for x in range(base.width):
        for y in range(base.height-adjust,base.height):
            positionsMatrix[x,y] = 0
    # Right border
    for x in range(base.width-adjust,base.width):
        for y in range(base.height):
            positionsMatrix[x,y] = 0

    return positionsMatrix



