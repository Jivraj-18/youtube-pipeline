# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google",
#    "google-api-python-client",
# ]
# ///

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
import io
import os
import re

# Function to sanitize file names
def sanitize_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '112zkI5uJ3lwHorf6p4QuEYvVme9-j5Zo'

creds = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

response = service.files().list(
    q=f"'{FOLDER_ID}' in parents and trashed = false",
    orderBy='createdTime desc',
    pageSize=10).execute()

# write the response out to a json file 
with open('response.json','w') as f:
    import json
    json.dump(response, f, indent=4)

# filter all the fiels which have mimeType as application/vnd.google-apps.document
docs_files = [file for file in response.get('files', []) if file['mimeType'] == 'application/vnd.google-apps.document']

video_files = [file for file in response.get('files', []) if file['mimeType'] == 'video/mp4']

# for doc in docs_files:
#     doc = doc  # Pick the first doc (or loop through them)
#     file_id = doc['id']
#     file_name = sanitize_filename(doc['name']) + ".txt"

#     # Export as plain text
#     request = service.files().export_media(fileId=file_id, mimeType='text/plain')
#     with open(file_name, 'wb') as f:
#         f.write(request.execute())

#     print(f"Exported '{doc['name']}' as '{file_name}'")




for video in video_files[0:1]: 
    file_id = video['id']
    file_name = sanitize_filename(video['name']) + ".mp4"0
    # Create a request to download the video
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()

    # Download the video
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    fh.seek(0)
    # Save the video to a file
    with open(file_name, 'wb') as f:
        f.write(fh.getbuffer())

    print(f"Downloaded '{video['name']}' as '{file_name}'")
