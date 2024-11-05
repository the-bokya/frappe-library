from sqlite3 import connect, Row

conn = connect("frappe.db", check_same_thread=False)

# Foreign keys have to be turned on manually in sqlite3 as it turns out
conn.execute("PRAGMA foreign_keys = ON")

# Return query output as dict key_value pairs instead of a confusing tuple
conn.row_factory = Row

conn.commit()
