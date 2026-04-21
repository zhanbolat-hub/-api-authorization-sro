api-authorization-sro/
│
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
│
├── models/
│   └── user.py
│
├── routes/
│   ├── auth.py
│   └── protected.py
│
├── database/
│   └── db.sqlite3
│
└── .gitignore
  class Config:
    SECRET_KEY = "secret-key"
    JWT_SECRET_KEY = "jwt-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
from flask import Flask
from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from routes.protected import protected_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(protected_bp)

# База құру
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
  from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
      from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(username=data["username"])
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        token = create_access_token(identity=user.username)
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user = get_jwt_identity()
    return jsonify(msg="Access granted", user=user)
Flask
flask-jwt-extended
flask-sqlalchemy
werkzeug
venv/
__pycache__/
*.pyc
instance/
pip install -r requirements.txt
python app.py
