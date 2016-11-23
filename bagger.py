import numpy as np


file = open('ROCStories__spring2016.tsv', 'r')
data = [row.strip().split('\t') for row in file]
header = data[0]
data = data[1:]
title_col = header.index("storytitle")
labels = [row[title_col] for row in data]
data = [row[:title_col] + row[title_col + 1:] for row in data]
a = 0
