from ..db import conn


def read():
    cur = conn.cursor()
    cur.execute(
        "select bookid, title, authors, isbn, language_code, publication_date, publisher, amount from books"
    )
    books = cur.fetchall()
    cur.close()
    return books


def get_from_id(bookid):
    cur = conn.cursor()
    cur.execute(
        "select bookid, title, authors, isbn, language_code, publication_date, publisher, amount from books where bookid = ?",
        (bookid,),
    )
    book = cur.fetchone()
    cur.close()
    return book


def create(
    bookid, title, authors, isbn, language_code, publication_date, publisher, amount
):
    cur = conn.cursor()
    try:
        cur.execute(
            "insert into books (bookid, title, authors, isbn, language_code, publication_date, publisher, amount) values (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                bookid,
                title,
                authors,
                isbn,
                language_code,
                publication_date,
                publisher,
                amount,
            ),
        )
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
        cur.execute(f"delete from books where bookid in ({selectors})", ids)
        cur.close()
        conn.commit()
    except:
        return False
    return True


def update(
    bookid, title, authors, isbn, language_code, publication_date, publisher, amount
):
    cur = conn.cursor()
    try:
        cur.execute(
            "update books set title=?, authors=?, isbn=?, language_code=?, publication_date=?, publisher=?, amount=? where bookid=?",
            (
                title,
                authors,
                isbn,
                language_code,
                publication_date,
                publisher,
                amount,
                bookid,
            ),
        )
        print(cur.lastrowid)
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True
