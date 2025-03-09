from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)

# User model definition
class User(db.Model):
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(80), nullable = False)
    password_hash = db.Column(db.String(120), nullable=False)
    angelapi = db.Column(db.String(120))
    angelusername = db.Column(db.String(120))
    angelpassword = db.Column(db.String(120))
    angeltoken = db.Column(db.String(120))

    def __repr__(self):
        return f'<User {self.id}>'

# User registration endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or 'id' not in data or 'password' not in data:
        return jsonify({'message': 'ID and password are required.'}), 400

    if User.query.get(data['id']):
        return jsonify({'message': 'User ID already exists.'}), 409

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        password_hash=hashed_password,
        angelapi=data.get('angelapi'),
        angelusername=data.get('angelusername'),
        angelpassword=data.get('angelpassword'),
        angeltoken=data.get('angeltoken')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

# User authentication endpoint
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data or 'id' not in data or 'password' not in data:
        return jsonify({'message': 'ID and password are required.'}), 400

    user = User.query.get(data['id'])
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Login successful.', "status": True}), 200
    else:
        return jsonify({'message': 'Invalid ID or password.', "status": False}), 401

if __name__ == '__main__':
    app.run(debug=True)
