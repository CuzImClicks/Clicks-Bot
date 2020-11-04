import discord
import logging
import util.logger

lg = logging.getLogger(__name__)

'''embed = discord.Embed(title="Credits", description="Credit to the ones who deserve", color=0x00ff00)
embed.add_field(name="first_line", value="Idee und coding: Henrik | Clicks", inline=False)
embed.add_field(name="second_line", value="Textgestaltung : Kai | K_Stein", inline=False)
embed.add_field(name="third_line", value="Bereitstellung des Servers : Luis | DasVakuum", inline=False)'''

async def send_embed(bot, ctx, infos=(), names=(), values=(), inline=(), send=True):

    try:
        embed = discord.Embed(title=infos[0], description=infos[1], color=0x2b4f22)

    except Exception as e:

        util.logger.log_error(e)

    for i in range(0, len(names)):

        try:
            embed.add_field(name=names[i], value=values[i], inline=inline[i])

        except Exception as e:

            util.logger.log_error(e)

    await ctx.send(embed=embed)






