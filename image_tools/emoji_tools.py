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

# Given a positions matrix and a position, turns 0s nearby the position to 0s (In a square like shape) so no emotes can be placed nearby this one in the future.
async def removePositionsFromPositionsMatrix(positionsMatrix: numpy.ndarray, position: tuple):
    leftX = position[0]-45 # Get left most x position of the square we turn to 0s
    rightX = position[0]+60 # Get right most x position of square
    topY = position[1]-36 # Get top most position of square
    bottomY = position[1]+63 # Get bottom most position of square

    shape = positionsMatrix.shape
    # Make sure rightX and bottomY don't go out of bounds, based on the matrix's shape
    if (rightX>shape[0]-1):
        rightX=shape[0]-1
    if (bottomY>shape[1]-1):
        bottomY=shape[1]-1

    for x in range(leftX,rightX):
        for y in range(topY,bottomY):
            if (x>=0 and y>=0):
                positionsMatrix[x,y] = 0

# Pastes images (sticker) onto another image (base) in the corner randomly based on the possible positions, in a chaotic way. Returns final image.
async def pasteEmotesChaos(base: Image, emotes: list, positionsMatrix: numpy.ndarray):        
    posX = range(base.width)
    posY = range(base.height)

    numPlacementPositions = numpy.sum(positionsMatrix)
    emotesLength = len(emotes)

    # Calculate how many emotes we want to send. 2.5 * number of possible emotes that can fit (if we just count their pixels).
    numEmotes = int((numPlacementPositions/5184.0)*2.5)

    # Paste the emotes.
    for i in range(numEmotes):
        sticker = emotes[i%emotesLength]
        # A do while loop: ends when we find a position in the matrix with a 1
        while True:
            position = (numpy.random.choice(posX),numpy.random.choice(posY))
            if (positionsMatrix[position[0],position[1]]==1):
                break
        position = (position[0]-15,position[1]-15) # Slightly adjust position (subtract 15) so left and top sides of the border have some emotes clipping through
        # Paste sticker onto base image
        base.paste(sticker,position,sticker)
    return base

# Pastes images (sticker) onto another image (base) in the corner randomly based on the possible positions, and based on placement type. Returns final image.
async def pasteEmotesNormal(base: Image, emotes, positionsMatrix: numpy.ndarray):        
    posX = range(base.width)
    posY = range(base.height)
    # Count the number of 1s in the positionsMatrix
    numPlacementPositions = numpy.sum(positionsMatrix)
    emotesLength = len(emotes)

    # Calculate how many emotes we want to send. We use the number of possible emotes that can fit (if we just count their pixels) * 1.2.
    numEmotes = int(numPlacementPositions/5184.0*1.2)

    # Paste the emotes.
    for i in range(numEmotes):
        sticker = emotes[i%emotesLength]
        # A do while loop: ends when we find a position in the matrix with a 1
        while True:
            position = (numpy.random.choice(posX),numpy.random.choice(posY))
            if (positionsMatrix[position[0],position[1]]==1):
                break
        position = (position[0]-15,position[1]-15) # Slightly adjust position so left and top sides of the border have some emotes clipping through
        # Paste sticker onto base image
        base.paste(sticker,position,sticker)
        # Remove placement positions from positionsMatrix. This keeps the emotes in good spacing.
        await removePositionsFromPositionsMatrix(positionsMatrix,position)

    return base

# Pastes images (sticker) onto another image (base) in the corner randomly based on the possible positions, and based on placement type. Returns final image.
async def pasteEmotesLight(base: Image, emotes, positionsMatrix: numpy.ndarray):        
    posX = range(base.width)
    posY = range(base.height)
    # Count the number of 1s in the positionsMatrix
    numPlacementPositions = numpy.sum(positionsMatrix)
    emotesLength = len(emotes)

    # Calculate how many emotes we want to send. We use the number of possible emotes that can fit (if we just count their pixels) / 2
    numEmotes = int(numPlacementPositions/5184.0/5.0)

    # Paste the emotes.
    for i in range(numEmotes):
        sticker = emotes[i%emotesLength]
        # A do while loop: ends when we find a position in the matrix with a 1
        while True:
            position = (numpy.random.choice(posX),numpy.random.choice(posY))
            if (positionsMatrix[position[0],position[1]]==1):
                break
        position = (position[0]-15,position[1]-15) # Slightly adjust position so left and top sides of the border have some emotes clipping through
        # Paste sticker onto base image
        base.paste(sticker,position,sticker)
        # Remove placement positions from positionsMatrix. This keeps the emotes in good spacing.
        await removePositionsFromPositionsMatrix(positionsMatrix,position)

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



