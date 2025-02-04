import streamlit as st
import preprocessor, helper

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
        num_messages,words = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)