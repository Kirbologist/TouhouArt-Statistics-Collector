"""
Author: Kirbologist

A simple Python script for finding and saving some post flair stats on the TouhouArt subreddit.
Could be modified to gather similar stats on other similar subreddits.
"""

import datetime
import praw
from psaw import PushshiftAPI
import pandas as pd

reddit = praw.Reddit(...) # Write your own parameters here! (See praw documentation for details)
api = PushshiftAPI(reddit)
gen = api.search_submissions(subreddit='TouhouArt')
results = list(gen)

flair_list = {'None': 0}
deleted_list = []
deleted_flair_list = []
none_list = []
total_upvotes = {'None': 0}
timestamps = []
upvotes = []

# Sifting through all TouhouArt posts and gathering info
for post in results:
    if post.removed or post.selftext == "[deleted]" or post.banned_at_utc != None:
        deleted_list.append(post.id)
        continue
    flair_text = post.link_flair_text
    if flair_text == None:
        flair_list['None'] += 1
        total_upvotes['None'] += post.ups
        none_list.append(post.id)
    else:
        if flair_list.get(flair_text) == None:
            flair_list[flair_text] = 1
            total_upvotes[flair_text] = post.ups
        else :
            flair_list[flair_text] += 1
            total_upvotes[flair_text] += post.ups

# Calculating average number of upvotes
average_upvotes = {}
for flair in flair_list.keys():
    average_upvotes[flair] = total_upvotes[flair] / flair_list[flair]

# Constructing pandas dataframes and saving it to .csv files
sorted_flair_list = {k: v for k, v in sorted(flair_list.items(), key=lambda item: item[0])}
sorted_upvote_list = {k: v for k, v in sorted(average_upvotes.items(), key=lambda item: item[0])}
sorted_total_list = {k: v for k, v in sorted(total_upvotes.items(), key=lambda item: item[0])}
df = pd.DataFrame({"Flair": sorted_flair_list.keys(),
                   "No. of posts": sorted_flair_list.values(),
                   "Total no. of upvotes": sorted_total_list.values(),
                   "Average no. of upvotes": sorted_upvote_list.values()})
df.to_csv("TouhouArt_2hu_data.csv")

dates = []
for timestamp in timestamps:
    ts = int(timestamp)
    dt = datetime.date.fromtimestamp(ts)
    dates.append(dt.strftime('%Y-%m-%d'))

pd_dt = pd.to_datetime(dates)
df2 = pd.DataFrame({"Date": pd_dt, "Upvotes": upvotes})
df2.to_csv("Post_upvote_data.csv")

df2['Date'] -= pd.to_timedelta(7, unit='d')
df2count = df2.groupby(pd.Grouper(key="Date", freq="1W")).count()
df2sum = df3 = df2.groupby(pd.Grouper(key="Date", freq="1W")).sum()
df2mean = df2.groupby(pd.Grouper(key="Date", freq="1W")).mean()
df2count = df2count.rename(columns={"Upvotes":"No. of posts"})
df2sum = df2sum.rename(columns={"Upvotes":"Total no. of upvotes"})
df2mean = df2mean.rename(columns={"Upvotes":"Mean no. of upvotes"})
df3 = pd.concat([df2count, df2sum, df2mean], axis=1)
df3.to_csv("TouhouArt_weekly_data.csv")
