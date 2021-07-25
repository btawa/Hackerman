from discord.ext import commands
import logging
import datetime
import argparse
from loops import Tasks

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

parser = argparse.ArgumentParser(description='Run a Hackerman bot"')
parser.add_argument('-t', '--token', type=str, help='Discord bot token that will be used', required=True)
args = parser.parse_args()

DISCORD_TOKEN = args.token

bot = commands.Bot(command_prefix="#")
bot.add_cog(Tasks(bot))


@bot.event
async def on_ready():
    logging.info(f"Logged in as")
    logging.info(f"{bot.user.name}")
    logging.info(f"{bot.user.id}")
    logging.info(f"Startup Time: {str(datetime.datetime.utcnow())}")
    logging.info(f"Guilds Added: {str(len(bot.guilds))}")
    logging.info(f"------")


bot.run(args.token)
