from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0] #fetching number of messages shared

    words=[] #fetching number of words shared
    for messages in df['user_messages']:
        words.extend(messages.split())  

    media_msg = df[df['user_messages'] == '<Media omitted>\n'].shape[0] #fetching number of medias shared

    links = [] #fetching number of links shared 
    extractor = URLExtract()
    for messages in df['user_messages']:
        links.extend(extractor.find_urls(messages))

    return num_messages,len(words),media_msg,len(links)

def most_active_users(df):
    user_msgs_count = df['users'].value_counts().head(7)
    percentage_df = round((df['users'].value_counts()/df.shape[0]*100),2).reset_index().rename(columns={'index':'users', 'count':'percent'})

    return (user_msgs_count), percentage_df
 
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    df = df[(df['user_messages'] != '<Media omitted>\n') & (~df['user_messages'].str.contains('https', na=False))]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['user_messages'].str.cat(sep = ""))

    return df_wc

def most_used_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    words_df = df[(df['users'] != 'chat/group notification') & (df['user_messages'] != '<Media omitted>\n')]
    file = open("hinglish_stopwords.txt", "r", encoding="utf-8")
    stop_words = file.read()
    words = []
    for messages in words_df['user_messages']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)    
    df_words = pd.DataFrame(Counter(words).most_common(20), columns=['words', 'frequency'])   
    
    return df_words