from ..db import conn


def read():
    cur = conn.cursor()
    cur.execute("select memberid, name, registration_timestamp, pending_books, due_amount from members_view")
    members = cur.fetchall()
    cur.close()
    return members


def get_from_id(id):
    cur = conn.cursor()
    cur.execute(
        "select memberid, name, registration_timestamp, pending_books, due_amount from members_view where memberid = ?",
        (id,),
    )
    member = cur.fetchone()
    cur.close()
    return member


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


def delete(ids):
    cur = conn.cursor()
    try:
        # I myself have never batch deleted before.
        # What this does is give the list of ids as parameters and the corresponding
        # '?'s as a string to the query.
        # This is messy but safe, and avoids the n+1 problem
        selectors = ", ".join("?" for id in range(len(ids)))
        cur.execute(f"delete from members where memberid in ({selectors})", ids)
        cur.close()
        conn.commit()
    except:
        return False
    return True


def update(id, name, timestamp):
    cur = conn.cursor()
    try:
        cur.execute(
            "update members set name=?, registration_timestamp=? where memberid=?",
            (name, timestamp, id),
        )
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True
