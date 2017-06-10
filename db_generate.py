# -*- coding: utf-8 -*-
#!flask/bin/python
from app import db
from app.user.models import User
from app.role.models import Role
from app.case.models import Case
from app.traitement.models import Traitement
from app.sample.models import Sample
import json
import uuid

# drop all tables
db.drop_all()

# create all tables
db.create_all()

alzheimer = Case(name='Alzheimer')
pregnancy = Case(name='Grossesse')
diabetic = Case(name='Diabetique')
db.session.add(alzheimer)
db.session.add(pregnancy)
db.session.add(diabetic)
db.session.commit()

# create roles
patient_role = Role(name="patient")
doctor_role = Role(name="doctor")
driver_role = Role(name="driver")
admin_role = Role(name="admin")
super_user_role = Role(name="super_user")
db.session.add(patient_role)
db.session.add(doctor_role)
db.session.add(admin_role)
db.session.add(driver_role)
db.session.add(super_user_role)
db.session.commit()

# create super user
super_user = User(id=uuid.uuid4().hex, username="admin", email="care360@contact.com",
                  phone_number="021325487", description="Just a Super User",
                  address="OuedSmar Alger",
                  password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
                  first_name="Care 360", last_name="Team", role=super_user_role)
db.session.add(super_user)
db.session.commit()

# create moderator
admin_user = User(id=uuid.uuid4().hex, username="chu_admin", email="admin@chu.dz",
                  phone_number="023646221", description="Just an Admin",
                  password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
                  first_name="CHU", last_name="Admin", role=admin_role)

db.session.add(admin_user)
db.session.commit()

doctor_user = User(id=uuid.uuid4().hex, username="doctor", email="doctor@chu.dz",
                   phone_number="023646221", description="Just a Doctor",
                   password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
                   first_name="Karim", last_name="toubib", role=doctor_role)
doctor_user.add_cases([1])
db.session.add(doctor_user)
db.session.commit()

patient_user = User(id=uuid.uuid4().hex, username="patient", email="patient@chu.dz",
                    phone_number="023646221", description="Just a patient",address="OuedSmar",
                    password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",birthday="29/02/1987",
                    first_name="Amina", last_name="Abdellaoui", role=patient_role)
patient_user.add_cases([2, 3])
db.session.add(patient_user)
db.session.commit()

# add users
with open("users.json", "r") as users_json:
    users = json.load(users_json)

for user in users:
    new_user = User(id=uuid.uuid4().hex, username=user['username'], email=user['email'],
                first_name=user['first_name'], last_name=user['last_name'], address=user['address'],
                role_id=user['role'], birthday=user['birthday'], description=user['description'], phone_number=user['phone_number'])
    new_user.hash_password(user['password'])

    cases = user['cases']
    if cases:
        new_user.add_cases(cases)
    db.session.add(new_user)
    db.session.commit()

with open("traitement.json", "r") as traitement_json:
    traitements = json.load(traitement_json)

for traitement in traitements:
    db.session.add(Traitement(content=traitement['content'],done=traitement["done"],deleted=traitement["deleted"],user_id=patient_user.id))
    db.session.commit()

with open("samples.json", "r") as samples_json:
    samples = json.load(samples_json)

for sample in samples:
    db.session.add(Sample(value=sample['value'],type=sample["type"],user_id=patient_user.id))
    db.session.commit()