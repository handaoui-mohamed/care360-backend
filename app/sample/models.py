from app import db
import datetime

class Sample(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	value = db.Column(db.Float, default=0)
	type = db.Column(db.String(20))
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	user_id = db.Column(db.String(50),db.ForeignKey('user.id'))

	def to_json(self):
		return {
			"id": self.id,
			"value": self.value,
			"type": self.type,
			"date": str(self.date)
		} 