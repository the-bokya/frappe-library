from ..db import conn
def read():
    cur = conn.cursor()
    cur.execute("select memberid, name, registration_timestamp from members")
    members = cur.fetchall()
    cur.close()
    return members
