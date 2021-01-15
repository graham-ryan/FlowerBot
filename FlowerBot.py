import discord
import PIL.Image
from discord.ext import commands

bot = commands.Bot(command_prefix = '~')

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
        elif not (message.attachments[0].filename.endswith('.jpg') or message.attachments[0].filename.endswith('.png')):
            await ctx.send('This isn\'t an image.')
        else:
           f = await message.attachments[0].to_file()
           await ctx.send(file=f)
    else:
        await ctx.send('You have to reference something for me to give you it.')

# Sends a wolf to the server
@bot.command()
async def sendpics(ctx):
    f = discord.File("C:/Users/graha/OneDrive/Pictures/wolfs.jpg", filename="wolfys.jpg")
    await ctx.send(file=f) 

# Sends the emoji you sent back as an image
@bot.command()
async def emoji(ctx):
    print(ctx.message.content)
    b = bytes(ctx.message.content, 'utf-8')
    print(b)

# Put the bot's client secret key here
bot.run('')