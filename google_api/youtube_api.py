import googleapiclient.discovery
from data import format

api_service_name="youtube"
api_version="v3"
api_key=""

youtube=googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=api_key)

def get_data(channel_id):

    video_ids=get_channel_videos(channel_id)
    return [get_channel_data(channel_id), get_playlist_data(channel_id),
            get_video_data(video_ids), get_comment_data(video_ids)]


def get_channel_videos(channel_id):

    data=youtube.activities().list(
        part="snippet, contentDetails",
        channelId=channel_id
    ).execute()

    video_ids=[]
    for item in data["items"]:
        if "upload" in item["contentDetails"].keys():
            video_ids.append(item["contentDetails"]["upload"]["videoId"])
        elif "upload" in item["contentDetails"].keys():
            video_ids.append(item["contentDetails"]["playlistItem"]["resourceId"]["videoId"])
    return [*set(video_ids)]        


def get_channel_data(channel_id):
    channel_data=[]

    data=youtube.channels().list(
        part="snippet,contentDetails, statistics, status",
        id=channel_id
    ).execute()

    for item in data["items"]:
        if "viewCount" not in item["statistics"].keys():
            item["statistics"]["viewCount"] = 0

        channel_data.append({
            "dtype": "channel_data",
            "channel_id": item["id"],
            "channel_title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "view_count": int(item["statistics"]["viewCount"]),
            "video_count":int(item["statistics"]["videoCount"]),
            "status": item["status"]["privacyStatus"]
        })

    return channel_data


def get_playlist_data(channel_id):
    playlist_data=[]

    data=youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id
    ).execute()

    for item in data["items"]:
        playlist_data.append({
            "dtype": "playlist_data",
            "channel_id": item["snippet"]["channelId"],
            "playlist_id": item["id"],
            "playlist_title": item["snippet"]["title"]
        })

    return playlist_data


def get_video_data(video_id_list):
    video_data=[]

    for video_id in video_id_list:
        data=youtube.videos().list(
            part="snippet,contentDetails, statistics",
            id=video_id
        ).execute()

        for item in data["items"]:
            stats={"viewCount":0,
                     "likeCount":0,
                     "favouriteCount":0,
                     "commentCount":0
                     }
            for stat in stats.keys():
                if stat not in item["statistics"]:
                    item["statistics"][stat]=stats[stat]

            video_data.append({
                "dtype": "video_data",
                "video_id": item["id"],
                "channel_id": item["snippet"]["channelId"],
                "video_title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "published_date": item["snippet"]["publishedAt"],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                "duration_min": format.get_duration_minutes(item["contentDetails"]["duration"]),
                "view_count": int(item["statistics"]["viewCount"]),
                "like_count": int(item["statistics"]["likeCount"]),
                "favourite_count":int(item["statistics"]["favouriteCount"]),
                "comment_count":int(item["statistics"]["commentCount"])
            })

    return video_data


def get_comment_data(video_id_list):
    comment_data=[]

    for video_id in video_id_list:
        data = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id
        ).execute()

        for item in data["items"]:
            comment_data.append({
                "dtype": "comment_data",
                "comment_id": item["id"],
                "video_id": item["snippet"]["videoId"],
                "comment_text": item["snippet"]["topLevelComment"]["snippet"]["videoId"],
                "comment_author": item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                "published_date": item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
            })

    return comment_data