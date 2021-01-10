import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity

from src.log_print import *


def log_print(log, message):
    if log:
        print(message)


def map_recomendation(player_data, map_df, log=False):
    log_print(log, "Looking at player data")

    return [
        [int(i), num]
        for i, num in enumerate(
            (
                cosine_similarity(
                    (
                        (
                            player_data.drop(
                                ["beatmapid", "beatmapsetid", "mapper"], axis=1,
                            )
                        )
                        .mean()
                        .to_frame()
                        .T
                    ),
                    (map_df.copy()).drop(
                        ["beatmapid", "beatmapsetid", "mapper"], axis=1
                    ),
                ).tolist()
            )[0]
        )
    ]


if __name__ == "__main__":
    map_data = pickle.load(open("map_data/map_data.pkl", "rb"))
    map_df = pd.DataFrame(map_data)
    map_df_sample = map_df.sample(n=10)
    recommended = map_recomendation(map_df_sample, map_df)
    # cosine_in = (
    #     (map_df_sample.drop(["beatmapid", "beatmapsetid", "mapper"], axis=1))
    #     .mean()
    #     .to_frame()
    #     .T
    # )

    # """beatmapid, beatmapsetid, mapper"""
    # cosine_df = map_df.copy()
    # cosine_df = cosine_df.drop(["beatmapid", "beatmapsetid", "mapper"], axis=1)
    # cosine_sim = cosine_similarity(cosine_in, cosine_df)

    # 2703904
    # map_index = map_data_df[map_data_df["beatmapid"] == 2703904].index
    # similar_maps = np.insert(
    #     cosine_sim[map_index], list(range(cosine_sim[map_index].size))
    # )
    # similar_maps = np.array(
    #     [(int(i), num) for i, num in enumerate((cosine_sim.tolist())[0])]
    # )
    # sorted_similar_maps = sorted(similar_maps, key=lambda x: x[1], reverse=True)
