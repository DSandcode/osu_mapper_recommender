import os
from src.osufileparser import convert_osufile
import pickle


def log_print(log, message):
    if log:
        print(message)


def scan_parse_save(directory=".", log=False):

    log_print(log, f"\nParsing Directory {directory}")

    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename

            file_split = filepath.split("/")

            if filepath.endswith(".osu"):

                log_print(log, f"Parsing {filepath}")

                parsed = convert_osufile(filepath)

                filename = (file_split[-1].replace(" ", "_")).replace(".osu", ".pkl")

                log_print(log, f"Saving to {directory}/{filename}")

                pickle.dump(parsed, open(f"{directory}/{filename}", "wb"))


if __name__ == "__main__":
    scan_parse_save("./data/13869387/1192164", log=True)
