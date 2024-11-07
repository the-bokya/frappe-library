from ..db import conn


def view_transactions():
    cur = conn.cursor()
    cur.execute(
        """
        select
            transactionid,
            members.memberID as memberID,
            members.name as member_name,
            books.bookID as bookID,
            books.title as book_title,
            issue_date,
            return_date,
            returned
        from transactions
            join books on books.bookID=transactions.bookID
            join members on members.memberID=transactions.memberID
        """
    )
    transactions = cur.fetchall()
    return transactions


def return_book(transactionid):
    cur = conn.cursor()
    try:
        cur.execute(
            "update transactions set returned = 1, return_date = date('now') where transactionid=?",
            (transactionid,),
        )
        cur.close()
        conn.commit()
        return True
    except:
        conn.rollback()
    return False
