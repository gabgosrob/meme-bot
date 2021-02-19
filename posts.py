import praw
import time
import os
import random


class Posts:
    # Reddit instance
    reddit = praw.Reddit(
            client_id=os.environ.get("MEME_BOT_REDDIT_ID"),
            client_secret=os.environ.get("MEME_BOT_REDDIT_SECRET"),
            user_agent=os.environ.get("MEME_BOT_REDDIT_USER"))

    # List of meme subreddits
    MEME_SUBS = [
        "memes",
        "dankmemes",
        "me_irl",
        "cursedcomments",
        "blackpeopletwitter",
        "im14andthisisdeep",
        "madlads",
        "suicidebywords",
        "prequelmemes"
    ]

    def __init__(self):
        self.INIT_TIME = time.time()
        self.memes_served = 0
        self.img_posts = {}
        self.last_updated = time.time()
        self.update_posts()


    def get_uptime(self):
        """Gets the initialization time

        Returns:
            time: initialization time in seconds
        """
        total_seconds = int(time.time() - self.INIT_TIME)

        days = total_seconds // 86400
        total_seconds -= days * 86400
        hours = total_seconds // 3600
        total_seconds -= hours * 3600
        minutes = total_seconds // 60
        total_seconds -= minutes * 60
        seconds = total_seconds

        if not days and not hours and not minutes:
            return f"{seconds} seconds"
        elif not days and not hours:
            return f"{minutes} minutes and {seconds} seconds"
        elif not days:
            return f"{hours} hours, {minutes} minutes and {seconds} seconds"
        return f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds"


    def get_memes_served(self):
        """Gets the total amount of memes served since last restart

        Returns:
            int: memes served since last reset
        """
        return self.memes_served


    def increment_memes_served(self):
        """Increments the total amount of memes served since last restart
        """
        self.memes_served += 1

    
    def get_meme_subs(self):
        """Gets the supported subreddits list

        Returns:
            list: supported subreddits
        """
        return self.MEME_SUBS
    

    def get_posts_dict(self):
        """Gets the latest posts dictionary

        Returns:
            dict: latest posts
        """
        return self.img_posts


    def get_last_uptaded_time(self):
        """Gets the last update time

        Returns:
            time: last update
        """
        return self.last_updated


    def get_recent_posts(self, sub, num):
        """Gets recent hot posts of specified subreddit

        Args:
            sub (str): subreddit
            num (int): number of posts

        Returns:
            list: all posts
        """
        posts = [x for x in self.reddit.subreddit(sub).hot(limit=num) if (
                not x.stickied and not x.is_self and not x.media)]
        return posts


    def get_random_sub(self):
        """Gets a random supported subreddit

        Returns:
            str: subreddit name
        """
        return self.MEME_SUBS[random.randint(0, len(self.MEME_SUBS)-1)]


    def get_random_meme(self, sub):
        """Gets a random meme from specified subreddit

        Args:
            sub (str): subreddit name

        Returns:
            post: submission
        """
        meme_list = self.img_posts[sub]
        return meme_list[random.randint(0, len(meme_list)-1)]


    def get_random_meme_from_random_sub(self):
        """Gets a random meme from a random subreddit

        Returns:
            post: submission
        """
        return self.get_random_meme(self.get_random_sub())
    

    def should_update(self):
        """Decides whether or not the posts list should be updated

        Returns:
            bool: y/n
        """
        update = False
        if time.time() - self.last_updated > 1800:
            update = True
        return update

    
    def update_posts(self):
        """Updates the posts list
        """
        for sub in self.MEME_SUBS:
            self.img_posts[sub] = self.get_recent_posts(sub, 100)
        self.last_updated = time.time()
