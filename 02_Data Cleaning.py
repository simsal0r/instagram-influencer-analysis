# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
import pandas as pd

# %%
df = pd.read_csv('results.csv',sep="|",names=["nr","user","timestamp","text","like1","like2","video_views"],parse_dates=["timestamp"])

# %%
df.info()

# %%
df.timestamp.value_counts().head(4)

# %%
df = df[df.timestamp != "Error"]

# %%
df = df.drop(columns=['nr'])

# %%
len(df)

# %%
df = df.drop_duplicates()

# %%
len(df)

# %%
df["date"] = pd.to_datetime(df.timestamp)

# %%
df["date_year_month"] = df['date'].apply(lambda x: x.strftime('%Y-%B')) 

# %%
df["date_year_month2"] = df['date'].apply(lambda x: x.strftime('%Y-%m')) 

# %%
df["date_year_week"] = df['date'].apply(lambda x: x.strftime('%Y-%W')) 

# %%
df[df.like1 != "Error"]

# %%
df.at[1098, 'like2'] = "137.332"
df.at[9328, 'like2'] = "136.019"

# %%
df = df.drop(columns=['like1'])

# %%
df = df.rename(columns={"like2": "likes", "user": "url"})


# %%
def clean_url(url):
    result = url
    if url[-1] == "/":
        result = url[:-1]
    return(result)   


# %%
df["url"] = df.url.apply(lambda x: clean_url(x))

# %%
df["user"] = df.url.apply(lambda x: x[26:])

# %%
df.head()

# %%
df["likes"] = df.likes.apply(lambda x: x.replace(".",""))

# %%
df.to_csv("posts_data.csv",sep="|")

# %%
