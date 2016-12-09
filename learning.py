from sklearn.linear_model import LinearRegression


def test(stories, titles, title_feature_names):

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

    print(str(num_predicted) + ',' + str(num_correct))
    for i in nonempty_predicted_ind:
        print('actual: ' + str(actual_words[i]) + ', predicted: ' + str(predicted_words[i]))


def vec_to_words(vector, title_feature_names):
    rounded = [round(x) for x in vector]
    indices = list(filter(lambda x: rounded[x] >= 1, range(len(rounded))))
    words = []
    for i in indices:
        words.append(title_feature_names[i])
    return words
