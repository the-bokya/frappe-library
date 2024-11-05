from ..db import conn


def read():
    cur = conn.cursor()
    cur.execute("select memberid, name, registration_timestamp from members")
    members = cur.fetchall()
    cur.close()
    return members


def create(name):
    cur = conn.cursor()
    try:
        cur.execute("insert into members(name) values (?)", (name,))
        id = cur.lastrowid
        print(id)
        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True
