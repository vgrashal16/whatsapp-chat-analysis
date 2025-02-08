from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

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

    words_df = df[(df['users'] != 'group notification') & (df['user_messages'] != '<Media omitted>\n')]
    file = open("hinglish_stopwords.txt", "r", encoding="utf-8")
    stop_words = file.read()

    def remove_stopwords(message):
        temp = []
        for word in message.lower().split():
            if word not in stop_words:
                temp.append(word)
        return " ".join(temp)

    words_df['user_messages'] = words_df['user_messages'].apply(remove_stopwords)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(words_df['user_messages'].str.cat(sep = ""))
    return df_wc

def most_used_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    words_df = df[(df['users'] != 'group notification') & (df['user_messages'] != '<Media omitted>\n')]
    file = open("hinglish_stopwords.txt", "r", encoding="utf-8")
    stop_words = file.read()
    words = []
    for messages in words_df['user_messages']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)    
    df_words = pd.DataFrame(Counter(words).most_common(20), columns=['words', 'frequency'])   
    
    return df_words

def most_used_emoji(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    emojis = []
    for message in df['user_messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    timeline_df = df.groupby(['year', 'month_num',  'month']).count()['user_messages'].reset_index()

    timeline = []
    for i in range(timeline_df.shape[0]):
        timeline.append(timeline_df['month'][i] + " - " + str(timeline_df['year'][i]))
    timeline_df['timeline'] = timeline

    return timeline_df

def day_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    return df['month'].value_counts()


def activity_heatmap(selected_user, df):
    df_copy = df.copy() 

    if selected_user != 'Overall':
        df_copy = df_copy[df_copy['users'] == selected_user]

    df_copy['day_name'] = pd.Categorical(df_copy['day_name'], 
                                         categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
                                         ordered=True)

    df_copy['period'] = pd.Categorical(df_copy['period'], 
                                       categories=[f"{i}-{i+1}" if i != 23 else "23-00" for i in range(24)], 
                                       ordered=True)

    return df_copy.pivot_table(index='day_name', columns='period', values='user_messages', aggfunc='count').fillna(0)

    