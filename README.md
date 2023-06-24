# gdrive-sync
Simple python script to sync the files using Google Drive.
I thought It would be great to have a sync system that downloads the file to the designated file path.
Works for Windows/Linux/Mac.

### How to use it

First, You need 3 things to start:
1. Google Cloud API credentials
2. Folder called `Sync` in your Google Drive
3. new config file for `gdrive-sync`

### 1. Get Google Cloud API Credentials
1. Login to the Google, and go to: https://console.cloud.google.com/apis/credentials
2. Follow this article to download your `credentials.json`: https://developers.google.com/drive/api/quickstart/python
3. Put your `credentials.json` into `~/.config/gdrive-sync/
   - If you are using Windows, Use `AppData/Roadming/gdrive-sync/` instead.

### 2. Create Folder called `Sync` in your Google Drive
1. Login to the Google, and go to your drive.
2. Create the folder named `Sync`(you can name it to anything tbh)
3. Get in to the folder and get the folder id in the link.

### 3. Create config file
1. On your machine, go to `$HOME` and make a folder called `gdrive-sync` and also make a config file.
   - for Linux, `~/.config/gdrive-sync/config.json`
   - for Windows, `AppData/Roadming/gdrive-sync/config.json`
2. config.json looks like this:
```
{
    "PATH": "the folder id you got",
    "DRIVE": [
        "relative_path1",
        "relative_path2",
        ...
    ],
    "LOCAL": [
        "absolute_path1",
        "absolute_path2",
        ...
    ]
}
```
of course, replace the paths to the one you want to sync.

### How do I use it?
- use `gdrive-sync --pull` to pull the files from the drive
- use `gdrive-sync --push` to push the files to the drive
- it follows the rule(paths) you set in the `config.json`.
    - If you `pull`, file/folder on `relative_path1` will be downloaded on `absolute_path1`.
    - and for `relative_path2`, It will be downloaded on `absolute_path2`
    - If you `push`, file/folder on `absolute_path + relative_path` will be uploaded to `relative_path` in the drive.

- That's pretty much it. BE SURE TO MATCH THE INDEX between `DRIVE` and `LOCAL`.
- WARN: If you use it for the first time, upload the files you want to sync first on the drive.

# 日本語
個人的にパスごと同期できるものがあるといいな～と思って作りました。
