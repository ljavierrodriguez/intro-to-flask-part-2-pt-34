import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db, User

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') if os.getenv('DATABASE_URI') else "sqlite:///database.db"

db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade

# Windows = SET FLASK_APP=src/app.py
# Mac o Linux = export FLASK_APP=src/app.py


@app.route('/')
def main():
    return jsonify({ "message": "Welcome to Flask App"});

@app.route('/api/users/search')
def search_users():
    q = request.args.get('q') # query string

    users = User.query.filter_by(email=q) # [<User 2>]
    users = list(map(lambda user: user.serialize(), users)) # [{"id": 2, "email": "john.doe@gmail.com", "is_active": true }]

    return jsonify(users), 200


@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    datos = request.get_json()

    user = User() # Crear un nuevo objeto de tipo usuario 
    user.email = datos['email']
    user.password = datos['password']
    user.is_active = datos['is_active']
    user.save()

    #db.session.add(user)
    #db.session.commit()

    return jsonify({ "msg": "User created", "user": user.serialize()}), 201

@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    datos = request.get_json()

    user = User.query.get(id)
    user.email = datos['email'] if datos['email'] else user.email  
    user.password = datos['password'] if datos['password'] else user.password  
    user.is_active = datos['is_active'] if datos['is_active'] else user.is_active
    user.update()

    #db.session.add(user)
    #db.session.commit()

    return jsonify({ "msg": "User updated", "user": user.serialize()}), 200

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    user.delete()
    return jsonify({ "msg": "User deleted", "user": {}}), 200


if __name__ == '__main__':
    app.run()