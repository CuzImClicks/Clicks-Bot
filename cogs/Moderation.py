import logging
from os import name
import discord
from discord.errors import Forbidden
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
from clicks_util import timeconvert


lg = logging.getLogger(__name__[5:])

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
                                  timestamp=timeconvert.getTime())
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
    @commands.has_role(config.getBotAdminRole())
    async def mute(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(user.name)
        muteEmbed = discord.Embed(title="Mute", description=f"Muted {user.name}", colour=config.getDiscordColour("blue"),
                                  timestamp=timeconvert.getTime())
        await ctx.send(embed=muteEmbed)

        lg.info(f"Muted {user.name}")
        await user.edit(mute=True)

    @commands.command(name="unmute", help="Unmutes a user")
    @commands.has_role(config.getBotAdminRole())
    async def unmute(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        lg.info(user)
        unmuteEmbed = discord.Embed(title="Unmute", description=f"Unmuted {user.name}", colour=config.getDiscordColour("blue"),
                                    timestamp=timeconvert.getTime())
        await ctx.send(embed=unmuteEmbed)

        lg.info(f"Unmuted {user.name}")
        await user.edit(mute=False)

    @commands.command(name="kick")
    @commands.has_role(config.getBotAdminRole())
    async def kick(self, ctx, target):

        user = discord.utils.get(ctx.author.guild.members, name=str(target))

        kickEmbed = discord.Embed(title="Kick", description=f"Kicked {user.name} from the server",
                                  colour=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())
        await ctx.send(embed=kickEmbed)
        await self.bot.kick(user)

    @commands.command(name="muteall", help=strings.get_help("help_muteall"), aliases=["ma"])
    @commands.has_role(config.getBotAccessRole())
    async def muteall(self, ctx):

        try:
            for user in ctx.author.voice.channel.members:

                if user == self.bot.user:
                    return

                else:
                    await user.edit(mute=True)
                    lg.info(f"Muted user: {user.nick}")

            maEmbed = discord.Embed(title="Mute All", description=f"Muted all users in {ctx.author.voice.channel.name}",
                                    colour=config.getDiscordColour("red"), timestamp=timeconvert.getTime())
            await ctx.send(embed=maEmbed)

        except Exception as e:
            errorEmbed = discord.Embed(title="Command Error", description="You're not in a voice channel",
                                       colour=config.getDiscordColour("blue"), timestamp=timeconvert.getTime())
            await ctx.send(embed=errorEmbed)
            lg.error(e)

    @commands.command(name="unmuteall", help=strings.get_help("help_unmuteall"), aliases=["uma"])
    @commands.has_role(config.getBotAccessRole())
    async def unmuteall(self, ctx):

        try:
            for user in ctx.author.voice.channel.members:
                try:
                    await user.edit(mute=False)
                    lg.info(f"Unmuted user: {user.nick}")
                except discord.errors.NotFound as e:
                    lg.error(f"User {user.nick} is not connected to the voice chat anymore")

            await ctx.send(f"Unmuted all users in '{ctx.author.voice.channel.name}'")

        except Exception as e:
            await ctx.send("Du bist in keinem Voice Channel")
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
                                      timestamp=timeconvert.getTime())
            await ctx.send(embed=infoEmbed)
        except Exception as e:
            errorEmbed = discord.Embed(title="Lock Error",
                                       description="You are not connected to a voice channel!",
                                       colour=config.getDiscordColour("red"),
                                       timestamp=timeconvert.getTime())
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
            await ctx.send(f"Changed status to: Online on {len(self.bot.guilds)} servers")

        else:

            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="{}".format(" ".join(args))))
            await ctx.send("Changing status to {}".format(" ".join(args)))

    @commands.command(name="clear")
    @commands.has_role(config.getBotAdminRole())
    async def clear(self, ctx):

        channel = ctx.message.channel
        await channel.purge(await channel.history().flatten())

    @commands.command(name="botaccess")
    @commands.has_role(config.getBotAdminRole())
    async def botaccess(self, ctx):

        user = ctx.message.mentions[0]

        lg.info(f"Got User {user.name} as target for promotion")

        role = ctx.author.guild.roles[12]

        await user.add_roles(role)
        lg.info(f"Added '{role.name}' to '{user.name}'")

        infoEmbed = discord.Embed(title="Access to the bots features", description=f"The admin has granted you access to the role 'bot-access'\n"\
            + "You can use .help to see all of the bots features. \nIf you have any problems with using the bot please contact a admin")
        infoEmbed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await user.create_dm()
        await user.dm_channel.send(embed=infoEmbed)

    @commands.command(name="shutdown", help="Shuts the Bot off.")
    @commands.has_role(config.getBotAdminRole())
    async def shutdown(self, ctx):

        shutdown_msg = "Bot1 going dark... ... ..."

        await ctx.send(shutdown_msg)
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
    @commands.has_role(config.getBotAdminRole())
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


    @commands.command(name="friend_add")
    @commands.has_role(config.getBotAdminRole())
    async def friend_add(self, ctx):
        try:
            user = ctx.message.mentions[0]
            if not user:
                errorEmbed = discord.Embed(title="Command Error", description="No user was mentioned",
                                        color=config.getDiscordColour("red"))            
            await user.send_friend_request()
        except Forbidden:
            errorEmbed = discord.Embed(title="Forbidden", description="Bots cannot use this endpoint", colour=config.getDiscordColour("red"))
            await ctx.send(embed=errorEmbed)

def setup(bot):
    bot.add_cog(Moderation(bot))
