import preprocessing
import sys
import nltk
from collections import defaultdict
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

N_MOST_FREQUENT= 30
LABEL_SIZE=12
NUM_STORIES=45500

def patternTitles(titles):
    pattern_titles= defaultdict(int)

    for title in titles:
        ttitle= nltk.word_tokenize(title)
        #retrieving part of speech tags from title
        pos_tag_title= nltk.pos_tag(ttitle)
        pos_tag_title = [tag for (word,tag) in pos_tag_title]
        pattern_titles[" ".join(pos_tag_title)]+=1

        d = Counter(pattern_titles)

    #getCumulativePercentage(d.most_common(N_MOST_FREQUENT))
    return d.most_common(N_MOST_FREQUENT)


def getCumulativePercentage(title_patterns):

    freqwords = [seq[0] for seq in title_patterns]
    frequencies = [seq[1] for seq in title_patterns]

    x = list(range(N_MOST_FREQUENT))
    percentages = [freq / float(NUM_STORIES) for freq in frequencies]

    cs = np.cumsum(percentages)

    plt.rc('xtick', labelsize=LABEL_SIZE)
    plt.xticks(x, freqwords)
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.gcf().subplots_adjust(bottom=0.4)
    plt.plot(x, percentages)
    plt.title('Accumulative percentage of titles covered  by the top \n' + str(N_MOST_FREQUENT) + ' most frequent patterns in title' )
    plt.plot(x, cs, 'r--')
    plt.show()

# def learnCollocations(self,titles):
#     for title in titles:
#
#




