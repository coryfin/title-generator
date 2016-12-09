from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
import sys
import preprocessing


def bag(data, num_dimensions):
    """
    Transforms a list of strings into a Bag of Words.
    :param data: a list of strings
    :param num_dimensions:
    :return:
    """

    data = [preprocessing.clean(row) for row in data]

    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer="word",
                                 tokenizer=None,
                                 preprocessor=None,
                                 stop_words='english',
                                 max_features=num_dimensions)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(data)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    train_data_features = train_data_features.toarray()

    return train_data_features, vectorizer.get_feature_names()


def test(stories, titles, title_feature_names):
    """
    Runs linear regression tests using Bag of Words model
    :param stories:
    :param titles:
    :param title_feature_names:
    :return:
    """

    split = round(0.7 * len(stories))
    train_features = stories[:split]
    test_features = stories[split + 1:]
    train_targets = titles[:split]
    test_targets = titles[split + 1:]

    model = LinearRegression()
    model.fit(train_features, train_targets)

    predicted = model.predict(test_features)
    predicted_words = [vec_to_words(x, title_feature_names) for x in predicted]
    actual_words = [vec_to_words(x, title_feature_names) for x in test_targets]
    num_predicted = 0
    num_correct = 0
    nonempty_predicted_ind = []
    for i in range(len(predicted_words)):
        if len(predicted_words[i]) > 0:
            nonempty_predicted_ind.append(i)
            num_predicted += 1
            if predicted_words[i] == actual_words[i]:
                num_correct += 1

    print(str(len(train_features[0])) + ',' + str(len(train_targets[0])) + ',' + str(num_predicted) + ',' + str(num_correct))
    print('actual: ')
    for i in nonempty_predicted_ind:
        print('\t' + str(actual_words[i]))
    print('predicted: ')
    for i in nonempty_predicted_ind:
        print('\t' + str(predicted_words[i]))


def vec_to_words(vector, title_feature_names):
    """
    Converts a bag of words vector to a list of words
    :param vector:
    :param title_feature_names:
    :return:
    """

    rounded = [round(x) for x in vector]
    indices = list(filter(lambda x: rounded[x] >= 1, range(len(rounded))))
    words = []
    for i in indices:
        words.append(title_feature_names[i])
    return words


corpus_path = sys.argv[1]
num_stories = int(sys.argv[2])
num_dimensions = int(sys.argv[3])

ids, stories, titles = preprocessing.load_stories(corpus_path, num_stories)
bagged_stories, story_feature_names = bag(stories, num_dimensions)
bagged_titles, title_feature_names = bag(titles, num_dimensions)

test(bagged_stories, bagged_titles, title_feature_names)