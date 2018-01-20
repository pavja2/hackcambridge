from flask import request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from whiteboard import app
from whiteboard.models import *
from whiteboard.analysis import analyze_image
import os
import json


@app.cli.command("initdb")
def initdb():
    """
    Creates a basic empty database / deletes existing one
    """
    db.drop_all()
    db.create_all()


@app.route('/', methods=["GET"])
def index():
    return app.send_static_file('userinterface.html')

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
            analyze_image(filename)
            return "Uploaded to " + str(url_for('uploaded_file', filename=filename))
    else:
        return "Method not allowed", 405

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/messages')
def message_view():
    messages = []
    for message in Message.query.all():
        messages.append(message.to_dict())
        message.viewed = True
        db.session.commit()
    message_dict = {"messages": messages}
    return json.dumps(message_dict), 200
