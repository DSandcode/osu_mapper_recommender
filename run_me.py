import numpy as np
import os

from src.gather_data import *

if __name__ == "__main__":
    try:
        os.mkdir("map_data")
    except:
        pass
    unsaved_mapper = np.loadtxt("map_data/unsaved_mappers", delimiter="\n")
    df, saved_mappers = gather_map_data(
        unsaved_mapper.astype(int), "map_data", log=True
    )
    all_mappers = np.unique(saved_mappers.astype(int) + unsaved_mapper.astype(int))
    np.savetxt(
        "map_data/all_mapperids", all_mappers.astype(int), delimiter="\n", fmt="%4d"
    )
    np.savetxt("map_data/unsaved_mappers", np.array([]), delimiter="\n", fmt="%4d")
