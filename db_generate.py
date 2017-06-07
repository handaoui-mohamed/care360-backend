#!flask/bin/python
from app import db
from app.user.models import User
from app.role.models import Role
import json
import uuid

# drop all tables
db.drop_all()

# create all tables
db.create_all()

# add tags
# with open("tags.json", "r") as tag_json:
#     tags = json.load(tag_json)

# for tag in tags:
#     db.session.add(Tag(name=tag["name"].lower()))
#     db.session.commit()

# create roles
driver_role = Role(name="driver")
patient_role = Role(name="patient")
doctor_role = Role(name="doctor")
admin_role = Role(name="admin")
super_user_role = Role(name="super_user")
db.session.add(driver_role)
db.session.add(patient_role)
db.session.add(doctor_role)
db.session.add(admin_role)
db.session.add(super_user_role)
db.session.commit()

# create super user
super_user = User(id=uuid.uuid4().hex,username="admin",email="care360@contact.com",\
            phone_number="021325487",description="Just a Super User",\
            address="OuedSmar Alger",\
            password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
            first_name="Care 360",last_name="Team",role=super_user_role)
db.session.add(super_user)
db.session.commit()

# create moderator
admin_user = User(id=uuid.uuid4().hex,username="chu_admin",email="admin@chu.dz",\
            phone_number="023646221",description="Just an Admin",\
            password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
            first_name="CHU",last_name="Admin",role=admin_role)

db.session.add(admin_user)
db.session.commit()
