import logging
import discord
from discord.ext import commands
from discord.utils import get

import ClicksBot
from util import config
import datetime
from multiprocessing import Process, Lock
import os
from clicks_util import timeconvert

path = os.getcwd()

lg = logging.getLogger(__name__[5:])
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class MainEvents(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        
        total_users = 0
        for guild in self.bot.guilds:

            if guild.name == "GUILD":
                break

            # print(
            # f'{client.user} is connected to the following guild:\n'
            # f'{guild.name}(id: {guild.id})'
            # )
            
            lg.info(f'{self.bot.user} is connected to the following guild: {guild.name}')
            total_users += len(guild.members)
        
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"{total_users} Benutzer an"))

    @commands.Cog.listener()
    async def on_member_join(self, member):

        lg.info(f"{member} joined the guild {member.guild.name}")
        if member.guild.name == "RezURekted":

            await member.add_roles("Member")

            embed = discord.Embed(color=0x2b4f22, description=f"Ein wildes {member.name} erscheint!")
            embed.set_thumbnail(url=str(member.avatar_url))
            embed.set_footer(text=f"{member.guild} - {timeconvert.getStrDateAndTime()}", icon_url=member.guild.icon_url)
            embed.set_thumbnail(url=member.guild.banner_url)
            #TODO: Test and change channel to lobby
            channel = self.bot.get(member.guild.channels, "bot-testing")

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):

        lg.info(f"{member} left the guild {member.guild}")
        if member.guild == "RezURekted":
            await member.add_roles("Member")

            embed = discord.Embed(color=0x2b4f22, description=f"Das wilde {member.name} ist geflüchtet!")
            embed.set_thumbnail(url=str(member.avatar_url))
            embed.set_footer(text=f"{member.guild} - {timeconvert.getStrDateAndTime()}", icon_url=member.guild.icon_url)
            embed.set_thumbnail(url=member.guild.banner_url)
            #TODO: Test and change channel to lobby
            channel = self.bot.get(member.guild.channels, "bot-testing")

            await channel.send(embed=embed)

            await member.create_dm()


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not before.status == after.status:
            if config.getActivity():
                lg.info(f"{after.name} changed their status from {before.status} to {after.status}")
        
        if not before.activity == after.activity:
            if config.getActivity():
                if before.activity:
                    if not before.activity == "Fortnite" and after.activity == "Fortnite":
                        lg.info(f"{after.name} changed their activity from {before.activity.name} to {after.activity.name}")

                    else:
                        lg.info(f"{after.name} started to play {after.activity.name}")

        if not before.nick == after.nick:
            lg.info(f"{after.name} changed their nick from {before.nick} to {after.nick}")
        
        if not before.roles == after.roles:
            for role in before.roles:
                if not role in after.roles:
                    lg.info(f"{role.name} was removed from {after.name}")

            for role  in after.roles:
                if not role in before.roles:
                    lg.info(f"{role.name} was added to {after.name}")


def setup(bot):

    bot.add_cog(MainEvents(bot))
