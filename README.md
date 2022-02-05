# TouhouArt-Statistics-Collector
Collects data and statistics on the post and post flairs of the TouhouArt subreddit. Code can potentially be modified for doing the same thing with other subreddits.

Code uses the PRAW and PSAW Python API's. The two are wrappers around the Reddit and PushShift API's respectively. PushShift API searches for Reddit posts recorded through the PushShift database, and the Reddit API gives up-to-date data on each post. Pandas is used to postprocess and structure the data.

**Warning:** As of January 2022, the PushShift database is still missing data from various points throughout 2020 and 2021, most noticeably, during February to April of 2021. As such, the data will be incomplete.
