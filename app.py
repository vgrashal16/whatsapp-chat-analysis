import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

st.sidebar.title("WhatsApp Chat Analyser")
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
upload_file = st.sidebar.file_uploader("Choose any exported WhatsApp Chat")

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    sentiments = SentimentIntensityAnalyzer()
    
    #creating different columns for (Positive/Negative/Neutral)
    df["po"] = [sentiments.polarity_scores(i)["pos"] for i in df["user_messages"]] # Positive
    df["ne"] = [sentiments.polarity_scores(i)["neg"] for i in df["user_messages"]] # Negative
    df["nu"] = [sentiments.polarity_scores(i)["neu"] for i in df["user_messages"]] # Neutral
    
    #to indentify true sentiment per row in message column
    def sentiment(d):
        if d["po"] >= d["ne"] and d["po"] >= d["nu"]:
            return 1
        if d["ne"] >= d["po"] and d["ne"] >= d["nu"]:
            return -1
        if d["nu"] >= d["po"] and d["nu"] >= d["ne"]:
            return 0

    #creating new column & Applying function
    df['value'] = df.apply(lambda row: sentiment(row), axis=1)

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
            
            # Getting names per sentiment
            x = df['users'][df['value'] == 1].value_counts().head(10)
            y = df['users'][df['value'] == -1].value_counts().head(10)
            z = df['users'][df['value'] == 0].value_counts().head(10)

            col1,col2,col3 = st.columns(3)
            with col1:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Most Positive Users</h3>",unsafe_allow_html=True)
                
                # Displaying
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Most Neutral Users</h3>",unsafe_allow_html=True)
                
                # Displaying
                fig, ax = plt.subplots()
                ax.bar(z.index, z.values, color='grey')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col3:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Most Negative Users</h3>",unsafe_allow_html=True)
                
                # Displaying
                fig, ax = plt.subplots()
                ax.bar(y.index, y.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        
        #wordcloud
        col1,col2,col3 = st.columns(3)
        with col1:
            try:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Positive WordCloud</h3>",unsafe_allow_html=True)
                
                # Creating wordcloud of positive words
                df_wc = helper.create_wordcloud(selected_user, df,1)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except:
                # Display error message
                st.image('error.webp')
        with col2:
            try:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Neutral WordCloud</h3>",unsafe_allow_html=True)
                
                # Creating wordcloud of neutral words
                df_wc = helper.create_wordcloud(selected_user, df,0)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except:
                # Display error message
                st.image('error.webp')
        with col3:
            try:
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Negative WordCloud</h3>",unsafe_allow_html=True)
                
                # Creating wordcloud of negative words
                df_wc = helper.create_wordcloud(selected_user, df,-1)
                fig, ax = plt.subplots()
                ax.imshow(df_wc)
                st.pyplot(fig)
            except:
                # Display error message
                st.image('error.webp')

        #most used words
        col1, col2, col3 = st.columns(3)
        with col1:
            # Data frame of most common positive words.
            most_common_df = helper.most_common_words(selected_user, df,1)
            
            # heading
            st.markdown("<h3 style='text-align: center; color: white;'>Positive Words</h3>",unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            # Data frame of most common neutral words.
            most_common_df = helper.most_common_words(selected_user, df,0)
            
            # heading
            st.markdown("<h3 style='text-align: center; color: white;'>Neutral Words</h3>",unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1],color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
  
        with col3:
                # Data frame of most common negative words.
                most_common_df = helper.most_common_words(selected_user, df,-1)
                
                # heading
                st.markdown("<h3 style='text-align: center; color: white;'>Negative Words</h3>",unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.barh(most_common_df[0], most_common_df[1], color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
 
        #most used emojis
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Most Used Emoji(Positive)</h3>",unsafe_allow_html=True)
            
            df_emoji = helper.most_used_emoji(selected_user, df, 1)
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(df_emoji[1].head(), labels = df_emoji[0].head(), autopct="%0.2f")
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Most Used Emoji(Neutral)</h3>",unsafe_allow_html=True)
            
            df_emoji = helper.most_used_emoji(selected_user, df, 0)
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(df_emoji[1].head(), labels = df_emoji[0].head(), autopct="%0.2f")
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Most Used Emoji(Negative)</h3>",unsafe_allow_html=True)
            
            df_emoji = helper.most_used_emoji(selected_user, df, -1)
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(df_emoji[1].head(), labels = df_emoji[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        #message timeline
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Timeline(Positive)</h3>",unsafe_allow_html=True)
            
            timeline = helper.monthly_timeline(selected_user, df,1)
            
            fig, ax = plt.subplots()
            ax.plot(timeline['timeline'], timeline['user_messages'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Timeline(Neutral)</h3>",unsafe_allow_html=True)
            
            timeline = helper.monthly_timeline(selected_user, df,0)
            
            fig, ax = plt.subplots()
            ax.plot(timeline['timeline'], timeline['user_messages'], color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Timeline(Negative)</h3>",unsafe_allow_html=True)
            
            timeline = helper.monthly_timeline(selected_user, df,-1)
            
            fig, ax = plt.subplots()
            ax.plot(timeline['timeline'], timeline['user_messages'], color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #activity map        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Activity map(Positive)</h3>",unsafe_allow_html=True)
            
            busy_day = helper.day_activity_map(selected_user, df,1)
            
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Activity map(Neutral)</h3>",unsafe_allow_html=True)
            
            busy_day = helper.day_activity_map(selected_user, df, 0)
            
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Daily Activity map(Negative)</h3>",unsafe_allow_html=True)
            
            busy_day = helper.day_activity_map(selected_user, df, -1)
            
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Activity map(Positive)</h3>",unsafe_allow_html=True)
            
            busy_month = helper.month_activity_map(selected_user, df,1)
            
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Activity map(Neutral)</h3>",unsafe_allow_html=True)
            
            busy_month = helper.month_activity_map(selected_user, df, 0)
            
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Monthly Activity map(Negative)</h3>",unsafe_allow_html=True)
            
            busy_month = helper.month_activity_map(selected_user, df, -1)
            
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #activity heat map
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h3 style='text-align: center; color: white;'>Weekly Activity Map(Positive)</h3>",unsafe_allow_html=True)
            
            user_heatmap = helper.activity_heatmap(selected_user, df, 1)
            
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)
   
        with col2: 
            st.markdown("<h3 style='text-align: center; color: white;'>Weekly Activity Map(Neutral)</h3>",unsafe_allow_html=True)
            
            user_heatmap = helper.activity_heatmap(selected_user, df, 0)
            
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

        with col3:
            st.markdown("<h3 style='text-align: center; color: white;'>Weekly Activity Map(Negative)</h3>",unsafe_allow_html=True)
            
            user_heatmap = helper.activity_heatmap(selected_user, df, -1)
            
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

