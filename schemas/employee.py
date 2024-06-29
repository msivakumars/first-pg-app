from marshmallow import Schema, fields


class EmployeeSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)