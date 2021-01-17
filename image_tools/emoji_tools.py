# Assorted methods to help convert emojis into images, and paste them onto images
import PIL.Image
import os

# Find Code Point for Emoji. Returns false if there isn't one.
def findCodePoint(arg: str):
    line = findAssociatedLine(arg)
    if (line == False):
        return False
    else:
        # Make line into just a substring
        line = line[0:19].strip().replace(" ","-")
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

def imagePaste():
    pass