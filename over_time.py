import json
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from tqdm import tqdm
import re
import os
import pandas as pd
from scipy.ndimage.filters import gaussian_filter1d

plt.style.use("./everforest.mplstyle")
plt.rc("xtick", labelsize=8)
plt.rc('legend', fontsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('font', size=8)

dirs = list(os.walk("data"))[0][1]

haha_reg = re.compile("[ахпвсщычъзэжук]+$")

MAAVG = 7
SMOOTHING = 1.5
START_CUTOFF = datetime(2022, 10, 1)
END_CUTOFF = datetime.today()
COLORS = ['#7fbbb3', '#a7c080', '#dbbc7f', '#e67e80', '#d699b6', '#83c092', '#e69875']

dialogue_analysis = {}

for directory_name in dirs:
    with open(f"data/{directory_name}/result.json", "r") as f:
        data = json.load(f) 

    messages = data["messages"]
    author = data["name"]

    dialogue_analysis[author] = {}
    print(f"Working on directory data/{directory_name}; dialogue with {author}")

    dialogue_analysis[author]["total_n"] = len(messages)
    dialogue_analysis[author]["sent_n"] = 0
    dialogue_analysis[author]["received_n"] = 0

    start = datetime.strptime(messages[0]["date"].split("T")[0], "%Y-%m-%d")

    x = []
    y = []

    if start > START_CUTOFF:
        for i in range((start - START_CUTOFF).days):
            x.append(START_CUTOFF + timedelta(days=i))
            y.append(0)
    else:
        x = [start]
        y = [0]


    for message in tqdm(messages):
        if message["type"] == "message":
            if message["from"] == author:
                dialogue_analysis[author]["received_n"] += 1
            else:
                dialogue_analysis[author]["sent_n"] += 1

            time = datetime.strptime(message["date"].split("T")[0], "%Y-%m-%d")


            last_message_time = x[-1]
            if last_message_time == time:
                y[-1] += 1
            else:
                for i in range((time - last_message_time).days-1):
                    last_message_time += timedelta(days=1)
                    x.append(last_message_time)
                    y.append(0)

                x.append(time)
                y.append(1)
    
    last_message_time = x[-1]
    if last_message_time < END_CUTOFF:
        for i in range((END_CUTOFF - last_message_time).days):
            x.append(last_message_time + timedelta(days=i))
            y.append(0)

    dialogue_analysis[author]["x"] = x
    dialogue_analysis[author]["y"] = y

    y_ser = pd.Series(y)
    y_win = y_ser.rolling(MAAVG)
    y_ma = y_win.mean().to_list()
    dialogue_analysis[author]["y_ma"] = y_ma

    y_ma_smooth = gaussian_filter1d(y_ma, sigma=SMOOTHING)
    dialogue_analysis[author]["y_ma_smooth"] = y_ma_smooth

ax = plt.subplot()

color_index = 0

for author in dialogue_analysis:
    x = dialogue_analysis[author]["x"]
    y = dialogue_analysis[author]["y_ma_smooth"]
    ax.plot(
        x,
        y,
        linewidth=1,
        label = author,
        color = COLORS[color_index]
    )
    ax.fill_between(x, y, color=COLORS[color_index], alpha=0.1)

    color_index += 1

ax.grid(True)
ax.set_xlabel("Date")
ax.set_ylabel("MA of messages")
ax.set_xlim([START_CUTOFF, END_CUTOFF])
ax.set_ylim([0, None])
ax.legend()
plt.tight_layout()
        
plt.show()
#print(dialogue_analysis)
    
