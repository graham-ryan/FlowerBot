# Some helper functions for FlowerBot.py
import discord
import io
import aiohttp
from PIL import Image, ImageDraw

# Checks if the message sent is replying to a message with an image either attached, embedded, or has a link to. If it does, return it as an image.
async def getReplyingImage(ctx):
     if ctx.message.reference is not None: 
          # Get the referenced message
          message = ctx.message.reference.resolved 
          if ((len(message.attachments)>0) and (message.attachments[0].filename.endswith('.jpg') or message.attachments[0].filename.endswith('.jpeg') or message.attachments[0].filename.endswith('.png'))):
               # If message content contains an attachment with an image
               return await urlToImage(message.attachments[0].url)
          elif (message.content.endswith('.jpg') or message.content.endswith('.jpeg') or message.content.endswith('.png')):
               # If message content contains a link with an image
               return await urlToImage(message.content)
          elif (len(message.embeds)>0):
               # If message content has an embed, check if there is an image
               if (message.embeds[0].thumbnail != message.embeds[0].Empty):
                    return await urlToImage(message.embeds[0].thumbnail.url)
          else:
               return None
     else:
          return None

# Given a Discordpy Asset object, returns a PIL image object.
async def assetToImage(asset: discord.Asset) -> Image:
     imageBytes = io.BytesIO(await asset.read())
     return Image.open(imageBytes)

# Given a url string, returns a PIL image object. Returns none if something fails.
async def urlToImage(url: str):
     try:
          # Check if URL works
          connector = aiohttp.ClientSession()
          resp = await connector.get(url)
          buffer = io.BytesIO(await resp.read())
          img = Image.open(buffer)
          await connector.close()
          return img
     except Exception:
          # Something failed along the way                       
          await connector.close()
          return None