from whiteboard.models import Message, db
from whiteboard.entity_linking import entity_linked_messages
from whiteboard.OCRAPI import OCRAPI
import boto3


def analyze_image(filename):
    """
    Parses an image and creates any relevant messages in the database

    :param filename: The name of the file you are downloading
    :return int - the number of messages created
    """
    message_count = 0
    text = get_plaintext(filename)
    print(text)
    #message_count += transcription_analyzer(text)
    message_count+= entity_based_analyzer(text)
    return 1

def entity_based_analyzer(text):
    messages = entity_linked_messages(text)
    for message in messages:
        db.session.add(message)
    db.session.commit()
    return len(messages)

def create_and_save_message(message_text="", img_url="", message_link=""):
    """
    Adds a message to the database
    :param message_text: the text that will be displayed to a user
    :param img_url: any relevant thumbnail images
    :param message_link: the link the user navigates to when they click on a message
    """

    test_message = Message(message_text=message_text, img_url=img_url, message_link=message_link)
    db.session.add(test_message)
    db.session.commit()

def transcription_analyzer(text):
    create_and_save_message(text + " (Automatically Transcribed Via OCR)", "http://via.placeholder.com/350x150.png", "http://google.com")
    return 1

def get_plaintext(filename):
    message_string = OCRAPI(filename)
    return message_string
