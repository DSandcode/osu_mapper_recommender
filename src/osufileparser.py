import re
from itertools import zip_longest
import pandas as pd


def convert_osufile(file):
    # Reads the osu file and splits it into sections
    osufile_txt = open(file, "r")
    read_osu = osufile_txt.read()
    read_osu = read_osu.replace("\n\n\n", "\n\n")
    sections = read_osu[:-1].split("\n\n")

    # Dictionary to be returned
    r_dict = {}

    # Keys for the lists
    time_keys = [
        "time",
        "beatlength",
        "meter",
        "sampleset",
        "sampleindex",
        "volume",
        "uninherited",
        "effects",
    ]
    hit_keys = ["x", "y", "time", "type", "hitsound", "hitsample", "objectparams"]
    col_lst = ["general", "editor", "metadata", "difficulty", "colours"]
    dataframe_lst = ["timingpoints", "hitobjects"]

    # Loops throught the sections
    for sect in sections:

        # Makes the section sections and the keys to loop through
        sect_lst = sect.split("\n")
        key = ((sect_lst[0].replace("[", "")).replace("]", "")).lower()

        # Creating the keys for the section and defining the keys variables
        r_dict[key] = (
            {}
            if key in col_lst
            else []
            if key == "events"
            else {}
            if key in dataframe_lst
            else None
        )

        if key == "timingpoints":
            for timei in time_keys:
                r_dict[key][timei] = []

        if key == "hitobjects":
            for hiti in hit_keys:
                r_dict[key][hiti] = []

        # Loops through the section sections
        for i, line in enumerate(sect_lst):

            # Skips the key
            if i == 0:
                continue

            # This is for the sections that are colon sep list
            if key in col_lst:

                # Splits the list and lowercase the keys
                split = line.split(":")
                s_key = (split[0].strip()).lower()

                # Some of the variables are stored differently these if are for those
                if s_key == "bookmarks":
                    r_dict[key][s_key] = [int(x) for x in (split[1].strip()).split(",")]

                elif key == "colours":
                    r_dict[key][s_key] = [int(x) for x in (split[1].strip()).split(",")]

                else:
                    try:
                        r_dict[key][s_key] = int(split[1].strip())
                    except:
                        try:
                            r_dict[key][s_key] = float(split[1].strip())
                        except:
                            r_dict[key][s_key] = split[1].strip()

            # I didn't feel like doing the storyboard since it's not that important for what I am doing maybe later /shrug
            if key == "events":
                r_dict[key].append(line)

            # For the timingpoint section
            if key == "timingpoints":

                # loops through the info and yeah
                for t_info, t_key in zip_longest(line.split(","), time_keys):

                    # Again different parts are stored differently
                    if t_info == None:
                        r_dict[key][t_key].append(0)
                    elif t_key in [
                        "time",
                        "meter",
                        "sampleset",
                        "sampleindex",
                        "volume",
                        "uninherited",
                        "effects",
                    ]:
                        if t_info.find(".") != -1:
                            r_dict[key][t_key].append(int(t_info[: t_info.find(".")]))
                        else:
                            r_dict[key][t_key].append(int(t_info))
                    else:
                        r_dict[key][t_key].append(float(t_info))

            # For hitobjects oh boi this section
            if key == "hitobjects":

                # Splits the line
                h_split = line.split(",")

                # Moves parts to make it easier to go through
                if bool(re.match(r"\d:\d:\d:\d:", h_split[-1])) or bool(
                    re.match(r"\d:\d:\d", h_split[-1])
                ):
                    h_split.insert(5, h_split[-1])
                    h_split.pop()
                else:
                    h_split.insert(5, "0:0:0:0:")

                # Set's the type
                type = 0

                # Loops through the info
                for h_ind, (h_info, h_key) in enumerate(zip_longest(h_split, hit_keys)):

                    # These where the easy ones cause they are just stored as what they are
                    if h_key in ["x", "y", "time", "type", "hitsound"]:
                        r_dict[key][h_key].append(int(h_info))
                        if h_key == "type":
                            type = int(h_info)

                    # This was the pain the sliders anyways objectparams
                    if h_key == "objectparams":

                        # Circle no new combo
                        if type == 1:
                            r_dict[key][h_key].append(
                                {
                                    "objectype": "circle",
                                    "newcombo": False,
                                    "params": None,
                                }
                            )
                        # Spinners weeeee
                        elif type in [12, 8]:
                            r_dict[key][h_key].append(
                                {
                                    "objectype": "spinner",
                                    "newcombo": True,
                                    "params": {"endtime": int(h_split[-1])},
                                }
                            )

                        # Slider no new combo
                        elif type == 2:

                            s_dict = {
                                "curvetype": "",
                                "curvepoints": [],
                                "slides": int(h_split[h_ind + 1]),
                                "length": float(h_split[h_ind + 1]),
                                "edgesounds": [],
                                "edgesets": [],
                            }

                            if re.match(r"\d\|\d\|\d", h_split[-2]):
                                for es_sp in h_split[-2].split("|"):
                                    s_dict["edgesounds"].append(int(es_sp))

                            if re.match(r"\d:\d\|\d:\d\|\d:\d", h_split[-1]):
                                for es_sp in h_split[-1].split("|"):
                                    s_dict["curvepoints"].append(
                                        [int(es_sp_i) for es_sp_i in es_sp.split(":")]
                                    )

                            for si, s_l in enumerate(h_info.split("|")):
                                if si == 0:
                                    s_dict["curvetype"] = s_l
                                else:
                                    s_dict["curvepoints"].append(
                                        [int(s_l_i) for s_l_i in s_l.split(":")]
                                    )

                            r_dict[key][h_key].append(
                                {
                                    "objectype": "slider",
                                    "newcombo": True,
                                    "params": s_dict,
                                }
                            )

                        # New combo slider
                        # elif type == 6 and type == 102:
                        else:
                            # New combo circle
                            if h_info == None:
                                r_dict[key][h_key].append(
                                    {
                                        "objectype": "circle",
                                        "newcombo": True,
                                        "params": None,
                                    }
                                )
                            else:
                                # New combo slider
                                # print(type, h_info, h_split)
                                s_dict = {
                                    "curvetype": "",
                                    "curvepoints": [],
                                    "slides": int(h_split[h_ind + 1]),
                                    "length": float(h_split[h_ind + 1]),
                                    "edgesounds": [],
                                    "edgesets": [],
                                }

                                if re.match(r"\d\|\d\|\d", h_split[-2]):
                                    for es_sp in h_split[-2].split("|"):
                                        s_dict["edgesounds"].append(int(es_sp))

                                if re.match(r"\d:\d\|\d:\d\|\d:\d", h_split[-1]):
                                    for es_sp in h_split[-1].split("|"):
                                        s_dict["curvepoints"].append(
                                            [
                                                int(es_sp_i)
                                                for es_sp_i in es_sp.split(":")
                                            ]
                                        )

                                for si, s_l in enumerate(h_info.split("|")):
                                    if si == 0:
                                        s_dict["curvetype"] = s_l
                                    else:
                                        s_dict["curvepoints"].append(
                                            [int(s_l_i) for s_l_i in s_l.split(":")]
                                        )

                                r_dict[key][h_key].append(
                                    {
                                        "objectype": "slider",
                                        "newcombo": True,
                                        "params": s_dict,
                                    }
                                )

                    # Hit samples ye
                    if h_key == "hitsample":

                        samp_key = [
                            "normalset",
                            "additionset",
                            "index",
                            "volume",
                            "filename",
                        ]

                        hit_dict = dict.fromkeys(samp_key, 0)

                        for samp, sa_key in zip(h_info.split(":"), samp_key):
                            if sa_key == "filename":
                                hit_dict[sa_key] = samp
                            else:
                                hit_dict[sa_key] = int(samp)
                        r_dict[key][h_key].append(hit_dict)

    # for aaaaa in r_dict["hitobjects"]:
    #     print(len(r_dict["hitobjects"][aaaaa]))
    # print("\n")

    # for aaaaa in r_dict["timingpoints"]:
    #     print(len(r_dict["timingpoints"][aaaaa]))

    # Converts what I want to a DataFrame
    for df_key in dataframe_lst:
        r_dict[df_key] = pd.DataFrame(r_dict[df_key])

    # Finally, returns the dictionary
    return r_dict


if __name__ == "__main__":
    # file = "./data/33599/22809/songs_osu_files/Yoko Shimomura - Sinister Sundown (osuplayer111) [xxheroxx's Hard].osu"
    file = "data/33599/918518/songs_osu_files/96neko - Ai Kotoba III (Andrea) [Daisuki!].osu"
    # file = "data/songs_osu_files/test/test.osu"
    osu_data = convert_osufile(file)
    # print(osu_data)
