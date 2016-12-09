import bagger
import learning
import sys


corpus_path = sys.argv[1]
num_stories = int(sys.argv[2])
num_dimensions = int(sys.argv[3])

ids, stories, titles = bagger.format_stories(corpus_path, num_stories)
bagged_stories, story_feature_names = bagger.bag(stories, num_dimensions)
bagged_titles, title_feature_names = bagger.bag(titles, num_dimensions)

learning.test(bagged_stories, bagged_titles, title_feature_names)
