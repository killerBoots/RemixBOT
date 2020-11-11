# bot.py
import os
import psycopg2
import random
import discord
from discord.ext import commands


# from dotenv import load_dotenv
# load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='frost', help='Link to frost resist guide.')
async def frost(ctx):
    response = 'https://bittsguides.com/frost-resistance-gear-naxxramas/'
    await ctx.send(response)


@bot.command(name='roll', help='Syntax: "!roll 20 55"  Simulates rolling x to y. Default 1 to 100.')
async def roll(ctx, x = 1, y = 101):
    response = random.randint(x, y)
    await ctx.send(response)

@bot.command(name='addons', help='List of required and usefull raid addons.')
async def addons(ctx):
    response = (
        'Deadly Boss Mods: https://www.curseforge.com/wow/addons/deadly-boss-mods/files \n'
        'Details!: https://www.curseforge.com/wow/addons/details/files \n'
        'Power Raid: https://www.curseforge.com/wow/addons/power-raid \n'
        'Community DKP: https://www.curseforge.com/wow/addons/community-dkp \n'
    )
    await ctx.send(response)

@bot.command(name='schedule', help='Raid team schedules.')
async def schedule(ctx):
    response = (
        'ALB: Tuesday and Wednesday, 9pm Server Time \n'
        'RSC: Thursday and Monday, 8pm Server Time \n'
        'APD: Sunday and Monday, 8pm Server Time \n'
    )
    await ctx.send(response)

@bot.command(name='scourge', help='Link the scourge event guide.')
async def scourge(ctx):
    response = (
        'Scourge Invasion: https://bittsguides.com/scourge-invasion-guide/'
    )
    await ctx.send(response)

@bot.command(name='bench', help='Command for managing absent or benched raid memebers who would be available for an alt raid team.')
async def bench(ctx, name=None, spec=None):
    if name == None or spec==None:
        response = ('Syntax for use: "!bench Crypto DPS')
        await ctx.send(response)
    else:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("INSERT INTO test (name, spec) VALUES ('{}', '{}')".format(name, spec))
        cur.close()
        conn.close()
        response = ('Added!')
        await ctx.send(response)

@bot.command(name='whobench', help='Command for managing absent or benched raid memebers who would be available for an alt raid team.')
async def whobench(ctx):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT * FROM test')
    response = cur.fetchall()
    cur.close()
    conn.close()
    await ctx.send(response)

# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
#     if message.content == 'happy birthday':
#         response = 'Happy Birthday!!'
#         await message.channel.send(response)

bot.run(TOKEN)
