import pafy
import yaml
import collections
from shell_player.server import vlc

class Player:
    def __init__(self, in_file = None):
        self.instance = vlc.Instance()

        self.list_player = self.instance.media_list_player_new()
        self.player = self.instance.media_player_new()
        self.set_volume(100)
        self.list_player.set_media_player(self.player)
        self.playlists = {}
        if in_file:
            self.populate(in_file)
            self.playing = list(self.playlists.values())[0]
            self.use_playlist(self.playing.name)
            self.update()

    # populate playlists
    def populate(self, in_file):
        with open(in_file, 'r') as f:
            content = yaml.load(f)
            for name, urls in content.items():
                self.playlists[name] = Playlist(name, urls)
    
    # update the current playing track
    def update(self):
        if self.player.get_media():
            self.playing.playing_track = self.playing[self.player.get_media().get_mrl()]
            self.playing.next_track()

    # set actual playlist
    def use_playlist(self, name):
        urls = self.playlists[name].get_tracks_url()
        media_list = self.instance.media_list_new(urls)
        self.list_player.set_media_list(media_list)
        self.playlists[name].playing_track = self.playlists[name].tracks[urls[0]]
        self.playing.next = self.playing.playing_track

    def line_playing_info(self):
        line_info = ''
        if self.playing.playing_track:
            line_info += self.playing.playing_track.title
            line_info += "  ||  Next:"
            next_tr =  self.playing.next_track()
            if next_tr:
                line_info += self.playing.next_track().title
            else:
                line_info += "END"
            line_info += "  ||  "
            line_info += str(self.volume)
        return line_info

    def get_info(self):
        info = {}
        info['playlist'] = self.playing.get_info()
        info['track'] = self.playing.playing_track.get_info()
        info['player'] = "Volume: {}\n".format(self.volume)
        return info

    def play(self):
        self.list_player.play()
        self.update()
    
    def stop(self):
        self.list_player.stop()
        self.update()

    def pause(self):
        self.list_player.pause()
        self.update()

    def play_next(self):
        self.list_player.next()
        self.update()

    def play_prev(self):
        self.list_player.previous()
        self.update()

    def play_index(self, idx):
        self.list_player.play_item_at_index(idx)
        self.update()

    def set_volume(self, volume):
        self.volume = volume
        self.player.audio_set_volume(self.volume)

    def set_playlist(self, name):
        self.list_player.stop()
        self.player.set_media(None)
        self.playing = self.playlists[name]
        self.use_playlist(name)
        self.update()

class Track:
    def __init__(self, url, video = None):
        if video is None:
            video = pafy.new(url)
        self.title = video.title
        self.duration = video.duration
        self.author = video.author
        self.rating = video.rating
        self.audiostream = video.getbestaudio()

    def get_info(self):
        info = "Title: {}\n".format(self.title)
        info += "Author: {}\n".format(self.author)
        info += "Duration: {}\n".format(self.duration)
        info += "Rating: {}\n".format(self.rating)
        return info


class Playlist:
    def __init__(self, name, url):
        self.tracks = collections.OrderedDict()
        self.playing_track = None
        self.next = None
        self.title = None
        if isinstance(url, str):
            playlist = pafy.get_playlist2(url)
            self.name = name
            self.title = playlist.title
            self.author = playlist.author
            for track in playlist:
                new_track = Track(track.watchv_url, track)
                self[new_track.audiostream.url] = new_track
        else:
            self.name = name
            self.author = 'me'
            for track_url in url:
                new_track = Track(track_url)
                self[new_track.audiostream.url] = new_track
        self.size = len(self.tracks)

    def __getitem__(self, index):
        return self.tracks[index]

    def __setitem__(self, index, item):
        self.tracks[index] = item

    def append(self, url):
        self.tracks.append(Track.watchv_url)

    def get_tracks_url(self):
        return [track.audiostream.url for url, track in self.tracks.items()]
    
    def get_info(self):
        info = "Playlist : {}\n".format(self.name)
        if self.title is not None:
            info += "Title : {}\n".format(self.title)
        info += "Playlist author : {}\n".format(self.author)
        info += "Tracks : {}\n".format(self.size)
        return info

    def next_track(self):
        if self.playing_track is None:
            self.next = None
        else:
            index = list(self.tracks.keys()).index(self.playing_track.audiostream.url)
            track_list = list(self.tracks.items())
            if len(track_list) > index + 1:
                self.next = list(self.tracks.items())[index + 1][1]
            else:
                self.next = None
        return self.next

