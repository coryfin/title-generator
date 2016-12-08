import numpy as np
import copy
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer


def format_stories(in_filename):

    file = open(in_filename, 'r')
    data = [row.strip().split('\t') for row in file]
    file.close()

    # Isolate header row
    header = data[0]
    data = data[1:]

    id_col = header.index('storyid')
    title_col = header.index("storytitle")

    # Separate ids and titles, and then join sentences of stories
    labels = [row[title_col] for row in data]
    ids = [row[id_col] for row in data]
    stories = [' '.join(row[1:title_col] + row[title_col + 1:]) for row in data]

    # data = ['id,story,title\n']
    # data.extend([ids[i] + ',' + stories[i] + ',' + labels[i] + '\n' for i in range(10)])
    # data.extend([ids[i] + ',' + stories[i] + ',' + labels[i] + '\n' for i in range(len(stories))])
    return ids, stories, labels


def clean(story):
    """
    Story prepocessing, such as removing punctuation, possessive 's, and de-capitalization.
    :param story:
    :return:
    """
    # TODO: remove stop words?

    # Remove punctuation
    story = story.replace('.', '').replace('?', '').replace(',', '').replace('!', '')

    # TODO: remove possession?
    # Remove possession
    story = story.replace("'s", "")

    # TODO: capitalize names?
    # Convert to lower case
    story = ' '.join([word.lower() for word in story.split(' ')])
    return story


def bag(data):
    """
    Transforms a list of strings into a Bag of Words
    :param data: a list of strings
    :return:
    """

    data = [clean(row) for row in data]

    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words=None,
                                 max_features=5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(data)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    return train_data_features, vectorizer.get_feature_names()


def write(data, filename):
    file = open(filename, 'w')
    file.writelines(data)
    file.close()


id, stories, titles = format_stories('ROCStories__spring2016.tsv')
bagged_stories, story_feature_names = bag(stories)
bagged_titles, title_feature_names = bag(titles)
# data = np.concatenate((bagged_stories, bagged_titles), axis=1)
np.savetxt('stories.csv', bagged_stories, delimiter=',', header=','.join(story_feature_names), fmt='%i', comments='')
np.savetxt('titles.csv', bagged_titles, delimiter=',', header=','.join(title_feature_names), fmt='%i', comments='')
