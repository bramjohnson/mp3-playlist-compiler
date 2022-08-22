# Playlist Compiler
Compiles a directory of .mp3 or .m3u/.m3u8 playlists of any file format to a single .mp3/.mp4

# Instructions
Download the [latest release](https://github.com/bramjohnson/playlist-compiler/releases) of the program.

Use the terminal to run commands through the program:

compile [-h] [-s START END] [-n] [-f] [-d] [-t THUMBNAIL] -i INPUT [-o OUTPUT]

## Commands
-h/--help - Receive information about commands.

-i/--input <directory/path-to-playlist> (required) - Either the path of the src folder or an m3u file.

-o/--output <directory> - The destination folder (same as exe if unspecified)

-t/--thumbnail <path-to-thumbnail> - If specified, the program will create a .mp4 with the image as the backgorund. If unspecified, the program will create a .mp3

-d/--data - Create a file with a list of all tracks and formatted captions.

-n/--normalize - Normalize the audio of all songs in the playlist.

-f/--fits - Stretches the thumbnail to 1920x1080 (if specified).

-s/--silence <start-threshold> <end-threshold> - Removes silence from the start and end of each song (threshold in seconds).

# Requirements
All python requirements are included in "requirements.txt"

The following programs are also required:
- FFmpeg