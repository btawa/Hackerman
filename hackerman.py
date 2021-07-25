from discord.ext import commands
from scraper import Scraper
import logging
import datetime
import argparse

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')

parser = argparse.ArgumentParser(description='Run a Hackerman bot"')
parser.add_argument('-t', '--token', type=str, help='Discord bot token that will be used', required=True)
args = parser.parse_args()

DISCORD_TOKEN = args.token

bot = commands.Bot(command_prefix="#")
scraper = Scraper(bot=bot)

@bot.event
async def on_ready():
    logging.info(f"Logged in as")
    logging.info(f"{bot.user.name}")
    logging.info(f"{bot.user.id}")
    logging.info(f"Startup Time: {str(datetime.datetime.utcnow())}")
    logging.info(f"Guilds Added: {str(len(bot.guilds))}")
    logging.info(f"------")


@bot.command()
async def start(ctx):
    scraper.usapi_loop.start(ctx)
    scraper.jpcardstxt_loop.start(ctx)
    await ctx.channel.send('```starting loops\nscraper.usapi_loop\nscraper.jpcardstxt_loop```')


@bot.command()
async def stop(ctx):
    scraper.usapi_loop.stop(ctx)
    scraper.jpcardstxt_loop.stop(ctx)
    await ctx.channel.send('```stopping loops\nscraper.usapi_loop\nscraper.jpcardstxt_loop```')


bot.run(args.token)