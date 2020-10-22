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
import numpy as np
from matplotlib import pyplot as plt

# %%
from IPython.display import display, HTML

#Sets jupyter width to 100%
display(HTML("<style>.container { width:100% !important; }</style>"))
#pd.set_option('display.max_colwidth', None)

# %%
#plt.style.use('ggplot')
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 12})

# %%
df_info = pd.read_csv("profiles_data.csv", sep = "|",index_col=0)

# %%
df_posts = pd.read_csv("posts_data.csv", sep = "|",index_col=0)

# %%
mask = (df_posts['date_year_month2'] < "2020-07") & (df_posts['date_year_month2'] > "2019-02")
df_posts = df_posts.loc[mask]

# %%
len(df_posts)

# %%
plot_df = pd.DataFrame(df_posts.groupby(["date_year_month2"]).size())


# %% [markdown]
# ### Plotting functions

# %%
def plot_two_bars(plot_df):
    labels = ['March', 'April', 'May']
    means_2019 = [plot_df.loc["2019-03"].values[0], plot_df.loc["2019-04"].values[0], plot_df.loc["2019-05"].values[0]]
    means_2020 = [plot_df.loc["2020-03"].values[0], plot_df.loc["2020-04"].values[0], plot_df.loc["2020-05"].values[0]]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(8,5))
    rects1 = ax.bar(x - width/2, means_2019, width, label='2019')
    rects2 = ax.bar(x + width/2, means_2020, width, label='2020')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Posts')
    ax.set_title('Posts by year and month')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
 
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    
    #plt.savefig("2bars.pdf")

    plt.show()


# %%
def get_percentages(plot_df):
    mar = (plot_df.loc["2020-03"].values[0] - plot_df.loc["2019-03"].values[0])/plot_df.loc["2019-03"].values[0]
    apr = (plot_df.loc["2020-04"].values[0] - plot_df.loc["2019-04"].values[0])/plot_df.loc["2019-04"].values[0]
    may = (plot_df.loc["2020-05"].values[0] - plot_df.loc["2019-05"].values[0])/plot_df.loc["2019-05"].values[0]
    return(mar,apr,may)


# %%
def get_total_percentage(plot_df):
    
    a = plot_df.loc["2020-03"].values[0] + plot_df.loc["2020-04"].values[0] + plot_df.loc["2020-05"].values[0]
    b = plot_df.loc["2019-03"].values[0] + plot_df.loc["2019-04"].values[0] + plot_df.loc["2019-05"].values[0]

    return((a-b)/b)


# %%
#Hotfix, inserts 0 if no posts are available 
def get_total_percentage2(user_grouped_df):
    try:
        a = user_grouped_df.loc["2019-03"].values[0]
    except:
        a = 0
        
    try:
        b = user_grouped_df.loc["2019-04"].values[0]
    except:
        b = 0
        
    try:
        c = user_grouped_df.loc["2019-05"].values[0]
    except:
        c = 0
        
    try:
        d = user_grouped_df.loc["2020-03"].values[0]
    except:
        d = 0
        
    try:
        e = user_grouped_df.loc["2020-04"].values[0]
    except:
        e = 0
        
    try:
        f = user_grouped_df.loc["2020-05"].values[0]
    except:
        f = 0
        
        
    total_3month_19 = a + b + c
    total_3month_20 = d + e + f

    month_sample = total_3month_19 + total_3month_20
    
    months_difference = -999
    
    if not(total_3month_20 == 0 or total_3month_19 == 0): 
        months_difference = (total_3month_20 - total_3month_19)/total_3month_19
    return(months_difference,month_sample)


# %%
def plot_bar_chart(plot_df):
    x = plot_df.index
    energy = plot_df[0]

    x_pos = [i for i, _ in enumerate(x)]

    plt.figure(figsize=(17,4))
    plt.bar(x_pos, energy, color = "grey")
    plt.xlabel("Month")
    plt.ylabel("Posts")

    plt.xticks(x_pos, x,rotation=90)

    axes = plt.gca()

    #Limits of Y axis
    axes.set_ylim([1000,1600])
    #plt.savefig("bars.pdf",bbox_inches='tight')
    plt.show()


# %% [markdown]
# # 1) Theory: Total post volume decreased after CV-19 lockdown?

# %%
plot_bar_chart(plot_df)

# %%
get_total_percentage(plot_df)

# %%
plot_two_bars(plot_df)

# %%
get_percentages(plot_df)

# %% [markdown]
# ### Let's investigate the distribution of the decrease

# %%
del plot_df

# %%
plot_df = pd.DataFrame()

# %%
for user1 in df_posts.user.unique():
    user_df = df_posts[df_posts.user == user1]
    user_grouped_df = pd.DataFrame(user_df.groupby(["date_year_month2"]).size())
        
    try:
        a = user_grouped_df.loc["2019-03"].values[0]
    except:
        a = 0
        
    try:
        b = user_grouped_df.loc["2019-04"].values[0]
    except:
        b = 0
        
    try:
        c = user_grouped_df.loc["2019-05"].values[0]
    except:
        c = 0
        
    try:
        d = user_grouped_df.loc["2020-03"].values[0]
    except:
        d = 0
        
    try:
        e = user_grouped_df.loc["2020-04"].values[0]
    except:
        e = 0
        
    try:
        f = user_grouped_df.loc["2020-05"].values[0]
    except:
        f = 0
        
        
    total_3month_19 = a + b + c
    total_3month_20 = d + e + f

    month_sample = total_3month_19 + total_3month_20
    
    months_difference = -999
    
    if not(total_3month_20 == 0 or total_3month_19 == 0): 
        months_difference = (total_3month_20 - total_3month_19)/total_3month_19
    
    plot_df = plot_df.append({"user": user1,"months_difference":months_difference, "month_sample" : month_sample},ignore_index=True)

# %%
#Exclude outliers
plot_df = plot_df[plot_df.month_sample >= 30]
plot_df = plot_df[plot_df.months_difference != -999]
plot_df = plot_df[plot_df.months_difference < 1.5]

# %%
#Scaling
plot_df["months_difference"] = plot_df.months_difference.apply(lambda x: x*100)

# %%
plot_df

# %%
clean_bins = [-100,-75,-50,-25,0,25,50,75,100]

for feature in ["months_difference"]:

    n, bins, patches = plt.hist(x=plot_df[feature], bins=clean_bins, color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    #plt.title(feature)
    plt.xlabel("Percentage decrease / increase")
    plt.ylabel("Users")
    plt.grid(axis='y', alpha=0.75)
    maxfreq = n.max()
    fig = plt.gcf()
    fig.set_size_inches(8, 5)
    #plt.savefig("distusers.pdf")
    plt.show()

# %% [markdown]
# ### What about travel influencers? Did they less often?

# %%
plot_df = pd.DataFrame(df_posts[df_posts.url.isin(df_info[df_info.is_travel == True].url.values)].groupby(["date_year_month2"]).size())

# %%
plot_two_bars(plot_df)

# %%
get_percentages(plot_df)

# %%
get_total_percentage(plot_df)

# %% [markdown]
# ### So travel influencers didn't really stop posting... What about the complementary group?

# %%
plot_df = pd.DataFrame(df_posts[df_posts.url.isin(df_info[df_info.is_travel == False].url.values)].groupby(["date_year_month2"]).size())
plot_two_bars(plot_df)

# %%
get_percentages(plot_df)

# %%
get_total_percentage(plot_df)

# %%
#Receive list of influencers that are categorized as travel but not fashion
#np.setdiff1d(df_info[df_info.is_travel == True].url.values,df_info[df_info.is_fashion == True].url.values)

# %% [markdown]
# # 2) Theory: Behavior adoption (topic shift) prevents post volume decrease

# %% [markdown]
# ### Influencers without topic shift

# %%
plot_df = pd.DataFrame(df_posts[df_posts.url.isin(df_info[df_info.has_topic_shift == False].url.values)].groupby(["date_year_month2"]).size())
#plot_two_bars(plot_df)
get_total_percentage(plot_df)

# %% [markdown]
# ### Influencers with topic shift

# %%
plot_df = pd.DataFrame(df_posts[df_posts.url.isin(df_info[df_info.has_topic_shift == True].url.values)].groupby(["date_year_month2"]).size())
get_total_percentage(plot_df)

# %%
#Share of influencers with topic shift
len(df_info[df_info.has_topic_shift == True])/len(df_info)

# %%
len(np.intersect1d(df_info[df_info.is_travel == True].url.values,df_info[df_info.has_topic_shift == True].url.values))/len(df_info[df_info.is_travel == True])

# %%
len(np.intersect1d(df_info[df_info.is_travel == False].url.values,df_info[df_info.has_topic_shift == True].url.values))/len(df_info[df_info.is_travel == False])

# %%
len(df_info[df_info.is_travel == True])

# %% [markdown]
# # 3) Inspect a particular influencer

# %%
plot_df = pd.DataFrame(df_posts[df_posts.url.isin(["https://www.instagram.com/pamela_rf"])].groupby(["date_year_month2"]).size())
get_percentages(plot_df)

# %%
plot_two_bars(plot_df)

# %% [markdown]
# ### Likes per post

# %%
likes = list(filter(lambda x : x != 'Error', df_posts[df_posts.url.isin(["https://www.instagram.com/pamela_rf"])].likes.values))
likes.reverse()
likes = list(map(int, likes))
likes = pd.DataFrame(likes)
plt.figure(figsize=(8,3))
plt.plot(likes.index,likes[0])

# %% [markdown]
# # 4) How many influencers posted about CV-19 or BLM?

# %%
df_info.has_cv_19_post.value_counts()

# %%
df_info.has_blm_post.value_counts()

# %% [markdown]
# # 5) Theory: Ad volume decreased because of CV-19 lockdown

# %%
ad_keywords = ["Werbung","werbung","WERBUNG","Anzeige","anzeige","ANZEIGE"," #ad", "advertisement", "sponsored", "gesponsort", "promotion", "Promotion"]

# %%
#Test
any(word in 'some one long two phrase promotionthree' for word in ad_keywords)


# %%
df_posts["is_ad"] = df_posts.text.apply(lambda x: any(word in x for word in ad_keywords))

# %%
df_posts = df_posts[df_posts.date_year_month2 > "2019-02"]

# %%
df_ads = pd.DataFrame(df_posts.groupby(["date_year_month2","is_ad"]).size())

# %%
df_ads = df_ads.reset_index()

# %%
df_ads.head(4)

# %%
df_ads[df_ads.date_year_month2 == '2019-03'][df_ads[df_ads.date_year_month2 == '2019-03'].is_ad == True][0].values[0]

# %%
df_ads.groupby("date_year_month2")[0].sum()["2019-03"]

# %%
share_of_ads = []
for month in df_ads.date_year_month2.unique():
    share_of_ads.append(df_ads[df_ads.date_year_month2 == month][df_ads[df_ads.date_year_month2 == month].is_ad == True][0].values[0]/df_ads.groupby("date_year_month2")[0].sum()[month])

# %%
df_ads_aggregated = pd.DataFrame(df_posts.groupby(["date_year_month2"]).size())

# %%
df_ads_aggregated["share_of_ads"] = share_of_ads

# %%
total_ads = []
for month in df_ads.date_year_month2.unique():
    total_ads.append(df_ads[df_ads.date_year_month2 == month][df_ads[df_ads.date_year_month2 == month].is_ad == True][0].values[0])

# %%
df_ads_aggregated["total_ads"] = total_ads

# %%
df_ads_aggregated

# %% [markdown]
# ### Proportion of ads of all posts

# %%
x = df_ads_aggregated.index
energy = df_ads_aggregated.share_of_ads

x_pos = [i for i, _ in enumerate(x)]

plt.figure(figsize=(15,7))
plt.bar(x_pos, energy)
plt.xlabel("Month")
plt.ylabel("Share of ads")

plt.xticks(x_pos, x)

#axes = plt.gca()
#axes.set_ylim([1000,1600])

plt.show()

# %% [markdown]
# ### Absolut amount of ads

# %%
x = df_ads_aggregated.index
energy = df_ads_aggregated.total_ads

x_pos = [i for i, _ in enumerate(x)]

plt.figure(figsize=(15,7))
plt.bar(x_pos, energy)
plt.xlabel("Month")
plt.ylabel("Total ads")

plt.xticks(x_pos, x)

#axes = plt.gca()
#axes.set_ylim([1000,1600])

plt.show()

# %%
get_total_percentage(pd.DataFrame(df_ads_aggregated["total_ads"]))

# %%
get_total_percentage(pd.DataFrame(df_ads_aggregated["share_of_ads"]))

# %% [markdown]
# # 6) Did the number of likes decrease?

# %%
df_likes = df_posts.sort_values(by = ["date"])

# %%
df_likes = df_likes[df_likes.likes != "Error"]

# %%
df_likes["likes"] = list(map(int, df_likes["likes"]))

# %%
df_likes.groupby(["date_year_month2"]).size()

# %%
df_likes.groupby(["date_year_month2"]).size().values

# %%
likes_per_post = df_likes.groupby(["date_year_month2"]).likes.sum().values / df_likes.groupby(["date_year_month2"]).size().values

# %%
likes_per_post

# %%
plt.plot(likes_per_post)
axes = plt.gca()
axes.set_ylim([0,50000])
plt.show()

# %%
likes_per_post.mean()

# %%
likes_per_post.std()

# %% [markdown]
# ### Top posts (likes)

# %%
df_likes = df_posts.sort_values(by=["likes"],ascending=False)

# %%
df_likes = df_likes[df_likes.likes != "Error"]
df_likes["likes"] = list(map(int, df_likes["likes"]))

# %%
df_likes = df_likes.sort_values(by=["likes"],ascending=False)

# %%
df_likes.head(20)

# %%
