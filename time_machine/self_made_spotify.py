import spotipy
from spotipy.oauth2 import SpotifyOAuth
from unidecode import unidecode

client_id = "fbf056376e3b4d108ec882cf8dac839b"
client_secret = "80b6ee19161746f484584bbb8379857b"
redirect = "http://example.com"
scope = "playlist-modify-private"


class MySpotify:

    def __init__(self):
        self.auth = SpotifyOAuth(client_id=client_id,
                                 client_secret=client_secret,
                                 redirect_uri=redirect,
                                 scope=scope
                                 )
        self.sp = spotipy.Spotify(auth_manager=self.auth)
        self.user_id = self.find_user_id()

    def find_user_id(self):
        return self.sp.current_user()["id"]

    def find_spotify_uri(self, search_song_list: list) -> list:
        """
        looks through the spotipy, Spotify class

        :return: the list of song uris
        """
        spotify_song_list = []
        for song in search_song_list:
            top_100_song = song["song"]
            top_100_artist = song["artist"]
            search_query = f"{top_100_song} {top_100_artist}"
            search_results = self.sp.search(search_query, type="track")
            # pprint.pprint(search_results)
            try:
                first_result = search_results["tracks"]["items"][0]
            except IndexError:
                continue
            else:
                spotify_song_uri = first_result["uri"]
                spotify_album_name = first_result["album"]["name"]
                spotify_artist_name = unidecode(first_result["artists"][0]["name"].lower())
                spotify_song_name = unidecode(first_result["name"].lower())
                if spotify_song_name not in top_100_song.lower() and spotify_artist_name not in top_100_artist.lower():
                    print(f"'{top_100_song}' by '{top_100_artist}' is not available on spotify")
                    print(f"{spotify_song_name}, {spotify_artist_name} are the results")
                    continue
                spotify_song_list.append(spotify_song_uri)

        return spotify_song_list

    def add_user_playlist(self, year_of_playlist: str) -> dict:
        """ adds a new playlist to the user

        :param year_of_playlist: - name of the playlist to be added
        :return: the content of the creation in form of a dictionary
        """
        user = self.user_id
        playlist_name = f"{year_of_playlist} Billboard 100"
        public_status = False
        description = "Getting back to the good old days"

        creation = self.sp.user_playlist_create(user=user,
                                                name=playlist_name,
                                                public=public_status,
                                                collaborative=False,
                                                description=description
                                                )

        return creation

    def add_songs_playlist(self, songs: list, playlist_id: str) -> dict:
        """
        adds songs to a playlist on spotify

        :param songs: the list of songs to be added to the playlist
        :param playlist_id: the id of the playlist to which your adding the songs
        :return: a dictionary with an item of snapshot id upon being successful
        """
        id_of_playlist = playlist_id
        song_list = songs

        added = self.sp.playlist_add_items(id_of_playlist, song_list)
        return added


