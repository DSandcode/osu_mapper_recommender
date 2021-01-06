import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
import numpy as np
import math

# Colour analysis

# New combo length
# Slider length
# Slider velocity
# Slider type
# slider points
# Distance of slider points
# Combo number
## Difficulty
# Timing points (count, length, everything after sample set?)
# Kiai count and length ratio?
# Ratio objects
# Distance
# Hit sounds

# Mapper


def osu_df_basic():

    r_dict = {
        "newcombolen": [],
        "sliderlen": [],
        "sliderslides": [],
        "slidervelocity": [],
        "sliderperfectratio": [],
        "sliderlinearratio": [],
        "slidercatmullratio": [],
        "sliderbezierratio": [],
        "sliderpointamount": [],
        "sliderpointdistance": [],
        "combocount": [],
        "timecount": [],
        "timelen": [],
        "sampleset": [],
        "samplesetdefaultratio": [],
        "samplesetnormalratio": [],
        "samplesetsoftratio": [],
        "samplesetdrumratio": [],
        "sampleindex": [],
        "volume": [],
        "uninherited": [],
        "effects": [],
        "kiaicount": [],
        "kiailength": [],
        "kiairatio": [],
        "circleratio": [],
        "sliderratio": [],
        "spinnerratio": [],
        "distance": [],
        "hitsounds": [],
        "mapper": [],
    }
    for subdir, dirs, files in os.walk("."):
        filenum = 0
        for filename in files:
            filepath = subdir + os.sep + filename

            if filepath.endswith(".pkl"):
                filenum += 1
                print(filenum, filepath)
                # try:
                pickle_file = pickle.load(open(filepath, "rb"))

                df_row = make_df_row(pickle_file)

                r_dict["newcombolen"].append(df_row["newcombolen"])
                r_dict["sliderlen"].append(df_row["sliderlen"])
                r_dict["sliderslides"].append(df_row["sliderslides"])
                r_dict["slidervelocity"].append(df_row["slidervelocity"])

                r_dict["sliderperfectratio"].append(df_row["sliderperfectratio"])
                r_dict["sliderlinearratio"].append(df_row["sliderlinearratio"])
                r_dict["slidercatmullratio"].append(df_row["slidercatmullratio"])
                r_dict["sliderbezierratio"].append(df_row["sliderbezierratio"])

                r_dict["sliderpointamount"].append(df_row["sliderpointamount"])
                r_dict["sliderpointdistance"].append(df_row["sliderpointdistance"])
                r_dict["combocount"].append(df_row["combocount"])
                r_dict["timecount"].append(df_row["timecount"])
                r_dict["timelen"].append(df_row["timelen"])
                r_dict["sampleset"].append(df_row["sampleset"])

                r_dict["samplesetdefaultratio"].append(df_row["samplesetdefaultratio"])
                r_dict["samplesetnormalratio"].append(df_row["samplesetnormalratio"])
                r_dict["samplesetsoftratio"].append(df_row["samplesetsoftratio"])
                r_dict["samplesetdrumratio"].append(df_row["samplesetdrumratio"])

                r_dict["sampleindex"].append(df_row["sampleindex"])
                r_dict["volume"].append(df_row["volume"])
                r_dict["uninherited"].append(df_row["uninherited"])
                r_dict["effects"].append(df_row["effects"])

                r_dict["kiaicount"].append(df_row["kiaicount"])
                r_dict["kiailength"].append(df_row["kiailength"])

                r_dict["kiairatio"].append(df_row["kiairatio"])

                r_dict["circleratio"].append(df_row["circleratio"])
                r_dict["sliderratio"].append(df_row["sliderratio"])
                r_dict["spinnerratio"].append(df_row["spinnerratio"])

                r_dict["distance"].append(df_row["distance"])
                r_dict["hitsounds"].append(df_row["hitsounds"])
                if pickle_file["metadata"]["creator"] == "Sotarks":
                    r_dict["mapper"].append("Sotarks")
                else:
                    r_dict["mapper"].append("Andrea")

                # except:
                #     pass
    return pd.DataFrame(r_dict)


def make_df_row(osu_dict):

    r_row = {
        "newcombolen": 0,
        "sliderlen": 0,
        "sliderslides": 0,
        "slidervelocity": 0,
        "sliderperfectratio": 0,
        "sliderlinearratio": 0,
        "slidercatmullratio": 0,
        "sliderbezierratio": 0,
        "sliderpointamount": 0,
        "sliderpointdistance": 0,
        "combocount": 0,
        "timecount": 0,
        "timelen": 0,
        "sampleset": 0,
        "samplesetdefaultratio": 0,
        "samplesetnormalratio": 0,
        "samplesetsoftratio": 0,
        "samplesetdrumratio": 0,
        "sampleindex": 0,
        "volume": 0,
        "uninherited": 0,
        "effects": 0,
        "kiaicount": 0,
        "kiailength": 0,
        "kiairatio": 0,
        "circleratio": 0,
        "sliderratio": 0,
        "spinnerratio": 0,
        "distance": 0,
        "hitsounds": 0,
        "mapper": 0,
    }

    timing_df = osu_dict["timingpoints"]

    (
        slidervelocity,
        timecount,
        timelen,
        sampleset,
        samplesetdefaultratio,
        samplesetnormalratio,
        samplesetsoftratio,
        samplesetdrumratio,
        sampleindex,
        volume,
        uninherited,
        effects,
        kiaicount,
        kiailength,
        kiairatio,
        notkiai,
    ) = ([], 0, [], [], [], [], [], [], [], [], [], [], 0, [], [], [])

    pretime = 0
    currentlykiai = False
    prekiai_time = 0
    for index, row in timing_df.iterrows():

        timecount += 1

        timelen.append(row["time"] - pretime)
        pretime = row["time"]

        if row["uninherited"] == 0:
            slidervelocity.append(100 / (-row["beatlength"]))

        sampleset.append(row["sampleset"])
        if row["sampleset"] == 0:
            samplesetdefaultratio.append(row["sampleset"])
        elif row["sampleset"] == 1:
            samplesetnormalratio.append(row["sampleset"])
        elif row["sampleset"] == 2:
            samplesetsoftratio.append(row["sampleset"])
        elif row["sampleset"] == 3:
            samplesetdrumratio.append(row["sampleset"])

        sampleindex.append(row["sampleindex"])

        volume.append(row["volume"])

        uninherited.append(row["uninherited"])

        effects.append(row["effects"])

        if currentlykiai:
            kiailength.append(row["time"] - prekiai_time)

        if row["effects"] == 1:
            currentlykiai = True
            kiaicount += 1
            kiairatio.append(1)
        else:
            currentlykiai = False
            notkiai.append(1)

    hit_df = osu_dict["hitobjects"]

    (
        newcombolen,
        sliderlen,
        sliderslides,
        sliderperfectratio,
        sliderlinearratio,
        slidercatmullratio,
        sliderbezierratio,
        sliderpointamount,
        sliderpointdistance,
        combocount,
        circleratio,
        sliderratio,
        spinnerratio,
        distance,
        hitsounds,
    ) = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        0,
        [],
        [],
        [],
        [],
        [],
    )

    prenewcomboindex = 0

    for index, row in hit_df.iterrows():

        object_params = row["objectparams"]
        params = object_params["params"]
        object_type = object_params["objectype"]

        if object_params["newcombo"]:
            newcombolen.append(index - prenewcomboindex)
            prenewcomboindex = index
            combocount += 1

        if object_type == "slider":
            sliderlen.append(params["length"])
            sliderslides.append(params["slides"])

            if params["curvetype"] == "P":
                sliderperfectratio.append(1)
            elif params["curvetype"] == "L":
                sliderlinearratio.append(1)
            elif params["curvetype"] == "C":
                slidercatmullratio.append(1)
            elif params["curvetype"] == "B":
                sliderbezierratio.append(1)

            sliderpointamount.append(len(params["curvepoints"]))

            s_distance = []
            for point_i, point in enumerate(params["curvepoints"]):
                if point_i == 0:
                    s_distance.append(
                        calc_distance(row["x"], row["y"], point[0], point[1],)
                    )
                else:
                    s_distance.append(
                        calc_distance(
                            params["curvepoints"][point_i - 1][0],
                            params["curvepoints"][point_i - 1][1],
                            point[0],
                            point[1],
                        )
                    )

            sliderpointdistance.append(mean_lst(s_distance))

            sliderratio.append(1)

        elif object_type == "circle":
            circleratio.append(1)

        elif object_type == "spinner":
            spinnerratio.append(1)

        if index != 0:
            previous_row = hit_df.iloc[index - 1]
            distance.append(
                calc_distance(previous_row["x"], previous_row["y"], row["x"], row["y"])
            )

        hitsounds.append(row["hitsound"])
    r_row["newcombolen"] = mean_lst(newcombolen)
    r_row["sliderlen"] = mean_lst(sliderlen)
    r_row["sliderslides"] = mean_lst(sliderslides)
    r_row["slidervelocity"] = mean_lst(slidervelocity)

    sliderratios = calc_ratio(
        [sliderperfectratio, sliderlinearratio, slidercatmullratio, sliderbezierratio,]
    )

    r_row["sliderperfectratio"] = sliderratios[0]
    r_row["sliderlinearratio"] = sliderratios[1]
    r_row["slidercatmullratio"] = sliderratios[2]
    r_row["sliderbezierratio"] = sliderratios[3]

    r_row["sliderpointamount"] = mean_lst(sliderpointamount)
    r_row["sliderpointdistance"] = mean_lst(sliderpointdistance)
    r_row["combocount"] = combocount
    r_row["timecount"] = timecount
    r_row["timelen"] = mean_lst(timelen)
    r_row["sampleset"] = mean_lst(sampleset)

    samplesetratios = calc_ratio(
        [
            samplesetdefaultratio,
            samplesetnormalratio,
            samplesetsoftratio,
            samplesetdrumratio,
        ]
    )

    r_row["samplesetdefaultratio"] = samplesetratios[0]
    r_row["samplesetnormalratio"] = samplesetratios[1]
    r_row["samplesetsoftratio"] = samplesetratios[2]
    r_row["samplesetdrumratio"] = samplesetratios[3]

    r_row["sampleindex"] = mean_lst(sampleindex)
    r_row["volume"] = mean_lst(volume)
    r_row["uninherited"] = mean_lst(uninherited)
    r_row["effects"] = mean_lst(effects)
    r_row["kiaicount"] = kiaicount
    r_row["kiailength"] = mean_lst(kiailength)

    kiairatios = calc_ratio([kiairatio, notkiai])

    r_row["kiairatio"] = kiairatios[0]

    objectsratios = calc_ratio([circleratio, sliderratio, spinnerratio])

    r_row["circleratio"] = objectsratios[0]
    r_row["sliderratio"] = objectsratios[1]
    r_row["spinnerratio"] = objectsratios[2]

    r_row["distance"] = mean_lst(distance)
    r_row["hitsounds"] = mean_lst(hitsounds)

    return r_row


def mean_lst(list):
    length = len(list) if len(list) != 0 else 1
    return sum(list) / length


def calc_distance(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def calc_ratio(list_list):
    den = sum([len(lis) for lis in list_list])
    den = den if den != 0 else 1
    return [sum(lis) / den for lis in list_list]


if __name__ == "__main__":
    df = osu_df_basic()

    try:
        os.mkdir("./data/csv/")
    except:
        pass

    df.to_csv("./data/csv/basic_osu_df.csv", index=False)

