# Discord Meme Bot

This is a python discord bot that pulls random memes from various meme subreddits and posts them in a text channel when asked to.

## Requirements

This bot has a few requirements, notably the [Discord API wrapper](https://github.com/Rapptz/discord.py) and the [Reddit API wrapper](https://github.com/praw-dev/praw), which are located in the requirements.txt file.

```bash
pip install -r requirements.txt
```
You're also going to need your own Discord bot token and your Reddit API id/secret/agent set as environment variables.

To run the bot, simply execute the main file:
```bash
python bot.py
```
## Usage

After running the bot.py file, simply type 'meme help' in a text channel for all the commands.

## Deployment

This repo contains a Procfile and a requirements.txt file, it is therefore ready for deployment. Just don't forget to set the environment variables on your virtual environment to use the correct API keys.
