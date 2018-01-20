from whiteboard.models import Message, db


def analyze_image(filename):
    """
    Parses an image and creates any relevant messages in the database

    :param filename: The name of the file you are downloading
    :return int - the number of messages created
    """
    test_message = Message(message_text="Test Message", img_url="http://via.placeholder.com/350x150.png", message_link="http://google.com")
    db.session.add(test_message)
    db.session.commit()
    return 1


def create_and_save_message(message_text="", img_url="", message_link=""):
    """
    Adds a message to the database
    :param message_text: the text that will be displayed to a user
    :param img_url: any relevant thumbnail images
    :param message_link: the link the user navigates to when they click on a message
    """

    test_message = Message(message_text, img_url, message_link)
    db.session.add(test_message)
    db.session.commit()
