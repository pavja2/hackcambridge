import boto3
import json

from whiteboard import app

comprehend = boto3.client(service_name='comprehend', region_name="us-east-1",
                          aws_access_key_id=app.config["AWS_ACCESS_KEY"],
                          aws_secret_access_key=app.config["AWS_SECRET_KEY"],
                          )

def get_key_terms(text):
    terms = []
    api_result = comprehend.detect_key_phrases(Text=text, LanguageCode='en')

    if "KeyPhrases" in api_result:
        for phrase in api_result["KeyPhrases"]:
            if "Score" in phrase and phrase["Score"] > .01 and "Text" in phrase:
                terms.append(phrase["Text"])
    return terms


def get_named_entities(text):
    terms =  []
    api_result = comprehend.detect_entities(Text=text, LanguageCode='en')
    if "Entities" in api_result:
        for entity in api_result["Entities"]:
            if "Score" in entity and entity["Score"] > .1 and "Text" in entity and "Type" in entity:
                terms.append((entity["Text"], entity["Type"]))
    return terms
