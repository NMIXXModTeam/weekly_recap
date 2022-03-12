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
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("$hello"):
    await message.channel.send(hello())

@commands.command(name="meme")
async def meme(self, ctx, subred="memes"): # default subreddit is memes, later in the command you can select one of your choice (example: !meme python --> chooses r/python reddit post)
    msg = await ctx.send('Loading ... ')

    reddit = asyncpraw.Reddit(client_id='clientid',
                              client_secret='clientsecret',
                              username='username',
                              password='password',
                              user_agent='useragent')

    subreddit = await reddit.subreddit(subred)
    all_subs = []
    top = subreddit.top(limit=250) # bot will choose between the top 250 memes

    async for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    embed = Embed(title=f'__{name}__', colour=discord.Colour.random(), timestamp=ctx.message.created_at, url=url)

    embed.set_image(url=url)
    embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
    embed.set_footer(text='Here is your meme!')
    await ctx.send(embed=embed)
    await msg.edit(content=f'<https://reddit.com/r/{subreddit}/> :white_check_mark:') # < and > remove the embed link
    return
client.run('OTUxOTg5NDAxMTY3MjMzMTE2.YivfOA.Eu4RpqzDw5qJ8b-wkx5U_MhLw1U')
