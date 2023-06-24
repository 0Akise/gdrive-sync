#!/usr/bin/env python3
from __future__ import print_function

import os
import os.path
import io
import argparse
import json
import platform

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload

os_name = platform.system()

if os_name == 'Windows':
    config_dir = os.path.join(os.getenv('APPDATA'), 'gdrive-sync')
else:
    config_dir = os.path.expanduser('~/.config/gdrive-sync/')

config_path = os.path.join(config_dir, 'config.json')
token_path = os.path.join(config_dir, 'token.json')
creds_path = os.path.join(config_dir, 'credentials.json')

with open(config_path, 'r') as file:
    config = json.load(file)

SCOPES = ['https://www.googleapis.com/auth/drive']
PATH = config['PATH']
DRIVE = config['DRIVE']
LOCAL = config['LOCAL']

def delete_existing(service, name, parent_id):
    results = service.files().list(q=f"name='{name}' and '{parent_id}' in parents", fields="files(id, name)").execute()
    items = results.get('files', [])

    for item in items:
        service.files().delete(fileId=item['id']).execute()

def download_file(service, file_id, local_path):
    request = service.files().get(fileId=file_id)
    file = request.execute()

    if file['mimeType'] == 'application/vnd.google-apps.folder':
        results = service.files().list(q=f"'{file_id}' in parents", pageSize=100, fields="nextPageToken, files(id, name, mimeType)").execute()
        items = results.get('files', [])

        for item in items:
            download_file(service, item['id'], os.path.join(local_path, item['name']))
    else:
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(local_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            _, done = downloader.next_chunk()

def upload_file(service, file_path, parent_id):
    name = os.path.basename(file_path)

    delete_existing(service, name, parent_id)

    if os.path.isdir(file_path):
        folder_metadata = {
            'name': os.path.basename(file_path),
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        new_parent_id = folder.get('id')

        for filename in os.listdir(file_path):
            upload_file(service, os.path.join(file_path, filename), new_parent_id)
    else:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [parent_id]
        }
        media = MediaFileUpload(file_path, resumable=True)
        request = service.files().create(body=file_metadata, media_body=media, fields='id')
        response = None

        while response is None:
            _, response = request.next_chunk()

        print(f"File '{os.path.basename(file_path)}' uploaded. ID: {response.get('id')}")

def get_file_path(service, file):
    if not 'parents' in file:
        return file['name']

    parents = file['parents']

    if len(parents) == 0:
        print('File has more than one parent')

    parent = service.files().get(fileId=parents[0], fields='id, name, parents').execute()

    return os.path.join(get_file_path(service, parent), file['name'])

def main():
    creds = None
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull", action="store_true")
    parser.add_argument("--push", action="store_true")
    
    args = parser.parse_args()

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        if args.push:
            print("Pushing to the drive...")

            for i, local_path in enumerate(LOCAL):
                full_local_path = os.path.join(local_path, DRIVE[i])
                upload_file(service, full_local_path, PATH)

        if args.pull:
            print("pulling from the drive...")

            for i, drive_path in enumerate(DRIVE):
                results = service.files().list(q=f"'{PATH}' in parents", pageSize=10, fields="nextPageToken, files(id, name, parents)").execute()
                items = results.get('files', [])

                if not items:
                    print(f'No files found in DRIVE:{drive_path}.')
                    continue

                for item in items:
                    if item['name'] == DRIVE[i]:
                        file_path = get_file_path(service, item)
                        local_path = os.path.join(LOCAL[i], item['name'])

                        print(f"DRIVE:{file_path} >> LOCAL:{local_path}")
                        download_file(service, item['id'], local_path)
                    continue

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
