from subprocess import CREATE_NO_WINDOW, PIPE
import os
import subprocess
import progress

def remove_silence(song, start_threshold, end_threshold):
    # p = subprocess.Popen(['ffmpeg', '-i', song, '-af',
    # '\"silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse\"',
    # song])

    # This feature is not supported yet
    return

def concat(songs, length):
    f = open("./concat.txt", "w", encoding='utf-8')
    for song in songs:
        f.write('file \''
        + song.replace("\'", "\'\\\'\'") # Sanitizes the ' character
        + '\'\n')
    f.close()

    p = subprocess.Popen(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', "concat.txt", 'big_audio.mp3'],
                         stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                         creationflags=CREATE_NO_WINDOW,
                         universal_newlines=True)
    
    progress.printProgressBar(0, length, prefix = 'Progress:', suffix = 'Concatenating MP3s', length = 50)
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            progress.printProgressBar(seconds_time, length, prefix = 'Progress:', suffix = 'Concatenating MP3s', length = 50)
    print("\n")


def normalize_audio(audio_bitrate, length):
    p = subprocess.Popen(['ffmpeg', '-i', 'big_audio.mp3', '-b:a', str(audio_bitrate), '-filter_complex', 'loudnorm',
                        'normalized_audio.mp3'], stdin=PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                        creationflags=CREATE_NO_WINDOW, universal_newlines=True)

    progress.printProgressBar(0, length, prefix = 'Progress:', suffix = 'Normalizing Audio', length = 50)
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            progress.printProgressBar(seconds_time, length, prefix = 'Progress:', suffix = 'Normalizing Audio', length = 50)
    print("\n")

    os.remove('big_audio.mp3')
    os.rename('normalized_audio.mp3', 'big_audio.mp3')

def generate_mp4(thumbnail, title, audio_bitrate, video_bitrate, length, fc):
    p = subprocess.Popen(
        ['ffmpeg', '-y', '-loop', '1', '-framerate', '5', '-i', thumbnail, '-i', 'big_audio.mp3', '-c:v', 'libx264',
         '-tune', 'stillimage', '-c:a', 'aac', '-b:v', str(video_bitrate), '-b:a', str(audio_bitrate), '-pix_fmt',
         'yuv420p', '-vf', 'crop=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', '-shortest', '-fflags',
         '+shortest', '-max_interleave_delta', '100M', title + '.mp4'], stdout=PIPE, stderr=subprocess.STDOUT, creationflags=CREATE_NO_WINDOW, universal_newlines=True)
    
    progress.printProgressBar(0, length, prefix = 'Progress:', suffix = 'Generating Output', length = 50)
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            progress.printProgressBar(seconds_time, length, prefix = 'Progress:', suffix = 'Generating Output', length = 50)
    
    # Collect file
    fc.append(title + '.mp4')
