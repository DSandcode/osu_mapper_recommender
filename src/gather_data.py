import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import zipfile
import glob, os, shutil

from src.get_beatmaps import *


def gather_map_data(userid, log=False):

    try:
        os.mkdir("data")
    except:
        log_print(log, "data dir exists")

    try:
        os.mkdir(f"data/{userid}")
    except:
        log_print(log, f"{userid} already has a directory")

    user_json = get_user_beatmaps(userid)
    mapids = store_mapids(userid, user_json)

    log_print(log, "\nstarting \n")

    for beatmap_id in mapids:

        log_print(log, beatmap_id)

        try:
            os.mkdir(f"data/{userid}/{beatmap_id}")
        except:
            log_print(log, "Failed to make directories or directory exists")

        log_print(log, "Starting process")

        try:

            log_print(log, f"Downloading {beatmap_id}")
            # https://beatconnect.io/b/1030134
            #  f"https://bloodcat.com/osu/s/{beatmap_id}",
            download_url(
                f"https://beatconnect.io/b/{beatmap_id}",
                f"data/{userid}/{beatmap_id}/{beatmap_id}.osz",
            )

            log_print(
                log,
                f"Successfully downloaded from https://beatconnect.io/b/{beatmap_id}",
            )

        except:
            log_print(log, "failed to download")

        try:

            log_print(log, f"unzipping data/{userid}/{beatmap_id}/{beatmap_id}.osz")

            unzip(userid, beatmap_id)

            log_print(log, "Successfully unzipped")

        except:

            log_print(log, "Failed to unzip file")

        try:

            log_print(log, "Removing Extra")

            delete_extra(f"data/{userid}/{beatmap_id}/unzipped_osz/")

        except:
            log_print(log, "failed to remove files")

            # move_osu_files(
            #     f"data/{userid}/{beatmap_id}/unzipped_osz/",
            #     f"data/{userid}/{beatmap_id}/songs_osu_files/",
            # )

        log_print(log, "\n-----NEXT MAP-----\n")

    log_print(log, "Finished")


if __name__ == "__main__":
    userid = "13869387"
    # unzip("13869387", "1192164")
    gather_map_data(userid, log=True)
