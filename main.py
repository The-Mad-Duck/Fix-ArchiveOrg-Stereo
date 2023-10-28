from os.path import isfile, join
from pydub import AudioSegment, effects
import os
import shutil
import sys
str(sys.argv)


# Merges all the LR files in the specified directory
def SingleFolderMerge(directory):
    folderName = os.path.normpath(directory)
    onlyFiles = [f for f in os.listdir(folderName) if isfile(join(folderName, f))]
    mergeable = []
    print(onlyFiles)
    for file in onlyFiles:
        if file.endswith("-L.wav"):
            mergeable.append(file.replace("-L.wav", ""))
        elif file.endswith(".asd") or file.endswith(".s3p"):
            os.remove(os.path.join(folderName, file))

    # Make a folder to dump the LR audio when done
    try:
        os.mkdir(folderName + "/left-right", 0o666)
    except:
        print("Dir already made :3")


    for file in mergeable:
        try:
            # Get the left and right filenames
            left = folderName + r"/" + file + "-L.wav"
            right = folderName + r"/" + file + "-R.wav"

            # Create AudioSegment instances of each and normalize them
            left_channel = AudioSegment.from_wav(left)
            right_channel = AudioSegment.from_wav(right)
            left_channel = effects.normalize(left_channel)
            right_channel = effects.normalize(right_channel)

            # Dump to stereo audio
            stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)

            # Export
            stereo_sound.export(out_f=(folderName + r"/" + file + ".wav"), format="wav")

            # Move LR to folder
            shutil.move(src=left, dst=folderName + r"/left-right/" + file + "-L.wav")
            shutil.move(src=right, dst=folderName + r"/left-right/" + file + "-R.wav")
        except:
            print("Failure to merge files under name" + file + "-?.wav")


# Clean empty folders when done
def RemoveEmptyFolders(path_abs):
    walk = list(os.walk(path_abs))
    for path, _, _ in walk[::-1]:
        if len(os.listdir(path)) == 0:
            os.removedirs(os.path.normpath(path))


if __name__ == "__main__":
    arg1 = sys.argv[1]
    dirs = next(os.walk(arg1))[1]
    print(dirs)
    for d in dirs:
        find = next(os.walk(arg1 + "/" + d))[1]
        print(find)
        for sd in find:
            SingleFolderMerge(arg1 + "/" + d + "/" + sd)
    RemoveEmptyFolders(arg1)






