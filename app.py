import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyser")

upload_file = st.sidebar.file_uploader("Choose any exported WhatsApp Chat")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    #fetching unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Select User: ", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Messages Statistics")
        num_messages,words,media_msg,links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media_msg)
        with col4:
            st.header("Links Shared")
            st.title(links)

        #finding most active users
        if selected_user == 'Overall':
            st.title("Most Active Users")
            user_msgs_count, percentage_df = helper.most_active_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:       
                ax = ax.bar(user_msgs_count.index, user_msgs_count.values, color = "red")
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(percentage_df)
        
        #wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.imshow(df_wc)
        st.pyplot(fig, use_container_width=False)

        #most used words
        st.title("Most Used Words")
        df_words = helper.most_used_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(df_words['words'], df_words['frequency'])
        st.pyplot(fig, use_container_width=False)

        #most used emojis
        st.title("Most Used Emojis")
        df_emoji = helper.most_used_emoji(selected_user, df)
        plt.rcParams['font.family'] = 'Segoe UI Emoji'
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(df_emoji[1].head(), labels = df_emoji[0].head(), autopct="%0.2f")
        st.pyplot(fig, use_container_width=False)

        #message timeline
        st.title("Monthly Timeline")
        df_timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.plot(df_timeline['timeline'], df_timeline['user_messages'], color="green")
        num_labels = len(df_timeline['timeline'].unique())  # Unique timeline labels
        fontsize = max(5, min(12, 100 / num_labels))  # Adjust between 5 and 12 
        plt.xticks(rotation = "vertical", fontsize=fontsize)
        st.pyplot(fig, use_container_width=False)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.day_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_day.index, busy_day.values)  
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(busy_month.index, busy_month.values, color='orange')  
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

