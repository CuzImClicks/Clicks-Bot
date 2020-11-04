import discord


async def send(target, msg):

    await target.create_dm()
    await target.dm_channel.send(msg)