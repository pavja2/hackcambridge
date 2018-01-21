from whiteboard.models import Message, db
from whiteboard.entity_linking import entity_linked_messages
from whiteboard.OCRAPI import OCRAPIfunc
from whiteboard.NLP import NLPfun
from whiteboard.NLPAPI import keyWordExtractorAPI
from whiteboard.aws_comprehend import get_key_terms, get_named_entities
from whiteboard.country_finder import get_countries_from_text
from whiteboard.WikipediaAPI import WikipediaAPIfunc
from whiteboard.KnowledgeGraphAPI import academiaTest
from whiteboard.CrossRefAPI import CrossRefAPIfunc
from whiteboard.specialized_microsoft import split_images_from_slide_to_entities
import boto3


def analyze_image(filename):
    """
    Parses an image and creates any relevant messages in the database

    :param filename: The name of the file you are downloading
    :return int - the number of messages created
    """
    message_count = 0
    text = "AS291asd1adf   " + str(get_plaintext(filename))

    wiki_conflicts = []
    author_conflicts = []
    country_conflicts = []
    element_conflicts = []

    #get_microsoft_wikipedia_messages
    wiki_conflicts.extend(entity_based_analyzer(text, conflicts=wiki_conflicts))

    # AWS Entities
    aws_entities = get_named_entities(text)
    for entity in aws_entities:
        # if the entity is not in wiki conflicts, see if there's a wki page option
        if entity[0] not in wiki_conflicts:
            wiki_conflicts.extend(wikify_entry(entity[0], wiki_conflicts))
        if entity not in author_conflicts and len(entity[0].split()) <= 4:
            if academiaTest(entity[0]):
                author_conflicts.append(entity[0])
                url, title, authors, date = CrossRefAPIfunc(entity[0])
                if url and title is not None:
                    if Message.query.filter_by(message_title="Relevant Publication: " + str(title), message_text="Authors: " +  str(authors) + " Date: " + str(date),
                                               message_link=url).first() is None:
                        create_and_save_message("Relevant Publication: " + str(title),
                                                          "Authors: " +  str(authors) + " Date: " + str(date),
                                                          img_url="http://via.placeholder.com/350x150.png",
                                                          message_link=url)

    # MS Named Entities
    for entity in keyWordExtractorAPI(text):
        if entity not in wiki_conflicts:
            wiki_conflicts.extend(wikify_entry(entity, wiki_conflicts))
        if entity not in author_conflicts and len(entity.split()) <= 4:
            if academiaTest(entity):
                author_conflicts.append(entity)
                url, title, authors, date = CrossRefAPIfunc(entity)
                if url and title is not None:
                    if Message.query.filter_by(message_title="Relevant Publication: " + str(title),
                                               message_text=  "Authors: " +  str(authors) + " Date: " + str(date),
                                               message_link=url).first() is None:
                        create_and_save_message("Relevant Publication: " + str(title),
                                                          "Authors: " +  str(authors) + " Date: " + str(date),
                                                          img_url="http://via.placeholder.com/350x150.png",
                                                          message_link=url)

    # Analyze Country information
    country_analyzer(text, country_conflicts)

    #MS Image Splitting
    # IF buggy, uncomment due to OS compatibility challenges
    try:
        specialized_entities = split_images_from_slide_to_entities(filename)
        print(specialized_entities)
    except:
        specialized_entities = []
    for entity in specialized_entities:
        if entity not in wiki_conflicts:
            wiki_conflicts.extend(wikify_entry(entity, wiki_conflicts))
        if entity not in author_conflicts and len(entity.split()) <= 4:
            if academiaTest(entity):
                author_conflicts.append(entity)
                url, title, authors, date = CrossRefAPIfunc(entity)
                if url and title is not None:
                    if Message.query.filter_by(message_title="Relevant Publication: " + str(title),
                                               message_text=  "Authors: " +  str(authors) + " Date: " + str(date),
                                               message_link=url).first() is None:
                        create_and_save_message("Relevant Publication: " + str(title),
                                                          "Authors: " +  str(authors) + " Date: " + str(date),
                                                          img_url="http://via.placeholder.com/350x150.png",
                                                          message_link=url)

    return 1


def entity_based_analyzer(text, conflicts=[]):
    messages = entity_linked_messages(text)
    conflicts = []
    for message in messages:
        if message.message_title in conflicts:
            continue
        else:
            conflicts.append(message.message_title)
            if Message.query.filter_by(message_title=message.message_title, message_text=message.message_text, message_link=message.message_link).first() is None:
                db.session.add(message)
    db.session.commit()
    return conflicts


def nlp_analyzer(filename):
    titles, extracts, images, urls = NLPfun(filename)
    for i in range(0, len(titles)):
        create_and_save_message(message_title="Some info about " + str(titles[i]), message_text=str(extracts[i]), img_url=images[i], message_link=urls[i])
    return len(titles)

def country_analyzer(text, conflicts=[]):
    messages = get_countries_from_text(text)
    conflicts = conflicts
    for message in messages:
        if message.message_title in conflicts:
            continue
        else:
            conflicts.append(message.message_title)
            if Message.query.filter_by(message_title=message.message_title, message_text=message.message_text, message_link=message.message_link).first() is None:
                db.session.add(message)
            db.session.commit()
    return conflicts

def wikify_entry(text_entity, conflicts=[]):
    conflicts = conflicts
    title, extract, img_url, wiki_path = WikipediaAPIfunc(text_entity)
    if title is not None and len(title) > 2 and "may refer to:" not in extract[:32] and wiki_path is not None:
        conflicts.append(title)
        if Message.query.filter_by(message_title=title, message_text=extract,
                                   message_link=img_url).first() is None:
            create_and_save_message(title, extract, img_url, wiki_path)
    return conflicts

def create_and_save_message(message_title="", message_text="", img_url="", message_link=""):
    """
    Adds a message to the database
    :param message_text: the text that will be displayed to a user
    :param img_url: any relevant thumbnail images
    :param message_link: the link the user navigates to when they click on a message
    """

    test_message = Message(message_title=message_title, message_text=message_text, img_url=img_url, message_link=message_link)
    db.session.add(test_message)
    db.session.commit()

def transcription_analyzer(text):
    create_and_save_message(text + " (Automatically Transcribed Via OCR)", "http://via.placeholder.com/350x150.png", "http://google.com")
    return 1

def get_plaintext(filename):
    message_string = OCRAPIfunc(filename)
    return message_string
