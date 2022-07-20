from textblob import TextBlob
from newspaper import Article


url = 'https://en.wikipedia.org/wiki/The_Lord_of_the_Rings'
article = Article(url).download().parse().nlp()

text = article.text
print(text)
