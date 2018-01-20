from whiteboard import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_title = db.Column(db.String(), default="")
    message_text = db.Column(db.String(), default="")
    img_url = db.Column(db.String(), default="")
    message_link = db.Column(db.String(), default="")

    viewed = db.Column(db.Boolean(), default=False)
    shared = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return "<MESSAGE %r>" % self.message_text

    def to_dict(self):
        output_dict = {
            "message_title" : self.message_title,
            "message_text": self.message_text,
            "img_url": self.img_url,
            "message_link": self.message_link,
            "id": self.id
        }
        return output_dict