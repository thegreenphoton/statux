#for machine learning model
from sklearn import svm
import pandas as pd

import spacy
from spacy.training.example import Example
from trainForCompanyExtraction import TRAIN_DATA




#company and position extraction model using spacy 

    #load blank spacy model
""" nlp = spacy.blank("en")

    #create NER component
ner = nlp.add_pipe("ner")

    #add labels to NER component
ner.add_label("ORG")
ner.add_label("JOB")

    #training loop
optimizer = nlp.begin_training()

for epoch in range(10):
    for text, annotations in TRAIN_DATA:
        
        example = Example.from_dict(nlp.make_doc(text), annotations)
        nlp.update([example], sgd=optimizer)
        

nlp.to_disk("custom_ner_model") """

nlp = spacy.load("custom_ner_model")
def extract_name_from_custom_nlp(email_content):
    doc = nlp(email_content)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text.strip()
    return None

#structure and load data from CSV files 
