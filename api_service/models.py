from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class FileData(db.Model):
    __tablename__ = 'file_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
