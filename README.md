FluidReview Business Email Query
================================

Configuration
-------------

To change the database, edit DATABASE__URI in the environment variable.

Update Local Database
---------------------

The database content is pulled from IAM Oracle database. The content is updated daily by a cron job under root account. In case there is a need of manually updating the local database, run the following command:

    cd /path/to/busiq
    PYTHONUNBUFFERED=1 python dbupdate.py

Make sure the ORACLE_URI and SQLITE3_URI environment variables are set. On production server, they are set in /etc/profile.d/busiq.sh.

Deployment
----------

The production deployment is using uwsgi and nginx. The setting is /etc/uwsig.conf. The config file contains settings to run uwsgi server and the environment variables for the app config as well.

To deploy the script, include the following line on FluidReview page where the invitation form is presented.

    <script src="http://busiq.ctlt.ubc.ca/static/js/busiq.js"></script>

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

Note you may need to change the script URLs in the two html files to point to the local file instead of busiq.ctlt.ubc.ca