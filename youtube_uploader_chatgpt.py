import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config_chatgpt as config

def get_authenticated_service():
    """Authenticate and return YouTube service"""
    credentials = None
    
    # Load saved credentials
    if os.path.exists(config.TOKEN_FILE):
        with open(config.TOKEN_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    # Refresh or get new credentials
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.CLIENT_SECRETS_FILE,
                config.SCOPES
            )
            credentials = flow.run_local_server(port=8080)
        
        # Save credentials
        with open(config.TOKEN_FILE, 'wb') as token:
            pickle.dump(credentials, token)
    
    return build('youtube', 'v3', credentials=credentials)

def upload_video(video_path, title, description, tags, category_id="22"):
    """Upload video to YouTube"""
    print(f"Uploading: {title}")
    
    youtube = get_authenticated_service()
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    
    video_id = response['id']
    print(f"✅ Video uploaded! ID: {video_id}")
    print(f"   URL: https://www.youtube.com/watch?v={video_id}")
    
    return video_id
