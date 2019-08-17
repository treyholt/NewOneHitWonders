# __author__ = "Diego Baugh + Trey Holterman"
# __version__ = "0.1.0"
# __license__ = "MIT"
# test username (pass as the only argument): 1252330876

import sys
import spotipy
import spotipy.util as util
import functools 
import time
from concurrent.futures import ThreadPoolExecutor

def printFoundSongs(allTargetSongs):
    print("The Songs for you are: ")
    result = sorted(allTargetSongs, key=lambda trackTuple: trackTuple[1])
    for songTuple in result:
        print("Song name is: " + songTuple[0]['name'] + " by " + songTuple[0]['artists'][0]['name'] + " With a score of: " + str(songTuple[1]))

def calculateScore(topTrack, targetRatio, artist):
    inverseArtistPop = 100 - artist['popularity'] # Want to reward for low popularity
    inverseSongPop = 100 - topTrack['popularity']
    finalScore = (targetRatio * targetRatio * inverseArtistPop * inverseSongPop) / 1000
    return finalScore

def findTopSongAndAvg(sp, artist, allTargetSongs):
    allTopTracks = sp.artist_top_tracks(artist['id'] , country='US')['tracks']
    if len(allTopTracks) <= 3: return
    singleTopTrack = allTopTracks[0] # Grabs top Track
    restOfTopTracks = allTopTracks[1:] # Grabs all top tracks other than the first
    if len(restOfTopTracks) <= 1: return
    averagePopOfRest = sum(int(track['popularity']) for track in restOfTopTracks) / len(restOfTopTracks) 
    if averagePopOfRest <= 0: return
    targetRatio = singleTopTrack['popularity'] / averagePopOfRest
    if targetRatio >= 1.3 and singleTopTrack['popularity'] >= 50:
        score = calculateScore(singleTopTrack, targetRatio, artist)
        print("Adding in tuple")
        allTargetSongs.append(tuple((singleTopTrack, score)))
  

#   Takes sp for auth, the current artist being looked at, the current threshold for popularity
# and how far removed (linkLevel) the current artist is from the original favorite artists. 
# Ultimately the goal of this function is to take someone's top 10 favorite artists and return 
# underground artists with on especially popular song relative to the average of their top 5 songs. 
def findUnpopularRelated(sp, artist, popThresh, linkLevel, allTargetSongs):
    relatedArtists = sp.artist_related_artists(artist['id'])
    if len(relatedArtists) < 1: return
    if len(relatedArtists['artists']) < 1: return
    artist = relatedArtists['artists'][0]
    for artist in relatedArtists['artists']:
        if artist['popularity'] < popThresh and popThresh >= 30: 
            findTopSongAndAvg(sp, artist, allTargetSongs)    
            findUnpopularRelated(sp, artist, popThresh - 10, linkLevel + 1, allTargetSongs)


def promptForArtists(sp):
    searchedArtists = []
    nextArtist = None
    while True:
        nextArtist = input("Please enter an artist's name: ")
        if nextArtist == "": return searchedArtists
        result = sp.search(nextArtist, limit=10, offset=0, type='artist', market=None)['artists']['items'][0]
        searchedArtists.append(result)


if __name__ == '__main__':
    username = "1260138450"
    token = util.prompt_for_user_token(username,scope = 'user-top-read',client_id='a5c2c927ceb242b2936166108355ac0e',client_secret='09557185c27b44a48e920986b097df4c',redirect_uri='http://localhost/')
    executor = ThreadPoolExecutor(max_workers=8)
    if token:
        sp = spotipy.Spotify(auth=token)
        allTargetSongs = []
        startingArtists = promptForArtists(sp)
        #grabs the user's top 5 favorite recent artists. Medium or long term goes back further
        # No longer using this, instead using the artists prompted by user. 
        # topArtists = sp.current_user_top_artists(5, 0, 'short_term')
        for artist in startingArtists:
            print("Onto artist: " + artist['name'])
            task = findUnpopularRelated(sp, artist, 60, 1, allTargetSongs)
        printFoundSongs(allTargetSongs)

    # else:
    #     print("Token has been invalidated")

