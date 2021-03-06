from flask import request, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from whiteboard import app
from whiteboard.models import *
from whiteboard.analysis import analyze_image
import base64
import hashlib
from whiteboard.spark_integrator import share_knowledge_with_class

import os
import json

class_chat_room = 'a51b4260-fe2d-11e7-9895-63f133b158d1'

@app.cli.command("initdb")
def initdb():
    """
    Creates a basic empty database / deletes existing one
    """
    db.drop_all()
    db.create_all()


@app.route('/testui')
def uitest():
    return app.send_static_file('ui_design.html')

@app.route('/', methods=["GET"])
def index():
    return app.send_static_file('ui_design.html')

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


@app.route('/share_message', methods=["POST"])
def share_message():
    if request.method == "POST":
        if 'id' not in request.form:
            return "Missing ID", 502

        output_message = Message.query.filter_by(id=request.form["id"]).first()
        if output_message is None:
            return "Invalid ID", 502
        share_knowledge_with_class(output_message, class_chat_room)
        output_message.shared = True
        db.session.commit()
        return "Message Shared", 200

@app.route('/hide_message', methods=["POST"])
def hide_message():
    if request.method == "POST":
        if 'id' not in request.form:
            return "Missing ID", 502
        output_message = Message.query.filter_by(id=request.form["id"]).first()
        output_message.hidden = True
        db.session.commit()
        return "Message Hidden", 200

@app.route('/clear_messages', methods=["POST"])
def clear_messages():
    if request.method == "POST":
        db.drop_all()
        db.create_all()

@app.route('/messages')
def message_view():
    messages = []
    for message in Message.query.filter_by(hidden=False).all():
        messages.append(message.to_dict())
        message.viewed = True
        db.session.commit()
    output_dict = {"results" : {"messages": messages}}
    return json.dumps(output_dict), 200
