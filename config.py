# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = False
SECRET_KEY = 'jlfkjsdlkf@opkzeofkps54654.sfdf168/++'"-è!-èùé'@@@'c;,nsdkjfsgkjrhgriuh"
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    HOST_URL = 'http://localhost:5000/api/v1'
    ERROR_404_HELP=True
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    HOST_URL = 'https://care360-api.herokuapp.com/api/v1'
    ERROR_404_HELP=False
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
SQLALCHEMY_TRACK_MODIFICATIONS=True
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','PNG'])
CORS_HEADERS = 'Content-Type'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
YEAR = 365
DAY = 24
NUM_PAGES = 10
POSTS_PER_PAGE = 12