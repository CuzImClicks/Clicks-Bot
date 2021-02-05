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
X Fix the loop function
X Create more moderation tools
- More documentation in the files
	- docstring for api stuff -> not custom methods
- Error Embed feedback
	- @<command_name>.error
X bugreport command
	X database
- convert all timestamps to time
- add aliases
X config
	X magmaboss 
	X minecraft online function
	X enable and disable command
X Lyrics command



FIXME:
X timestamp shows utc time not localtime
	- https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
X timestamp doesn't accept date.time()
	X use footer instead?
- cleanup function runs on every reload
X die command AtrributeError

