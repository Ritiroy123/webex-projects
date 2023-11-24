
from gpt import gpt
from webex_bot.webex_bot import WebexBot

# Create a Bot Object
bot = WebexBot("NWNiNTUyYTItZmU1Zi00YWIxLTllYTktYjEyNjUwYzI0NjIzMGFlNWYwOTgtM2Q0_PF84_3bf06e7b-f230-427f-9163-c54d2e428d6a")
bot.commands.clear()
# Add new commands for the bot to listen out for.
bot.add_command(gpt())
bot.help_command = gpt()

# Call `run` for the bot to wait for incoming messages.
bot.run()