import discord
from myfunctions import weekly_recap, hello

client = discord.Client()

@client.event
async def on_ready():
  print("We have loggied in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("$weeklyrecap"):
    await message.channel.send(weekly_recap())

client.run('OTUxOTg5NDAxMTY3MjMzMTE2.YivfOA.Eu4RpqzDw5qJ8b-wkx5U_MhLw1U')
