import logging
import discord
from discord.ext import commands

from util import strings
from cogs import MusicBot
from util.logger import *
from util import config

lg = logging.getLogger(__name__)
from util.logger import path
import logging
fl = logging.FileHandler(f"{path}\logs\log.log")
fl.setLevel(logging.INFO)
lg.addHandler(fl)

#TODO: rework the permissions maybe add a role for the music bot
#TODO: test all the commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", help="Mutes a user")
    @commands.has_role("Administrator")
    async def mute(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(user.name)

        await ctx.send(f"Muted {user.name}", delete_after=5)

        lg.info(f"Muted {user.name}")
        await user.edit(mute=True)

    @commands.command(name="unmute", help="Unmutes a user")
    @commands.has_role("Administrator")
    async def unmute(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(user)

        await ctx.send(f"Unmuted {user.name}", delete_after=5)

        lg.info(f"Unmuted {user.name}")
        await user.edit(mute=False)

    @commands.command(name="kick")
    @commands.has_role("Dev")
    async def kick(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        await ctx.send(f"Kicked user {user.name} from the server")

        await self.bot.kick(user)

    @commands.command(name="muteall", help=strings.get_help("help_muteall"))
    @commands.has_role("Bot Access")
    async def muteall(self, ctx):

        try:
            for user in ctx.author.voice.channel.members:

                if user == self.bot.user:
                    return

                else:
                    await user.edit(mute=True)
                    lg.info(f"Muted user: {user.nick}")

            await ctx.send(f"Muted all users in {ctx.author.voice.channel.name}", delete_after=5)

        except Exception as e:
            await ctx.send("Du bist in keinem Voice Channel", delete_after=5)
            lg.error(e)

    @commands.command(name="unmuteall", help=strings.get_help("help_unmuteall"))
    @commands.has_role("Bot Access")
    async def unmuteall(self, ctx):

        try:
            for user in ctx.author.voice.channel.members:
                try:
                    await user.edit(mute=False)
                    lg.info(f"Unmuted user: {user.nick}")
                except discord.errors.NotFound as e:
                    lg.error(f"User {user.nick} is not connected to the voice chat anymore")

            await ctx.send(f"Unmuted all users in '{ctx.author.voice.channel.name}'", delete_after=5)

        except Exception as e:
            await ctx.send("Du bist in keinem Voice Channel", delete_after=5)
            lg.error(e)

    @commands.command(name="status", help="Changes the Status of the bot")
    @commands.has_role(config.getBotAdminRole())
    async def status(self, ctx, *args):

        lg.info(f"Changing the status to {str(args[0])}")

        if str(args[0]) == "servers":

            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Online on {len(self.bot.guilds)} servers"))
            lg.info(f"Changed the status to: Online on {len(self.bot.guilds)} servers")
            await ctx.send(f"Changed status to: Online on {len(self.bot.guilds)} servers", delete_after=5)

        else:

            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="{}".format(" ".join(args))))
            await ctx.send("Changing status to {}".format(" ".join(args)), delete_after=5)

    @commands.command(name="clear")
    @commands.has_role("Dev")
    async def clear(self, ctx):

        channel = ctx.message.channel

        await channel.delete_messages(await channel.history().flatten())

    @commands.command(name="botaccess")
    @commands.has_role("Dev")
    async def botaccess(self, ctx, target):

        lg.info(target)
        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(f"Got User {user.name} as target for promotion")

        role = ctx.author.guild.roles[12]

        await user.add_roles(role)
        lg.info(f"Added '{role.name}' to '{user.name}'")

        # await embed.send_embed_dm(bot, user, infos=("Bot Access", "Bot Access Output"), names=("Granted bot access"), values=(strings.get_promotion_text(ctx.author, user)))

        await ctx.send(f"Added '{role.name}' to '{user.name}'")
        await log_send(ctx, f"Added '{role.name} to {user.name}'")

        await user.create_dm()
        await user.dm_channel.send(strings.get_promotion_text(ctx.author, user))

    @commands.command(name="shutdown", help="Shuts the Bot off.")
    @commands.has_role("Administrator")
    async def shutdown(self, ctx):

        shutdown_msg = "Bot1 going dark... ... ..."

        await ctx.send(shutdown_msg, delete_after=5)
        await log_send(ctx, shutdown_msg)
        await lg.warning(f"Shutting down")
        await ctx.bot.logout()


def setup(bot):
    bot.add_cog(Moderation(bot))