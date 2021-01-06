import numpy as np


def sort_unique(file_name):
    og_file = np.loadtxt(file_name, delimiter="\n")
    sorted_unique = np.unique(og_file)
    np.savetxt(file_name, sorted_unique, delimiter="\n", fmt="%4d")


if __name__ == "main":
    file_name = "data/mapperid_l1"
