from datetime import datetime
import self_made_spotify
from hot_100 import TopSongs

machine_on = False

while not machine_on:
    date_back = input("What year would you like to travel back? YYYY-MM-DD\n")
    format_yyyymmdd = "%Y-%M-%d"
    try:
        date = datetime.strptime(date_back, format_yyyymmdd)
        machine_on = True

        top = TopSongs(date_back)
        song_list = top.song_list()

        spotify = self_made_spotify.MySpotify()
        spotify_song_lists = spotify.find_spotify_uri(song_list)

        new_playlist = spotify.add_user_playlist(date_back)
        new_playlist_id = new_playlist["id"]

        add_songs = spotify.add_songs_playlist(spotify_song_lists, new_playlist_id)
        print(add_songs)

    except ValueError:
        print("please input a right date time format")
        continue


