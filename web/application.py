import spotipy
from datetime import date
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:5000/callback'
scopes = 'playlist-modify-public user-top-read user-read-recently-played'
USERNAME = 'x'

app.secret_key = CLIENT_SECRET

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/middle")
def middle():
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI, scope=scopes, username=USERNAME)
    sp_obj = spotipy.Spotify(client_credentials_manager=auth_manager)
    user = sp_obj.me()['display_name']
    return render_template("middle.html", username=user)

@app.route("/create", methods=["POST", "GET"])
def create_playlist():
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI, scope=scopes, username=USERNAME)
    sp_obj = spotipy.Spotify(client_credentials_manager=auth_manager)
    res = sp_obj.current_user_recently_played(limit=50)

    playlist_name = date.today().strftime('%m-%d')
    # Checks if playlist already exists
    playlists = sp_obj.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            print('Playlist', playlist_name, 'already exists')
            return render_template("failure.html", playlist_name=playlist_name)
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
    return render_template("success.html")

@app.route("/auth", methods=["POST"])
def auth():
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI, scope=scopes)
    auth_url = auth_manager.get_authorize_url()

    return redirect(auth_url)

@app.route("/callback")
def success():
    auth_manager = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI, scope=scopes, username=USERNAME)
    session.clear()
    code = request.args.get('code')
    token_info = auth_manager.get_access_token(code)
    session["token_info"] = token_info
    return redirect("middle")
