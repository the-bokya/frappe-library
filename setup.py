from sqlite3 import connect

conn = connect("frappe.db")

# Initialise members
# registration time is set through current_timestamp (this should be an editable property I guess in the CRUD view).
conn.execute(
    "create table if not exists members (memberid integer primary key autoincrement, name text, registration_timestamp datetime default current_timestamp)"
)

# Initialise books
conn.execute(
    "create table if not exists books (bookid integer primary key, title text, authors text, isbn text,language_code text, publication_date date, publisher text, amount integer)"
)
# Initialise transactions
conn.execute(
    "create table if not exists transactions(bookid integer, memberid integer, issue_date date default (date('now')), return_date date, returned boolean default 0, foreign key(bookid) references books(bookid), foreign key (memberid) references members(memberid))"
)
conn.commit()
