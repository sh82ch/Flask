from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
uname = os.getenv('USER_NAME')
pword = os.getenv('PASSWORD')
hst = os.getenv("HOST")
dbname = os.getenv("DB_NAME")
print(uname, pword, hst, dbname)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{uname}:{pword}@{hst}/{dbname}'
db = SQLAlchemy(app)

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.String(255), nullable=False)

    def __init__(self, title, description, owner):
        self.title = title
        self.description = description
        self.owner = owner

@app.route('/advertisements', methods=['POST'])
def create_advertisement():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    owner = data.get('owner')

    if not title or not description or not owner:
        return jsonify({'error': 'Не указаны все обязательные поля'}), 400

    advertisement = Advertisement(title=title, description=description, owner=owner)
    db.session.add(advertisement)
    db.session.commit()

    return jsonify({'message': 'Объявление успешно создано'}), 201

@app.route('/advertisements/<int:advertisement_id>', methods=['GET'])
def get_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if not advertisement:
        return jsonify({'error': 'Объявление не найдено'}), 404
    advertisement_data = {
        'id': advertisement.id,
        'title': advertisement.title,
        'description': advertisement.description,
        'date_created': advertisement.date_created.isoformat(),
        'owner': advertisement.owner
    }

    return jsonify(advertisement_data), 200

@app.route('/advertisements/<int:advertisement_id>', methods=['DELETE'])
def delete_advertisement(advertisement_id):
    advertisement = Advertisement.query.get(advertisement_id)
    if not advertisement:
        return jsonify({'error': 'Объявление не найдено'}), 404
    db.session.delete(advertisement)
    db.session.commit()

    return jsonify({'message': 'Объявление успешно удалено'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
