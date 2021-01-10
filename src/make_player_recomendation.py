from re import match
import numpy as np
import pandas as pd

from src.get_player_data import *
from src.map_recomendation import *
from src.log_print import *


def make_player_df(user_beatmapdids, map_df, mode, log=False):
    saved_id = find_saved_id(user_beatmapdids, map_df["beatmapid"], log=log)
    map_df_mode = map_df[map_df["mode"] == mode]
    return (
        map_df_mode[map_df_mode["beatmapid"].isin(saved_id)],
        saved_id,
    )


def find_saved_id(user_beatmapids, saved, log=False):
    isin = np.isin(user_beatmapids, saved)
    not_saved = np.loadtxt("map_data/unsaved_beatmaps", delimiter="\n")
    np.savetxt(
        "map_data/unsaved_beatmaps",
        np.unique((user_beatmapids[~isin]).tolist() + not_saved.tolist()),
        delimiter="\n",
        fmt="%4d",
    )
    return user_beatmapids[isin]


def make_player_recomendation(userid, mode="osu", log=False):
    log_print(log, f"Making recomendations for {userid} in mode: {mode}")
    user_beatmapids = get_user_beatmapids(userid, mode=mode, log=log)
    mode = (
        0
        if mode == "osu"
        else 1
        if mode == "taiko"
        else 2
        if mode == "catch"
        else 3
        if mode == "mania"
        else 0
    )
    map_data = pickle.load(open("map_data/map_data.pkl", "rb"))
    map_df = pd.DataFrame(map_data)
    player_df, player_maps = make_player_df(user_beatmapids, map_df, mode)
    map_df = map_df[map_df["mode"] == mode]
    map_df = map_df[~map_df["beatmapid"].isin(player_maps)]
    # print(player_df)
    map_rec = map_recomendation(player_df, map_df, log=log)

    map_rec_idx_rank = [i[1] for i in map_rec]
    # print(map_rec_idx)
    map_df["percent"] = np.array(map_rec_idx_rank)
    map_df = map_df.sort_values(by=["percent"], ascending=False)
    beatmapid_rec = map_df[["beatmapid", "beatmapsetid", "percent"]]
    # print(map_rec_idx)
    # 29822
    return (beatmapid_rec, map_rec)


if __name__ == "__main__":
    # userid = 13869387
    # p_df, player_rec = make_player_recomendation(userid, log=True)
    arc_id = 13869387
    hero_id = 12727076
    # 2625, 18292, 13543
    arc_df, arc_rec = make_player_recomendation(arc_id, log=True)
    # 2626, 18286, 13539
    hero_df, hero_rec = make_player_recomendation(hero_id, log=True)

