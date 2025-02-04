def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    num_messages = df.shape[0] #fetching number of messages
    words=[] #fetching number of words
    for messages in df['user_messages']:
        words.extend(messages.split())  
    return num_messages,len(words)
 