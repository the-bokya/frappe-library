from sqlite3 import connect

conn = connect("frappe.db")

# Initialise members
# registration time is set through current_timestamp (this should be an editable property I guess in the CRUD view).
conn.execute(
    """
    create table if not exists members
    (
        memberid integer primary key autoincrement,
        name text,
        registration_timestamp datetime default current_timestamp
    )
    """
)

# Initialise books
conn.execute(
    """create table if not exists books
    (
        bookid integer primary key,
        title text,
        authors text,
        isbn text,
        language_code text,
        publication_date date,
        publisher text,
        amount integer
    )
    """
)
# Initialise transactions
conn.execute(
    """create table if not exists transactions
    (
        bookid integer,
        memberid integer,
        issue_date date default (date('now')),
        return_date date,
        returned boolean default 0,
        foreign key(bookid) references books(bookid),
        foreign key (memberid) references members(memberid)
    )
    """
)

# The view that gets member info alongwith pending amount and issued books. This will be the default view from now on ig
conn.execute(
    """
    create view if not exists members_view as
    with a (memberid, pending_books, due_amount) as (
        select memberid, count(*), sum(cast(julianday('now') - julianday(issue_date) as int)) * 20
        from transactions
        where returned = 0
        group by memberid
    )
    select
        mbs.memberid,
        mbs.name,
        mbs.registration_timestamp, 
        coalesce(a.pending_books, 0) as pending_books, 
        coalesce(a.due_amount, 0) as due_amount
    from members as mbs
    left join a on mbs.memberid = a.memberid;
    """
)

# books_view: contains an additional field on the number of books issued.
conn.execute(
    """
    create view if not exists books_view as
    with a (bookid, currently_available) as (
        select transactions.bookid, books.amount - count(*)
        from transactions
        inner join books on books.bookid = transactions.bookid
        where returned = 0
        group by transactions.bookid
    )
    select
        bks.bookid,
        bks.title,
        bks.authors, 
        bks.isbn,
        bks.language_code,
        bks.publication_date,
        bks.publisher,
        bks.amount,
        coalesce(a.currently_available, bks.amount) as currently_available
    from books as bks
    left join a on bks.bookid = a.bookid;
    """
)
conn.commit()
