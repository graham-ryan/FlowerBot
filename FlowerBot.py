import discord
import os
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
        message = ctx.message.reference.resolved # Gets the referenced message
        if (not message.attachments):
            await ctx.send('This isn\'t an image.')
        elif not (message.attachments[0].filename.endswith('.jpg') or message.attachments[0].filename.endswith('.png') or message.attachments[0].filename.endswith('.jpeg')):
            await ctx.send('This isn\'t an image.')
        else:
           f = await message.attachments[0].to_file()
           await ctx.send(file=f)
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
    # List of emote pics
    emotes = []
    # Loop through each arg
    for arg in args:
        # Try converting to Emoji object:
        try:
            Converter = commands.PartialEmojiConverter()
            emote = await Converter.convert(ctx=ctx,argument=arg)
            await ctx.send(emote.url)
            emotes.append(emote.url)
        except (commands.EmojiNotFound, commands.errors.PartialEmojiConversionFailure):
            # Try to find emoji
            codePoint = emoji_tools.findCodePoint(arg)
            if (codePoint != False):
                # Get the image and send it
                f = discord.File(f"{dirname}/72x72/{codePoint}.png")
                await ctx.send(file=f)              
            else:
                await ctx.send(f'\'{arg}\' is not an emote.')

# Put the bot's client secret key here
bot.run('Nzk4NjY4OTUyOTMzNzYxMDQ0.X_4YbA.4P0i8MdDL8mXXSoEAoZ9KW_YH2w')