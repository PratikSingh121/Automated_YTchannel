def upload(book_name):
    import datetime
    import os
    from Google import Create_Service
    from googleapiclient.http import MediaFileUpload

    CLIENT_SECRET_FILE = os.path.join(os.path.dirname(os.getcwd()),'yt_api','client_secrets.json')
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.force-ssl']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    #upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

    exp_path = os.path.join(os.path.dirname(os.getcwd()), 'exported', book_name)
    with open(os.path.join(exp_path,'oneSentScript.txt')) as f:
        oneSent = f.read()
    with open(os.path.join(exp_path,'tags.txt'), 'r') as f:
        tags = f.read().split('\n')
    playlists = tags
    tags.extend([
        'book', 'Self help', book_name, 'intellegence', 'upgrade', 'career', 'bussiness',
         'startup','progess', 'writer', 'summary'
    ])

    description = f'''{oneSent} \n\n For more such amazing books, do subscribe to the channel and dont forget to Leave a like. Also suggest me a book you want me to make summary of in the comment and i would try to upload it.\n\n
    Music Credits:-
    ___________________________________
    Music from Free To Use Music
    Track: Kyoto by Pratzapp & Another Kid
    https://youtu.be/rlxvg-Sy-sY
    ___________________________________'''
# #UPLOADING VIDEO
    request_body = {
        'snippet': {
            'categoryI': 27,
            'title': f'{book_name.title()} Summary',
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'public',
           # 'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': True
    }

    video = os.path.join(os.path.dirname(os.getcwd()),'exported', book_name, f'{book_name.title()}.mp4')
    mediaFile = MediaFileUpload(video)

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    videoID = response_upload.get('id')

    print('\nVIDEO UPLOADED...\n')
    # service.thumbnails().set(
    #    videoId=response_upload.get('id'),
    #    media_body=MediaFileUpload(os.path.dirname(os.getcwd()),'exported', book_name, 'vid_image.jpg')
    # ).execute()

    '''
    #CREATING PLAYLIST
    with open(os.path.join(os.path.dirname(os.getcwd()), 'books_list', 'categories.txt'), 'r') as f:
        playlists = f.read().split('\n')
    for playlist in playlists[17:]:
        request = service.playlists().insert(
            part="snippet,status",
            body={
              "snippet": {
                "title": f'{playlist.title()}',
                "description": f"Book Summaries Category - {playlist.title()}",
                "tags": [
                  playlist, 'summary', '5mins', 'books', 'knowledge', 'money', 'wealth', 'progess','development'
                ],
                "defaultLanguage": "en"
              },
              "status": {
                "privacyStatus": "public"
              }
            }
        )
        response = request.execute()
    '''

#Checking for existing playlist
    request = service.playlists().list(
        part="snippet",
        mine=True
    )
    response = request.execute()
    playlist_dict = {}
    for item in response['items']:
        playlist_dict[item['snippet']['title']] = item['id']

    print(playlist_dict)
#ADDING VIDEO TO PLAYLIST
    for playlist in playlists:
        if playlist.title() in playlist_dict.keys():
            print(playlist)
            playlistID = playlist_dict[playlist.title()]

            add_video_request=service.playlistItems().insert(
                part="snippet",
                body={
                    'snippet': {
                      'playlistId': playlistID, 
                      'resourceId': {
                              'kind': 'youtube#video',
                          'videoId': videoID
                        }
                    }
            }
             ).execute()