import streamlit as st
import preprocessor
import Helper
import matplotlib.pyplot as plt
import  seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a File")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    #fetch unique user

    User_list = df["Name"].unique().tolist()
    User_list.remove("group_notification")
    User_list.sort()
    User_list.insert(0,"Overall")

    Selected_User = st.sidebar.selectbox("Show Analysis WRT",User_list)

    if st.sidebar.button("Show Analysis"):

        #Stats Area

        Num_messages, words, Num_Media_Messages, Num_Links = Helper.fetch_stats(Selected_User,df)
        st.title("Top Statistics")
        Col1, Col2, Col3, Col4 = st.columns(4)

        with Col1:
            st.header("Total Messages")
            st.title(Num_messages)
        with Col2:
            st.header("Total Words")
            st.title(words)
        with Col3:
            st.header("Media Shared")
            st.title(Num_Media_Messages)
        with Col4:
            st.header("Links Shared")
            st.title(Num_Links)

        # monthly Timeline

        st.title("Monthly Timeline")
        Time_line = Helper.Monthly_Timeline(Selected_User,df)
        fig,ax = plt.subplots()
        ax.plot(Time_line["Time"], Time_line["Message"],color = "#c603fc")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


        # Daily Timeline

        st.title("Daily Timeline")
        Daily_Timeline = Helper.Daily_Timeline(Selected_User, df)

        fig, ax = plt.subplots()
        ax.plot(Daily_Timeline["date"], Daily_Timeline["Message"], color="#3b0207")
        plt.xticks(rotation="vertical")
        plt.figure(figsize=(20, 10))
        st.pyplot(fig)


        # Activity Map
        st.title("Activity_Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            Busy_Day = Helper.Weekly_activity_map(Selected_User,df)
            fig,ax = plt.subplots()
            ax.bar(Busy_Day.index,Busy_Day.values,color = "#735e02")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            Busy_Month = Helper.Month_Activity_Map(Selected_User, df)
            fig, ax = plt.subplots()
            ax.bar(Busy_Month.index, Busy_Month.values, color="#381f36")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)


        #Heatmap
        st.title("Weekly_Activity_Map")
        User_heatmap = Helper.Activity_Heatmap(Selected_User,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(User_heatmap)
        st.pyplot(fig)


        #Finding the busy users in group(Group level)

        if Selected_User == "Overall":
            st.title("Most Busy Users")
            x, new_df = Helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color = "#60e84d")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Wordcloud
        st.title("Wordcloud")
        df_wc = Helper.create_wordcloud(Selected_User,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = Helper.most_common_words(Selected_User,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color = "#54181a")
        plt.xticks(rotation = "vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        #Emoji Analysis
        #
        # emoji_df = Helper.emoji(Selected_User,df)
        # st.dataframe(emoji_df)



