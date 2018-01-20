import requests
import json
from whiteboard.models import Message

access_token = 'YzY3ZTJiMmUtOWI0Yy00ZWNmLWI1MzUtM2Q0MjQ4ZTg0NTdlNmY1OTM5YjQtMTZm'
headers = {
    "Content-type": "application/json; charset=utf-8",
    "Authorization": "Bearer YzY3ZTJiMmUtOWI0Yy00ZWNmLWI1MzUtM2Q0MjQ4ZTg0NTdlNmY1OTM5YjQtMTZm"
}

messaging_url = 'https://api.ciscospark.com/v1/messages'

def share_knowledge_with_class(message, room_id):
    request_string = f'### A Classmate shared some knowledge!\n' \
                     f'**{message.message_title}**\n\n' \
                     f'{message.message_text}\n\n' \
                     f'[More Info]({message.message_link})'

    params = {
        "roomId" : "a51b4260-fe2d-11e7-9895-63f133b158d1",
        "markdown": request_string
        #"file": message.img_url
    }

    request = requests.post(messaging_url, data=json.dumps(params), headers=headers)
    print(request.text)

if __name__ == '__main__':
    test_message = Message(message_title="Test Message", message_text="Test message body with information about things.",
                           img_url="http://via.placeholder.com/350x150.png", message_link="http://google.com")
    share_knowledge_with_class(test_message, 'a51b4260-fe2d-11e7-9895-63f133b158d1')
