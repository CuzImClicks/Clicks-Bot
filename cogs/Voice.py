import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from colorama import Fore
from clicks_util import info

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}\logs\log.log", encoding='utf-8')
fl.setLevel(logging.INFO)
lg.addHandler(fl)
blocked = []
def isBlocked(member: discord.Member):
    if member in blocked:
        lg.info(f"{member.nick} is blocked")
        return True
    lg.info(f"{member.nick} is not blocked")
    return False

class VoiceEvents(commands.Cog):

    current_streamers = []
    current_muted = []
    current_deaf = []
    current_fmuted = []
    current_fdeaf = []

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if not before.channel:
            if after.channel.id == 774629025805107230:  
                if (not "Dev" == member.top_role.name or "Clicks Bot" == member.top_role.name):
                    
                    await member.edit(mute=True)
                    blocked.append(member)
                    infoEmbed = discord.Embed(description="You tried to connect to a private channel, a request has been sent to the admin of this channel. Please wait for confirmation.")
                    try:
                        #await member.create_dm()
                        #await member.dm_channel.send(embed=infoEmbed)
                        pass
                    except discord.Forbidden:
                        pass

                    infoEmbed = discord.Embed(description=f"{member.name} tried to connect to your channel. Please type 'Yes' or 'No'")
                    user = discord.utils.get(member.guild.members, id=408722814808358914)
                    try:
                        await user.create_dm()
                        await user.dm_channel.send(embed=infoEmbed)
                    
                    except discord.Forbidden:
                        pass
                    check = lambda m: m.content == "Yes" or m.content == "No" and m.author == user
                    answer = await self.bot.wait_for("message", check=check)
                        
                    if str(answer.content).lower() == "yes" or str(answer.content).lower() == "y":
                        blocked.remove(member)
                        await member.edit(mute=False)
                        lg.info("Unmuted the user")
                        
                    else:
                        blocked.remove(member)
                        await member.edit(mute=False)
                        lg.info("Unmuted the user")
                        await member.move_to(None)
                        
                           
            
            lg.info(f"{Fore.LIGHTGREEN_EX}{member.guild} - {member.name} joined '{after.channel.name}'")

        if before.channel and not after.channel:
            lg.info(f"{Fore.LIGHTRED_EX}{member.guild} - {member.name} left the channel '{before.channel.name}'")

        if before.channel and after.channel:
            if before.channel.id != after.channel.id:
                if after.channel.id == 774629025805107230:  
                    if (not "Dev" == member.top_role.name or "Clicks Bot" == member.top_role.name):
                        await member.edit(mute=True)
                        blocked.append(member)
                        infoEmbed = discord.Embed(description="You tried to connect to a private channel, a request has been sent to the admin of this channel. Please wait for confirmation.")
                        try:
                            #await member.create_dm()
                            #await member.dm_channel.send(embed=infoEmbed)
                            pass
                    
                        except discord.Forbidden:
                            pass
                        infoEmbed = discord.Embed(description=f"{member.name} tried to connect to your channel. Please type 'Yes' or 'No'")
                        user = discord.utils.get(member.guild.members, id=408722814808358914)
                        try:
                            await user.create_dm()
                            await user.dm_channel.send(embed=infoEmbed)
                        except discord.Forbidden:
                            pass
                        check = lambda m: m.channel == user.dm_channel and m.author == user
                        answer = await self.bot.wait_for("message", check=check)
                        
                        if str(answer.content).lower() == "yes" or str(answer.content).lower() == "y":
                            blocked.remove(member)
                            await member.edit(mute=False)
                            lg.info("Unmuted the user")
                            
                        else:
                            blocked.remove(member)
                            await member.edit(mute=False)
                            lg.info("Unmuted the user")
                            await member.move_to(before.channel)
                                 
                lg.info(f"{Fore.LIGHTCYAN_EX}{member.guild} - {member.name} switched channels from '{before.channel.name}' to '{after.channel.name}'")
            else:
                if member.voice.self_stream:
                    lg.info(f"{member.guild} - {member.name} started streaming in {after.channel.name}")
                    self.current_streamers.append(member.id)

                if member.voice.self_mute:
                    lg.info(f"{member.guild} - {member.name} muted himself")
                    self.current_muted.append(member.id)

                if member.voice.self_deaf:
                    lg.info(f"{member.guild} - {member.name} deafened himself")
                    self.current_deaf.append(member.id)

                if member.voice.mute:
                    lg.info(f"{member.guild} - {member.name} was muted by the guild")
                    self.current_fmuted.append(member.id)

                if member.voice.deaf:
                    lg.info(f"{member.guild} - {member.name} was deafened by the guild")
                    self.current_fdeaf.append(member.id)

                for streamer in self.current_streamers:
                    if member.id == streamer:
                        if not member.voice.self_stream:
                            self.current_streamers.remove(member.id)
                            lg.info(f"{member.guild} - {member.name} stopped streaming")

                for muted in self.current_muted:
                    if member.id == muted:
                        if not member.voice.self_mute:
                            self.current_muted.remove(member.id)
                            lg.info(f"{member.guild} - {member.name} unmuted himself")

                for deaf in self.current_deaf:
                    if member.id == deaf:
                        if not member.voice.self_deaf:
                            self.current_deaf.remove(member.id)
                            lg.info(f"{member.guild} - {member.name} undeafened himself")

                for muted in self.current_fmuted:
                    if member.id == muted:
                        if not member.voice.mute:
                            self.current_fmuted.remove(member.id)
                            lg.info(f"{member.guild} - {member.name} was unmuted by the guild")
                            if isBlocked(member):
                                lg.info(f"{member.nick} tried to unmute but failed due to being in a locked channel")
                                await member.edit(mute=True)

                for deaf in self.current_fdeaf:
                    if member.id == deaf:
                        if not member.voice.deaf:
                            self.current_fdeaf.remove(member.id)
                            lg.info(f"{member.guild} - {member.name} was undeafened by the guild")


def setup(bot):
    bot.add_cog(VoiceEvents(bot))
