from ..db import conn

def issue(bookID, memberID):
    cur = conn.cursor()
    try:
        print(bookID, memberID, "meow")
        cur.execute("""
        insert into transactions (bookID, memberID)
        select books_view.bookID, members_view.memberID
        from books_view
        join members_view
        where
        books_view.bookID = ?
        and members_view.memberID = ?
        and books_view.currently_available > 0
        and members_view.due_amount < 500
        """, (bookID, memberID))
        if cur.rowcount == 0:
            conn.rollback()
            return False
        cur.close()
        conn.commit()
    except:
        conn.rollback()
        return Falss
    return True