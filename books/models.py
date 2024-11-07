from ..db import conn


def read():
    cur = conn.cursor()
    cur.execute(
        "select bookID, title, authors, isbn, language_code, publication_date, publisher, amount, currently_available from books_view"
    )
    books = cur.fetchall()
    cur.close()
    return books


def get_from_id(bookID):
    cur = conn.cursor()
    cur.execute(
        "select bookID, title, authors, isbn, language_code, publication_date, publisher, amount, currently_available from books_view where bookID = ?",
        (bookID,),
    )
    book = cur.fetchone()
    cur.close()
    return book


def create(
    bookID, title, authors, isbn, language_code, publication_date, publisher, amount
):
    cur = conn.cursor()
    try:
        cur.execute(
            "insert into books (bookID, title, authors, isbn, language_code, publication_date, publisher, amount) values (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                bookID,
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


def delete(bookIDs):
    cur = conn.cursor()
    try:
        # I myself have never batch deleted before.
        # What this does is give the list of ids as parameters and the corresponding
        # '?'s as a string to the query.
        # This is messy but safe, and avoids the n+1 problem
        selectors = ", ".join("?" for bookID in range(len(bookIDs)))
        cur.execute(f"delete from books where bookID in ({selectors})", bookIDs)
        cur.close()
        conn.commit()
    except:
        return False
    return True


def update(
    bookID, title, authors, isbn, language_code, publication_date, publisher, amount
):
    cur = conn.cursor()
    try:
        cur.execute(
            "update books set title=?, authors=?, isbn=?, language_code=?, publication_date=?, publisher=?, amount=? where bookID=?",
            (
                title,
                authors,
                isbn,
                language_code,
                publication_date,
                publisher,
                amount,
                bookID,
            ),
        )
        print(cur.lastrowid)
        conn.commit()
    except Exception as e:
        print(e)
        return False
    return True
