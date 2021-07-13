import logging
import discord
from discord.ext import commands

import ClicksBot
from clicks_util import info
from util.logger import path
import logging
from util import config
import datetime
from clicks_util import json_util

lg = logging.getLogger(__name__[5:])
fl = ClicksBot.fl
fl.setLevel(logging.INFO)
lg.addHandler(fl)

one = "1️⃣"
two = "2️⃣"
three = "3️⃣"
four = "4️⃣"
five = "5️⃣"


def try_int(content: str) -> int:
    try:
        content = int(content)
        return content
    except Exception:
        return 0


def get_emoji(number: int):
    if number == 1:
        return one

    elif number == 2:
        return two

    elif number == 3:
        return three

    elif number == 4:
        return four

    elif number == 5:
        return five

    else:
        return ""


class Bet_Handler(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        pass

    @commands.command(name="bet")
    async def bet(self, ctx):

        user = ctx.message.author
        channel = ctx.channel
        infoEmbed = discord.Embed(title="Bet", description="This is the creator for bets, "
                                                           "the bot will edit this message with instructions for you to"
                                                           " follow. When you write a message, "
                                                           "it will be deleted and added to this message.")
        infoEmbed.add_field(name="Title", value="What should the bet be called?", inline=False)
        message = await ctx.send(embed=infoEmbed)
        message_id = message.id
        check = lambda m: m.author == user
        answer = await self.bot.wait_for("message", check=check)
        await answer.delete()

        if answer is not None:
            title = answer.content
            infoEmbed = message.embeds[0]
            infoEmbed.set_field_at(index=0, name="Title", value=title, inline=False)
            infoEmbed.add_field(name="Options", value="How many options should there be? Please write a number under 5")
            message = await channel.fetch_message(message_id)
            message_id = message.id
            await message.edit(embed=infoEmbed)

            check = lambda m: m.author == user
            options_amount = await self.bot.wait_for("message", check=check)
            await options_amount.delete()

            number = try_int(options_amount.content)
            if number == 0 or number > 5:
                errorEmbed = discord.Embed(description="Something went wrong with creating your bet. "
                                                       "Please try again and correct any mistakes you made. "
                                                       "If you believe this is a bug, contact a developer.",
                                           colour=config.getDiscordColour("red"))
                message = await channel.fetch_message(message_id)
                message_id = message.id
                await message.edit(embed=errorEmbed, delete_after=10)
                return

            lg.info(title)
            lg.info(number)
            lg.info(user.id)
            bet_ = Bet(title=title, options_amount=number, options=list(), author_id=user.id)

            infoEmbed = message.embeds[0]
            options_string = f"""
            Amount of options: {number}
            """
            infoEmbed.set_field_at(index=1, name="Options", value=options_string, inline=False)
            message = await channel.fetch_message(message_id)
            message_id = message.id
            await message.edit(embed=infoEmbed)
            for num in range(1, number + 1):
                options_string = options_string + f"\n{num}. <Send the first message as a message>"

                infoEmbed.set_field_at(index=1, name="Options", value=options_string, inline=False)
                message = await channel.fetch_message(message_id)
                message_id = message.id
                await message.edit(embed=infoEmbed)

                check = lambda m: m.author == user
                option = await self.bot.wait_for("message", check=check)
                await option.delete()

                options_string = options_string.replace(f"\n{num}. <Send the first message as a message>",
                                                        f"\n{num}. {option.content}")
                lg.info(options_string)

                bet_.options.append(option)

                infoEmbed.set_field_at(index=1, name="Options", value=options_string, inline=False)
                message = await channel.fetch_message(message_id)
                message_id = message.id
                await message.edit(embed=infoEmbed)
                await message.add_reaction(get_emoji(num))
                bet_.message_id = message_id

            # TODO: implement the actual message of the bet
            # TODO: create an actual channel specifically for bets
            # TODO: add the actual voting part
            # TODO: add loading of the bets on start
            bet_.update_dict()
            bet_.save()
            infoEmbed = discord.Embed(description="The rest of the bet system is not yet finished. Coming soon TM")
            await ctx.send(embed=infoEmbed)


class Bet:

    def __init__(self, title: str, options_amount: int, options: list, author_id: int):
        self.dictionary = dict()
        self.title = title
        self.options_amount = options_amount
        self.options = options
        self.author_id = author_id

        self.update_dict()
        self.json_file = json_util.JsonFile("bets.json", path=path)

    def update_dict(self):
        self.dictionary = {
            "title": self.title,
            "options_amount": self.options_amount,
            "options": self.options,
            "author": self.author_id
        }

    def save(self):
        data = self.json_file.read()
        data[self.title] = self.dictionary
        self.json_file.write(data)


def setup(bot):
    bot.add_cog(Bet_Handler(bot))
