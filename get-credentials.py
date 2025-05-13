# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-auth-oauthlib",
# ]
# ///


from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
creds = flow.run_local_server(port=8080)

# save the credentials to a file
with open("token.pickle", "wb") as token:
    pickle.dump(creds, token)
