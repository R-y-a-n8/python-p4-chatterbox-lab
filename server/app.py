from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Chatterbox API!"})

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/messages')
def messages():
    messages = Message.query.all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.get(id)
    if not message:
        return make_response({"error": "Message not found"}, 404)
    return jsonify(message.to_dict())

if __name__ == '__main__':
    app.run(port=5555)
