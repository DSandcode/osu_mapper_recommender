import os
from osufileparser import convert_osufile
import pickle


def scan_parse_save():

    try:
        os.mkdir("./data/pkl_files")
    except:
        pass

    for subdir, dirs, files in os.walk("."):
        for filename in files:
            filepath = subdir + os.sep + filename

            file_split = filepath.split("/")

            if filepath.endswith(".osu") and file_split[-2] == "songs_osu_files":
                print(filepath)
                parsed = convert_osufile(filepath)

                filename = (file_split[-1].replace(" ", "_")).replace(".osu", ".pkl")

                pickle.dump(parsed, open(f"./data/pkl_files/{filename}", "wb"))


if __name__ == "__main__":
    scan_parse_save()
