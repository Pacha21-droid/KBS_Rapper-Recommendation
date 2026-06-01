import json

with open("knowledge/rules.json","r",encoding="utf-8") as f:
    rules=json.load(f)

#Scores
direct_match_topic=5
direct_match_style=4
exact_match_rapper=10
similar_match_rapper=8
inferred_match_style=3

def user_prefs(input):
    inferred_styles={}

    # Process topic
    for topic in input["topics"]:
        topic_rule = rules["topics"].get(topic)
        if not topic_rule:
            continue
        rule_weight = topic_rule.get( "weight",1)
        inferred_rule_styles = topic_rule.get( "infer_styles",[]) 

        # Get style importance
        for style in inferred_rule_styles:
            if style not in inferred_styles:
                inferred_styles[style] = 0
            inferred_styles[style] += rule_weight
    return inferred_styles

#Recommendation section
def apply_rules(user_data,rappers_data):
    #Preferences
    inferred_styles = user_prefs(user_data)
    recommendations = []

    for rapper in rappers_data:
        score = 0
        matched_topics = []
        matched_styles = []
        inferred_matches = []

        # NORMALIZE RAPPER DATA
        rapper_topics = [
            topic.lower()
            for topic in rapper["topics"]]

        rapper_styles = [
            style.lower()
            for style in rapper["styles"]]

        rapper_name = rapper["name"].lower()

        if rapper_name in user_data["rappers"]:
            score += exact_match_rapper

        #Direct match by topic
        for topic in user_data["topics"]:
            if topic in rapper_topics:
                score += direct_match_topic
                matched_topics.append(topic)

        # Direct match by style
        for style in user_data["styles"]:
            if style in rapper_styles:
                score += direct_match_style
                matched_styles.append(style)

        #Inferred match by style
        for inferred_style, weight in inferred_styles.items():
            if inferred_style in rapper_styles:
                score += (inferred_match_style + weight)
                inferred_matches.append(inferred_style)

        #Similar rapper match
        for artist in user_data["rappers"]:
            current_rapper = next(
                (r for r in rappers_data
                 if r["name"].lower() == artist),
                None)
            if current_rapper:
                similar_rappers = [
                    s.lower()
                    for s in current_rapper.get("similar_artists", [])]
                if rapper_name in similar_rappers:
                    score += similar_match_rapper

        #Exact rapper match
        if rapper_name in user_data["rappers"]:
            score += exact_match_rapper

        #Ignore empty results
        if score <= 0:
            continue

        #Save recommendation
        recommendations.append({
            "name": rapper["name"],
            "score": score,
            "matched_topics": matched_topics,
            "matched_styles": matched_styles,
            "inferred_matches": inferred_matches,
            "region": rapper.get("region"),
            "era": rapper.get("era")
        })

    #Sort results
    recommendations.sort(
        key=lambda x: x["score"], reverse=True)

    return recommendations, inferred_styles