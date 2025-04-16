import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import urllib.parse
import os
from models import FileData, db
from schemas import FileDataSchema
from utils import get_paginated_query


RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
HOST = os.getenv('DB_HOST', '127.0.0.1')
USER = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', 'root')

app = Flask(__name__)

enc_password = urllib.parse.quote_plus(PASSWORD)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{USER}:{enc_password}@{HOST}:5432/test"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def get_data():
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    name = args.get('name')
    condition = []
    if name:
        condition.append(FileData.name.ilike(f'%{name}%'))
    query = db.session.query(FileData).filter(and_(*condition)).order_by(FileData.created_date.desc())
    paginated_data, count = get_paginated_query(query, page, per_page)
    file_data_schema = FileDataSchema()
    results = file_data_schema.dump(paginated_data, many=True)
    response = {"count": count, "page": page, "per_page": per_page, "results": results}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
