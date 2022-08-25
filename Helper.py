from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(Selected_User, df):

    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]
    num_messages = df.shape[0]

    #fetching the total number of words
    words = []
    for Message in df["Message"]:
        words.extend(Message.split())

    #fetching the number of media messages

    Num_Media_Messages = df[df["Message"] == "<Media omitted>\n"].shape[0]

    # Fetching the total Links Shared
    Links = []
    for Message in df["Message"]:
        Links.extend(extract.find_urls(Message))

    return num_messages, len(words), Num_Media_Messages, len(Links)


def most_busy_users(df):
    x = df["Name"].value_counts().head()
    df = round((df["Name"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"Name","Name":"Percent"})

    return  x, df

def create_wordcloud(Selected_User,df):

    f = open("StopWords.txt", "r")
    Stopwords = f.read()

    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

        # removing grp notifications
    temp = df[df["Name"] != "group_notification"]
    temp = temp[temp["Message"] != "<Media omitted>\n"]

    def remove_stop_words(Message):
        y = []
        for word in Message.lower().split():
            if word not in Stopwords:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    temp["Message"] = temp["Message"].apply(remove_stop_words)
    df_wc = wc.generate(temp["Message"].str.cat(sep=" "))
    return df_wc

def most_common_words(Selected_User,df):

    f = open("StopWords.txt","r")
    Stopwords = f.read()

    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

        # removing grp notifications
    temp = df[df["Name"] != "group_notification"]
    temp = temp[temp["Message"] != "<Media omitted>\n"]

    words = []

    for Message in temp["Message"]:
        for word in Message.lower().split():
            if word not in Stopwords:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(30))

    return most_common_df

# def emoji(Selected_User,df):
#     if Selected_User != "Overall":
#         df = df[df["Name"] == Selected_User]
#
#     emojis = []
#     for Message in df["Message"]:
#         emojis.extend([c for c in Message if c in emoji.get_emoji_regexp])
#
#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df

def Monthly_Timeline(Selected_User,df):

    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

    Time_line = df.groupby(["Year", "Month_num", "Month"]).count()["Message"].reset_index()

    Time = []
    for i in range(Time_line.shape[0]):
        Time.append(Time_line["Month"][i] + "-" + str(Time_line["Year"][i]))

    Time_line["Time"] = Time

    return Time_line


def Daily_Timeline(Selected_User,df):

    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

    Daily_Timeline = df.groupby("date").count()["Message"].reset_index()

    return Daily_Timeline


def Weekly_activity_map(Selected_User,df):

    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

    return df["Day_name"].value_counts()


def Month_Activity_Map(Selected_User,df):
    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

    return df["Month"].value_counts()


def Activity_Heatmap(Selected_User,df):
    if Selected_User != "Overall":
        df = df[df["Name"] == Selected_User]

    User_heatmap = df.pivot_table(index="Day_name", columns="period", values="Message", aggfunc="count").fillna(0)


    return User_heatmap