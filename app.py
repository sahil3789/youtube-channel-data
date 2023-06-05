import streamlit as st
import pandas as pd
from google_api import youtube_api
from database import mongo
from database import mysql

st.set_page_config(layout="wide")

hide_streamlit_style="""
<style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 2rem;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header('Youtube Data Harvesting and Warehousing using MySQL, MongoDB and Streamlit')

input_column, query_column = st.columns([2,4])

options={ 
        'List names of all the videos and their corresponding channels':'1',
        'Which channels have the most number of videos, and how many videos do they have':'2',
        'What are the top 10 most viewed videos and their respective channels':'3',
        'How many comments were made on each video, and what are their corresponding video names':'4',
        'Which videos have the highest number of likes, and what are their corresponding channel names':'5',
        'What is the total number of likes and dislikes for each video, and what are their corresponding video names':'6',
        'What is the total number of views for each channel, and what are their corresponding channel names':'7',
        'What are the names of all the channels that have published videos in the year 2022':'8',
        'What is the average duration of all videos in each channel, and what are their corresponding channel names':'9',
        'Which videos have the highest number of comments, and what are their corresponding channel names':'10'
}

query={
    "1":"SELECT channel_data.channel_id, video_data.video_title, channel_data.channel_title FROM channel_data INNER JOIN video_data ON channel_data.channel_id=video_data.channel_id;",
    "2":"SELECT * FROM channel_data ORDER BY video_count DESC LIMIT 10;",
    "3":"SELECT channel_data.channel_id, channel_data.channel_title, video_data.video_title, video_data.view_count FROM channel_data INNER JOIN video_data ON channel_data.channel_id=video_data.channel_id ORDER BY video_data.view_count DESC LIMIT 10;",
    "4":"SELECT video_data.video_title, video_data.comment_count from video_data;",
    "5":"SELECT video_data.video_title, video_data.like_count FROM video_data ORDER BY video_data.like_count DESC;",
    "6":"SELECT video_data.video_title, video_data.like_count FROM video_data;",
    "7":"SELECT video_data.video_title, video_data.view_count FROM video_data;",
    "8":"SELECT * FROM video_data WHERE published_date LIKE '2022%';",
    "9":"SELECT AVG(video_data.duration_min), video_data.video_title from video_data GROUP BY video_data.video_title;",
   "10":"SELECT channel_data.channel_id, video_data.video_title, video_data.comment_count, channel_data.channel_title FROM channel_data INNER JOIN video_data ON channel_data.channel_id=video_data.channel_id ORDER BY video_data.comment_count DESC LIMIT 10;"
}   

with input_column: 

    st.markdown(":red[Fetch data and export it to MongoDB]")

    channel_id_list=st.text_input('Enter Youtube channel ids (use , as separator for multiple id)', 'channel id')
    mongo_uri=st.text_input('Enter Mongo Atlas URI to export to', 'Mongo URI')
    db_name=st.text_input('Enter database name to export to', 'DB_Name')

    if st.button('Fetch data and export it to MongoDB'):
        for channel_id in list(channel_id_list.split(",")):
            [mongo.insert({"mongo_uri":mongo_uri, "db_name":db_name}, collection_data) for collection_data in youtube_api.get_data(channel_id.strip())]
                
    st.markdown(":red[Migrate data from MongoDB to MySQL]")

    channel_id=st.text_input('Enter Youtube channel id to export data', 'channel id')
    mongo_uri=st.text_input('Enter Mongo Atlas URI to fetch from', 'Mongo URI')
    db_name=st.text_input('Enter database Name to fetch from', 'DB_Name')

    if st.button('insert data in MySQL database (configurable in app )'):

        mysql.create_tables('./database/tables.sql')

        for collection_name in ["channel_data","playlist_data","video_data","comment_data"]:
            collection_data=mongo.read({"mongo_uri":mongo_uri, "db_name":db_name}, collection_name, channel_id)
            mysql.insert(collection_data, collection_name)

with query_column:

    option=st.selectbox(
    'Get data from MySQL',
    tuple(options.keys()))
    
    if st.button('Query database'):

        df=mysql.run_query(query[options[option]])
        st.table(df)
        