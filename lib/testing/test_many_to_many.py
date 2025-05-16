import pytest
from many_to_many import Author, Book, Contract

@pytest.fixture(autouse=True)
def clear_data():
    Author.all_authors.clear()
    Book.all_books.clear()
    Contract.all_contracts.clear()

def test_book_init():
    book = Book("Title")
    assert book.title == "Title"

def test_author_init():
    author = Author("Name")
    assert author.name == "Name"

def test_contract_init():
    book = Book("Title")
    author = Author("Name")
    date = '01/01/2001'
    royalties = 40000
    contract = Contract(author, book, date, royalties)

    assert contract.author == author
    assert contract.book == book
    assert contract.date == date
    assert contract.royalties == royalties

def test_contract_validates_author():
    book = Book("Title")
    date = '01/01/2001'
    royalties = 40000

    with pytest.raises(Exception):
        Contract("Author", book, date, royalties)

def test_contract_validates_book():
    author = Author("Name")
    date = '01/01/2001'
    royalties = 40000

    with pytest.raises(Exception):
        Contract(author, "Book", date, royalties)

def test_contract_validates_date():
    author = Author("Name")
    book = Book("Title")
    royalties = 40000

    with pytest.raises(Exception):
        Contract(author, book, 1012001, royalties)

def test_contract_validates_royalties():
    author = Author("Name")
    book = Book("Title")
    date = '01/01/2001'

    with pytest.raises(Exception):
        Contract(author, book, date, "Royalties")

def test_author_has_contracts():
    author = Author("Name")
    book = Book("Title")
    contract = Contract(author, book, '01/01/2001', 50000)

    assert author.contracts() == [contract]

def test_author_has_books():
    author = Author("Name")
    book = Book("Title")
    Contract(author, book, '01/01/2001', 50000)

    assert book in author.books()

def test_book_has_contracts():
    author = Author("Name")
    book = Book("Title")
    contract = Contract(author, book, '01/01/2001', 50000)

    assert book.contracts() == [contract]

def test_book_has_authors():
    author = Author("Name")
    book = Book("Title")
    Contract(author, book, '01/01/2001', 50000)

    assert author in book.authors()

def test_author_can_sign_contract():
    author = Author("Name")
    book = Book("Title")

    contract = author.sign_contract(book, "01/01/2001", 60000)

    assert isinstance(contract, Contract)
    assert contract.author == author
    assert contract.book == book
    assert contract.date == "01/01/2001"
    assert contract.royalties == 60000

def test_author_has_total_royalties():
    author = Author("Name")
    book1 = Book("Title 1")
    book2 = Book("Title 2")
    book3 = Book("Title 3")

    Contract(author, book1, "01/01/2001", 10)
    Contract(author, book2, "01/01/2001", 20)
    Contract(author, book3, "01/01/2001", 30)

    assert author.total_royalties() == 60

def test_contract_contracts_by_date():
    author1 = Author("Name 1")
    book1 = Book("Title 1")
    book2 = Book("Title 2")
    book3 = Book("Title 3")
    author2 = Author("Name 2")
    book4 = Book("Title 4")
    
    contract1 = Contract(author1, book1, "02/01/2001", 10)
    contract2 = Contract(author1, book2, "01/01/2001", 20)
    contract3 = Contract(author1, book3, "03/01/2001", 30)
    contract4 = Contract(author2, book4, "01/01/2001", 40)

    assert Contract.contracts_by_date('01/01/2001') == [contract2, contract4]
