import discord
from myfunctions import recap, hello

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
    
client.run('OTUxOTg5NDAxMTY3MjMzMTE2.YivfOA.Eu4RpqzDw5qJ8b-wkx5U_MhLw1U')
