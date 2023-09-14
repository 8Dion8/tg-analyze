import json
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from tqdm import tqdm


with open("data/0/result.json", "r") as f:
    data0 = json.load(f)

messages0 = data0["messages"]

current_day = -1
current_message_count = 0

message_count0 = []
x0 = []

for message in tqdm(messages0):
    time = message["date"] #     "2022-10-02T01:44:59"
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    day = date.second
    if current_day != day:
        message_count0.append(current_message_count)
        current_day = day
        current_message_count = 1
        x0.append(date)
    else:
        current_message_count += 1

cumulative_count0 = []
cumul = 0
for i in message_count0:
    cumul += i
    cumulative_count0.append(cumul)






with open("data/1/result.json", "r") as f:
    data1 = json.load(f)

messages1 = data1["messages"]

current_day = -1
current_message_count = 0

message_count1 = []
x1 = []

for message in tqdm(messages1):
    time = message["date"] #     "2022-10-02T01:44:59"
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    day = date.second
    if current_day != day:
        message_count1.append(current_message_count)
        current_day = day
        current_message_count = 1
        x1.append(date)
    else:
        current_message_count += 1

cumulative_count1 = []
cumul = 0
for i in message_count1:
    cumul += i
    cumulative_count1.append(cumul)



with open("data/2/result.json", "r") as f:
    data2 = json.load(f)

messages2 = data2["messages"]

current_day = -1
current_message_count = 0

message_count2 = []
x2 = []

for message in tqdm(messages2):
    time = message["date"] #     "2022-10-02T01:44:59"
    date = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    day = date.second
    if current_day != day:
        message_count2.append(current_message_count)
        current_day = day
        current_message_count = 1
        x2.append(date)
    else:
        current_message_count += 1

cumulative_count2 = []
cumul = 0
for i in message_count2:
    cumul += i
    cumulative_count2.append(cumul)

fig = plt.figure()


plt.plot(x0, cumulative_count0, color="#98971a", label="Майя")
plt.fill_between(x0, 0, cumulative_count0, alpha=.1, color="#98971a")

plt.plot(x1, cumulative_count1, color="#cc241d", label="Серега")
plt.fill_between(x1, 0, cumulative_count1, alpha=.1, color="#cc241d")

plt.plot(x2, cumulative_count2, color="#458588", label="Полина")
plt.fill_between(x2, 0, cumulative_count2, alpha=.1, color="#458588")

plt.legend()



plt.show()