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

# Add a route for the root URL to prevent the 404 error
@app.route('/')
def home():
    return "Welcome to the Flask API"

@app.route('/messages')
def messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    message = Message.query.get(id)
    if message:
        return jsonify(message.to_dict())
    else:
        return jsonify({"error": "Message not found"}), 404

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if message:
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict())
    else:
        return jsonify({"error": "Message not found"}), 404

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "Message deleted"}), 200
    else:
        return jsonify({"error": "Message not found"}), 404

if __name__ == '__main__':
    app.run(port=5555)
