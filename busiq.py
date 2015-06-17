import os
from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal
from flask.ext.restful_extend import support_jsonp
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri if db_uri else 'sqlite:///test.db'
app.debug = True
app.config['SQLALCHEMY_ECHO'] = True
api = restful.Api(app)
support_jsonp(api)
db = SQLAlchemy(app)


whitelist = []
with open(os.path.dirname(os.path.realpath(__file__)) + '/whitelist.txt') as f:
    lines = f.readlines()
    whitelist = [line.rstrip() for line in lines]


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    employee_id = db.Column(db.String(10))

    def __init__(self, first_name, last_name, email, employee_id):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.employee_id = employee_id

    def __repr__(self):
        return '<Staff %r>' % self.first_name + self.last_name


def getStaffFields():
    """
    For marshal

    :return: fields that we want to jsonify
    """
    return {
        'first_name': fields.String,
        'last_name': fields.String,
        'email': fields.String
    }


parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str)
parser.add_argument('last_name', type=str)
parser.add_argument('email', type=str)


class Busiq(restful.Resource):
    def get(self):
        args = parser.parse_args()
        query = db.session.query(Staff)
        if args['first_name']:
            query = query.filter(Staff.first_name.like(args['first_name']+'%'))
        if args['last_name']:
            query = query.filter(Staff.last_name.like(args['last_name']+'%'))
        if args['email']:
            query = query.filter(Staff.email.like(args['email']+'%'))

        if not args['first_name'] and not args['last_name'] and not args['email']:
            return {'staff': {}}

        # filter empty emails
        query = query.filter(Staff.email.isnot(None))

        # filter based on white list
        clauses = or_(* [Staff.email.like('%' + term + '%') for term in whitelist])
        query = query.filter(clauses)
        # for term in whitelist:
        #     query = query.filter(Staff.email.like('%' + term + '%'))

        result = query.order_by(Staff.first_name).limit(30).all()

        return {'staff': marshal(result, getStaffFields())}

api.add_resource(Busiq, '/', '/staff')


if __name__ == '__main__':
    app.run()
