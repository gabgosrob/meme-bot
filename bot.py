import random
import os
import discord
from misc import *
from posts import Posts


# Initializing reddit and discord clients
client = discord.Client()
imgs = Posts()


def make_meme_embed(post):
    """Makes a meme discord embed

    Args:
        post (submission): reddit submission

    Returns:
        embed: meme embed ready to send
    """ 
    to_send = discord.Embed(
        title=post.title,
        url=f"https://www.reddit.com/r/{post.subreddit}/comments/{str(post)}",
        description=f"u/{str(post.author)}",
        color=random_color_int())
    to_send.set_author(
        name=f"r/{str(post.subreddit)}",
        url=f"https://www.reddit.com/r/{post.subreddit}",
        icon_url=post.subreddit.icon_img)
    to_send.set_image(url=post.url)
    to_send.set_footer(
        text="This bot was made by twig#1234",
        icon_url="https://cdn.discordapp.com/avatars/178997121737949184/a_1625128860ca511929ac2f45395e1e46.webp?size=256")
    return to_send


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    words = message.content.split()
    global imgs

    if message.content == "meme":
        # Update the posts list if the last command was over 30 minutes ago
        if imgs.should_update():
            await message.channel.send("**Updating the meme list, please wait...**")
            imgs.update_posts()
            await message.channel.send("**Updated!**")

        # This sends a random meme from a random meme subreddit
        post = imgs.img_posts[random.randint(0, len(imgs.img_posts)-1)]
        await message.channel.send(embed=make_meme_embed(post))

    elif len(words) == 2 and words[0] == "meme":
        if words[1] == "help":
            # This displays the help message
            to_send = discord.Embed(title="__List of commands__")
            to_send.add_field(name="**meme**",
                            value="posts a random meme from a random meme subreddit",
                            inline=False)
            to_send.add_field(name="**meme <subreddit>**",
                            value="posts a random meme from the specified meme subreddit",
                            inline=False)
            to_send.add_field(name="**meme subs**",
                            value="displays the list of all supported meme subreddits",
                            inline=False)
            to_send.add_field(name="**meme stats**",
                            value="displays this bot's stats",
                            inline=False)
            to_send.add_field(name="**meme help**",
                            value="displays this list of commands",
                            inline=False)
            await message.channel.send(embed=to_send)
        elif words[1] == "stats":
            # This displays the bot's stats
            await message.channel.send("**Not yet supported.**")
        elif words[1] == "subs":
            # This displays the supported meme subreddits
            subs_string = ""
            for sub in sorted(imgs.MEME_SUBS):
                subs_string += f"[r/{sub}](https://www.reddit.com/r/{sub})\n"
            to_send = discord.Embed()
            to_send.add_field(name="__Supported Meme Subreddits__",
                            value=subs_string)
            await message.channel.send(embed=to_send)
        else:
            # This sends a random meme from a specified meme subreddit
            if len(words[1]) > 2 and words[1][:2] == "r/":
                words[1] = words[1][2:]
            if words[1] in imgs.MEME_SUBS:
                post = imgs.get_recent_posts(words[1], 100)[random.randint(0, 99)]
                await message.channel.send(embed=make_meme_embed(post))
            else:
                await message.channel.send("**This subreddit is not supported. Type 'meme help' for more information.**")

#TODO: 'meme stats' command (shows stats like uptime, total memes served)
#TODO: add reactions to messages after bot recognizes them


client.run(os.environ.get("MEME_BOT_DISCORD_TOKEN"))