import discord
from discord.ext import commands
import P5R as p
import sqlite3
import math
import random


client = commands.Bot(command_prefix="--")
client.remove_command("help")
db = sqlite3.connect('../../../Downloads/Personas.db')
cursor = db.cursor()
rare_persona = ["Regent", "Queen's Necklace", "Stone of Scone", "Koh-i-Noor",
                "Orlov", "Emperor's Amulet", "Hope Diamond", "Crystal Skull", "Orichalum"]


@client.event
async def on_ready():
    cursor.execute('''CREATE TABLE IF NOT EXISTS players(id BIGINT, 
                                                        level INTEGER, 
                                                        xp INTEGER, 
                                                        melee TEXT, 
                                                        gun TEXT,
                                                        hp INTEGER,
                                                        sp INTEGER)''')
    print("Ready!")


@client.event
async def on_message_delete(message):
    if message.guild.id == 808898721072283658:
        guild = client.get_guild(808898721072283658)
        channel = guild.get_channel(809253973839577099)
        await channel.send(embed=discord.Embed(title=f"Message by {message.author.display_name}#{message.author.discriminator} deleted in #{message.channel}", description=message.content))


@client.command()
async def start(ctx):
    try:
        cursor.execute('''SELECT * FROM p{}'''.format(str(ctx.author.id)))
        result = cursor.fetchone()
        cursor.execute('''SELECT * FROM players WHERE id = {}'''.format(ctx.author.id))
        result2 = cursor.fetchone()
        await ctx.send(str(result) + "\n" + str(result2))
    except sqlite3.OperationalError:
        cursor.execute('''CREATE TABLE IF NOT EXISTS p{} (name TEXT,
                                                         level INTEGER,
                                                         xp INTEGER,
                                                         affinities TEXT,
                                                         stats TEXT,
                                                         moves TEXT,
                                                         info TEXT)'''.format(str(ctx.author.id)))
        sql = '''INSERT INTO players(id, level, xp, melee, gun, hp, sp) VALUES(?, ?, ?, ?, ?, ?, ?)'''
        val = (ctx.author.id, 1, 0, "Rebel Knife", "Handgun", , ,)
        db.commit()
        await ctx.send("You have no profile")


@client.after_invoke
async def committing(ctx):
    db.commit()


@client.command()
async def fuse(ctx, *, persona):
    persona = p.fuse_persona(persona.split("|")[0], persona.split("|")[1])
    if isinstance(persona, p.Persona):
        await ctx.send(persona.name)
    else:
        await ctx.send(persona)


@client.command()
async def help(ctx):
    await ctx.send(embed=discord.Embed(title="Help command",
                                       color=0xfe0000,
                                       description="**--fuse (persona | persona 2):** Fuse 2 persona,"
                                                   " EX: --fuse Pixie | Arsene"))


@client.command()
async def encounter(ctx, level: int):
    absorb, weak, resist, repel, null, neutral = "Absorb: ", "Weak: ", "Resist: ", "Repel: ", "Null: ", ""
    types = {0: "Physical", 1: "Gun", 2: "Fire", 3: "Ice", 4: "Electric", 5: "Wind", 6: "Psychic",
             7: "Nuclear", 8: "Bless", 9: "Curse"}
    roundedlevel, finalstring = math.ceil(level/7), ""
    if roundedlevel < 2:
        roundedlevel = 2
    levels = [x for x in range(level, level-roundedlevel, -1) if not str(x).startswith("-")] + \
             [y for y in range(level+1, level+roundedlevel) if y <= 95]
    personae = []
    while not personae:
        finallevel = random.choice(levels)
        cursor.execute('SELECT * FROM personas WHERE level = {}'.format(finallevel))
        personae = cursor.fetchall()
    finalpersona = random.choice(personae)
    cursor.execute('SELECT * FROM stats WHERE name = "{}"'.format(finalpersona[1]))
    stats = cursor.fetchone()
    cursor.execute('SELECT * FROM affinities WHERE name = "{}"'.format(finalpersona[1]))
    affinities = cursor.fetchone()
    personaobject = p.Persona(finalpersona[1], finalpersona[2], finalpersona[3],
                              affinities[1:-1], stats[1:-1])
    embed = discord.Embed(title=f"Persona Encounter - {personaobject.name}",
                          description=f"Arcana: {personaobject.arcana}\nLevel: {personaobject.level}")
    for index, affinity in enumerate(personaobject.affinities):
        if affinity == "ab":
            absorb += f"{types[index]}, "
        elif affinity == "rp":
            repel += f"{types[index]}, "
        elif affinity == "nu":
            null += f"{types[index]}, "
        elif affinity == "wk":
            weak += f"{types[index]}, "
        elif affinity == "rs":
            resist += f"{types[index]}, "
    for affinity in [absorb, weak, resist, repel, null]:
        if len(affinity) > 10:
            finalstring += affinity[:-2] + "\n"
    print(finalstring)
    if finalstring == "":
        finalstring == "None"
    embed.add_field(name="Affinities", value=finalstring)
    await ctx.send(embed=embed)


client.run("token")
