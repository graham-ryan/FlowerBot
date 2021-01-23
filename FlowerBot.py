# Main File for FlowerBot
import discord
import os
import io
import aiohttp
import FlowerBotHelpers
from PIL import Image, ImageDraw
from discord.ext import commands
from image_tools import emoji_tools

# Choose bot command prefix
bot = commands.Bot(command_prefix = '~')

dirname = os.path.dirname(__file__)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# If you reference a message with an image in yours when using this command, it will send back the image you referenced.
@bot.command()
async def gimmethat(ctx):
    if ctx.message.reference is not None: 
        # Get the referenced message
        message = ctx.message.reference.resolved 
        if ((len(message.attachments)>0) and (message.attachments[0].filename.endswith('.jpg') or message.attachments[0].filename.endswith('.jpeg') or message.attachments[0].filename.endswith('.png'))):
            # If message content contains an attachment, send it back
            f = message.attachments[0].url
            await ctx.send(f)
        elif (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
            # If message content contains a link with an image, send the link back
            try:
                # Check if URL works
                connector = aiohttp.ClientSession()
                await connector.get(message.content)
                await ctx.send(message.content)
            except Exception:
                await ctx.send('That isn\'t an image.')           
            await connector.close()
        elif (len(message.embeds)>0):
            # If message content has an embed, check if there is an image
            if (message.embeds[0].thumbnail != message.embeds[0].Empty):
                await ctx.send(message.embeds[0].thumbnail.url)
        else:
            await ctx.send('That isn\'t an image.')
    else:
        await ctx.send('You have to reference something for me to give you it.')

# Sends a picture to the server from this folder called pic.png
@bot.command()
async def sendpics(ctx):
    f = discord.File(f"{dirname}/pic.png")
    await ctx.send(file=f) 

# Sends the emojis you sent back as an image
@bot.command()
async def emojitoimage(ctx, *args : str):
    # Loop through each arg
    for arg in args:
        # Try converting to Emoji object:
        try:
            print (arg)
            Converter = commands.PartialEmojiConverter()
            emote = await Converter.convert(ctx=ctx,argument=arg)
            await ctx.send(emote.url)
        except (commands.EmojiNotFound, commands.errors.PartialEmojiConversionFailure):
            # Try to find emoji
            codePoint = emoji_tools.findCodePoint(arg)
            if (codePoint != False):
                # Get the image and send it
                f = discord.File(f"{dirname}/72x72/{codePoint}.png")
                await ctx.send(file=f)              
            else:
                await ctx.send(f'\'{arg}\' is not an emote.')

# Creates a border of emotes with the given integer and emotes, pasted onto the image this message was replying to.
@bot.command()
async def border(ctx, placementType: str, *args : str):
    if placementType.lower()!='light' and placementType.lower()!='normal' and placementType.lower()!='chaos':
        # First arg is invalid
        await ctx.send(f'Please specify either Light, Normal, or Chaos.\nUsage: `{bot.command_prefix}border [Light/Normal/Chaos] <Emote>...`')
    else:
        # First command arg was valid, and message is replying to an image.
        # Download image that message is replying to (if there is one)
        base = await FlowerBotHelpers.getReplyingImage(ctx)
        if (base == None):
            await ctx.send('You must reply to a message with an image to use this command.')
        else:
            # Base image successfully created
            # Create list of emoji pics
            emotes = []
            # Loop through each arg and get emotes
            for arg in args:
                # Try converting to Emoji object:
                try:
                    Converter = commands.EmojiConverter()
                    emote = await Converter.convert(ctx=ctx,argument=arg)
                    emotes.append(await FlowerBotHelpers.assetToImage(emote.url))
                except (commands.EmojiNotFound):
                    # Try to find emoji
                    codePoint = emoji_tools.findCodePoint(arg)
                    if (codePoint != False):
                        # Get the image and send it
                        emotes.append(Image.open(f"{dirname}/72x72/{codePoint}.png"))             
                    else:
                        await ctx.send(f'\'{arg}\' is not a valid emote.')
            # Check if any emotes were successfully parsed. If so, generate the image. Else, display an error.
            if len(emotes) > 0:
                possiblePositions = emoji_tools.generatePossibleBorderPositions(base,True) # Generate possible positions matrix
                # Convert PIL Image to bytes object so discord can send it as a file.
                with io.BytesIO() as by:
                    for emote in emotes:
                        finalImage = await emoji_tools.pasteEmotes(base, emote, possiblePositions, placementType)
                    finalImage.save(by,"PNG")
                    by.seek(0)
                    await ctx.send(file=discord.File(fp=by,filename="border.png"))
            else:
                await ctx.send('No valid emotes were provided.')
                
    
# Put the bot's client secret key here
bot.run('')