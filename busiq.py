from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse, fields, marshal
from flask.ext.restful_extend import support_jsonp
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import or_


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.debug = True
app.config['SQLALCHEMY_ECHO'] = True
api = restful.Api(app)
support_jsonp(api)
db = SQLAlchemy(app)


class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120))

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<Staff %r>' % self.first_name + self.last_name


def getStaffFields():
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
            db_filter = query.filter(Staff.first_name.like('%'+args['first_name']+'%'))
        elif args['last_name']:
            db_filter = query.filter(Staff.last_name.like('%'+args['last_name']+'%'))
        elif args['email']:
            # allow user to use first name or last name to search in email field
            db_filter = query. \
                filter(or_(Staff.first_name.like('%'+args['email']+'%'),
                           Staff.last_name.like('%'+args['email']+'%'),
                           Staff.email.like('%'+args['email']+'%')))
        else:
            return {'staff': {}}

        result = db_filter.order_by(Staff.first_name).all()

        return {'staff': marshal(result, getStaffFields())}

api.add_resource(Busiq, '/', '/staff')


if __name__ == '__main__':
    app.run()
