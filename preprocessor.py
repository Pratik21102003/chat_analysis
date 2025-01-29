import re
import pandas as pd
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message=re.split(pattern,data)[1:]
    date=re.findall(pattern,data)
    df=pd.DataFrame({'message':message,'date':date})
    df['date']=pd.to_datetime(df['date'],format="%m/%d/%y, %H:%M - ")
    users = []
    messages = []
    for message in df['message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:  # user name
                users.append(entry[1])
                messages.append(" ".join(entry[2:]))
            else:
                users.append('group_notification')
                messages.append(entry[0])

    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    return df