# shell_player

Simple online music player in your terminal.  
It only works with zsh and youtube musics at the moment.
shell_player is a music player in command line, the player is available from all your open terminals.

## Install

install vlc  
`pip install -r requirements.txt`  
vlc may bug with youtube videos, some tricks have to be done with youtube.lua ... google it.  
put the content of config/zshrc at the end of your zshrc  

## Usage

First, you have to launch the player with the start `command`.
Then you can use commands from other terminals.  
You'll need a music file, like example.yml. You have to create playlist in the file then put each music url OR only put a youtube playlist url.

### Commands
Commands are like `./shell_player <COMMAND>`  
commands:  
* `start <MUSIC_FILE>` to start the player
* `play`
* `pause`
* `next`
* `prev`
* `goto <NB>` go to music
* `stop`
* `info`
* `vol <VOLUME>` 0 to 100
* `playlists` list all playlists
* `set_playlist <PLAYLIST_NAME>` use this playlist
* `link` link your terminal with the player
* `close` close the player
