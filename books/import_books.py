import requests


def import_books(title, authors, isbn, publisher):
    page = 1
    params = dict()

    params["title"] = title
    params["authors"] = authors
    params["isbn"] = isbn
    params["publisher"] = publisher

    books = []

    # loop that keeps on incrementing page till the response is empty (we have got all books).
    while True:
        params["page"] = page
        response = requests.get(
            "https://frappe.io/api/method/frappe-library", params=params
        )
        print(page)
        print(response.json())
        page += 1
        books_list = response.json()["message"]
        if len(books_list) == 0:
            break
        books.extend(books_list)

    # Frappe's API has a lot of duplicates. This removes them.
    books = {book["bookID"]: book for book in books}.values()
    print(books, "meow")
    return books
