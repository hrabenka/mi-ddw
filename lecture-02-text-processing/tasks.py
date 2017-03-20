import os
import pprint
from string import punctuation

import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

import tkinter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def extract_entities(_ne_chunked):
    data = {}
    for entity in _ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data


def token_counts(tokens):
    counts = nltk.Counter(tokens)
    sorted_counts = sorted(counts.items(), key=lambda count: count[1], reverse=True)
    return sorted_counts


pp = pprint.PrettyPrinter(indent=4)

text = None
with open(os.path.join(os.path.dirname(__file__), 'book.txt'), 'r') as f:
    text = f.read()

stops = stopwords.words('english')
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.PorterStemmer()
vader_analyzer = SentimentIntensityAnalyzer()

tokens = nltk.word_tokenize(text)
filtered_tokens = [token for token in tokens if token not in punctuation]
filtered_tokens = [token for token in filtered_tokens if token not in stops]

count = token_counts(filtered_tokens)

print("Tokens:")
print(sorted(count, key=lambda x: x[1])[-20:-1])

# stems = {token: stemmer.stem(token) for token in filtered_tokens}
# print("Stems:")
# print(stems)
# 
# lemmas = {token: lemmatizer.lemmatize(token) for token in filtered_tokens}
# print("Lemmas:")
# print(lemmas)
# 
tagged = nltk.pos_tag(tokens)
print("Tagged:")
print(tagged)
# 
# ne_chunked = nltk.ne_chunk(tagged, binary=True)
# print("Entities:")
# print(extract_entities(ne_chunked))

# sentiment = vader_analyzer.polarity_scores(text)
# print("Sentiment:")
# print(sentiment)

print("--------------------------------------------------------------------------------")

sentences = nltk.sent_tokenize(text)
result = []
positive_count = 0
negative_count = 0
for sentence in sentences:
    print("Sentence:")
    print(sentence)

    tokens = nltk.word_tokenize(sentence)
    filtered_tokens = [token for token in tokens if token not in punctuation]
    filtered_tokens = [token for token in filtered_tokens if token not in stops]

    print("Tokens:")
    print(filtered_tokens)

    stems = {token: stemmer.stem(token) for token in filtered_tokens}
    print("Stems:")
    print(stems)

    lemmas = {token: lemmatizer.lemmatize(token) for token in filtered_tokens}
    print("Lemmas:")
    print(lemmas)

    tagged = nltk.pos_tag(tokens)
    print("Tagged:")
    print(tagged)

    ne_chunked = nltk.ne_chunk(tagged, binary=True)
    print("Entities:")
    print(extract_entities(ne_chunked))

    sentiment = vader_analyzer.polarity_scores(sentence)
    print("Sentiment:")
    print(sentiment)

    compound = sentiment.get('compound')

    result.append([sentence, compound])

    if compound > 0:
        positive_count += 1

    if compound < 0:
        negative_count += 1

result = sorted(result, key=lambda x: x[1])

print("--------------------------------------------------------------------------------")

pp.pprint(result[0:10])

print("--------------------------------------------------------------------------------")
pp.pprint(result[-10:-1])

print("--------------------------------------------------------------------------------")
print("Positive " + str(positive_count) + " Negative " + str(negative_count))

wordcloud = WordCloud().generate(text)

plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
