import json
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
from tqdm import tqdm
import re

plt.style.use("./nord-dark-talk.mplstyle")
plt.rc("xtick", labelsize=8)
plt.rc('legend', fontsize=8)
plt.rc('ytick', labelsize=8)
plt.rc('font', size=8)


with open("/home/dion/Downloads/Telegram Desktop/ChatExport_2023-01-27 (2)/result.json", "r", encoding='utf-8') as f:
    data = json.load(f)

with open("stopwords-ru.txt", "r") as f:
    stopwords = [x.strip() for x in f.readlines()]

messages = data["messages"]

authors = []
field_types = []

total_messages = {}
words = {}
months = {}

haha_reg = re.compile("[ахпвсщычъзэжук]+$")


for message in tqdm(messages):
    for i in message.keys():
        if i not in field_types:
            field_types.append(i)
    if message["type"] == "message" and \
    "forwarded_from" not in message.keys():

        author = message["from"]
        if author not in authors:
            authors.append(author)
            words[author] = {}

        
        try:

            text = message["text"].lower()
            
            text_words = "".join(x for x in text if x.isalpha() or x.isspace()).split(" ")

            for word in text_words:
                if word in stopwords or word == "":
                    continue
                if haha_reg.match(word):
                    word = "axaxa"
                if word.strip() in words[author]:
                    words[author][word.strip()] += 1
                else:
                    words[author][word.strip()] = 1
        except:
            pass
        
        time = message["date"] #     "2022-10-02T01:44:59"
        date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        month = str(date.year) + " " + str(date.month)


        if author in total_messages:
            total_messages[author] += 1
        else:
            total_messages[author] = 1

        if month in months:
            if author in months[month]:
                months[month][author] += 1
            else:
                months[month][author] = 1
        else:
            months[month] = {}

#['forwarded_from', 'reply_to_message_id', 'photo', 'media_type', 'sticker_emoji']
#print(field_types)

for auth in words:
    words[auth] = {k: v for k, v in sorted(words[auth].items(), key=lambda item: item[1], reverse=True)}


with open("word_arch.json", "w") as f:
    json.dump(words, f)


BARWIDTH = 0.35

fig, ax = plt.subplots(1, 2)



def addlabels(x,y,ax,flg):
    if flg:
        for i in range(len(x)):
            ax.text(i-len(x)*0.045, y[i]+50, y[i], ha = 'center')
    else:
        for i in range(len(x)):
            ax.text(i+len(x)*0.045, y[i]+50, y[i], ha = 'center')



month_author_label_loc = np.arange(len(months.keys()))
month_author0_bars = ax[0].bar(
    month_author_label_loc - BARWIDTH/2,
    [months[i][authors[0]] for i in months],
    BARWIDTH,
    label = authors[0]
)
'''
addlabels(
    month_author_label_loc,
    [months[i][authors[0]] for i in months],
    ax[0],
    True
)
'''
month_author1_bars = ax[0].bar(
    month_author_label_loc + BARWIDTH/2,
    [months[i][authors[1]] for i in months],
    BARWIDTH,
    label = authors[1]
)
'''
addlabels(
    month_author_label_loc,
    [months[i][authors[1]] for i in months],
    ax[0],
    False
)
'''

ax[0].set_ylabel("Number Of Messages")
ax[0].set_title("Number Of Messages By Month")
ax[0].set_xticks(month_author_label_loc, months.keys())
ax[0].legend()


total_message_pie = ax[1].pie(
    total_messages.values(),
    labels = total_messages.keys(),
    autopct='%1.1f%%'
)



fig.tight_layout()
plt.show()

