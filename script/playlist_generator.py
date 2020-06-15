import sys
import spotipy
from datetime import date

CLIENT_ID = '760e54f503eb4aaa88285c1605e6ca92'
CLIENT_SECRET = '24c97aeebcf24966a65962679ac27f3e'
REDIRECT_URI = 'http://localhost:8888/callback'

def create_playlist(res, sp_obj):
    playlist_name = date.today().strftime('%m-%d')
    # Checks if playlist already exists
    playlists = sp_obj.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            print('Playlist', playlist_name, 'already exists')
            return
    # Adds top tracks to track_ids
    track_ids = []
    for item in res['items']:
        track_ids.append(item['track']['id'])

    # Creates playlist with name MM-DD
    user = sp_obj.me()['id']
    sp_obj.user_playlist_create(user, playlist_name)

    # Gets playlist id of created playlist
    playlists = sp_obj.current_user_playlists()
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
        print("Usage: python3 playlist_generator.py <username>")
        sys.exit()

    scopes = 'playlist-modify-public user-top-read user-read-recently-played'

    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI, scope=scopes, username=username)
    sp = spotipy.Spotify(client_credentials_manager=auth_manager)
        # ranges = ['short_term', 'medium_term', 'long_term']
        # for range in ranges:
        #     print("range:", range)
        #     results = sp.current_user_top_tracks(time_range=range, limit=50)
        #     for i, item in enumerate(results['items']):
        #         print(i, item['name'], '//', item['artists'][0]['name'])
        #     print()
    results = sp.current_user_recently_played(limit=50)
    create_playlist(results, sp)
