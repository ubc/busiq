import os
import sys
import cx_Oracle
import sqlite3
from math import ceil

# insert 50 record at a time
batch_num = 50
insert_prefix = 'INSERT INTO staff (first_name, last_name, email, employee_id) VALUES (?, ?, ?, ?)'
inserts = []

ora_uri = os.environ.get('ORACLE_URI')
ora_conn = cx_Oracle.connect(ora_uri)

sqlite_uri = os.environ.get('SQLITE3_URI')
sqlite_conn = sqlite3.connect(sqlite_uri)

sqlite_conn.execute('DELETE FROM staff')

ora_cur = ora_conn.cursor()
ora_cur.execute("select * from CTLT_IAM_EMAIL_LOOKUP")


def sqlite_insert(rows):
    # sqlite that comes with python 2.6 doesn't support insert multiple rows in one insert
    # so one insert at a time
    # for row in rows:
    #     clean_row = [item if item is not None else 'NULL' for item in row]
    #     sqlite_conn.execute(insert_prefix + '(' + ','.join('"' + item + '"' for item in clean_row) + ')')
    sqlite_conn.executemany(insert_prefix, rows)
    sqlite_conn.commit()


for i, result in enumerate(ora_cur):
    inserts.append(result)
    if i % batch_num == 0:
        sys.stdout.write('.')
        sqlite_insert(inserts)
        del inserts[:]

sqlite_insert(inserts)
del inserts[:]

ora_cur.close()

sqlite_conn.close()
ora_conn.close()

print 'Done'
