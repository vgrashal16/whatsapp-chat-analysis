import re
import pandas as pd

def preprocess(data):
    pattern_re = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\s-\s"
    messages = re.split(pattern_re, data)[1:]
    dates = re.findall(pattern_re, data)
    df = pd.DataFrame({'messages':messages, 'dates': dates})
    df['dates'] = df['dates'].str.replace("\u202f", " ", regex=True)  
    df['dates'] = df['dates'].str.replace(" - $", "", regex=True)
    df['dates'] = pd.to_datetime(df['dates'], format='%m/%d/%y, %I:%M %p')
    users = []
    user_msgs = []
    for msg in df['messages']:
        entry = re.split(r'([\w\W]+?):\s', msg)
        if entry[1:]:
            users.append(entry[1])
            user_msgs.append(entry[2])
        else:
            users.append("chat/group notification")
            user_msgs.append(entry[0])

    df['users'] = users
    df['user_messages'] = user_msgs

    df.drop(columns=['messages'], inplace=True)
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['month_num'] = df['dates'].dt.month
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute

    return df