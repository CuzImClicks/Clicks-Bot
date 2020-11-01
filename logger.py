import logging

lg = logging.getLogger(__name__)

fl = logging.FileHandler(r"D:\GitHub Repos\Clicks-Bot\logs\log.log")
fl.setLevel(logging.INFO)


async def file_logger(level):

    if level == "DEBUG":

        fl.setLevel(logging.DEBUG)
        return fl

    elif "ERROR":

        fl.setLevel(logging.ERROR)
        return fl

    elif "INFO":

        fl.setLevel(logging.INFO)
        return fl

    elif "WARNING":

        fl.setLevel(logging.WARNING)
        return fl

    lg.info(f"Set file logger level to {level}")

    async def write(data):

        fl.emit(data)

async def log_typing(channel, user, when):

    lg.info(f"[{str(user)}] is typing in {str(channel)} since {when}")


async def log_send(ctx, msg):

    lg.info(f"Sent message to #{str(ctx.channel)} containing '{msg}'")


async def log_recv(ctx):

    lg.info(f"#{ctx.channel} - {ctx.author} - {str(ctx.message.content)}")


async def log(msg, ctx="", raw=False):



    if raw:
        lg.info(msg)

    if ctx:

        lg.info(f"#{ctx.channel} - {ctx.author} - {str(ctx.message.content)}")

    else:

        lg.log(msg)


async def log_error(msg):

    lg.error(msg)


async def log_warning(msg):

    lg.warning(msg)


async def log_reaction(payload):

    lg.info(f"{payload.member.name} reacted with {payload.emoji} to message_id: {payload.message_id}")


async def log_role(payload, *args):

    roless = []

    for role in args:

        roless.append(role.name)

    lg.info(f"Added {roless} to {payload.member.nick}")


async def log_reaction_remove(payload):

    lg.info(f"{payload.emoji} was removed from message_id: {payload.message_id}")


async def log_join(member):

    lg.info(f"{member.nick} joined {member.guild.name}")