import os
from PIL import Image
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

class Tracklist:
    def __init__(self, songs) -> None:
        time_in_sec = 0
        songs_starts = {}
        tracklist = {}     

        for song in songs:
            songs_starts[song] = time_in_sec
            time_in_sec += MP3(song).info.length

        if time_in_sec >= 0:
            for song in songs_starts:
                seconds = str(int(songs_starts[song] % 60))
                if (len(seconds) < 2):
                    seconds = "0" + seconds
                tracklist[song] = seconds
        
        if time_in_sec >= 60:
            for song in songs_starts:
                minutes = str(int(songs_starts[song] / 60) % 60) + ":"
                if (len(minutes) < 3):
                    minutes = "0" + minutes
                tracklist[song] = minutes + tracklist[song]

        if time_in_sec >= 3600:
            for song in songs_starts:
                tracklist[song] = str(int((songs_starts[song] / 60) / 60) % 12) + ":" + tracklist[song]
        
        self.time_in_sec = time_in_sec
        self.songs_starts = songs_starts
        self.tracklist = tracklist
    
    def export_tracklist(self, songs, fc):
        # Tracklist
        tracklist_txt = open("./tracklist.txt" , "w", encoding='utf-8')
        for song in self.tracklist:
            audio = ID3(song)
            album = "Undefined"
            if "TALB" in audio.keys():
                album = audio["TALB"].text[0]

            title = "Undefined"
            if "TIT2" in audio.keys(): 
                title = audio["TIT2"].text[0]

            tracklist_txt.write(self.tracklist[song] + " - " + title + " [" + album + "]\n")
        
        # Collect tracklist file
        fc["tracklist"] = "./tracklist.txt"

        # Captions
        captions_txt = open("./captions.txt", "w", encoding="utf-8")
        track_num = 1
        for i in range(len(songs) - 1):
            captions_txt.write(str(track_num) + "\n")

            start_stamp = self.tracklist[songs[i]]
            end_stamp = self.tracklist[songs[i + 1]]

            captions_txt.write(start_stamp + ",000 --> " + end_stamp + ",000\n")

            audio = ID3(songs[i])
            album = "Undefined"
            if "TALB" in audio.keys():
                album = audio["TALB"].text[0]

            title = "Undefined"
            if "TIT2" in audio.keys(): 
                title = audio["TIT2"].text[0]

            captions_txt.write(title + " [" + album + "]\n\n")

            track_num += 1
        captions_txt.write(str(track_num) + "\n")
        captions_txt.write(self.tracklist[songs[-1]] + ",000 --> 11:59:59,000\n")
        audio = ID3(songs[-1])
        album = "Undefined"
        if "TALB" in audio.keys():
            album = audio["TALB"].text[0]

        title = "Undefined"
        if "TIT2" in audio.keys(): 
            title = audio["TIT2"].text[0]

        captions_txt.write(title + " [" + album + "]\n")

        # Collect captions file
        fc["captions"] = "./captions.txt"

def cleanup():
    if (os.path.exists('./big_audio.mp3')):
        os.remove('./big_audio.mp3')
    if (os.path.exists('./concat.txt')):
        os.remove('./concat.txt')
    if (os.path.exists('./tracklist')):
        for file in os.listdir('./tracklist'):
            os.remove(os.path.join('./tracklist', file))

def stretch_image(path):
    with Image.open(path) as im:
        print(im.width)
        print(im.height)
        size = (1280,720)
        if im.width > im.height:
            width = 80 * round(im.width/80)
            size = (width, int(45*(width/80)))
        elif im.height > im.width:
            height = 45 * round(im.width/45)
            size = (int(80*(height/45)), height)
        else:
            width = 80 * round(im.width/80)
            size = (width, int(45*(width/80)))
        im = im.resize(size)
        im.save("thumbnail.png", "PNG")
        return "thumbnail.png"