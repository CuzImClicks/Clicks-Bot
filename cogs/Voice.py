import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from colorama import Fore
from clicks_util import info

lg = logging.getLogger(__name__)
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)


class VoiceEvents(commands.Cog):

    current_streamers = []
    current_muted = []
    current_deaf = []

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if not before.channel:
            if after.channel.id == 774629025805107230:  
                if not "Dev" == member.top_role.name or "Clicks Bot" == member.top_role.name:
                    await member.move_to(None)
                    return    
            
            lg.info(f"{Fore.LIGHTGREEN_EX}{member.guild} - {member.name} joined '{after.channel.name}'")

        if before.channel and not after.channel:
            lg.info(f"{Fore.LIGHTRED_EX}{member.guild} - {member.name} left the channel '{before.channel.name}'")

        if before.channel and after.channel:
            if before.channel.id != after.channel.id:
                if after.channel.id == 774629025805107230:  
                    if not "Dev" == member.top_role.name or "Clicks Bot" == member.top_role.name:
                        await member.move_to(before.channel)
                        return   
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


def setup(bot):
    bot.add_cog(VoiceEvents(bot))
