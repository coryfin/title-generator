from nltk.corpus import stopwords


def load_stories(in_filename, num_stories):
    """
    Extracts stories and titles from a csv file
    :param in_filename:
    :param num_stories:
    :return:
    """
    file = open(in_filename, 'r')
    data = [row.strip().split('\t') for row in file]
    file.close()

    # Isolate header row
    header = data[0]
    data = data[1:num_stories + 1]

    id_col = header.index('storyid')
    title_col = header.index("storytitle")

    # Separate ids and titles, and then join sentences of stories
    titles = [row[title_col] for row in data]
    ids = [row[id_col] for row in data]
    stories = [' '.join(row[1:title_col] + row[title_col + 1:]) for row in data]

    return ids, stories, titles


def clean(story, remove_stop_words=False, remove_possessive=False):
    """
    Story pre-processing, such as removing punctuation, possessive 's, and de-capitalization.
    :param story: a string containing the story text
    :return:
    """

    # Remove punctuation
    story = story.replace('.', '').replace('?', '').replace(',', '').replace('!', '')

    # Remove possessive form
    if remove_possessive:
        story = story.replace("'s", "")

    # Remove stop words
    words = story.split(' ')
    if remove_stop_words:
        words = [word for word in words if word not in stopwords.words('english')]

    # Convert to lower case
    story = ' '.join([word.lower() for word in words])
    return story
