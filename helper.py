from urlextract import URLExtract
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
 