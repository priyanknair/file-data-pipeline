from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models import FileData


class FileDataSchema(SQLAlchemyAutoSchema):
    created_date = fields.DateTime(attribute='created_date', format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = FileData
        fields = ["id", "name", "created_date"]
