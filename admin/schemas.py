from app import ma
from marshmallow import Schema, fields


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email()
    phone = fields.String()
    full_name = fields.String()
    avatar = fields.String()
    username = fields.String()
    role = fields.Integer()
    gender = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    # last_login = fields.DateTime()


user_schema = UserSchema()
users_schema = UserSchema(many=True)
