import discord
import sys
import config
from cogs import stringlogic
from discord.ext import commands

bot = commands.Bot(command_prefix='$', case_insensitive=True)

def is_channel_viewable(bot, channel):
    """Check if bot can view channel"""
    if bot.user in channel.members:
        return True
    return False

@bot.event
async def on_ready():
    print('Logged in as ')
    print(bot.user.name)
    print(bot.user.id)
    print('~~~~')
    sys.stdout.flush()

@bot.command()
async def makesentences(ctx):
    guild = ctx.guild
    if guild:
        guild = ctx.guild
        all_messages = [];
        for channel in guild.text_channels:
            if is_channel_viewable(bot, channel):
                channel_messages = await channel.history(limit=1000).flatten()
                message_strings = [x.content for x in channel_messages]
                result = stringlogic.make_markov_sentence(message_strings, bot)
                all_messages.extend(message_strings)
                if result and len(result) > 0:
                    to_send = "Generated message for channel " + channel.name + ": \n" + result
                    await ctx.channel.send(to_send)
        complete_result = stringlogic.make_markov_sentence(all_messages, bot)
        if complete_result and len(complete_result) > 0:
            to_send = "Generated message for all channels:\n" + complete_result
            await ctx.channel.send(to_send)

@bot.event
async def on_error(event, *args, **kwargs):
    """Print error to console when it happens."""
    print('Error happened, code {event}')
    sys.stdout.flush()

bot.run(config.TOKEN)
