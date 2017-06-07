#!/usr/bin/env python
import os
from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g, send_from_directory
from werkzeug import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, basedir
from models import PostUpload, ProfilePicture
from serializers import upload_filename, post_file, profile_image, user_file
from app.user.decorators import login_required, admin_required


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# Posts files upload
post_upload_api = api.namespace('posts/uploads', description="Upload picture for a post")

@post_upload_api.route('/<string:post_id>')
class UploadPost(Resource):
    @post_upload_api.expect(authorization, post_file)
    @login_required
    def post(self, post_id):
        """
        Upload a cover image for a post
        """
        file = post_file.parse_args()['post_image']
        post = Post.query.get(post_id)
        if g.user.id is not post.user.id:
            abort(403)
        filename = uploadFile(file, os.path.join(basedir, UPLOAD_FOLDER, 'post', post_id), post)
        uploaded_image = PostUpload(name=filename,post=post,user=g.user)
        db.session.add(uploaded_image)
        db.session.commit()
        return {'element':post.to_json()}

    @post_upload_api.expect(authorization)
    @login_required
    def delete(self, post_id):
        """
        Deletes a post image
        """
        file = PostUpload.query.filter_by(post_id=post_id).first()
        if g.user.id is not file.user_id:
            abort(403)
        if not file:
            abort(404)
        db.session.delete(file)
        db.session.commit()
        file_path = os.path.join(basedir, UPLOAD_FOLDER, 'post', post_id, file.name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return '', 204

    @post_upload_api.expect(upload_filename)
    def get(self, post_id):
        """
        Returns a post image
        """
        filename = upload_filename.parse_args()['filename']
        directory = os.path.join(basedir, UPLOAD_FOLDER, 'post', post_id)
        return send_from_directory(directory, filename)

# profile picture upload
profile_image_api = api.namespace("profile/uploads", description="Upload picture for a user\'s profile")

@profile_image_api.route('')
class UploadProfile(Resource):
    @profile_image_api.expect(authorization,profile_image)
    @login_required
    def post(self):
        """
        Upload a profile image
        """
        file = profile_image.parse_args()['profile_image']
        filename = uploadFile(file, os.path.join(basedir, UPLOAD_FOLDER, g.user.username, 'profile'), g.user)
        uploaded_image = ProfilePicture(name=filename,user=g.user)
        db.session.add(uploaded_image)
        db.session.commit()
        return {'element':g.user.to_json()}
    
    @profile_image_api.expect(user_file)
    def get(self):
        """
        Return profile image
        """
        parse = user_file.parse_args()
        username = parse["username"]
        filename = parse["filename"]
        directory = os.path.join(basedir, UPLOAD_FOLDER, username, 'profile')
        return send_from_directory(directory, filename)


# upload files function
def uploadFile(file, path, owner):
    if not file or not allowed_file(file.filename):
        abort(400)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        directory = path
        if os.path.exists(directory):
            old_picture = owner.image
            file_path = os.path.join(directory, old_picture.name)
            db.session.delete(old_picture)
            db.session.commit()
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            os.makedirs(directory)
        file_path = os.path.join(directory, filename)
        file.save(file_path)
    return filename