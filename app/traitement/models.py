from app import db

class Traitement(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	content = db.Column(db.String(100))
	done = db.Column(db.Boolean, default=False)
	deleted = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.String(30), db.ForeignKey('user.id'))

	def to_json(self):
		return {
			"id": self.id,
			"content": self.content,
			"deleted": self.deleted,
			"done": self.done
		}