import os
import sys
import cx_Oracle
import sqlite3

insert_prefix = 'INSERT INTO staff (first_name, last_name, email) VALUES '
inserts = []

ora_uri = os.environ.get('ORACLE_URI')
ora_conn = cx_Oracle.connect(ora_uri)

sqlite_uri = os.environ.get('SQLITE3_URI')
sqlite_conn = sqlite3.connect(sqlite_uri)

sqlite_conn.execute('DELETE FROM staff')

ora_cur = ora_conn.cursor()
ora_cur.execute("select * from CTLT_IAM_EMAIL_LOOKUP")


def sqlite_insert(rows):
    sqlite_conn.execute(insert_prefix + ','.join(rows))
    sqlite_conn.commit()


for i, result in enumerate(ora_cur):
    inserts.append('(' + ','.join('"' + item + '"' for item in result) + ')')
    if i % 50 == 0:
        sys.stdout.write('.')
        sqlite_insert(inserts)
        del inserts[:]

sqlite_insert(inserts)
del inserts[:]

ora_cur.close()

sqlite_conn.close()
ora_conn.close()

print 'Done'