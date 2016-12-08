from sklearn.linear_model import LinearRegression
from scipy.spatial import distance


file = open('stories.csv')
stories = [row.split(',') for row in file]
file.close()

file = open('titles.csv')
titles = [row.split(',') for row in file]
file.close()

story_feature_names = stories[0]
stories = stories[1:]
title_feature_names = titles[0]
titles = titles[1:]

model = LinearRegression()
model.fit(stories, titles)
predicted = model.predict(stories[0])
actual = titles[0]
dist = distance.cosine(predicted, actual)
print(dist)
