import pytest
import os
from src import LibraryDB, Book, Charts
from .sample import library_items_sample
from main import remove_file

@pytest.fixture
def db():
    test_db = LibraryDB()
    test_db.create_table()
    print("Created table for testing")

    yield test_db

    test_db.delete_table()
    print("Deleted test table")

@pytest.fixture
def populated_db():
    test_db = LibraryDB()
    test_db.create_table()
    print("Created table for testing")
    
    for item in library_items_sample:
        book = Book(
            title=item[0],
            author=item[1],
            format=item[2],
            pub_year=item[3],
            rating=item[4],
            num_ratings=item[5],
            link=item[7])
        test_db.add_library_item(book)
    
    yield test_db

    test_db.delete_table()
    print("Deleted test table")

@pytest.fixture
def book():
    return Book("The Hobbit", "Tolkien, J.R.R.", "BOOK", 1937, 4.25, 2150000, "/catalog/12345")

@pytest.fixture
def query():
    return "test"

@pytest.fixture
def chart():
    return Charts()

@pytest.fixture
def image_file_path():
    test_image = "visuals/test.png"
    yield test_image
    remove_file(test_image)
    

