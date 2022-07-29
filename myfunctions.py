import praw
import pandas as pd
import os

def recap():
  # Define user agent
  user_agent = "praw_scraper_1.0"

  # Create an instance of reddit class
  reddit = praw.Reddit(client_id=os.getenv('CLIENTID'),
                       client_secret=os.getenv('CLIENTSECRET'),
                       user_agent=user_agent
  )

  # Create sub-reddit instance
  subreddit_name = "nmixx"
  subreddit = reddit.subreddit(subreddit_name)

  df = pd.DataFrame()

  titles=[]
  permalinks=[]
  dates=[]
  link_flair_texts=[]

  for submission in subreddit.new(limit=500):
      titles.append(submission.title)
      permalinks.append(submission.permalink)
      dates.append(submission.created_utc)
      link_flair_texts.append(submission.link_flair_text)

  df['Title'] = titles
  df['Permalinks'] = permalinks
  df['Submission Date (UTC)'] = dates
  df['Flair'] = link_flair_texts

  df['Submission Date (UTC)'] = pd.to_datetime(df['Submission Date (UTC)'], unit='s')

  import datetime
  from datetime import date, timedelta, timezone
  import pytz
  
  #today = datetime.datetime.now()
  #today = datetime.datetime(2022, 3, 8)

  today = datetime.datetime.now(timezone.utc)
  today = today.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone("Asia/Seoul"))
  offset = (today.weekday() - 1) % 7
  last_tuesday = today - timedelta(days=offset)

  start_last_week = (last_tuesday - datetime.timedelta(days=7)).strftime("%Y-%m-%d")# + " 09:00:00"
  end_last_week = last_tuesday.strftime("%Y-%m-%d")# + " 08:59:59"

  df['Timestamp'] = df.apply(lambda row: row['Title'].split(" ")[0], axis=1)

  # not perfect but should be enough tbh
  df = df[(df['Timestamp'].astype(str).str[:1] == '2') & (df['Timestamp'].str.len() == 6)]

  df['Timestamp_Y'] = df.apply(lambda row: int("20" + row['Timestamp'][:2]), axis=1)
  df['Timestamp_m'] = df.apply(lambda row: int(row['Timestamp'][2] + row['Timestamp'][3]), axis=1)
  df['Timestamp_d'] = df.apply(lambda row: int(row['Timestamp'][4] + row['Timestamp'][5]), axis=1)
  df['Timestamp_Date'] = df.apply(lambda row: datetime.datetime(row['Timestamp_Y'], row['Timestamp_m'], row['Timestamp_d']), axis=1)

  df = df[(df['Timestamp_Date']>=start_last_week) & (df['Timestamp_Date']<end_last_week)]
  df = df.sort_values(by='Timestamp_Date', ascending=1)
  
  df['Title'] = df['Title'].str[7:]

  news_articles  = df[(df['Flair'] == 'News') | (df['Flair'] == 'Article')]
  teasers = df[(df['Flair'] == 'Teaser')]
  cfs = df[(df['Flair'] == 'CF')]
  sns = df[(df['Flair'] == 'SNS')]
  vlives = df[(df['Flair'] == 'V Live')]
  variety = df[(df['Flair'] == 'Variety')]
  bts = df[(df['Flair'] == 'Behind The Scenes')]
  dance_practices = df[(df['Flair'] == 'Dance Practice')]
  performances = df[(df['Flair'] == 'Performance')]
  videos = df[(df['Flair'] == 'Video')]
  audios = df[(df['Flair'] == 'Audio')]
  images = df[(df['Flair'] == 'Image')]
  lives = df[(df['Flair'] == 'Live')]
  interactions = df[(df['Flair'] == 'Interaction')]
  song_covers = df[(df['Flair'] == 'Song Cover')]
  
  
  sns_twitter = sns[(sns['Title'].str.contains("twitter", case=False))]
  sns_instagram = sns[(sns['Title'].str.contains("instagram", case=False))]
  sns_tiktok = sns[(sns['Title'].str.contains("tiktok", case=False))]
  sns_weibo = sns[(sns['Title'].str.contains("weibo", case=False))]

  result_str = "#Weekly r/NMIXX Recap\n"

  if not news_articles.empty:
      result_str += "\n\n"
      result_str += "#News & Articles\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in news_articles.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  #if not sns.empty:
  #    result_str += "\n\n"
  #    result_str += "#Social Media\n"
  #    result_str += "Date|Title|Thread\n"
  #    result_str += "---|---|---\n"
  #    for index, row in sns.iterrows():
  #        title_str = row['Title'].translate(str.maketrans({"[": r"(",
  #                                                          "]": r")",
  #                                                          "|": r" "}))
  #        result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not teasers.empty:
      result_str += "\n\n"
      result_str += "#Teasers\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in teasers.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
  
  if not cfs.empty:
      result_str += "\n\n"
      result_str += "#Commercial Films\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in cfs.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
  
  if not sns.empty:
      result_str += "\n\n"
      result_str += "#Social Media\n"

      if not sns_twitter.empty:
          result_str += "\n**Twitter**\n\n"
          result_str += "Date|Title|Thread\n"
          result_str += "---|---|---\n"
          for index, row in sns_twitter.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

      if not sns_instagram.empty:
          result_str += "\n**Instagram**\n\n"
          result_str += "Date|Title|Thread\n"
          result_str += "---|---|---\n"
          for index, row in sns_instagram.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

      if not sns_tiktok.empty:
          result_str += "\n**TikTok**\n\n"
          result_str += "Date|Title|Thread\n"
          result_str += "---|---|---\n"
          for index, row in sns_tiktok.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

      if not sns_weibo.empty:
          result_str += "\n**Weibo**\n\n"
          result_str += "Date|Title|Thread\n"
          result_str += "---|---|---\n"
          for index, row in sns_weibo.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not vlives.empty:
      result_str += "\n\n"
      result_str += "#V Lives\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in vlives.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not variety.empty:
      result_str += "\n\n"
      result_str += "#Variety\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in variety.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not bts.empty:
      result_str += "\n\n"
      result_str += "#Behind The Scenes\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in bts.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  if not dance_practices.empty:
      result_str += "\n\n"
      result_str += "#Dance Practices\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in dance_practices.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  if not song_covers.empty:
      result_str += "\n\n"
      result_str += "#Song Covers\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in song_covers.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"   
               
          
  if not videos.empty:
      result_str += "\n\n"
      result_str += "#Videos\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in videos.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  if not audios.empty:
      result_str += "\n\n"
      result_str += "#Audios\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in audios.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  if not images.empty:
      result_str += "\n\n"
      result_str += "#Images\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in images.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  if not lives.empty:
      result_str += "\n\n"
      result_str += "#Lives\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in lives.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  if not interactions.empty:
      result_str += "\n\n"
      result_str += "#Interactions\n"
      result_str += "Date|Title|Thread\n"
      result_str += "---|---|---\n"
      for index, row in interactions.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  with open("weeklyrecap.txt", "w", encoding="utf-8") as text_file:
    text_file.write(result_str)

    
def update_wiki():
  from datetime import datetime

  # Define user agent
  user_agent = "praw_scraper_1.0"

  # Create an instance of reddit class
  reddit = praw.Reddit(client_id=os.getenv('CLIENTID'),
                       client_secret=os.getenv('CLIENTSECRET'),
                       user_agent=user_agent,
                       username=os.getenv('REDDITID'),
                       password=os.getenv('REDDITPW'),
  )

  # Create sub-reddit instance
  subreddit_name = "nmixx"
  subreddit = reddit.subreddit(subreddit_name)

  df = pd.DataFrame()

  titles=[]
  permalinks=[]
  dates=[]
  link_flair_texts=[]

  for submission in subreddit.new(limit=1000):
      titles.append(submission.title)
      permalinks.append(submission.permalink)
      dates.append(submission.created_utc)
      link_flair_texts.append(submission.link_flair_text)

  df['Title'] = titles
  df['Permalinks'] = permalinks
  df['Submission Date (UTC)'] = dates
  df['Flair'] = link_flair_texts

  df['Submission Date (UTC)'] = pd.to_datetime(df['Submission Date (UTC)'], unit='s')
  
  wiki_list = []

  variety_wiki = subreddit.wiki["variety"]

  wiki_list.append(variety_wiki)

  result_str = ""

  for wiki in wiki_list:
      rv_date = pd.to_datetime(wiki.revision_date, unit='s')

      old_content = wiki.content_md

      df = df[df['Submission Date (UTC)']>=rv_date]

      if not df.empty:
          df['Timestamp'] = df.apply(lambda row: row['Title'].split(" ")[0], axis=1)

          # not perfect but should be enough tbh
          df = df[(df['Timestamp'].astype(str).str[:1] == '2') & (df['Timestamp'].str.len() == 6)]

          df['Title'] = df['Title'].str[7:]
          df['Permalinks'] = "https://reddit.com" + df['Permalinks'].astype(str)

      old_content = old_content.replace("Date|Title|Thread", "")
      old_content = old_content.replace("---|---|---", "")
      old_content = old_content.replace("[Thread]", "")

      category_string = ''
      flair_string = ''

      for line in old_content.split('\n'):
          if len(line) > 1:
            if line[0] == "#" and line[1] != "#":
                if "#Variety" in line:
                    flair_string = "Variety"
            if line[:2] == "##":
                category_string = line[2:]
            if line[0] == "2" and len(line.split("|")[0]) == 6:
                line_values = line.split("|")
                perm_link = line_values[2].replace("(", "")
                perm_link = perm_link.replace(")", "")
                new_df_row = {'Timestamp': line_values[0], 'Title': line_values[1], 'Flair': flair_string.strip(), 'Permalinks': perm_link.strip()}
                df = df.append(new_df_row, ignore_index = True)


      df = df.sort_values(by='Timestamp', ascending=1)

      if wiki.name == "variety":

          variety = df[(df['Flair'] == 'Variety')]

          variety_mixxtory = variety[(variety['Title'].str.contains("mixxtory", case=False))]
          variety_picknmixx = variety[(variety['Title'].str.contains("pick nmixx", case=False))]
          variety_radios = variety[(variety['Title'].str.contains("radio", case=False))]

          drop_values = ["mixxtory", "pick nmixx", "radio"]
          variety_videos = variety[~variety['Title'].str.contains('|'.join(drop_values), case=False)]

          if not variety.empty:
              result_str = "#Variety\n"

              if not variety_mixxtory.empty:
                  result_str += "\n##MIXXTORY\n"
                  result_str += "Date|Title|Thread\n"
                  result_str += "---|---|---\n"
                  for index, row in variety_mixxtory.iterrows():
                      title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                        "]": r")",
                                                                        "|": r" "}))
                      result_str += row['Timestamp'] + "|" + title_str + "|" + "[Thread](" + row['Permalinks'] + ")\n"

              if not variety_picknmixx.empty:
                  result_str += "\n##PICK NMIXX\n"
                  result_str += "Date|Title|Thread\n"
                  result_str += "---|---|---\n"
                  for index, row in variety_picknmixx.iterrows():
                      title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                        "]": r")",
                                                                        "|": r" "}))
                      result_str += row['Timestamp'] + "|" + title_str + "|" + "[Thread](" + row['Permalinks'] + ")\n"

              if not variety_videos.empty:
                  result_str += "\n##Video Appearances\n"
                  result_str += "Date|Title|Thread\n"
                  result_str += "---|---|---\n"
                  for index, row in variety_videos.iterrows():
                      title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                        "]": r")",
                                                                        "|": r" "}))
                      result_str += row['Timestamp'] + "|" + title_str + "|" + "[Thread](" + row['Permalinks'] + ")\n"

              if not variety_radios.empty:
                  result_str += "\n##Radio Appearances\n"
                  result_str += "Date|Title|Thread\n"
                  result_str += "---|---|---\n"
                  for index, row in variety_radios.iterrows():
                      title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                        "]": r")",
                                                                        "|": r" "}))
                      result_str += row['Timestamp'] + "|" + title_str + "|" + "[Thread](" + row['Permalinks'] + ")\n"

              wiki.edit(content=result_str, reason="Automated Update from " + datetime.today().strftime('%Y-%m-%d'))
  

  
