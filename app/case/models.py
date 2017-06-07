from app import db


class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship('User', secondary='UserCase', backref='case')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }