import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

def create_keyfile_dict():
    variables_keys = {
        "type": st.secrets["TYPE"],
        "project_id": st.secrets["PROJECT_ID"],
        "private_key_id": st.secrets["PRIVATE_KEY_ID"],
        "private_key": st.secrets["PRIVATE_KEY"],
        "client_email": st.secrets["CLIENT_EMAIL"],
        "client_id": st.secrets["CLIENT_ID"],
        "auth_uri": st.secrets["AUTH_URI"],
        "token_uri": st.secrets["TOKEN_URI"],
        "auth_provider_x509_cert_url": st.secrets["AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": st.secrets["CLIENT_X509_CERT_URL"],
        "universe_domain" : st.secrets["UNIVERSE_DOMAIN"]
    }
    return variables_keys


def upload_to_drive(file_path):
    scope = ["https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(create_keyfile_dict(), scope)

    drive_service = build("drive", "v3", credentials=creds)

    # Define the file metadata (name and MIME type)
    file_metadata = {
        "name": file_path,
        "mimeType": "application/octet-stream"
    }

    # Create a media file upload object
    media = MediaFileUpload(file_path, mimetype="application/octet-stream", resumable=True)

    # Upload the file
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    file_id = file.get("id")
    # Print the file ID of the uploaded file
    st.info(f"File ID: {file_id}")