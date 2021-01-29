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
    ]

    def __init__(self):
        self.img_posts = {}
        self.last_updated = time.time()
        self.update_posts()

    
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
