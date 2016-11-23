import numpy as np
import copy


file = open('ROCStories__spring2016.tsv', 'r')
data = [row.strip().replace('.', '').replace('?', '').replace(',', '').replace('!', '').split('\t') for row in file]

# Isolate header row
header = data[0]
data = data[1:]

id_col = header.index('storyid')
title_col = header.index("storytitle")

# Separate ids and titles, and then join sentences
labels = [row[title_col] for row in data]
ids = [row[id_col] for row in data]
data = [' '.join(row[1:title_col] + row[title_col + 1:]) for row in data]

frequencies = {}
for row in data:
    words = [word.lower() for word in row.split(' ')]
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1

keys = list(frequencies.keys())
values = list(frequencies.values())
for i in range(10):
    print(keys[i] + ':' + str(values[i]))

# terms = list(frequencies.keys())
# frequencies = list(frequencies.values())

bags = []
for row in data:
    words = [word.lower() for word in row.split(' ')]
    term_frequencies = {k: 1 if v in words else 0 for k, v in frequencies.items()}
    bags.append(term_frequencies)

print('done')
