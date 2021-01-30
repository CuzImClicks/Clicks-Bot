import logging
from os import name
import discord
from discord.ext import commands
from datetime import datetime
from discord.utils import get
from util import strings
from util.logger import *
from util import config
from clicks_util.json_util import JsonFile
from util.logger import path
import logging
import varname


lg = logging.getLogger(__name__)

async def make_bugreport_embed(ctx, bugreport: dict) -> discord.Embed:
    user = get(ctx.guild.members, name=bugreport["author"])
    infoEmbed = discord.Embed(title="Bugreport", colour=config.getDiscordColour("green"))
    infoEmbed.add_field(name="Name", value=bugreport["name"], inline=False)
    infoEmbed.add_field(name="Command", value=bugreport["command"], inline=False)
    infoEmbed.add_field(name="description", value=bugreport["description"], inline=False)
    infoEmbed.add_field(name="Fixed", value=bugreport["status"], inline=False)
    infoEmbed.set_author(name=bugreport["author"], icon_url=user.avatar_url)
    return infoEmbed


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="blacklist")
    @commands.has_role(config.getBotAdminRole())
    async def blacklist(self, ctx, target):

        jf = JsonFile(name="blacklist.json", path=path)
        infoEmbed = discord.Embed(title="Blacklist",
                                  color=config.getDiscordColour("blue"),
                                  timestamp=datetime.now())
        if target == "list":
            member_ids = [member.id for member in ctx.author.guild.members]
            for user in jf.read()["blacklisted"]:
                user = discord.get(member_ids, id=user)
                infoEmbed.add_field(name=user, value="Blacklisted", inline=False)

            await ctx.send(embed=infoEmbed)
        else:
            user = discord.utils.get([member.id for member in ctx.author.guild.members], id=target)
            blacklisted = jf.read()["blacklisted"]
            blacklisted.append(user)
            infoEmbed.add_field(name=user, value=f"Blacklisted")
            await ctx.send(embed=infoEmbed)
            jf.write({"blacklisted": blacklisted})

    @commands.command(name="mute", help="Mutes a user")
    @commands.has_role("Administrator")
    async def mute(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(user.name)
        muteEmbed = discord.Embed(title="Mute", description=f"Muted {user.name}", color=discord.Colour(0x000030),
                                  timestamp=datetime.now())
        await ctx.send(embed=muteEmbed)

        lg.info(f"Muted {user.name}")
        await user.edit(mute=True)

    @commands.command(name="unmute", help="Unmutes a user")
    @commands.has_role("Administrator")
    async def unmute(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(user)
        unmuteEmbed = discord.Embed(title="Unmute", description=f"Unmuted {user.name}", color=discord.Colour(0x000030),
                                    timestamp=datetime.now())
        await ctx.send(embed=unmuteEmbed)

        lg.info(f"Unmuted {user.name}")
        await user.edit(mute=False)

    @commands.command(name="kick")
    @commands.has_role("Dev")
    async def kick(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        kickEmbed = discord.Embed(title="Kick", description=f"Kicked {user.name} from the server",
                                  color=discord.Colour(0x000030), timestamp=datetime.now())
        await ctx.send(embed=kickEmbed)
        await self.bot.kick(user)

    @commands.command(name="muteall", help=strings.get_help("help_muteall"), aliases=["ma"])
    @commands.has_role("Bot Access")
    async def muteall(self, ctx):

        try:
            for user in ctx.author.voice.channel.members:

                if user == self.bot.user:
                    return

                else:
                    await user.edit(mute=True)
                    lg.info(f"Muted user: {user.nick}")

            maEmbed = discord.Embed(title="Mute All", description=f"Muted all users in {ctx.author.voice.channel.name}",
                                    color=discord.Color(0x9D1309), timestamp=datetime.now())
            await ctx.send(embed=maEmbed)

        except Exception as e:
            errorEmbed = discord.Embed(title="Command Error", description="You're not in a voice channel",
                                       color=discord.Colour(0x000030), timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)
            lg.error(e)

    @commands.command(name="unmuteall", help=strings.get_help("help_unmuteall"), aliases=["uma"])
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

    @commands.command(name="lock", help="Locks the channel user limit to the current amount of users inside")
    @commands.has_role(config.getBotAdminRole())
    async def lock(self, ctx):
        try:
            await ctx.author.voice.channel.edit(user_limit=len(ctx.author.voice.channel.members))
            lg.info(
                f"Locked the channel {ctx.author.voice.channel.name} to a maximum of {len(ctx.author.voice.channel.members)}")
            infoEmbed = discord.Embed(title="Lock",
                                      description=f"Locked the channel {ctx.author.voice.channel.name} to a maximum"
                                                  f" of {len(ctx.author.voice.channel.members)}",
                                      color=config.getDiscordColour("blue"),
                                      timestamp=datetime.now())
            await ctx.send(embed=infoEmbed)
        except Exception as e:
            errorEmbed = discord.Embed(title="Lock Error",
                                       description="You are not connected to a voice channel!",
                                       colour=config.getDiscordColour("red"),
                                       timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)
            lg.error(e)

    @commands.command(name="unlock", help="Sets the user limit of your current channel to infinite")
    @commands.has_role(config.getBotAdminRole())
    async def unlock(self, ctx):
        try:
            await ctx.author.voice.channel.edit(user_limit=0)
            lg.info(f"Locked the channel {ctx.author.voice.channel.name} to a maximum of 0")

            infoEmbed = discord.Embed(title="Unlock",
                                      description=f"The channel {ctx.author.voice.channel.name} was unlocked",
                                      colour=config.getDiscordColour("blue"),
                                      timestamp=datetime.now())
        except Exception as e:
            errorEmbed = discord.Embed(title="Lock Error",
                                       description="You are not connected to a voice channel!",
                                       colour=config.getDiscordColour("red"),
                                       timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)
            lg.error(e)

    @commands.command(name="status", help="Changes the Status of the bot")
    @commands.has_role(config.getBotAdminRole())
    async def status(self, ctx, *args):

        lg.info(f"Changing the status to {str(args[0])}")

        if str(args[0]) == "servers":

            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                                     name=f"Online on {len(self.bot.guilds)} servers"))
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

    @commands.command(name="info")
    @commands.has_role(config.getBotAdminRole())
    async def info(self, ctx):

        user = ctx.message.mentions[0]

        infoEmbed = discord.Embed(title="Informations",
                                  colour=config.getDiscordColour("blue"))
        infoEmbed.set_author(name=user.name, icon_url=user.avatar_url)
        infoEmbed.add_field(name="Name", value=user.name)
        infoEmbed.add_field(name="Discriminator", value=user.discriminator)
        infoEmbed.add_field(name="Nick", value=user.nick, inline=False)
        if user.activity:
            infoEmbed.add_field(name="Type", value=user.activity.type.name)
            infoEmbed.add_field(name="Activity", value=user.activity.name)
        infoEmbed.set_thumbnail(url=user.avatar_url)
        infoEmbed.add_field(name="Status", value=user.status, inline=False)
        infoEmbed.add_field(name="Mobile", value=user.is_on_mobile())
        infoEmbed.add_field(name="Joined at", value=str(user.joined_at)[:-7])
        roles = [role.name for role in user.roles]
        roles.reverse()
        infoEmbed.add_field(name="Roles", value=str(roles), inline=False)
        infoEmbed.set_footer(text=str(user.id))

        await ctx.send(embed=infoEmbed)

    @commands.command(name="add_role", aliases=["create_role"])
    @commands.has_role(config.getBotAdminRole())
    async def add_role(self, ctx):
        user = ctx.message.mentions[0]
        role = ctx.message.role_mentions[0]
        lg.info(type(role))
        infoEmbed = discord.Embed(title="Add Role",
                                  colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name="Role", value=role, inline=False)
        infoEmbed.add_field(name="User", value=user.name, inline=False)
        await user.add_roles(role)
        await ctx.send(embed=infoEmbed)

    @commands.command(name="remove_role", aliases=["rem_role"])
    @commands.has_role(config.getBotAdminRole())
    async def remove_role(self, ctx):
        user = ctx.message.mentions[0]
        role = ctx.message.role_mentions[0]
        lg.info(type(role))
        infoEmbed = discord.Embed(title="Remove Role",
                                  colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name="Role", value=role, inline=False)
        infoEmbed.add_field(name="User", value=user.name, inline=False)
        await user.remove_roles(role)
        await ctx.send(embed=infoEmbed)

    @commands.command(name="bugreport")
    async def bugreport(self, ctx, name: str, theme: str, command:str ="",description: str=""):
        jf = JsonFile("bugreports.json", f"{os.getcwd()}/bugreports")

        data = jf.read()
        bugreport = {"name": name,"author": ctx.author.name, "command": command, "description": description, "status": True}
        infoEmbed = discord.Embed(title="Bugreport", colour=config.getDiscordColour("green"))
        infoEmbed.add_field(name="Name", value=bugreport["name"], inline=False)
        infoEmbed.add_field(name="Command", value=bugreport["command"], inline=False)
        infoEmbed.add_field(name="description", value=bugreport["description"], inline=False)
        infoEmbed.add_field(name="Status", value= bugreport["status"], inline=False)
        infoEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=infoEmbed)
        data[name] = bugreport
        jf.write(data)

    @commands.command(name="get_bugreports")
    @commands.has_role(config.getBotAdminRole())
    async def get_bugreports(self, ctx):

        jf = JsonFile("bugreports.json", f"{os.getcwd()}/bugreports")
        data = jf.read()
        for bugreport in list(data.keys()):
            bugreport = data[bugreport]
            user = get(ctx.guild.members, name=bugreport["author"])
            infoEmbed = discord.Embed(title="Bugreport", colour=config.getDiscordColour("green"))
            infoEmbed.add_field(name="Name", value=bugreport["name"], inline=False)
            infoEmbed.add_field(name="Command", value=bugreport["command"], inline=False)
            infoEmbed.add_field(name="description", value=bugreport["description"], inline=False)
            infoEmbed.add_field(name="Status", value= bugreport["status"], inline=False)
            infoEmbed.set_author(name=bugreport["author"], icon_url=user.avatar_url)
            if bugreport["status"] == False:
                await ctx.send(embed=infoEmbed)

    @commands.command(name="fixed")
    @commands.has_role(config.getBotAdminRole())
    async def fixed(self, ctx, name):
        jf = JsonFile("bugreports.json", f"{os.getcwd()}/bugreports")
        data = jf.read()

        if name in list(data.keys()):
            data[name]["status"] = False
            await ctx.send(embed=await make_bugreport_embed(ctx, data[name]))
            jf.write(data)


def setup(bot):
    bot.add_cog(Moderation(bot))
