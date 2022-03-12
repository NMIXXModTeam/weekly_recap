import discord
from discord import Embed
from discord.ext import commands
import asyncpraw
import random
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
    
@client.command(aliases=['memes'])
async def meme(ctx):
    subreddit = await reddit.subreddit("memes")
    all_subs = []
    top = subreddit.top(limit = 200)
    async for submission in top:
      
      all_subs.append(submission)
    
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    ups = random_sub.score
    link = random_sub.permalink
    comments = random_sub.num_comments
    embed = discord.Embed(title=name,url=f"https://reddit.com{link}", color=ctx.author.color)
    embed.set_image(url=url)
    embed.set_footer(text = f"👍{ups} 💬{comments}")
    await ctx.send(embed=embed)
    
client.run('OTUxOTg5NDAxMTY3MjMzMTE2.YivfOA.Eu4RpqzDw5qJ8b-wkx5U_MhLw1U')
