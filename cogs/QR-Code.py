import qrcode
import logging
import discord
from discord.ext import commands
from util.logger import path
import logging
from util import config
from datetime import datetime

lg = logging.getLogger(__name__)


class QR_Code(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @commands.command(name="qr_code")
    @commands.has_role(config.getBotAccessRole())
    async def qr_code(self, ctx, *args):

        if not args:
            errorEmbed = discord.Embed(title="QR-Code Error",
                                       description="No content provided",
                                       colour=config.getDiscordColour("red"),
                                       timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)
            return

        try:
            version = int(args[-1])

        except:
            errorEmbed = discord.Embed(title="QR-Code Error",
                                       description="Last element is not a version integer. Try something like 1 or 5",
                                       colour=config.getDiscordColour("red"),
                                       timestamp=datetime.now())
            await ctx.send(embed=errorEmbed)
            return

        args = list(args)
        args.remove(args[-1])
        string = ""
        for word in args:
            string = f"{string} {word}"

        infoEmbed = discord.Embed(title="QR Code",
                                  colour=config.getDiscordColour("blue"),
                                  timestamp=datetime.now())

        infoEmbed.add_field(name="Content", value=string, inline=False)
        infoEmbed.add_field(name="Requested by", value=ctx.author.name, inline=False)

        qr = qrcode.QRCode(version=version, border=2, error_correction=qrcode.ERROR_CORRECT_L)
        qr.add_data(string)
        qr.make()

        img = qr.make_image()
        img.save(f"{path}/qr_codes/qr.png")
        file = discord.File(f"{path}/qr_codes/qr.png")

        await ctx.send(embed=infoEmbed)
        await ctx.send(file=file)


def setup(bot):

    bot.add_cog(QR_Code(bot))
