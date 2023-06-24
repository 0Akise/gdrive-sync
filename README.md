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

### 4. Use it
- use `gdrive-sync --pull` to pull the files from the drive
- use `gdrive-sync --push` to push the files to the drive
- it follows the rule(paths) you set in the `config.json`.
    - If you `pull`, file/folder on `relative_path1` will be downloaded on `absolute_path1`.
    - and for `relative_path2`, It will be downloaded on `absolute_path2`
    - If you `push`, file/folder on `absolute_path + relative_path` will be uploaded to `relative_path` in the drive.

- That's pretty much it. BE SURE TO MATCH THE INDEX between `DRIVE` and `LOCAL`.
- WARN: If you use it for the first time, upload the files you want to sync first on the drive.

# 日本語
個人的にパスごと同期できるものがあるといいな～と思って作りました。同期すると指定されたパスごとにダウンロードできます。

### 使い方

まずは、３つ必要です：
1. Google Cloud API 認証ファイル
2. ドライブ上のフォルダ
3. `gdrive-sync`用のconfigフォルダ

### 1. Get Google Cloud API Credentials
1. GoogleにログインしてAPIポータルに接続します: https://console.cloud.google.com/apis/credentials
2. APIの`credentials.json`ファイルが必要なのでこの記事に沿ってダウンロードします: https://developers.google.com/drive/api/quickstart/python
3. ダウンロードした `credentials.json` をconfigフォルダー `~/.config/gdrive-sync/ に入れます。
   - Windowsの場合、configは `AppData/Roadming/gdrive-sync/` に作ります。
  
### 2. Google Drive上にフォルダー作成
1. Googleにログインしてドライブに行きます。
2. 名前は何でもいいんでフォルダを作りましょう。
3. 作ったフォルダーに入るとリンクにフォルダーのidが見れます。そのidは `config.json` に使うのでコピーしておきましょう。

### 3. Create config file
1. パソコンに config フォルダーと config.json ファイルを作ります。
   - Linux `~/.config/gdrive-sync/config.json`
   - Windows `AppData/Roadming/gdrive-sync/config.json`
2. `config.json`ってこんな感じです：
```
{
    "PATH": "フォルダid",
    "DRIVE": [
        "ドライブ内相対パス1",
        "ドライブ内相対パス2",
        ...
    ],
    "LOCAL": [
        "パソコン上絶対パス1",
        "パソコン上絶対パス2",
        ...
    ]
}
```
もちろんパスは同期したいパスに変えてください。ただし、相対パスと絶対パスを間違えないように。

### 4. 使う
- `gdrive-sync --pull` でドライブからダウンロードします。
- `gdrive-sync --push` でドライブにアップロードします。
- `config.json` に書いたパスに従ってダウンロード・アップロードされます。
    - `pull` すると、ドライブ上の `ドライブ内相対パス1` にあるファイル/フォルダーがパソコンの絶対パス `パソコン上絶対パス1` にダウンロードされます。
    - `ドライブ内相対パス2` は `パソコン上絶対パス2` にダウンロードされます。
    - `push` すると、`パソコン上絶対パス + ファイル名` がドライブ上の `ドライブ内相対パス` にアップロードされます。

- それが全部です。パスの順番は関係あるので `DRIVE` と `LOCAL` に書くパスの順番間違わないように注意しましょう。
- 初めて使うときはバグります。まずは同期したいファイルたちをドライブにアップロードしてから使ってください。
