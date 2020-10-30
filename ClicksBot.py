import discord
from discord.ext import commands

client = discord.Client()


@client.event
async def on_ready():

    for guild in client.guilds:

        if guild.name == "GUILD":

            break


        print(
            f'\n{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_member_join(member):

    await member.create_dm()
    await member.dm_channel.send(f"Test {member.name}")

@client.event
async def on_message(message):

    if message.author == client.user:

        return

    await message.channel.send("Test")







client.run("NzcxNDY5NDA1NTM1MjA3NDY1.X5sk3w.7R3_Jma2q6yibAVTVjSMGeLW3Ao")