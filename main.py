class Book:
    def __init__(self, title, author, isbn, copies=0, total_copies=0):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies
        self.total_copies = total_copies

    def check_availability(self):
        return self.copies > 0

    def update_total_copies(self, new_total):
        self.total_copies = new_total

    def update_copies(self, new_copies):
        self.copies = new_copies

    @staticmethod
    def validate_isbn(isbn):
        if len(isbn) == 17 and isbn.count("-") == 4:
            return True
        return False


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class Customer(User):
    def __init__(self, name, user_id, borrowed_books=None):
        super().__init__(name, user_id)
        if borrowed_books is None:
            borrowed_books = []
        self.borrowed_books = borrowed_books

    def borrow_book(self, book):
        if book.check_availability():
            self.borrowed_books.append(book)
            book.update_copies(book.copies - 1)
            return True
        else:
            return False

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.update_copies(book.copies + 1)
            return True
        else:
            return False


class Employee(User):
    def __init__(self, name, user_id, salary, library):
        super().__init__(name, user_id)
        self.salary = salary
        self.library = library

    def add_book_to_library(self, book):
        self.library.books.append(book)
        book.update_total_copies(book.total_copies + book.copies)

    def remove_book_from_library(self, book):
        if book in self.library.books:
            self.library.books.remove(book)
            book.update_total_copies(book.total_copies - book.copies)

    def register_user(self, user):
        self.library.users.append(user)


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def show_available_books(self):
        available_books = [book for book in self.books if book.check_availability()]
        return available_books


# Приклад використання
library = Library()

book1 = Book("Harry Potter", "J.K. Rowling", "978-0439554930", copies=5, total_copies=10)
book2 = Book("Python Programming", "John Doe", "978-0132678209", copies=3, total_copies=8)

customer1 = Customer("Alice", "12345")
employee1 = Employee("Bob", "67890", 3000, library)

employee1.add_book_to_library(book1)
employee1.add_book_to_library(book2)

employee1.register_user(customer1)

print("Is 'Harry Potter' available?", book1.check_availability())  # True

customer1.borrow_book(book1)
print("Is 'Harry Potter' available after borrowing?", book1.check_availability())  # False

print("Available books in library:", [book.title for book in library.show_available_books()])  # ['Python Programming']

employee1.remove_book_from_library(book1)
print("Is 'Harry Potter' available after removal?", book1.check_availability())  # True

print("Is ISBN '978-0439554930' valid?", Book.validate_isbn("978-0439554930"))  # True
print("Is ISBN '978-04395549300' valid?", Book.validate_isbn("978-04395549300"))  # False
