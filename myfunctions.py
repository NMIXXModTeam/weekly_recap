import praw
import pandas as pd

def recap():
  # Define user agent
  user_agent = "praw_scraper_1.0"

  # Create an instance of reddit class
  reddit = praw.Reddit(client_id=process.env.CLIENTID,
                       client_secret=process.env.CLIENTSECRET,
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

  for submission in subreddit.new(limit=200):
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
  from datetime import date
  from datetime import timedelta
  #today = datetime.datetime.now()
  #today = datetime.datetime(2022, 3, 8)


  today = date.today()
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

  news_articles  = df[(df['Flair'] == 'News') | (df['Flair'] == 'Article')]
  sns = df[(df['Flair'] == 'SNS')]
  vlives = df[(df['Flair'] == 'V Live')]
  variety = df[(df['Flair'] == 'Variety')]

  sns_twitter = sns[(sns['Title'].str.contains("twitter", case=False))]
  sns_instagram = sns[(sns['Title'].str.contains("instagram", case=False))]
  sns_tiktok = sns[(sns['Title'].str.contains("tiktok", case=False))]
  sns_weibo = sns[(sns['Title'].str.contains("weibo", case=False))]

  result_str = ""

  if not news_articles.empty:
      result_str += "\n\n"
      result_str += "#News & Articles\n"
      result_str += "|**Date**|**Title**|**Thread**|\n"
      result_str += ":--|:--|:--|\n"
      for index, row in news_articles.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  #if not sns.empty:
  #    result_str += "\n\n"
  #    result_str += "#Social Media\n"
  #    result_str += "|**Date**|**Title**|**Thread**|\n"
  #    result_str += ":--|:--|:--|\n"
  #    for index, row in sns.iterrows():
  #        title_str = row['Title'].translate(str.maketrans({"[": r"(",
  #                                                          "]": r")",
  #                                                          "|": r" "}))
  #        result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not sns.empty:
      result_str += "\n\n"
      result_str += "#Social Media\n"

      if not sns_twitter.empty:
          result_str += "\n**Twitter**\n\n"
          result_str += "|**Date**|**Title**|**Thread**|\n"
          result_str += ":--|:--|:--|\n"
          for index, row in sns_twitter.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

      if not sns_instagram.empty:
          result_str += "\n**Instagram**\n\n"
          result_str += "|**Date**|**Title**|**Thread**|\n"
          result_str += ":--|:--|:--|\n"
          for index, row in sns_instagram.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

      if not sns_tiktok.empty:
          result_str += "\n**TikTok**\n\n"
          result_str += "|**Date**|**Title**|**Thread**|\n"
          result_str += ":--|:--|:--|\n"
          for index, row in sns_tiktok.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

      if not sns_weibo.empty:
          result_str += "\n**Weibo**\n\n"
          result_str += "|**Date**|**Title**|**Thread**|\n"
          result_str += ":--|:--|:--|\n"
          for index, row in sns_weibo.iterrows():
              title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                                "]": r")",
                                                                "|": r" "}))
              result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not vlives.empty:
      result_str += "\n\n"
      result_str += "#V Lives\n"
      result_str += "|**Date**|**Title**|**Thread**|\n"
      result_str += ":--|:--|:--|\n"
      for index, row in vlives.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"

  if not variety.empty:
      result_str += "\n\n"
      result_str += "#Variety\n"
      result_str += "|**Date**|**Title**|**Thread**|\n"
      result_str += ":--|:--|:--|\n"
      for index, row in variety.iterrows():
          title_str = row['Title'].translate(str.maketrans({"[": r"(",
                                                            "]": r")",
                                                            "|": r" "}))
          result_str += "|" + row['Timestamp'] + "|" + title_str + "|" + "[Thread](https://reddit.com" + row['Permalinks'] + ")\n"
          
  with open("weeklyrecap.txt", "w", encoding="utf-8") as text_file:
    text_file.write(result_str)
