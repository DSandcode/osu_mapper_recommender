import numpy as np
import urllib.request, json
import requests
import zipfile
import glob, os, shutil


def get_user_beatmaps(userid):
    r_data = []
    s_len = 1
    while s_len != len(r_data):
        s_len = len(r_data)
        with urllib.request.urlopen(
            f"https://osu.ppy.sh/users/{userid}/beatmapsets/ranked_and_approved?offset={len(r_data)}&limit=51"
        ) as url:
            r_data.extend(json.loads(url.read().decode()))
    return r_data


def store_mapids(userid, beatmaps_json):
    beatmapsids = np.array([i["id"] for i in beatmaps_json])
    np.save(f"data/{userid}/{userid}.npy", beatmapsids)
    return beatmapsids


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def unzip(userid, beatmap_id):
    print("a")
    filepath = f"data/{userid}/{beatmap_id}/{beatmap_id}.osz"
    print("b")
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall()


def move_osu_files(source_dir, dest_dir):
    files = glob.iglob(os.path.join(source_dir, "*.osu"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, dest_dir)


def delete_extra(source_dir):
    for subdir, dirs, files in os.walk(source_dir):
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".osu"):
                print("osu file", filepath)
            else:
                print("deleting", filepath)
                os.remove(filepath)


def log_print(log, message):
    if log:
        print(message)


def get_user_ranked_maps(userid, log=False):

    try:
        os.mkdir("data")
    except:
        if log:
            print("data dir exists")

    try:
        os.mkdir(f"data/{userid}")
    except:
        if log:
            print(f"{userid} already has a directory")

    user_json = get_user_beatmaps(userid)
    mapids = store_mapids(userid, user_json)

    if log:
        print("\nstarting \n")

    for beatmap_id in mapids:

        if log:
            print(beatmap_id)

        try:
            os.mkdir(f"data/{userid}/{beatmap_id}")
            os.mkdir(f"data/{userid}/{beatmap_id}/osz")
            os.mkdir(f"data/{userid}/{beatmap_id}/unzipped_osz")
            os.mkdir(f"data/{userid}/{beatmap_id}/songs_osu_files")
        except:
            if log:
                print("Failed to make directories or exists")

        if log:
            print("Starting process")

        try:

            if log:
                print("downloading", beatmap_id)

            download_url(
                f"https://bloodcat.com/osu/s/{beatmap_id}",
                f"data/{userid}/{beatmap_id}/osz/{beatmap_id}.osz",
            )

            if log:
                print(
                    f"Successfully downloaded from https://bloodcat.com/osu/s/{beatmap_id}"
                )
                print("unzipping", beatmap_id)

            unzip(
                f"data/{userid}/{beatmap_id}/osz/{beatmap_id}.osz",
                f"data/{userid}/{beatmap_id}/unzipped_osz/",
            )

            if log:
                print("unzipped files")
                print("removing extra")

            # delete_extra(f"data/{userid}/{beatmap_id}/unzipped_osz/")

            # move_osu_files(
            #     f"data/{userid}/{beatmap_id}/unzipped_osz/",
            #     f"data/{userid}/{beatmap_id}/songs_osu_files/",
            # )

        except:
            if log:
                print("\nfailed", beatmap_id)

        if log:
            print("\n-----NEXT MAP-----\n")


if __name__ == "__main__":
    userid = "13869387"
    # beatmaps_json = get_user_beatmaps(userid)

    # store_mapids(userid, beatmaps_json)

    # download_url("https://bloodcat.com/osu/s/1272018", "data/osz/1272018.osz")

    # https://bloodcat.com/osu/s/1272018

    # unzip("data/osz/1272018.osz", "data/unzipped_osz/1272018")

    # move_osu_files("data/unzipped_osz/1272018", "data/songs_osu_files/1272018")

    get_user_ranked_maps(userid, log=True)
