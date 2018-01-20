from flask import request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from whiteboard import app
from whiteboard.models import *
from whiteboard.analysis import analyze_image
import base64
import hashlib
from io import BytesIO
from whiteboard.OCRAPI import OCRAPIfunc

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
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Upload Failed", 504
        file = request.files['file']

        if file.filename == "":
            return "Upload Failed", 504

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            analyze_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Uploaded to " + str(url_for('uploaded_file', filename=filename))
    else:
        return "Method not allowed", 405

@app.route('/base64upload', methods=["POST"])
def base64_upload():
    if request.method == "POST":
        if 'file' not in request.form:
            return "Upload Failed", 504
        base64string = request.form['file']
        print(base64string)
        m = hashlib.md5()
        m.update(base64string.encode('utf-8'))
        filename = os.path.join(app.config['UPLOAD_FOLDER'], str(m.hexdigest()) + str(".jpg"))
        with open(filename, "wb") as fh:
            fh.write(base64.decodebytes(base64string.encode('utf-8')))
        analyze_image(filename)
        return "Uploaded to " + str(url_for('uploaded_file', filename=filename))


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
