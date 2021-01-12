import urllib.request, json
import pandas as pd
import numpy as np
import pickle
import time

from src.get_beatmaps import *
from src.get_beatmaps import *


def check_for_update():
    saved_mappers = np.loadtxt("map_data/saved_mappers", delimiter="\n")
    saved_beatmaps = np.loadtxt("map_data/savedbeatmapsid", delimiter="\n")
    unsaved = np.loadtxt("map_data/unsaved_beatmaps", delimiter="\n").tolist()

    for id in saved_mappers:
        print("Adding", id)
        for map_id in get_user_beatmaps(id):
            if np.isin(map_id["id"], saved_beatmaps):
                pass
            else:
                unsaved.append(map_id["id"])
            time.sleep(0.1)
        print("saving unsaved")
        np.savetxt(
            "map_data/unsaved_beatmaps", np.unique(unsaved), delimiter="\n", fmt="%4d"
        )
    return unsaved


def check_for_unsaved_mapper():
    # https://osu.ppy.sh/home/quick-search?query=Donryu
    # with urllib.request.urlopen(
    #     f"https://osu.ppy.sh/users/{userid}/{api_address}offset={len(r_data)}&limit=51"
    # ) as url:
    #     r_data.extend(json.loads(url.read().decode()))
    unsaved_beatmaps = np.loadtxt("map_data/unsaved_beatmaps", delimiter="\n")
    unsaved_beatmapsets = np.unique(
        [find_beatmapsetid(mapid) for mapid in unsaved_beatmaps]
    )
    # unsaved_maps_mapper = np.unique(
    #     [find_mapper_id(mapid) for mapid in unsaved_beatmapsets.tolist()]
    # )


def find_beatmapsetid(id):
    data = []
    with urllib.request.urlopen(f"http://ripple.moe/api/get_beatmaps?b={id}") as url:
        data.extend(json.loads(url.read().decode()))
    time.sleep(0.0001)
    return int(data[0]["beatmapset_id"])


def find_mapper_id(id):
    # Need to find api
    map_data = []
    with urllib.request.urlopen(f"http://ripple.moe/api/get_beatmaps?s={id}") as url:
        map_data.extend(json.loads(url.read().decode()))
    query = urllib.parse.quote(map_data[1]["title"])
    maps_data = []
    with urllib.request.urlopen(
        f"https://osu.ppy.sh/beatmapsets/search?q={query}&s=ranked"
    ) as url:
        # print(json.loads(url.read().decode()))
        maps_data = json.loads(url.read().decode())
    map = []
    # for beatmap in maps_data['beatmapsets']:
    # print(beatmap['id'])
    return maps_data


if __name__ == "__main__":
    d = find_mapper_id(3)
