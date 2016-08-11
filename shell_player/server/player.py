import pafy

class Player:
    def __init__(self):
        self.vlc = None
        self.playlists = []
        self.playing = None

    # populate playlists
    def populate(self, in_file):
        #self.playlist = Playlist
        pass
    
    # update the current playing track
    def update(self):
        pass

    def play(self):
        print('playing')

    def stop(self):
        print('stop')

    def pause(self):
        print('pause')

    def play_rel(self, offset):
        print("playing {}".format(offset))

    def play_abs(self, idx):
        print("playing {}".format(idx))


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


class Playlist:
    def __init__(self, url = None):
        self.tracks = []
        if url:
            playlist = pafy.get_playlist2(url)
            self.title = playlist.title
            self.author = playlist.author
            for track in playlist:
                self.tracks.append(Track(track.watchv_url, track))
        else:
            self.title = 'Custom'
            self.author = 'me'

    def __getitem__(self, index):
        return self.tracks[index]

    def append(self, url):
        self.tracks.append(Track.watchv_url)


