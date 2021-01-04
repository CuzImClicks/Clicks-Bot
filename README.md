Clicks Bot

A discord bot specificly programmed for a private server.
It uses discord.py from:
https://www.github.com/Rapptz/discord.py

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
- on_member_remove event with logger
- help command
	- bot.remove_command("help")
- version update
	- using the last github commit
- Error Embed feedback
	- @<command_name>.error


