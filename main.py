from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from source.nlp import process_input
from source.inference import (apply_rules)
from source.similarity import (calculate_similarity_scores,merge_recommendation_scores)
import json

#Load rapper data
with open("knowledge/rappers.json","r",encoding="utf-8") as f:
    rappers_data = json.load(f)

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(
    directory="templates")

#Request model
class UserInput(BaseModel):
    text: str
@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )
#Recommendation
@app.post("/recommend")
async def recommend(user_input: UserInput):
    #NLP
    user_data = process_input(user_input.text)

    #Rules
    kbs_results, inferred_styles = apply_rules(user_data,rappers_data)
 
   #Similarity
    similarity_results = calculate_similarity_scores(user_data,inferred_styles,rappers_data)

    #Merge
    final_results = merge_recommendation_scores(kbs_results,similarity_results)
    #Return top 10
    final_results = final_results[:10]
    return {
        "input": user_input.text,
        "detected_topics":user_data["topics"],
        "detected_styles":user_data["styles"],
        "detected_rappers":user_data["rappers"],
        "inferred_styles":list(inferred_styles.keys()),
        "recommendations":final_results}