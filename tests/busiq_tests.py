from flask import json
from busiq import app, db, Staff
import unittest


class BusiqTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['TESTING'] = True
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_query(self):
        expected = {
            "staff": [
                {
                    "email": "test@ubc.ca",
                    "first_name": "First",
                    "last_name": "Last,"
                }
            ]
        }
        staff = Staff('First', 'Last,', 'test@ubc.ca', '1234567')
        db.session.add(staff)
        db.session.commit()

        # search by first name
        rv = self.client.get('/', data={'first_name': 'First'})
        self.assertEqual(json.loads(rv.data), expected)

        # search by last name
        rv = self.client.get('/', data={'last_name': 'Last'})
        self.assertEqual(json.loads(rv.data), expected)

        # search by email
        rv = self.client.get('/', data={'email': 'test@ubc.ca'})
        self.assertEqual(json.loads(rv.data), expected)

        # search by names
        rv = self.client.get('/', data={'first_name': 'First', 'last_name': 'Last'})
        self.assertEqual(json.loads(rv.data), expected)

        # search by partial
        rv = self.client.get('/', data={'first_name': 'Fir', 'last_name': 'L'})
        self.assertEqual(json.loads(rv.data), expected)

    def test_query_not_on_whitelist(self):
        expected = {
            "staff": [
            ]
        }
        staff = Staff('First', 'Last,', 'test@gmail.com', '1234567')
        db.session.add(staff)
        db.session.commit()

        # search by first name
        rv = self.client.get('/', data={'first_name': 'First'})
        self.assertEqual(json.loads(rv.data), expected)

if __name__ == '__main__':
    unittest.main()
