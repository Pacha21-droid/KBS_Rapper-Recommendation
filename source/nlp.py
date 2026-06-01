import json
import spacy
from source.fact import Fact

nlp=spacy.load("en_core_web_sm")
#Load knowledge
with open("knowledge/rappers.json","r",encoding="utf-8") as f:
    rappers_data=json.load(f)

#Extract knowledge
valid_topics=set()
valid_styles=set()
valid_rappers=set()

for rapper in rappers_data:
    rapper_name=rapper["name"].lower()
    valid_rappers.add(rapper_name)
    for topic in rapper["topics"]:
     valid_topics.add(topic.lower())
    for style in rapper["styles"]:
     valid_styles.add(style.lower())

#Process user input
def process_input(input):
   doc=nlp(input.lower())
   extracted_rappers=set()
   extracted_topics=set()
   extracted_styles=set()
   generated_facts=[]
   for token in doc:
      if token.is_punct:
         continue
      #if token.is_stop:
         #continue
      word=token.text.lower().strip()
      if not word: 
        continue
      if word in valid_topics:
       extracted_topics.add(word)
       generated_facts.append(Fact("topic",word))
      if word in valid_styles:
         extracted_styles.add(word)
         generated_facts.append(Fact("style",word))
   lw_txt=input.lower()
   normalized_text=lw_txt.replace(" ","_")
   for style in valid_styles:
      if style in normalized_text:
         extracted_styles.add(style)
         generated_facts.append(Fact("style",style))
   for rapper in valid_rappers:
      if rapper in lw_txt:
         extracted_rappers.add(rapper)
         generated_facts.append(Fact("rapper",rapper))
   return{
      "rappers":list(extracted_rappers),
      "topics":list(extracted_topics),
      "styles":list(extracted_styles),
      "facts":generated_facts}
