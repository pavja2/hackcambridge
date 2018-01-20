from flask import request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from whiteboard import app
import os
import json

@app.route('/')
def index():
    return "Test Page"


@app.route('/imgupload', methods=["POST"])
def image_upload():
    print("test")
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Upload Failed", 504
        file = request.files['file']

        if file.filename == "":
            return "Upload Failed", 504

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Uploaded to " + str(url_for('uploaded_file', filename=filename))
    else:
        return "Method not allowed", 405

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/messages')
def message_view():
    messages = []
    sample = {
        "message": "Here's a wikipedia page about John Locke!",
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/JohnLocke.png/330px-JohnLocke.png",
        "link": "https://en.wikipedia.org/wiki/John_Locke"
    }
    messages.append(sample)
    return json.dumps(messages), 200
