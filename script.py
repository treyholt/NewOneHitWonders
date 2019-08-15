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
    print("WE Have a token: ", token)

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
        print("Can't get token for", username)

# #!/usr/bin/env python3
# """
# Code to find artists and songs that greatly outperform the average
# content produced by said artist. 
# """
# __author__ = "Diego Baugh + Trey Holterman"
# __version__ = "0.1.0"
# __license__ = "MIT"

# import spotipy
# export SPOTIPY_CLIENT_ID = 'a5c2c927ceb242b2936166108355ac0e'
# export SPOTIPY_CLIENT_SECRET = '09557185c27b44a48e920986b097df4c'
# export SPOTIPY_REDIRECT_URI = 'http://localhost/'


# def setupAuth():
#     lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
#     spotify = spotipy.Spotify()
#     results = spotify.artist_top_tracks(lz_uri)
#     for track in results['tracks'][:10]:
#         print("track    : " + track['name'])
#         print("audio    : " + track['preview_url'])
#         print("cover art: " + track['album']['images'][0]['url'])
#         print()

# def main():
#     """ Main entry point of the app """
#     print("in main")
#    # setupAuth()


# if __name__ == "__main__":
#     main()