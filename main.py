# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-auth-oauthlib",
#    "google-api-python-client",
#    "httpx",
#    "python-dotenv"
# ]
# ///

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
import httpx

load_dotenv()

api_key = os.environ['API_KEY']
# openrouter_api_url = "https://aipipe.org/openrouter/v1/chat/completions"
openrouter_api_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
client = httpx.Client(timeout =60) 
headers={
        'Authorization':f'Bearer {api_key}'
}

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.pickle"

def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES)
        creds = flow.run_local_server(port=8080)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def generate_chapters(transcript_path):
    # Return string of chapters format e.g.:
    # 00:00 Introduction
    # 01:35 Topic A
    with open(transcript_path, "r") as f:
            transcript = f.read()   

    response = client.post(
        openrouter_api_url,
        headers=headers,
        json={
            'model': 'gpt-4o-mini',
            'messages': [
                {
                    'role': 'user',
                    'content': f'Generate chapters for the following transcript: {transcript}'
                },
                {
                    'role':'system',
                    'content': 'Generate a chapters for the video, chapters will be uploaded to youtube, so generate in format such that they can be directly copied to youtube. The format should be like this: 00:00 Introduction, 01:35 Topic A, 02:00 Topic B. The chapters should be in the format of time and then the topic name.'
                }
            ],
        }
    )
    # write response to file
    with open("response_chapters.json", "w") as f:
        f.write(str(response.json()))
    chapters = response.json().get('choices')[0].get('message').get('content')
    # write chapters to file
    with open("chapters.txt", "w") as f:
        f.write(chapters)
    return "00:00 Introduction\n01:00 First Topic\n02:00 First Topic"

def generate_detailed_description(transcript_path):
    # Return formatted transcript or summary
    with open(transcript_path, "r") as f:
            transcript = f.read()   
    response = client.post(
        openrouter_api_url,
        headers=headers,
        json={
            'model': 'gpt-4o-mini',
            'messages': [
                {
                    'role': 'user',
                    'content': f'Generate a detailed description for the following transcript: {transcript}'
                },
                {
                    'role':'system',
                    'content': 'Generate a detailed description for the video, descirption will be uploaded to youtube so keep it brief and useful for users in terms of searching.'
                }
            ],
        }
    )
    with open("response_description.json", "w") as f:
        f.write(str(response.json()))
    detailed_description = response.json().get('choices')[0].get('message').get('content')
    # write detailed description to file
    with open("detailed_description.txt", "w") as f:
        f.write(detailed_description)
    return "This is a detailed description with timestamps."

# ----------- Upload Function -----------
def upload_video(youtube, video_path, title, transcript_path, tags=None, privacy_status="unlisted"):
    chapters = generate_chapters(transcript_path)
    detailed_description = generate_detailed_description(transcript_path)

    full_description = f"{detailed_description}\n\nChapters:\n{chapters}"

    body = {
        "snippet": {
            "title": title,
            "description": full_description,
            "tags": tags or [],
            "categoryId": "27"  # 27 = Education
        },
        "status": {
            "privacyStatus": privacy_status  # 'private', 'public', or 'unlisted'
        }
    }
    return "done"
    # media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/*')
    # request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    # print("Uploading video...")
    # response = None
    # while response is None:
    #     status, response = request.next_chunk()
    #     if status:
    #         print(f"Uploaded {int(status.progress() * 100)}%")
    # print("Upload complete. Video ID:", response["id"])
    # return response["id"]

# ----------- Usage Example -----------
if __name__ == "__main__":
    youtube = get_authenticated_service()
    video_id = upload_video(
        youtube=youtube,
        video_path="fork_demo.mp4",
        title="Lecture 1: Introduction to Automation",
        transcript_path="sample_transcription.txt",
        tags=["automation", "python", "youtube api"],
        privacy_status="unlisted"
    )
