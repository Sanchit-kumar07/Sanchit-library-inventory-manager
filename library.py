# ---------------------- BOOK CLASS ----------------------

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"


# ------------------- LIBRARY INVENTORY -------------------

class LibraryInventory:
    def __init__(self, filename="books.txt"):
        self.filename = filename
        self.books = []
        self.load_from_file()

    def add_book(self, book):
        self.books.append(book)
        self.save_to_file()

    def search_by_title(self, title):
        title = title.lower()
        return [b for b in self.books if title in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in library.")
        else:
            for b in self.books:
                print(b)

    # ----------- File Save / Load -----------
    def save_to_file(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                for b in self.books:
                    f.write(f"{b.title}|{b.author}|{b.isbn}|{b.status}\n")
        except Exception as e:
            print("Error saving file:", e)

    def load_from_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.books = []
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 4:
                        self.books.append(Book(*parts))
        except FileNotFoundError:
            self.books = []


# --------------------- MENU FUNCTIONS ---------------------

def add_book_menu(inventory):
    title = input("Enter title: ")
    author = input("Enter author: ")
    isbn = input("Enter ISBN: ")

    if inventory.search_by_isbn(isbn):
        print("Book with this ISBN already exists.")
        return

    inventory.add_book(Book(title, author, isbn))
    print("Book added successfully.")


def issue_book_menu(inventory):
    isbn = input("Enter ISBN to issue: ")
    book = inventory.search_by_isbn(isbn)

    if not book:
        print("Book not found.")
    elif book.status == "issued":
        print("Book already issued.")
    else:
        book.status = "issued"
        inventory.save_to_file()
        print("Book issued.")


def return_book_menu(inventory):
    isbn = input("Enter ISBN to return: ")
    book = inventory.search_by_isbn(isbn)

    if not book:
        print("Book not found.")
    elif book.status == "available":
        print("Book is not issued.")
    else:
        book.status = "available"
        inventory.save_to_file()
        print("Book returned.")


def search_menu(inventory):
    print("1. Search by Title")
    print("2. Search by ISBN")
    choice = input("Enter choice: ")

    if choice == "1":
        title = input("Enter title: ")
        results = inventory.search_by_title(title)
        if results:
            for b in results:
                print(b)
        else:
            print("No books found.")
    elif choice == "2":
        isbn = input("Enter ISBN: ")
        book = inventory.search_by_isbn(isbn)
        print(book if book else "Book not found.")
    else:
        print("Invalid choice.")


# -------------------------- MAIN --------------------------

def main():
    inventory = LibraryInventory()

    while True:
        print("\n------ Library Menu ------")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book_menu(inventory)
        elif choice == "2":
            issue_book_menu(inventory)
        elif choice == "3":
            return_book_menu(inventory)
        elif choice == "4":
            inventory.display_all()
        elif choice == "5":
            search_menu(inventory)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()