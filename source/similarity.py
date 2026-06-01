from sklearn.feature_extraction.text import (TfidfVectorizer)
from sklearn.metrics.pairwise import (cosine_similarity)

#Build user document
def build_user_document(user_data,inferred_styles):
    """Creates semantic text profile
    for the user.Ex:politics,lyrical"""
    semantic_parts = []
    #User topics
    semantic_parts.extend(
        user_data["topics"])
    #User styles
    semantic_parts.extend(user_data["styles"])
    #Inferred styles
    semantic_parts.extend(
        inferred_styles.keys())
    #User rappers
    semantic_parts.extend(user_data["rappers"])
    return " ".join(semantic_parts)


#Build rapper document
def build_rapper_document(rapper):
    """ Creates semantic profile
    for a rapper.Ex:politics,struggle"""
    semantic_parts = []
    semantic_parts.extend(rapper["topics"])
    semantic_parts.extend(rapper["styles"])
    semantic_parts.append(rapper.get("region", ""))
    semantic_parts.append(rapper.get("era", ""))
    semantic_parts.extend(rapper.get("similar_artists",[] ))
    return " ".join(semantic_parts)

#Similarity section
def calculate_similarity_scores(user_data,inferred_styles,rappers_data):
    """Returns semantic similarity scores
    between user profile and artists. """
    #Build user doc
    user_document = build_user_document(user_data, inferred_styles)

    #Build rapper documents
    rappers_documents = []
    rappers_names = []
    for rapper in rappers_data:
        document = build_rapper_document(rapper)
        rappers_documents.append(document)
        rappers_names.append(rapper["name"])

    #TF-IDF
    vectorizer = TfidfVectorizer()

    # user doc first
    all_documents = [user_document] + rappers_documents
    tfidf_matrix = vectorizer.fit_transform(all_documents)
    #Split vectors
    user_vector = tfidf_matrix[0]
    artist_vectors = tfidf_matrix[1:]

    #Call cosine sim
    similarity_scores = cosine_similarity(user_vector,artist_vectors)[0]

   #Format results
    similarity_results = []
    for index, score in enumerate(similarity_scores):
        similarity_results.append({
            "name":rappers_names[index],
            "similarity_score":float(score)})

    #Sort results
    similarity_results.sort(
    key=lambda x: x["similarity_score"],reverse=True)
    return similarity_results

#Merge kbs+similarity

def merge_recommendation_scores(kbs_results,similarity_results):
    """Combines:
    - KBS scores
    - semantic similarity scores"""
    #Lookup
    similarity_lookup = {
        item["name"]:
            item["similarity_score"]
        for item in similarity_results}

    #Merge scores
    for rapper in kbs_results:
        similarity_score = similarity_lookup.get(
            rapper["name"],0)

        # ---------------------------------------------
        # FINAL HYBRID SCORE
        # ---------------------------------------------
        # similarity * 10 scales better
        # with KBS scores
        # ---------------------------------------------

        rapper["final_score"] = (
        rapper["score"]+(similarity_score * 10))
        rapper["similarity_score"] = ( similarity_score)

    #Sort final result
    kbs_results.sort(
        key=lambda x: x["final_score"],reverse=True)
    return kbs_results