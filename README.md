# Youtube Channel Data

Youtube Channel Data App, built using python and streamlit allows users to fetch, store, migrate and visualize youtube channel data.

Read the complete youtube data api documentation [here](https://developers.google.com/youtube/v3/docs)<br />

# Guide #

<h3>Install the dependencies</h3>
streamlit : <code> pip install streamlit </code> <br/>
pymongo : <code> pip install pymongo </code> <br/>
pysql : <code> pip install pysql </code> <br/>
googleapiclient : <code>pip install google-api-python-client</code><br/>

<h3>Youtube Api Documentation</h3>

<h4>1.Generating Google Developer API_Key</h4>
<ul>
<li>Go to the API Console.</li>
<li>From the projects list, select a project or create a new one.</li>
<li>If the APIs & services page isn't already open, open the left side menu and select APIs & services.</li>
<li>On the left, choose Credentials.</li>
<li>Click Create credentials and then select API key.</li>
</ul>
<h4>2.Making API Request-using API_Key</h4>

```  
#code snippet to fetch channel details

api_service_name="youtube"
api_version="v3"
api_key=""

youtube=googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)
  
data=youtube.channels().list(
    part="snippet,contentDetails, statistics, status",
    id=channel_id
).execute()
```

<h3>MySQL Table Schema</h3>

<h4>1.1.channel_data</h4>

```
CREATE TABLE IF NOT EXISTS channel_data(
        dtype VARCHAR(255),
        channel_id VARCHAR(255),
        channel_title VARCHAR(255),
        channel_description VARCHAR(10000),
        view_count BIGINT,
        video_count BIGINT,
        status VARCHAR(255));
```        

<h4>1.2.playlist_data</h4>

```
CREATE TABLE IF NOT EXISTS playlist_data(
       dtype VARCHAR(255),
       channel_id VARCHAR(255),
       playlist_id VARCHAR(255),
       playlist_title VARCHAR(255));
```

<h4>1.3.video_data</h4>

```
CREATE TABLE IF NOT EXISTS video_data(
        dtype VARCHAR(255),
        video_id VARCHAR(255),
        channel_id VARCHAR(255),
        video_title VARCHAR(255),
        video_description VARCHAR(10000),
        published_date VARCHAR(255),
        thumbnail VARCHAR(255),
        duration_min FLOAT,
        view_count BIGINT,
        like_count BIGINT,
        favourite_count BIGINT,
        comment_count BIGINT);
```

<h4>1.4.comment_data</h4>

```
CREATE TABLE IF NOT EXISTS comment_data(
        dtype VARCHAR(255),
        comment_id VARCHAR(255),
        video_id VARCHAR(255),
        comment_text VARCHAR(255),
        comment_author VARCHAR(255),
        published_date VARCHAR(255));
```
