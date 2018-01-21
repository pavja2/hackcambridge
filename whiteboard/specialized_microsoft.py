import json
import requests
import subprocess
import os
import glob

uri_base = 'http://westcentralus.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '09aadc1e91174ff1b8d150f1a52b799c'
}

params = {
    'details' : 'Celebrities,Landmarks',
    'language' : 'en'
}

def split_images_from_slide_to_entities(filename):
    cmd = subprocess.call(['splitter/multicrop.sh', '-d', '30', filename, 'splitter/splits/image_cut.jpg'])
    entity_list = []
    if cmd == 0:
        for filename in os.listdir('splitter/splits/'):
            entity_list.extend(get_unique_entities('splitter/splits/'+ str(filename)))
        files = glob.glob('/splitter/splits/*')
        for f in files:
            os.remove(f)
    return entity_list

def get_unique_entities(filename):
    with open(filename, 'rb') as f:
        body = f.read()
    if body is None:
        return

    unique_entities = []
    # Execute the REST API call and get the response.
    request = requests.post(uri_base + '/vision/v1.0/analyze', params=params, headers=headers, data=body)
    data = request.json()
    print(json.dumps(data))
    # 'data' contains the JSON data. The following formats the JSON data for display.
    if "categories" in data:
        for match in data["categories"]:
            if "detail" in match and "landmarks" in match["detail"]:
                for landmark in match["detail"]["landmarks"]:
                    if "confidence" in landmark and landmark["confidence"] > .5 and "name" in landmark:
                        if landmark["name"] not in unique_entities:
                            unique_entities.append(landmark["name"])
            if "detail" in match and "celebrities" in match["detail"]:
                for celebrity in match["celebrities"]:
                    if "confidence" in celebrity and celebrity["confidence"] > .5 and "name" in celebrity:
                        if landmark["name"] not in unique_entities:
                            unique_entities.append(landmark["name"])
    return unique_entities

#if  __name__ == '__main__':
#    print(split_images_from_slide('/home/ubuntu/uploads/monument_screen.JPG'))