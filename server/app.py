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
        messages = Message.query.order_by(Message.created_at.asc()).all()

        if messages:
            body = [message.to_dict() for message in messages]
            status = 200
        else:
            body = "No messages found!"
            status = 404

        return make_response(body, status)
    
    if request.method == 'POST':

        requests_json = request.get_json()

        new_message = Message(
            body=requests_json['body'], 
            username=requests_json['username'],
        )
        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict(), 201)



@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    
    if request.method == 'GET':
        message = Message.query.filter_by(id=id).first()

        return make_response(message.to_dict(), 200)
    
    if request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        form_json = request.get_json()

        for key, item in form_json.items():
            setattr(message, key, item)
        
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(), 202)
    
    if request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()

        return make_response("", 204)




if __name__ == '__main__':
    app.run(port=5555)
