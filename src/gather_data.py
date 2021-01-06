import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import zipfile
import glob, os, shutil

from src.get_beatmaps import *
from src.osufileparser import *
from src.parse_save import *
from src.osu_df_row import *


def gather_map_data(userids, save_path, log=False):
    r_dict = make_r_df()
    saved_mapper = []
    try:
        os.mkdir("data")
    except:
        log_print(log, "data dir exists")

    for userid in userids:
        saved_mapper.append(userid)
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

            map_dir = f"./data/{userid}/{beatmap_id}"

            log_print(log, f"Starting process in {map_dir}")

            try:

                log_print(log, f"Downloading {beatmap_id}")
                # f"https://beatconnect.io/b/{beatmap_id}"
                # f"https://bloodcat.com/osu/s/{beatmap_id}",
                download_url(
                    f"https://beatconnect.io/b/{beatmap_id}",
                    f"{map_dir}/{beatmap_id}.osz",
                )

                log_print(
                    log,
                    f"Successfully downloaded from https://beatconnect.io/b/{beatmap_id}",
                )

            except:
                log_print(log, "failed to download")

            try:
                log_print(log, f"unzipping {map_dir}/{beatmap_id}.osz")

                unzip(userid, beatmap_id)

                log_print(log, "Successfully unzipped")
            except:
                log_print(log, "Failed to unzip file")

            try:
                log_print(log, "Removing Extra")

                delete_extra(f"{map_dir}/", ".osu")

                log_print(log, "Successfully Removed Files")
            except:
                log_print(log, "failed to remove files")

            try:
                log_print(log, "Parsing files")

                scan_parse_save(map_dir, log=log)

                log_print(log, "Finished parsing\n")
            except:
                log_print(log, "Failed to parse")
            try:
                log_print(log, "Removing Extra")

                delete_extra(f"{map_dir}/", ".pkl")

                log_print(log, "Successfully Removed Files")
            except:
                log_print(log, "failed to remove files")

            try:
                log_print(log, "Making Rows\n")

                add_rows(map_dir, r_dict, log)

                log_print(log, "Added rows")

            except:
                log_print(log, "failed to make rows")

            log_print(log, "\n-----NEXT MAP-----\n")
            try:

                log_print(log, "Removing files")

                delete_extra(f"{map_dir}/", ".osu")
                os.rmdir(map_dir)

                log_print(log, "removed files")

            except:
                log_print(log, "Failed to remove files")

        try:
            mapper_dir = f"./data/{userid}/"
            log_print(log, "Removing files")

            delete_extra(f"{mapper_dir}/", ".osu")
            os.rmdir(mapper_dir)

            log_print(log, "Removed files")

        except:
            log_print(log, "Failed to remove files")

        log_print(log, "\n\n-- NEXT MAPPER--\n\n")

    log_print(log, "Finished")
    saved_mapper = np.unique(saved_mapper)
    np.savetxt(f"{save_path}/saved_mappers", saved_mapper, delimiter="\n", fmt="%4d")
    r_df = pd.DataFrame(r_dict)
    r_df.to_csv(f"{save_path}/map_data.csv", index=False)
    return r_df,saved_mapper


if __name__ == "__main__":
    userids = [13869387, 12337329, 16771869]
    # unzip("13869387", "1192164")
    aaa = gather_map_data(userids, "data", log=True)
