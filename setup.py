from sqlite3 import connect

conn = connect("frappe.db")

# Initialise members
# registration time is set through current_timestamp (this should be an editable property I guess in the CRUD view).
conn.execute(
    "create table if not exists members (memberid integer primary key autoincrement, name text, registration_timestamp datetime default current_timestamp)"
)

# Initialise books
conn.execute(
    "create table if not exists books (bookid integer primary key, title text, authors text, average_rating numeric real, isbn text, isbn13 text, language_code text, num_pages integer, ratings_count integer, text_reviews_count integer, publication_date date, publisher text, taken_by integer, foreign key (taken_by) references members(memberid))"
)
# Initialise transactions (transaction_type should be either "issue" or "return")
conn.execute(
    "create table if not exists transactions(bookid integer, memberid integer, time datetime default current_timestamp, transaction_type text, foreign key(bookid) references books(bookid), foreign key (memberid) references members(memberid))"
)
conn.commit()
