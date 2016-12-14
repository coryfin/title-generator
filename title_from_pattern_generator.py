import pattern_analysis
import semantic_relevance
import preprocessing
import sys
import nltk
from nltk.corpus import wordnet as wn
import itertools
from collections import defaultdict
import re

import requests

from bs4 import BeautifulSoup
import argparse

# parser = argparse.ArgumentParser(description='Get Google Count.')
# parser.add_argument('word', help='word to count')
# args = parser.parse_args()

def get_number_of_google_searchs(word):
    ##expect a word like "apple" or "San Francisco"
    r = requests.get('http://www.google.com/search',
                      params={'q':'"'+word+'"',
                              "tbs":"li:1"}
                     )

    soup = BeautifulSoup(r.text,"html.parser")
    s= soup.find('div',{'id':'resultStats'}).text
    newstr = s.replace(",", "")
    return int(''.join([s for s in newstr if s.isdigit()]))



NUMBER_PATTERNS=30

def nounify(verb_word):
    #for riding, it gives me rider instead of ride. Check.
    set_of_related_nouns = set()

    for lemma in wn.lemmas(wn.morphy(verb_word, wn.VERB), pos="v"):
        for related_form in lemma.derivationally_related_forms():
            for synset in wn.synsets(related_form.name(), pos=wn.NOUN):
                if wn.synset('person.n.01') in synset.closure(lambda s:s.hypernyms()):
                    set_of_related_nouns.add(synset)

    return set_of_related_nouns


def getTags(words):
    tagged_words= [nltk.pos_tag([word]) for word in words]
    tagged_words=list(itertools.chain.from_iterable(tagged_words))

    # see if this is necessary
    #verbs = filter(lambda (word, tag): tag == 'VBG' ,tagged_words)
    # if len(verbs)>0:
    #     nounified_verbs= [nounify(verb) for verb in verbs]
    #     tagged_words.append(nounified_verbs)

    return tagged_words



def match_title(pattern,tagwords):

    titletags= nltk.word_tokenize(pattern)
    titlegenerator= []
    all_match=True
    titles=[]
    used=defaultdict(list)

    #if there is a tag that is not present, then continue with next pattern
    wordtags= [y  for (x,y) in tagwords]
    wordtags+=['DT']

    for ttag in titletags:
        if ttag not in wordtags:
            all_match= False
            break

    # if there is a match for each tag of the pattern, fill pattern
    if all_match:
        for ttag in titletags:
            if ttag == 'DT':
                #should develop a function to determine the DT based on the following word instead,
                #but The is normally the DT for every title
                titlegenerator.append(['The'])
            else:
                matchlist=[]
                for word in tagwords:
                    if word[1] == ttag:
                        matchlist.append(word[0])

                titlegenerator.append(matchlist)

    if all_match:
        #cartesian product
        titles= list(itertools.product(*titlegenerator))

    return [list(x) for x in titles]

def generateTitles(title_patterns,relevant_words):
    words=getSet([word for (value,word) in relevant_words])

    # generate titles for the story and print them. Maybe compare to the original title
    titles=[]
    tagwords= getTags(words)

    title_patterns= [t for (t,y) in title_patterns] [0:NUMBER_PATTERNS]
    for title_pattern in title_patterns:
        titles.append(match_title(title_pattern,tagwords))
    full_titles = [x for x in titles if x != []]
    return full_titles

def getSet(relevant_words):
    seen = set()
    seen_add = seen.add
    return [x for x in relevant_words if not (x in seen or seen_add(x))]

def test(stories, titles):

    split = int(round(0.7 * len(stories)))
    train_stories = stories[:split]
    test_stories = stories[split + 1:]
    train_titles = titles[:split]
    test_titles = titles[split + 1:]
    final_titles= []

    title_patterns= pattern_analysis.patternTitles(train_titles)

    get_semantic_relevance = semantic_relevance.SemanticRelevance(ont_filename)
    semantic_relevance_stories= get_semantic_relevance.extract_vectors(train_stories[500:501], 5)

    for semantic_relevance_story in semantic_relevance_stories:
        final_titles.append(generateTitles(title_patterns,semantic_relevance_story))

    # final_titles= generateTitles(title_patterns,['bike', 'she', 'sneak' , 'ride'])

    selected_titles=[]

    for title in final_titles:
        max=-1
        for each_title in title:
            x= each_title[0]
            tags=[]
            for w in x:
                tags.append(nltk.pos_tag([w])[0][1])

            #if there are repeated tags
            if (len(tags) > len (set(tags))):
                for x in each_title:
                    num= get_number_of_google_searchs(" ".join(x))
                    if (num>max):
                        max=num
                        selected_title=x
                selected_titles.append(selected_title)
            else:
                selected_titles.append(each_title[0])
    for selected_title in selected_titles:
        print(" ".join(selected_title))

ont_filename = sys.argv[1]
story_filename = sys.argv[2]
num_stories = int(sys.argv[3])


ids, stories, titles = preprocessing.load_stories(story_filename, num_stories)
test(stories,titles)