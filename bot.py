import asyncio
import discord
import subprocess
import signal
from discord.ext import commands
import config

class Clipper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = None
        self.running = False

    @commands.command()
    async def start(self, ctx):
        """Starts running sclip on the host's computer"""

        if (not self.running):
            self.process = subprocess.Popen(["sclip"])
            self.running = True
            await ctx.send('sclip now running.')
        else:
            await ctx.send('sclip already running.')

    @commands.command()
    async def clip(self, ctx):
        """Sends a SIGUSR1 to the sclip process, writing the clip to disk."""

        if (self.running):
            self.process.send_signal(signal.SIGUSR1);
            await ctx.send('Sent signal to sclip.')
            if (self.process.poll() == None):
                self.running = False
        else:
            await ctx.send('sclip not running.')

    @commands.command()
    async def convert(self, ctx):
        """Converts pcm output to mp3 with ffmpeg."""

        result = subprocess.run(["ffmpeg", "-ar", "48000", "-ac", "2", "-f", "f32le", "-i", "output.pcm", "out.mp3"])

        if (result.returncode == 0):
            await ctx.send('Produced out.mp3.')
        else:
            await ctx.send('Failed')


    @commands.command()
    async def quit(self, ctx):
        """Ends the running sclip process"""

        self.process.kill()
        self.running = False

        await ctx.send('sclip killed.')

    @commands.command()
    async def status(self, ctx):
        """Prints sclip process status"""

        await ctx.send((f"Running: {self.running}\n"))

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Bot for interacting with sclip.')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


bot.add_cog(Clipper(bot))
bot.run(config.token)
