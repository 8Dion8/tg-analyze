import json
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np

plt.style.use("./nord-dark-talk.mplstyle")


with open("result.json", "r") as f:
    data = json.load(f)


messages = data["messages"]

authors = []

months = {}

for message in messages:
    if message["type"] == "message" and \
    "forwarded_from" not in message.keys():

        author = message["from"]
        if author not in authors:
            authors.append(author)

        text = message["text"]

        
        time = message["date"] #     "2022-10-02T01:44:59"
        date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        month = str(date.year) + " " + str(date.month)




        if month in months:
            if author in months[month]:
                months[month][author] += 1
            else:
                months[month][author] = 1
        else:
            months[month] = {}



BARWIDTH = 0.35

fig, ax = plt.subplots()


month_author_label_loc = np.arange(len(months.keys()))
month_author0_bars = ax.bar(
    month_author_label_loc - BARWIDTH/2,
    [months[i][authors[0]] for i in months],
    BARWIDTH,
    label = authors[0]
)
month_author1_bars = ax.bar(
    month_author_label_loc + BARWIDTH/2,
    [months[i][authors[1]] for i in months],
    BARWIDTH,
    label = authors[1]
)
ax.set_ylabel("Number Of Messages")
ax.set_title("Number Of Messages By Month")
ax.set_xticks(month_author_label_loc, months.keys())
ax.legend()



fig.tight_layout()
plt.show()

