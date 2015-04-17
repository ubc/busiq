FluidReview Business Email Query
================================

Configuration
-------------

To change the database, edit SQLALCHEMY_DATABASE__URI in busiq.py

Development
-----------

Create database structure and populate database:

    python
    >>> from busiq import db, Staff
    >>> db.create_all()
    >>> staff = Staff('John', 'Smith', 'john.smith@ubc.ca')
    >>> db.session.add(staff)
    >>> db.session.commit()
    
Start the backend server

    python busiq.py
    
This will run backend server at localhost:5000

    open static/index.html
    
Will open the test page. When typing in the first or last name field, an ajax request should be send to backend server to populate the dropdown list.
