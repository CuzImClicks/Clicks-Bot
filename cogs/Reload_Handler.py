import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
import datetime
from clicks_util import info

lg = logging.getLogger(__name__[5:])

white_check_mark = "✅"
reload_messages = []


def get_reload_message(message: discord.Message):
    for msg in reload_messages:
        if message == msg.message:
            return msg


class Bet_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="send_reload_message")
    async def send_reload_message(self, ctx: commands.Context, extension):

        if extension not in self.bot.cogs:
            raise commands.ExtensionNotFound(extension)

        if extension == "Reload_Handler":
            raise commands.ExtensionError(name="Access Denied", message="This extension can not be reloaded")

        infoEmbed = discord.Embed(title="Reload Message", description=f"Click on the reaction on this message to reload the extension: {extension}", colour=config.getDiscordColour("green"))
        if ctx.message.author.nick:
            infoEmbed.set_author(name=ctx.message.author.nick, icon_url=ctx.message.author.avatar_url)
        else:
            infoEmbed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        infoEmbed.add_field(name=extension, value="Current Status: Loaded")
        message = await ctx.send(embed=infoEmbed)
        await message.add_reaction(white_check_mark)
        rl_msg = ReloadMessage(message, extension)
        reload_messages.append(rl_msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        channel = self.bot.get_channel(payload.channel_id)
        if not type(channel) == discord.TextChannel:
            return

        message = await channel.fetch_message(payload.message_id)
        rl_msg = get_reload_message(message)
        if message in reload_messages and payload.emoji.name == white_check_mark and not payload.member.bot:
            user = self.bot.get_user(payload.user_id)
            await message.remove_reaction(white_check_mark, user)
            self.bot.reload_extension(f"cogs.{rl_msg.extension}")
            lg.info(f"Reloading the extension {rl_msg.extension}")


class ReloadMessage:

    message = discord.Message
    extension = ""

    def __init__(self, message: discord.Message, extension: str):
        self.message = message
        self.extension = extension

    def __eq__(self, other):
        return self.message == other


def setup(bot):

    bot.add_cog(Bet_Handler(bot))
