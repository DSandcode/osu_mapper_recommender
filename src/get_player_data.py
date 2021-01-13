import urllib.request, json
import re
import numpy as np

from src.log_print import *


def get_user_json(userid, mode="osu", log=False):
    log_print(log, f"Getting {userid} json")
    r_dict = {
        "best": 0,
        "activity": 0,
        "firsts": 0,
        "recent": 0,
    }
    api_addresses = [
        f"scores/best?mode={mode}&",
        "recent_activity?",
        f"scores/firsts?mode={mode}&",
        f"scores/recent?mode={mode}&",
    ]
    for api_address, key in zip(api_addresses, r_dict):
        log_print(
            log, f"Current address https://osu.ppy.sh/users/{userid}/{api_address}"
        )
        r_data = []
        s_len = 1
        while s_len != len(r_data):
            s_len = len(r_data)
            with urllib.request.urlopen(
                f"https://osu.ppy.sh/users/{userid}/{api_address}offset={len(r_data)}&limit=51"
            ) as url:
                r_data.extend(json.loads(url.read().decode()))
            if len(r_data) >= 100 and key == "most":
                break

        r_dict[key] = r_data
    log_print(log, f"Got {userid} json")
    return r_dict


def get_user_beatmapids(userid, mode="osu", log=False):
    log_print(log, f"Getting {userid} beatmapsid in mode:{mode}")
    r_list = []
    user_data = get_user_json(userid, mode=mode, log=log)
    for data_key in user_data:
        log_print(log, f"Getting ids from {data_key}")
        if data_key != "activity":
            for data in user_data[data_key]:
                r_list.append(int(data["beatmap"]["id"]))
        else:
            for data in user_data[data_key]:
                # \/\d*\?
                if data["type"] == "rank":
                    r_list.append(
                        int((re.search(r"\/\d*\?", data["beatmap"]["url"]))[0][1:-1])
                    )
    return np.unique(r_list)


# beatmapsets/ranked_and_approved
# scores/best?mode=osu
# recent_activity
# scores/firsts?mode=osu
# beatmapsets/favourite
# beatmapsets/most_played
# scores/recent?mode=osu
if __name__ == "__main__":
    userid = 13664116
    user_beatmapids = get_user_beatmapids(userid, log="true")
    # best: beatmap->id
    # activity: beatmap->url process->id
    # firsts: beatmap->id
    # most: beatmap->id
    # recent: beatmap->id
