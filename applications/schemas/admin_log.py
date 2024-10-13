from applications.extensions import ma
from marshmallow import fields


class LogOutSchema(ma.Schema):
    id = fields.Integer()
    method = fields.Str()
    uid = fields.Str()
    url = fields.Str()
    desc = fields.Str()
    ip = fields.Str()
    user_agent = fields.Str()
    success = fields.Bool()
    create_time = fields.DateTime()

class LogApiSchema(ma.Schema):
    id = fields.Integer()
    method = fields.Str()
    uid = fields.Str()
    url = fields.Str()
    request_body = fields.Str()
    response_body = fields.Str()
    starttime = fields.Str()
    endtime = fields.Str()
    totaltime = fields.Str()
    tips = fields.Str()
    success = fields.Bool()
