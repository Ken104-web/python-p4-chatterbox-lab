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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.order_by("created_at").all():
             message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at, 
                "updated_at": message.updated_at
            } 
        messages.append(message_dict)
        resp = make_response(
            jsonify(messages),
            200,
        )
        return resp
    elif request.method == 'POST':
        data = request.json
        new_message = Message(
            body=data['body'], 
            username=data['username']
            )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)

    if request.method == 'GET':
        return jsonify(message.to_dict())
    elif request.method == 'PATCH':
        data = request.json
        message.body = data.get('body', message.body)
        db.session.commit()
        return jsonify(message.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({"success": "Message deleted"}), 200)

if __name__ == '__main__':
    app.run(port=5555)