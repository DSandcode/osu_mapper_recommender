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
    userids = [int(i) for i in userids] if type(userids) == list else [userids]
    saved_mappers, all_mappers, saved_beatmapid, unsaved_mappers = (
        [],
        [],
        [],
        [],
    )
    try:
        saved_mappers = np.loadtxt("map_data/saved_mappers", delimiter="\n")
        saved_mappers = (
            [int(i) for i in saved_mappers.tolist()]
            if len(saved_mappers) > 1
            else [int(saved_mappers[0])]
        )
    except:
        pass
    try:
        all_mappers = np.loadtxt("map_data/all_mapperids", delimiter="\n").tolist()
        all_mappers = (
            [int(i) for i in all_mappers.tolist()]
            if len(all_mappers) > 1
            else [int(all_mappers[0])]
        )
    except:
        pass
    try:
        saved_beatmapid = np.loadtxt("map_data/savedbeatmapsid", delimiter="\n")
        saved_beatmapid = (
            [int(i) for i in saved_beatmapid.tolist()]
            if len(saved_beatmapid) > 1
            else [int(saved_beatmapid[0])]
        )
    except:
        pass
    try:
        unsaved_mappers = np.loadtxt("map_data/unsaved_mappers", delimiter="\n")
        unsaved_mappers = (
            [int(i) for i in unsaved_mappers.tolist()]
            if len(unsaved_mappers) > 1
            else [int(unsaved_mappers[0])]
        )
    except:
        unsaved_mappers = userids
    try:
        os.mkdir("data")
    except:
        log_print(log, "data dir exists")

    all_mappers = all_mappers + userids
    np.savetxt(
        "map_data/all_mapperids",
        np.unique(all_mappers).astype(int),
        delimiter="\n",
        fmt="%4d",
    )

    for userid in userids:
        try:
            os.mkdir(f"data/{userid}")
        except:
            log_print(log, f"{userid} already has a directory")

        user_json = get_user_beatmaps(userid)
        mapids = store_mapids(userid, user_json)

        log_print(log, f"\nstarting {userid} \n")

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

            try:

                log_print(log, "Removing files")

                delete_extra(f"{map_dir}/", ".osu")
                os.rmdir(map_dir)

                log_print(log, "removed files")

            except:
                log_print(log, "Failed to remove files")

            saved_beatmapid.append(beatmap_id)
            np.savetxt(
                f"{save_path}/savedbeatmapsid",
                np.unique(saved_beatmapid),
                delimiter="\n",
                fmt="%4d",
            )

            log_print(log, "\n-----NEXT MAP-----\n")
        try:
            mapper_dir = f"./data/{userid}/"
            log_print(log, "Removing files")

            delete_extra(f"{mapper_dir}/", ".a")
            os.rmdir(mapper_dir)

            log_print(log, "Removed files")

        except:
            log_print(log, "Failed to remove files")

        unsaved_mappers.remove(userid)
        np.savetxt(
            f"{save_path}/unsaved_mappers",
            np.unique(unsaved_mappers),
            delimiter="\n",
            fmt="%4d",
        )
        saved_mappers.append(userid)
        np.savetxt(
            f"{save_path}/saved_mappers",
            np.unique(saved_mappers),
            delimiter="\n",
            fmt="%4d",
        )

        pickle.dump(r_dict, open(f"{save_path}/map_data.pkl", "wb"))

        log_print(log, "\n\n-- NEXT MAPPER--\n\n")

    log_print(log, "Finished")
    r_df = pd.DataFrame(r_dict)
    r_df.to_csv(f"{save_path}/map_data.csv", index=False)
    return r_df, saved_mappers


if __name__ == "__main__":
    userids = [13869387, 12337329, 16771869]
    # unzip("13869387", "1192164")
    aaa = gather_map_data(userids, "data", log=True)
