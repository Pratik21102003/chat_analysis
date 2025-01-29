import streamlit as st
import preprocessor,helper
from matplotlib import pyplot as plt
import seaborn as sns
st.sidebar.title("Chat Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)
    
   
    
    # Display users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user=st.sidebar.selectbox("Analyze",user_list)
    
    if st.sidebar.button(" Show Analysis"):
        
        st.title("Top Stats")
        num_msg, num_word,media,emoji,msg=helper.stats(selected_user,df)
        col1,col2,col3,col4,col5=st.columns(5)
        
        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words used")
            st.title(num_word)
        with col3:
            st.header("Media Shared")
            st.title(media)
        with col4:
            st.header("Emoji shared")
            st.title(emoji)
        with col5:
            st.header("Daily Avg. Msg")
            st.title(msg)
       
        active,least=helper.rows(selected_user,df)
        col1,col2,col3=st.columns(3) 
        
        with col1:
            st.header("Active Dates")
            st.dataframe(active)
            
        with col2:
            st.header("Least Active")
            st.dataframe(least)
            
        with col3:
            st.header("Timeline")
            df_wc=helper.timelines(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(df_wc['time'],df_wc['messages'],color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        col1,col2,col3=st.columns(3)
        
        with col1:
            st.header("Month Analysis")
            monthly=helper.monthly_analysis(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(monthly['month'],monthly['count'],color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.header("Weekly Analysis")
            weekly=helper.weekly_analysis(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(weekly['day_name'],weekly['count'],color='cyan')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col3:
            st.header("Daily Analysis")
            new_df=helper.daily_analysis(selected_user,df)
            fig,ax=plt.subplots()
            ax=sns.heatmap(new_df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0))
            st.pyplot(fig)
                
        col1,col2=st.columns(2) 
        
        with col1:
            st.header("WordCloud")
            df_wc=helper.creat_wc(selected_user,df)
            fig,ax=plt.subplots()
            ax.imshow(df_wc,interpolation='bilinear')
            st.pyplot(fig)
        
        with col2:
            st.header("Common Words")
            df_cw=helper.common_words(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(df_cw[0],df_cw[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        st.header("Common Emoji")
        col1,col2=st.columns(2) 
        
        with col1:
            df_cw=helper.emoji_count(selected_user,df)
            st.dataframe(df_cw)
        
        with col2:
            df_cw=helper.emoji_count(selected_user,df)
            fig,ax=plt.subplots()
            ax.pie(df_cw[1].head(),labels=df_cw[0].head(),autopct="%0.2f")
            st.pyplot(fig)
            
        