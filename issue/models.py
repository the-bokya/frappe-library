from ..db import conn

def issue(bookid, memberid):
    cur = conn.cursor()
    try:
        print(bookid, memberid, "meow")
        cur.execute("""
        insert into transactions (bookid, memberid)
        select books_view.bookid, members_view.memberid
        from books_view
        join members_view
        where
        books_view.bookid = ?
        and members_view.memberid = ?
        and books_view.currently_available > 0
        and members_view.due_amount < 500
        """, (bookid, memberid))
        if cur.rowcount == 0:
            conn.rollback()
            return False
        cur.close()
        conn.commit()
    except:
        conn.rollback()
        return Falss
    return True