from flask import jsonify, request
from flask_restful import Api, Resource
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from googlesearch import search

df = pd.read_csv("jobss.csv")
df = df[["Job Title", "Key Skills"]]
df = df.dropna()
df = df[df["Key Skills"] != "vide"]

# create a list cooking recipes
corpus = df["Job Title"].tolist()

# create TfidfVectorizer object
tfidf = TfidfVectorizer()

# compute a sparse matrix of word vectors for all the cooking recipes
tfidf_matrix = tfidf.fit_transform(corpus)


def recommend_learning_site(skill):
    search_query = f"learn {skill} online"
    search_results = list(search(search_query, num_results=1))

    if search_results:
        recommended_site = search_results[0]
        return recommended_site
    else:
        return None


class Recommend_Competencies(Resource):
    def post(self):
        posted_data = request.get_json()
        new_query = posted_data["job"]["value"]

        new_query_vector = tfidf.transform([new_query])

        # Compute cosine similarity scores of this new query and each of the recipes
        cosine_sim = pd.DataFrame(
            cosine_similarity(tfidf_matrix, new_query_vector),
            columns=["cosine_similarity_score"],
            index=df.index,
        )

        # Rank cosine similarity scores from the highest to the lowest
        cosine_sim = cosine_sim.sort_values(
            by=["cosine_similarity_score"], ascending=False
        )

        # Output the top 3 matched results
        recommended_skills = df.loc[cosine_sim.index[0:4], :]
        recommended_skills = recommended_skills["Key Skills"].to_list()[0].split("|")
        recommended_skills_sites = [
            recommend_learning_site(skills) for skills in recommended_skills
        ]
        recommended_learning_sites = []

        for i in range(len(recommended_skills)):
            skill = recommended_skills[i]
            site = recommended_skills_sites[i]
            obj = {"name": skill, "link": site}
            recommended_learning_sites.append(obj)

        ret_json = {
            "status": 200,
            "msg": " Succes text annotated",
            "annotate_data": recommended_learning_sites,
        }
        return jsonify(ret_json)
