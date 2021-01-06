from matplotlib.pyplot import polar
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
import numpy as np
from matplotlib import cm
import matplotlib as mpl


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    v = mx * 100
    return h, s, v


def con_rgb_hsv_list(rgb_list):
    h, s, v = rgb_to_hsv(rgb_list[0], rgb_list[1], rgb_list[2])
    return [h, s, v]


def create_color_df():

    r_dict = {
        "h": [],
        "s": [],
        "v": [],
        "rgb": [],
        "mapper": [],
    }

    for subdir, dirs, files in os.walk("."):

        for filename in files:

            filepath = subdir + os.sep + filename

            if filepath.endswith(".pkl"):

                pickle_file = pickle.load(open(filepath, "rb"))

                try:

                    for col in pickle_file["colours"]:
                        hslist = con_rgb_hsv_list(pickle_file["colours"][col])
                        r_dict["h"].append(hslist[0])
                        r_dict["s"].append(hslist[1])
                        r_dict["v"].append(hslist[2])
                        r_dict["rgb"].append(pickle_file["colours"][col])
                        if pickle_file["metadata"]["creator"] == "Sotarks":
                            r_dict["mapper"].append(pickle_file["metadata"]["creator"])
                        else:
                            r_dict["mapper"].append("Andrea")

                except:
                    pass

    return pd.DataFrame(r_dict)


def dict_len(dict):
    for aba in dict:
        print(len(dict[aba]))


def split_mapper_color(df):
    r_dict = {k: [] for k in df.mapper.unique()}
    for mapper in r_dict:
        r_dict[mapper] = df[df["mapper"] == mapper]
    return r_dict


if __name__ == "__main__":
    a = create_color_df()
    a_split = split_mapper_color(a)
    # print(a)

    # fig, ax = plt.subplots(nrows=2, polar=True)

    for i, key in enumerate(a_split):
        # Hue theat, sat raid
        # Compute areas and colors

        r = 2 * (a_split[key]["s"] / 100)
        theta = a_split[key]["h"] * (np.pi / 180)

        colors = theta
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="polar")
        plt.title(key)
        c = ax.scatter(theta, r, c=theta, cmap="hsv", alpha=0.3)
        plt.savefig(f"images/colorgraph/{key}.png")

    plt.show()

    #  fig = plt.figure()

    #     display_axes = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection="polar")
    #     display_axes._direction = 2 * np.pi

    #     norm = mpl.colors.Normalize(0.0, 2 * np.pi)

    #     quant_steps = 2056
    #     cb = mpl.colorbar.ColorbarBase(
    #         display_axes,
    #         cmap=cm.get_cmap("hsv", quant_steps),
    #         norm=norm,
    #         orientation="horizontal",
    #     )
    #     display_axes.plot(0, 0)

    #     # cb.outline.set_visible(False)
    #     # display_axes.set_axis_off()
