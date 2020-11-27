import discord
import markovify
import re
from discord.utils import get

id_regex = re.compile('<@.?[0-9]*?>')

def replace_mentions(string_to_format, bot):
    """Replaces mentions in text to format @mentioned"""
    matches = id_regex.findall(string_to_format)
    for mention in matches:
        discord_name = mention.replace('<@', '') \
            .replace('>', '') \
            .replace('i', '') \
            .replace('!', '') \
            .replace('&', '')
        user = get(bot.get_all_members(), id=int(discord_name))
        if user:
            string_to_format = string_to_format.replace(mention, f'@ {user.name}')
        else:
            string_to_format = string_to_format.replace(mention, '')
    return string_to_format

def make_markov_sentence(messages, bot):
    """Generates markov sentence from given messages."""
    for msg in messages:
        replace_mentions(msg, bot)
    corpus = "\n".join(messages)
    model = markovify.NewlineText(corpus)
    result = model.make_sentence()
    return result;
