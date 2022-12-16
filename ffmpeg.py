from subprocess import CREATE_NO_WINDOW, PIPE
import os
import subprocess
import progress, sys, codecs

def remove_silence(song, start_threshold, end_threshold):
    # p = subprocess.Popen(['ffmpeg', '-i', song, '-af',
    # '\"silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse\"',
    # song])

    # This feature is not supported yet
    return

def concat_merge(songs, length):
    merge_songs = songs.copy()
    song_idx = 0

    prog_bar = progress.ProgressBar(0, length, prefix = 'Progress:', suffix = 'Concatenating Output', length = 50)
    while (len(merge_songs) > 1):
        merge_length = len(merge_songs)
        length_down = int(merge_length/2)
        for _ in range(length_down):
            # Get two files
            song1 = merge_songs.pop(0)
            song2 = merge_songs.pop(0)

            # Merge two files
            song_idx += 1
            merge_songs.append(concat_files(song1, song2, "./tracklist/mrg" + str(song_idx) + os.path.splitext(song1)[1], prog_bar))

            # Cleanup two unusable files
            if (os.path.exists(song1)):
                os.remove(song1)
            if (os.path.exists(song2)):
                os.remove(song2)
        if merge_length % 2 == 1:  # If extra element, add to back
            merge_songs.append(merge_songs.pop(0))
    prog_bar.finish()
    
    return merge_songs.pop()

def convert_mp3s(songs, thumbnail, a_bitrate, v_bitrate, length):
    # Create mp4 files
    mp4s = []
    song_idx = 0

    prog_bar = progress.ProgressBar(0, length, prefix = 'Progress:', suffix = 'Generating Output', length = 50)
    for song in songs:
        output = "./tracklist/vid" + str(song_idx) + '.mp4'
        # Make video
        song_idx += 1
        mp4s.append(mp4_from_song(input=song, output=output, thumbnail=thumbnail, audio_bitrate=a_bitrate, video_bitrate=v_bitrate, bar=prog_bar))
    prog_bar.finish()
    return mp4s

def mp4_from_song(input, output, thumbnail, audio_bitrate, video_bitrate, bar=None):
    print("Creating mp4 from file:", input)
    p = subprocess.Popen(
        ['ffmpeg', '-y', '-loop', '1', '-framerate', '5', '-i', thumbnail, '-i', input, '-c:v', 'libx264',
         '-tune', 'stillimage', '-ar', '44100', '-c:a', 'aac', '-b:v', str(video_bitrate), '-b:a', str(audio_bitrate), '-pix_fmt',
         'yuv420p', '-vf', 'crop=trunc(iw/2)*2:trunc(ih/2)*2', '-movflags', '+faststart', '-shortest', '-fflags',
         '+shortest', '-max_interleave_delta', '100M', output], stdout=PIPE, stderr=subprocess.STDOUT, creationflags=CREATE_NO_WINDOW, universal_newlines=True, encoding='utf-8')

    last_time = 0
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')

            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            if bar: bar.increment(seconds_time - last_time)
            last_time = seconds_time
    
    return output

def concat_files(in1, in2, output, bar=None):
    # print("Merging two files:", in1, in2, "into", output)
    f = open("./concat.txt", "w", encoding='utf-8')
    for file in [in1, in2]:
        f.write('file \''
        + file.replace("\'", "\'\\\'\'") # Sanitizes the ' character
        + '\'\n')
    f.close()

    p = subprocess.Popen(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', "concat.txt", "-c", "copy", output],
                         stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                         creationflags=CREATE_NO_WINDOW,
                         universal_newlines=True, encoding='utf-8')

    last_time = 0
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')

            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            if bar: bar.increment(seconds_time - last_time)
            last_time = seconds_time

    return output

def normalize_audio(input, output, length):
    p = subprocess.Popen(['ffmpeg', '-i', input, '-filter:a', 'loudnorm', output],
                        stdin=PIPE, stderr=subprocess.STDOUT, stdout=PIPE,
                        creationflags=CREATE_NO_WINDOW, universal_newlines=True, encoding='utf-8')

    # print("Length:", length)
    prog_bar = progress.ProgressBar(0, length, prefix = 'Progress:', suffix = 'Normalizing Audio', length = 50)
    last_time = 0
    for line in p.stdout:
        string_line = str(line)
        if "time=" in string_line:
            time = string_line[string_line.index("time=") + 6:string_line.index("bitrate=") - 1]
            h, m, s = time.split(':')
            s, ms = s.split('.')
            seconds_time = int(h) * 3600 + int(m) * 60 + int(s) + float(ms) / 100
            prog_bar.increment(seconds_time - last_time)
            last_time = seconds_time
    prog_bar.finish()
    return output