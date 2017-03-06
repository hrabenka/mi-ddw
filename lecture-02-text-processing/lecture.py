import pprint
from collections import Counter
from string import punctuation

import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

pp = pprint.PrettyPrinter(indent=4)

text = """Prague is the capital and largest city of the Czech Republic. It is the 14th largest city in the European Union.
It is also the historical capital of Bohemia. Situated in the north-west of the country on the Vltava river,
the city is home to about 1.26 million people, while its larger urban zone is estimated to have a population of nearly 2 million.
The city has a temperate climate, with warm summers and chilly winters."""

# Tokenize
tokens = nltk.word_tokenize(text)


def tokenCounts(tokens):
    counts = Counter(tokens)
    sortedCounts = sorted(counts.items(), key=lambda count: count[1], reverse=True)
    return sortedCounts


stops = stopwords.words('english')
tokens = nltk.word_tokenize(text)

filtered_tokens = [token for token in tokens if token not in punctuation]
filtered_tokens = [token for token in filtered_tokens if token not in stops]

pp.pprint(tokenCounts(filtered_tokens))

sentences = nltk.sent_tokenize(text)
pp.pprint(sentences)

# sentences = nltk.sent_tokenize(text)
# tokens = [nltk.word_tokenize(sent) for sent in sentences]
# pp.pprint(tokens)

# sentences = nltk.sent_tokenize(text)
# tokens = [nltk.word_tokenize(sent) for sent in sentences]
# tagged = [nltk.pos_tag(sent) for sent in tokens]
# 
# pp.pprint(tagged)
# 
# stemmer = nltk.PorterStemmer()
# tokens = nltk.word_tokenize(text)
# stems = {token: stemmer.stem(token) for token in tokens}
# print(stems)
# 
# lemmatizer = nltk.WordNetLemmatizer()
# tokens = nltk.word_tokenize(text)
# 
# lemmas = {token: lemmatizer.lemmatize(token) for token in tokens}
# print(lemmas)
# 
# tokens = nltk.word_tokenize(text)
# tagged = nltk.pos_tag(tokens)

# ne_chunked = nltk.ne_chunk(tagged, binary=True)
# print(ne_chunked)


def extractEntities(ne_chunked):
    data = {}
    for entity in ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data


pp.pprint(extractEntities(ne_chunked))

vader_analyzer = SentimentIntensityAnalyzer()
print(vader_analyzer.polarity_scores(text))
