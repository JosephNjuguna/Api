from flask import Flask, jsonify,json, render_template, flash, redirect, request, url_for, session, logging, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import jwt
import datetime
from functools import wraps
from flask_restful import Api,Resource
from data import ClassName

app = Flask(__name__)
api = Api(app)

data = ClassName.user_info()

User = {}

signup = {}
signin = {}

"""def token_required(f):
    @wraps(f)
    def decorated(*args , **kwargs):
        token = None
        if 'x-access-token' in request.headers:
             token  = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'Token is missing'}),401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id = data['public_id']),first()
        except:
            return jsonify({'invalid token': "token is invalid"}),401
            return f(current_user,*args, **kwargs)
        return decorated
"""
class SignUp(Resource):
    def post(self):
        userdata = request.get_json()
        hashed_password = generate_password_hash(userdata['password'], method = 'sha256')
        User = {
            'public_id': str(uuid.uuid4()),
            'name' : userdata['name'],
            'password' : hashed_password,
            'admin' :  False
        }
        data.append(User)
        return jsonify({' users register detail': User})

class SignIn(Resource):
    def post(self):
        auth = request.get_json()
        #hashed_password = generate_password_hash(auth['password'], method = 'sha256')
        username = auth['name']

        for name in data:
            if name['name'] == username:
                return jsonify({"message":"user found in db"})
        else:
            return jsonify({"message":"user not found in db"})

class allUsers(Resource):
    def get(self):
        return jsonify({'users': data})

class singleuser(Resource):
    def get(self,public_id):
        singleuser = [userid for userid in data if userid['public_id'] == id]
        return jsonify({'user': singleuser[0]})

    def put(self,public_id):
        for userid in data:
            if userid['public_id'] == public_id:
                nameupdate = {}
                name = request.get_json()
                userid['name'] = name['name']
                return jsonify({"updated":userid})
        else:
            return ("message not found user")
    def delete(self,public_id):
        for i,userid in enumerate(data):
            if userid['public_id'] == public_id:
                data.pop(i)
                return ("deleted")

        return ("message not found user")

api.add_resource(SignUp, '/register', '/register/')
api.add_resource(SignIn, '/login' , '/login/')
api.add_resource(allUsers, '/users' , '/users/')
api.add_resource(singleuser, '/users/<string:public_id>' , '/users/<string:public_id>/')


if __name__ == '__main__':
    app.run(debug = True)
