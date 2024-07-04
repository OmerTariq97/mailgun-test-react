from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Mailgun(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(200), nullable = False)
    sent_date = db.Column(db.String(25), nullable = False)
    
    def __repr__(self):
        return f'Task: {self.id}'


@app.route('/mailgun_recieve_email', methods=['POST', 'GET'])
def mailgun_recieve_email():
    payload = request.data
    payload_parsed = json.loads(payload)

    email = payload_parsed['event-data']['recipient']
    subject = payload_parsed['event-data']['message']['headers']['subject']
    timestamp = payload_parsed['event-data']['timestamp']
    print("here", email, subject, timestamp)
    
    new_task = Mailgun(subject = subject, sent_date = timestamp)

    try:
        db.session.add(new_task)
        db.session.commit()
    except:
        return 'an error has occurred'

    return "payload sent"







if __name__ == "__main__":
    app.run(debug=True)
    # app.run()

