from os.path import isfile, join
from pydub import AudioSegment, effects
import os
import shutil
import sys
str(sys.argv)

arg1 = sys.argv[1]

def SingleFolderMerge(dir):
    foldername = dir
    foldername = os.path.normpath(foldername)
    onlyfiles = [f for f in os.listdir(foldername) if isfile(join(foldername, f))]
    mergeable = []
    wiper = os.listdir(foldername)
    print(onlyfiles)
    for file in onlyfiles:
        if file.endswith("-L.wav"):
            mergeable.append(file.replace("-L.wav", ""))

    try:
        os.mkdir(foldername + "/left-right", 0o666)
    except:
        print("Dir already made :3")


    for item in wiper:
        if item.endswith(".asd"):
            os.remove(os.path.join(foldername, item))


    for file in mergeable:
        try:
            left = foldername + r"/" + file + "-L.wav"
            right = foldername + r"/" + file + "-R.wav"
            left_channel = AudioSegment.from_wav(left)
            right_channel = AudioSegment.from_wav(right)

            left_channel = effects.normalize(left_channel)
            right_channel = effects.normalize(right_channel)

            stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)

            stereo_sound.export(out_f=(foldername + r"/" + file + ".wav"), format="wav")

            shutil.move(src=left, dst=foldername + r"/left-right/" + file + "-L.wav")
            shutil.move(src=right, dst=foldername + r"/left-right/" + file + "-R.wav")
        except:
            print("Well fuck")

dirs = next(os.walk(arg1))[1]
print(dirs)
for d in dirs:
    find = next(os.walk(arg1 + "/" + d))[1]
    print(find)
    for sd in find:
        SingleFolderMerge(arg1 + "/" + d + "/" + sd)






