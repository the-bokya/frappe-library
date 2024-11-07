from ..db import conn


def view_transactions():
    cur = conn.cursor()
    cur.execute(
        """
        select
            transactionid,
            members.memberid as memberid,
            members.name as member_name,
            books.bookid as bookid,
            books.title as book_title,
            issue_date,
            return_date,
            returned
        from transactions
            join books on books.bookid=transactions.bookid
            join members on members.memberid=transactions.memberid
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
