from whiteboard import app
from urllib.parse import quote
from whiteboard.models import Message
import requests

headers = {
    # Request headers
    'Content-Type': 'text/plain',
    'Ocp-Apim-Subscription-Key': app.config["MICROSOFT_ENTITY_KEY"],
}

params = {
}

wiki_base = "https://en.wikipedia.org/wiki/"

url_base = 'https://westus.api.cognitive.microsoft.com'

def fetch_wiki_entities(text):
    entity_list = []
    seen_ids = set([])
    request = requests.post(url_base+'/entitylinking/v1.0/link', params=params, data=text, headers=headers)
    data = request.json()
    print(request.text)
    if "entities" in data:
        for entity in data["entities"]:
            if "name" in entity and "score" in entity and entity["score"] > .1:
                name = entity["name"]
                wikiId = ""
                if "wikipediaId" in entity:
                    wikiId = entity["wikipediaId"]
                if wikiId == "" or wikiId not in seen_ids:
                    seen_ids.add(wikiId)
                    entity_list.append((name, wikiId))
    return entity_list


def entity_linked_messages(text):
    message_list = []
    entity_list = fetch_wiki_entities(text)
    for entity in entity_list:
        if entity[1] != "":
            wiki_link = wiki_base + quote(entity[1])
            new_message = Message(message_title="Here's the wiki for: " + str(entity[0]), message_text="",
                                  img_url="", message_link=wiki_link)
            message_list.append(new_message)
    return message_list

if __name__ == "__main__":
    sample_text = "King Charles I of England, George Washington - First president"
    print(fetch_wiki_entities(sample_text))