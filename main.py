import discord
import os
from myfunctions import recap

client = discord.Client()

@client.event
async def on_ready():
  print("We have loggied in as {0.user}".format(client))

    
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("$recap"):
    recap()
    with open('weeklyrecap.txt', 'rb') as fp:
      await message.channel.send(file=discord.File(fp, 'weeklyrecap.txt'))
#    await message.channel.send(recap())
  elif message.content.startswith("$update_wiki"):
    update_wiki()
    await message.channel.send("Updated Wiki Pages")
    
client.run(os.getenv('TOKEN'))
