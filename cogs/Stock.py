import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
from clicks_util import timeconvert, info
import pandas_datareader as web
import matplotlib.pyplot as plt
import mplfinance as mpf
import datetime

lg = logging.getLogger(__name__[5:])


class example_cog(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.__currency = "EUR"
        self.__start = datetime.datetime(2020, 1, 1)
        self.__end = timeconvert.getDateAndTime()

    @commands.command(name="stock")
    @commands.has_role(config.getBotAccessRole())
    async def stock(self, ctx, _stock: str, currency: str = "EUR", source: str = "yahoo"):
        lg.info(f"{_stock.upper()}-{currency.upper()}")
        data = web.DataReader(f"{_stock.upper()}", source.lower(), self.__start, self.__end)
        
        plt.plot(data, label=_stock)
        plt.ylabel(currency)
        plt.xlabel("time")
        name = f"{path}/stocks/{_stock}-{currency}.png"
        plt.savefig(name)

        infoEmbed = discord.Embed(description=f"Showing the development of {_stock} in {currency}")
        await ctx.send(embed=infoEmbed)
        await ctx.send(file=discord.File(name))




def setup(bot):

    bot.add_cog(example_cog(bot))
