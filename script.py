# __author__ = "Diego Baugh + Trey Holterman"
# __version__ = "0.1.0"
# __license__ = "MIT"
# test username (pass as the only argument): 1252330876

import sys
import spotipy
import spotipy.util as util


def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s", (i, track['artists'][0]['name'],
            track['name']))


if __name__ == '__main__':
    username = "1252330876"
    token = util.prompt_for_user_token(username,scope = 'user-library-modify',client_id='a5c2c927ceb242b2936166108355ac0e',client_secret='09557185c27b44a48e920986b097df4c',redirect_uri='http://localhost/')

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Token has been invalidated")

