from . import db
import uuid


def generate_id():
    return str(uuid.uuid4())[:8]


class DecisionInstance(db.Model):
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    name = db.Column(db.String(100))
    scale = db.Column(db.String(200))  # comma-separated scale labels
    creator_id = db.Column(db.String(100))


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    description = db.Column(db.Text)
    decision_id = db.Column(db.String(8), db.ForeignKey('decision_instance.id'))


class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))
    score = db.Column(db.Integer)
    decision_id = db.Column(db.String(8))
