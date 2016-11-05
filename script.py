import requests
import json
from random import randint
from random import shuffle
import time

def getRandomSong(songList, songs):
    songIndex = randint(0,len(songList.json()["items"])-1)
    while (songIndex in songs):
        songIndex = randint(0,len(songList.json()["items"])-1)
    songs.append(songIndex)
    return songList.json()["items"][songIndex]

def getQuestion(playlistSongs):
    question = {}
    songs = []
    solutionSong = getRandomSong(playlistSongs, songs)

    question["previewURL"] = (solutionSong["track"]["preview_url"])
    question["solution"] = {}
    question["solution"]["name"] = (solutionSong["track"]["name"])
    question["solution"]["artists"] = []
    for artist in solutionSong["track"]["artists"]:
        question["solution"]["artists"].append((artist["name"]))

    question["songs"] = []
    question["songs"].append(solutionSong["track"]["name"])
    question["songs"].append(getRandomSong(playlistSongs, songs)["track"]["name"])
    question["songs"].append(getRandomSong(playlistSongs, songs)["track"]["name"])
    question["songs"].append(getRandomSong(playlistSongs, songs)["track"]["name"])

    shuffle(question["songs"])

    return question


#MAIN
def generate5Q(tokenSTR):
    print "Requesting featured playlist"
    featuredList = requests.get("https://api.spotify.com/v1/browse/featured-playlists",data={'country':'ES', 'limit':'1', 'locale':'es_ES'}, headers={"Authorization": "Bearer " + tokenSTR})
    print "Featured status: " + str(featuredList.status_code)



    i = 0
    for item in featuredList.json()["playlists"]["items"]:
        # print item["name"]
        i+=1
        # print "\n\n"

    randPlayList = randint(0,i-1)
    randomPlaylist = featuredList.json()["playlists"]["items"][randPlayList]
    print "Random playlist: " + randomPlaylist["name"]

    playlistSongs = requests.get("https://api.spotify.com/v1/users/" + randomPlaylist["owner"]["id"] + "/playlists/" + randomPlaylist["id"] + "/tracks", headers={"Authorization": "Bearer " + tokenSTR})

    print "Generating 5 questions"

    questions = []

    questions.append(getQuestion(playlistSongs))
    questions.append(getQuestion(playlistSongs))
    questions.append(getQuestion(playlistSongs))
    questions.append(getQuestion(playlistSongs))
    questions.append(getQuestion(playlistSongs))

    print "5 questions generated \n\n\n"

    return questions



#####################
root = "https://music-525ed.firebaseio.com/"
partidas = requests.get("https://music-525ed.firebaseio.com/games.json")

if partidas.text == u"null":
    numPartidas = 0
else:
    numPartidas = len(partidas.json())


tokenRequest = requests.post("https://accounts.spotify.com/api/token", data= {'grant_type':'client_credentials'}, auth=("b23a95bd67424734a26bfce011f3155d","5f577f73ff874eea9f7d5b856300888b"))
tokenJSON = tokenRequest.json()
tokenSTR = str(tokenJSON['access_token'])

print "Token code: " + str(tokenRequest.status_code)

while(numPartidas<50):
    game = {}
    game["questions"] = generate5Q(tokenSTR)
    game["status"] = "waiting2"
    request = requests.post(url=root+"games.json", data=json.dumps(game))

    numPartidas += 1