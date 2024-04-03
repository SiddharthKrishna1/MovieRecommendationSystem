import pandas as pd
import numpy as np
import seaborn as sns
import ast
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')  # Download 'punkt' if you haven't already

movies = pd.read_csv("movies.csv")
credits = pd.read_csv("credits.csv")
merged = movies.merge(credits, on="title")
m2 = merged[['movie_id', 'genres', 'keywords', 'title', 'overview', 'cast', 'crew']]

def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i["name"])
    return L

m2['genres'] = m2['genres'].apply(convert)
m2["keywords"] = m2['keywords'].apply(convert)

def con3(obj):
    L=[]
    counter =0
    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i["name"])
            counter += 1
        else:
            break
    return L

m2["cast"] = m2["cast"].apply(con3)

def fetchDirector(obj):
    L =[]
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            L.append(i["name"])
            break
    return L

m2["crew"] = m2["crew"].apply(fetchDirector)

m2["overview"] = m2["overview"].apply(lambda x:x.split())
m2["genres"] = m2["genres"].apply(lambda x:[i.replace(" ","") for i in x])
m2["keywords"] = m2["keywords"].apply(lambda x:[i.replace(" ","") for i in x])
m2["cast"] = m2["cast"].apply(lambda x:[i.replace(" ","") for i in x])
m2["crew"] = m2["crew"].apply(lambda x:[i.replace(" ","") for i in x])

m2['tags'] = m2["overview"] + m2["genres"] + m2["cast"] + m2["crew"] + m2["keywords"]
newdf = m2[['movie_id','title','tags']]
newdf["tags"] = newdf['tags'].apply(lambda x:" ".join(x))

cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(newdf["tags"]).toarray()

ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

similar = cosine_similarity(vectors)

def rec(movie):
    movie_index = newdf[newdf["title"] == movie].index[0]
    dist = similar[movie_index]
    movie_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]
    
    for i in movie_list:
        print(newdf.iloc[i[0]].title)

