import emoji.unicode_codes
import pandas as pd
import emoji
from wordcloud import WordCloud,STOPWORDS
from collections import Counter
f=open('stop_hinglish.txt','r')
data=f.read()

def count_emojis(text):
    return sum(1 for char in text if char in emoji.EMOJI_DATA)  

def stats(selected_user,df):
    count=0
    if selected_user=="Overall":  
        word=[]
        for msg in df['messages']:
            word.extend(msg.split())
            count= count+ count_emojis(msg)
        media=df[df['messages']=='<Media omitted>\n'].shape[0]
        daily=(round(df['messages'].shape[0]/df['only_date'].nunique()))
        return df.shape[0],len(word),media,count,daily
    else:
        new_df=df[df['user']==selected_user]
        word=[]
        for msg in new_df['messages']:
            word.extend(msg.split())
            count= count+ count_emojis(msg)
        media=new_df[new_df['messages']=='<Media omitted>\n'].shape[0]
        daily=(round(new_df['messages'].shape[0]/new_df['only_date'].nunique()))
        return new_df.shape[0],len(word),media,count,daily
    
def rows(selected_user,df):
    
    if selected_user=="Overall":
        active=df['only_date'].value_counts().reset_index().rename(columns={'only_date':'date','count':'msg_count'}).head()
        least=df['only_date'].value_counts(ascending=True).reset_index().rename(columns={'only_date':'date','count':'msg_count'}).head()
        return  active,least
    else:
        new_df=df[df['user']==selected_user]
        active=new_df['only_date'].value_counts().reset_index().rename(columns={'only_date':'date','count':'msg_count'}).head()
        least=new_df['only_date'].value_counts(ascending=True).reset_index().rename(columns={'only_date':'date','count':'msg_count'}).head()
        return  active,least
    
def creat_wc(selected_user,df):
       
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    temp_df=df[df['messages']!="<Media omitted>\n"]
    wc=WordCloud(width=500,height=300,min_font_size=6,background_color='white')
    y=[]
    def remove_words(message):
        y = []  # Define an empty list inside the function to collect filtered words
        for word in message.lower().split():
            if word not in data:  # 'data' should be defined globally or passed as an argument
                y.append(word)
        return " ".join(y)
    temp_df['messages'] = temp_df['messages'].apply(remove_words)
    df_wc=wc.generate(temp_df['messages'].str.cat(sep=" "))
    return df_wc    

def common_words(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    temp_df=df[df['messages']!="<Media omitted>\n"]
    words=[]
    for messages in temp_df['messages']:
        for word in messages.lower().split():
            if word not in data:
                words.append(word)
    ans=pd.DataFrame(Counter(words).most_common(20))
    return ans

def emoji_count(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    word=[]
    for msg in df['messages']:
        for words in msg:
            if emoji.is_emoji(words):
                  word.extend(words)
    ans=pd.DataFrame(Counter(word).most_common(20))
    return ans

def timelines(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year', 'month'])['messages'].count().reset_index().sort_values(by=['year', 'month'], ascending=True)
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+ str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def monthly_analysis(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    ans=df['month'].value_counts().reset_index()
    return ans

def weekly_analysis(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    ans=df['day_name'].value_counts().reset_index()
    return ans

def daily_analysis(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    period=[]
    for hour in df['hour']:
        if hour== 23 :
            period.append(str(hour)+"-"+str("00"))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period']=period
    return df