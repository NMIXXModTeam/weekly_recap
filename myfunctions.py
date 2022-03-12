import praw
import pandas as pd

def hello():
  # Define user agent
  user_agent = "praw_scraper_1.0"

  # Create an instance of reddit class
  reddit = praw.Reddit(client_id="yxI4dSUvZzWGpuqHEl4DqA",
                       client_secret="UDReCN0uxUF_56oAMGfmMTugmFPWbA",
                       user_agent=user_agent
  )

  # Create sub-reddit instance
  subreddit_name = "nmixx"
  subreddit = reddit.subreddit(subreddit_name)
  return "Hello World2"

def recap():  
  return "hello2"
