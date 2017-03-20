import itertools
import os
from string import punctuation

import nltk
from nltk.corpus import stopwords

stops = stopwords.words('english')

text = None
with open(os.path.join(os.path.dirname(__file__), 'book-shortened.txt'), 'r') as f:
    text = f.read()

tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
ne_chunked = nltk.ne_chunk(tagged, binary=True)


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


nodes = list(extractEntities(ne_chunked).keys())
print(nodes)

import networkx as nx

G = nx.Graph()
G.add_nodes_from(nodes)

sentences = nltk.sent_tokenize(text)
for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    filtered_tokens = [token for token in tokens if token not in punctuation]
    filtered_tokens = [token for token in filtered_tokens if token not in stops]
    intersect = list(set(filtered_tokens) & set(nodes))
    combinations = [tuple(x) for x in itertools.combinations(intersect, 2)]
    if len(combinations) > 0:
        print(combinations)
        G.add_edges_from(combinations)

import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
nx.draw(G, pos=None,
        labels={v: str(v) for v in G},
        cmap=plt.get_cmap("bwr"),
        node_color=[G.degree(v) for v in G],
        font_size=12
        )
plt.show()

nx.draw(G, None, with_labels=False, node_size=10)
plt.show()

centralities = [nx.degree_centrality, nx.closeness_centrality,
                nx.betweenness_centrality, nx.eigenvector_centrality]
region = 220
for centrality in centralities:
    region += 1
    plt.subplot(region)
    plt.title(centrality.__name__)
    nx.draw(G, None, labels={v: str(v) for v in G},
            cmap=plt.get_cmap("bwr"), node_color=[centrality(G)[k] for k in centrality(G)])
plt.show()

communities = {node: cid + 1 for cid, community in enumerate(nx.k_clique_communities(G, 5)) for node in community}
nx.draw(G, None,
        labels={v: str(v) for v in G},
        cmap=plt.get_cmap("rainbow"),
        node_color=[communities[v] if v in communities else 0 for v in G])
plt.show()
