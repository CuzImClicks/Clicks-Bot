Clicks Bot

A discord bot specificly programmed for a private server.
It uses discord.py from:
https://www.github.com/Rapptz/discord.py

cogs.SteamAPI-Handler.isOnline() from mg393/steamcheck.py
https://gist.github.com/mg393/3119259

integrated a few functions from Smudge-Studios/HypixelBot
cogs/GitHubFetcher.py is by mass1ve-err0r -> GitHub link in file

To create a webhook:

1. Create a channel
2. Create a webhook in the tab "Integrations"
3. Copy the link
4. Go to your GitHub Repo and go to settings
5. Create a webhook in the webhook tab
6. Paste the url and add /github to it
7. Select json

TODO:
- Fix the loop function
- Create more moderation tools
- More documentation in the files
- help command
	- bot.remove_command("help")
- Error Embed feedback
	- @<command_name>.error
- bugreport command
	- database


