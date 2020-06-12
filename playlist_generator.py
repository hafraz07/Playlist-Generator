# import requests
#
# people = requests.get('http://api.open-notify.org/astros.json')
# people_json = people.json()
# print(people_json['people'][0]['name'])


import sys
import spotipy
import spotipy.util as util
from datetime import date

CLIENT_ID = '760e54f503eb4aaa88285c1605e6ca92'
CLIENT_SECRET = '24c97aeebcf24966a65962679ac27f3e'
REDIRECT_URI = 'http://localhost:8888/callback'


def create_playlist(res, sp_obj, user):
    # print(res['items'][0]['track']['id'])
    # return
    playlist_name = date.today().strftime('%m-%d')
    # Checks if playlist already exists
    playlists = sp_obj.user_playlists(user)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            print('Playlist', playlist_name, 'already exists')
            return
    # Adds top tracks to track_ids
    track_ids = []
    for i, item in enumerate(res['items']):
        track_ids.append(item['track']['id'])

    # Creates playlist with name MM-DD
    sp_obj.user_playlist_create(user, playlist_name)

    # Gets playlist id of created playlist
    playlists = sp_obj.user_playlists(user)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    # Adds 50 recently played tracks to the playlist
    sp_obj.user_playlist_add_tracks(user, playlist_id, track_ids)
    print('Successfully created playlist', playlist_name)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python playlist_generator.py [username]")
        sys.exit()

    scopes = 'playlist-modify-public user-top-read user-read-recently-played'

    token = util.prompt_for_user_token(username, scopes, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        # ranges = ['short_term', 'medium_term', 'long_term']
        # for range in ranges:
        #     print("range:", range)
        #     results = sp.current_user_top_tracks(time_range=range, limit=50)
        #     for i, item in enumerate(results['items']):
        #         print(i, item['name'], '//', item['artists'][0]['name'])
        #     print()
        results = sp.current_user_recently_played(limit=50)
        create_playlist(results, sp, username)
    else:
        print("Can't get token for", username)
