from discord.ext import tasks, commands
from scraper import Scraper
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraper = Scraper()
        self.status = False

    @tasks.loop(seconds=30.0)
    async def usapi_loop(self, ctx):
        logging.info("Starting US API Loop")
        self.scraper.get_usapi_count()
        if self.scraper.lastus < self.scraper.us_api_count:
            await ctx.channel.send(f'```US API CARD COUNT HAS CHANGED:\nLast:{self.scraper.lastus}\nCurrent: {self.scraper.us_api_count}```')
        self.scraper.lastus = self.scraper.us_api_count

    @tasks.loop(seconds=30.0)
    async def jpcardstxt_loop(self, ctx):
        logging.info("Starting JP API Loop")
        self.scraper.get_listcardtxt_count()
        if self.scraper.lastjp < self.scraper.jp_listcardtxt_count:
            await ctx.channel.send(f'```JP CARDTXT COUNT HAS CHANGED:\nLast:{self.scraper.lastjp}\nCurrent: {self.scraper.jp_listcardtxt_count}```')
        self.scraper.lastjp = self.scraper.jp_listcardtxt_count

    @tasks.loop(seconds=5)
    async def spoof_loop(self, ctx):
        if self.scraper.lastspoof < self.scraper.spoof_count:
            await ctx.channel.send(f'```SPOOF COUNT HAS CHANGED:\nLast:{self.scraper.lastspoof}\nCurrent: {self.scraper.spoof_count}```')
        self.scraper.lastspoof = self.scraper.spoof_count

    @commands.command()
    async def spoof(self, ctx):
        self.scraper.spoof_count += 1

    @commands.command()
    async def cc(self, ctx):
        await ctx.channel.send(f"```Current Counts:\n\nJP (Card.txt): {self.scraper.lastjp}\nUS: {self.scraper.lastus}\nLast Spoof: {self.scraper.lastspoof}```")

    @commands.command()
    async def sources(self, ctx):
        us_source = "https://fftcg.square-enix-games.com/en/get-cards"
        jp_source = "http://www.square-enix-shop.com/jp/ff-tcg/card/data/list_card.txt"

        await ctx.channel.send(f"US: <{us_source}>\nJP: <{jp_source}>")

    @commands.command()
    async def start(self, ctx):
        self.usapi_loop.start(ctx)
        self.jpcardstxt_loop.start(ctx)
        self.spoof_loop.start(ctx)
        self.status = True
        await ctx.channel.send('```starting loops```')

    @commands.command()
    async def stop(self, ctx):
        self.usapi_loop.stop()
        self.jpcardstxt_loop.stop()
        self.spoof_loop.stop()
        self.status = False
        await ctx.channel.send('```stopping loops```')

    @commands.command()
    async def status(self, ctx):
        if self.status is True:
            await ctx.channel.send('```Loops are running```')
        if self.status is False:
            await ctx.channel.send('```Loops are not running```')
