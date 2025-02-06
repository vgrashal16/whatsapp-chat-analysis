import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyser")

upload_file = st.sidebar.file_uploader("Choose any exported WhatsApp Chat")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)
    
    #fetching unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('chat/group notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Select User: ", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title("Messages Analysis")
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
                st.pyplot(fig)
            with col2:
                st.dataframe(percentage_df)
        
        #wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most used words
        st.title("Most Used Words")
        df_words = helper.most_used_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(df_words['words'], df_words['frequency'])
        st.pyplot(fig)

        #most used emojis
        st.title("Most Used Emojis")
        df_emoji = helper.most_used_emoji(selected_user, df)
        plt.rcParams['font.family'] = 'Segoe UI Emoji'
        fig, ax = plt.subplots()
        ax.pie(df_emoji[1].head(), labels = df_emoji[0].head(), autopct="%0.2f")
        st.pyplot(fig)