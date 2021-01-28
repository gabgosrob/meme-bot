import praw
import time
import os


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
        self.img_posts = None
        self.last_updated = time.time()


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

    
    def get_recent_subs_posts(self, num):
        """Gets recent hot posts of meme subreddits

        Args:
            num (int): number of posts per sub

        Returns:
            list: all posts
        """
        posts = []
        for sub in self.MEME_SUBS:
            posts += self.get_recent_posts(sub, num)
        return posts
    

    def should_update(self):
        """Decides whether or not the posts list should be updated

        Returns:
            bool: y/n
        """
        update = False
        if not self.img_posts or time.time() - self.last_updated > 1800:
            update = True
        return update

    
    def update_posts(self):
        """Updates the posts list
        """
        self.img_posts = self.get_recent_subs_posts(100)
        self.last_updated = time.time()
