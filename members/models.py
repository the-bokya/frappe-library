from ..db import conn


def read():
    cur = conn.cursor()
    cur.execute(
        "select memberID, name, registration_timestamp, pending_books, due_amount from members_view"
    )
    members = cur.fetchall()
    cur.close()
    return members


def get_from_id(memberID):
    cur = conn.cursor()
    cur.execute(
        "select memberID, name, registration_timestamp, pending_books, due_amount from members_view where memberID = ?",
        (memberID,),
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


def delete(memberIDs):
    cur = conn.cursor()
    try:
        # I myself have never batch deleted before.
        # What this does is give the list of ids as parameters and the corresponding
        # '?'s as a string to the query.
        # This is messy but safe, and avoids the n+1 problem
        selectors = ", ".join("?" for _ in range(len(memberIDs)))
        cur.execute(f"delete from members where memberID in ({selectors})", memberIDs)
        cur.close()
        conn.commit()
    except:
        return False
    return True


def update(ID, name, timestamp):
    cur = conn.cursor()
    try:
        cur.execute(
            "update members set name=?, registration_timestamp=? where memberID=?",
            (name, timestamp, ID),
        )
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True
