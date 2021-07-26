from discord.ext import tasks, commands
from scraper import Scraper


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraper = Scraper()

    @tasks.loop(seconds=30.0)
    async def usapi_loop(self, ctx):
        self.scraper.get_usapi_count()
        if self.scraper.lastus < self.scraper.us_api_count:
            await ctx.channel.send(f'```US API CARD COUNT HAS CHANGED:\nLast:{self.scraper.lastus}\nCurrent: {self.scraper.us_api_count}```')
        self.scraper.lastus = self.scraper.us_api_count

    @tasks.loop(seconds=30.0)
    async def jpcardstxt_loop(self, ctx):
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
    async def start(self, ctx):
        self.usapi_loop.start(ctx)
        self.jpcardstxt_loop.start(ctx)
        self.spoof_loop.start(ctx)
        await ctx.channel.send('```starting loops```')

    @commands.command()
    async def stop(self, ctx):
        self.usapi_loop.stop(ctx)
        self.jpcardstxt_loop.stop(ctx)
        self.spoof_loop.stop(ctx)
        await ctx.channel.send('```stopping loops```')
