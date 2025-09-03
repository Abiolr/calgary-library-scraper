"""test_db.py - Unit tests for database operations and Book model.

Comprehensive tests for LibraryDB class methods including CRUD operations,
data retrieval, statistical calculations, and the Book data model.
Validates proper handling of edge cases and data integrity.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

import pytest
from src import LibraryDB, Book
from .sample import library_items_sample

def test_book(book):
    """Test Book model initialization and attributes.
    
    Args:
        book: Book instance fixture with test data.
    """
    assert book.title == "The Hobbit"
    assert book.author == "Tolkien, J.R.R."
    assert book.format == "BOOK"
    assert book.pub_year == 1937
    assert book.rating == 4.25
    assert book.num_ratings == 2150000
    assert book.link == "/catalog/12345"

def test_get_item_count(db):
    """Test database item counting functionality.
    
    Args:
        db: Empty database fixture.
    """
    assert db.get_item_count() == 0, "Table should be empty"
    
    for item in library_items_sample:
        book = Book(
            title=item[0],
            author=item[1],
            format=item[2],
            pub_year=item[3],
            rating=item[4],
            num_ratings=item[5],
            link=item[7])
        db.add_library_item(book)

    assert db.get_item_count() == 20, "Table should contain 20 books"

def test_get_all_library_items(db):
    """Test retrieval of all library items from database.
    
    Args:
        db: Empty database fixture.
    """
    assert db.get_all_library_items() == []
    
    for item in library_items_sample:
        book = Book(
            title=item[0],
            author=item[1],
            format=item[2],
            pub_year=item[3],
            rating=item[4],
            num_ratings=item[5],
            link=item[7])
        db.add_library_item(book)

    db.set_weighted_averages()

    assert db.get_all_library_items() == library_items_sample

def test_add_library_item(db, book):
    """Test adding individual book records to database.
    
    Args:
        db: Empty database fixture.
        book: Book instance fixture.
    """
    db.add_library_item(book)

    assert db.get_all_library_items() == [("The Hobbit", "Tolkien, J.R.R.", "BOOK", 1937, 4.25, 2150000, None, "/catalog/12345")]

def test_get_frequent_authors(populated_db):
    """Test retrieval of most frequent authors statistics.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    assert populated_db.get_frequent_authors()[0] == ("Tolkien, J.R.R.", 2)

def test_get_format_data(populated_db):
    """Test format distribution data retrieval.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    assert populated_db.get_format_data()[0] == ("BOOK", 13)
    assert populated_db.get_format_data()[1] == ("EBOOK", 3)
    assert populated_db.get_format_data()[2] == ("PAPERBACK", 3)
    assert populated_db.get_format_data()[3] == ("GRAPHIC NOVEL", 1)

def test_get_pub_year_data(populated_db):
    """Test publication year distribution data retrieval.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    pub_year_data = populated_db.get_pub_year_data()
    
    assert pub_year_data[0][0] == 2011
    assert pub_year_data[-1][0] == 1813
    
    assert (1985, 2) in pub_year_data
    assert (1951, 2) in pub_year_data

def test_get_top_books_unweighted(populated_db):
    """Test retrieval of highest rated books using raw ratings.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    top_books = populated_db.get_top_books_unweighted()
    
    assert len(top_books) == 10
    
    previous_rating = float('inf')
    for book in top_books:
        current_rating = book[2]
        assert current_rating <= previous_rating
        previous_rating = current_rating
    
    assert top_books[0][0] == "The Name of the Wind"
    assert top_books[0][2] == 4.52

def test_get_top_books_weighted(populated_db):
    """Test retrieval of highest rated books using Bayesian weighting.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    populated_db.set_weighted_averages()
    top_books = populated_db.get_top_books_weighted()
    
    assert len(top_books) == 10
    
    previous_rating = float('inf')
    for book in top_books:
        current_rating = book[2]
        assert current_rating <= previous_rating
        previous_rating = current_rating

def test_get_top_authors_unweighted(populated_db):
    """Test retrieval of top rated authors using raw ratings.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    top_authors = populated_db.get_top_authors_unweighted()
    
    assert len(top_authors) == 10
    
    previous_rating = float('inf')
    for author in top_authors:
        current_rating = author[1]
        assert current_rating <= previous_rating
        previous_rating = current_rating

def test_get_top_authors_weighted(populated_db):
    """Test retrieval of top rated authors using Bayesian weighting.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    populated_db.set_weighted_averages()
    top_authors = populated_db.get_top_authors_weighted()
    
    assert len(top_authors) == 10
    
    previous_rating = float('inf')
    for author in top_authors:
        current_rating = author[1]
        assert current_rating <= previous_rating
        previous_rating = current_rating

def test_get_ratings_per_num_ratings(populated_db):
    """Test retrieval of rating correlation data for scatter plots.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    ratings_data = populated_db.get_ratings_per_num_ratings()
    
    # Should return all books with both rating and num_ratings
    assert len(ratings_data) == 20  # One book has None rating in sample
    
    # Each item should be a tuple with (num_ratings, rating)
    for item in ratings_data:
        assert len(item) == 2
        assert isinstance(item[0], int) or item[0] is None
        assert isinstance(item[1], float) or item[1] is None

def test_set_weighted_averages(populated_db):
    """Test Bayesian weighted average calculation and storage.
    
    Args:
        populated_db: Database fixture with sample data.
    """
    initial_items = populated_db.get_all_library_items()
    for item in initial_items:
        assert item[6] is None

    populated_db.set_weighted_averages()
    
    updated_items = populated_db.get_all_library_items()
    for item in updated_items:
        if item[4] is not None and item[5] is not None:
            assert item[6] is not None
            assert isinstance(item[6], float)

def test_delete_table(db):
    """Test table deletion functionality.
    
    Args:
        db: Empty database fixture.
    """
    for item in library_items_sample[:3]:
        book = Book(
            title=item[0],
            author=item[1],
            format=item[2],
            pub_year=item[3],
            rating=item[4],
            num_ratings=item[5],
            link=item[7])
        db.add_library_item(book)

    assert db.get_item_count() == 3
    
    db.delete_table()
    
    assert db.get_item_count() == None

def test_empty_table_operations(db):
    """Test database operations on empty table handle gracefully.
    
    Args:
        db: Empty database fixture.
    """
    assert db.get_item_count() == 0
    assert db.get_all_library_items() == []
    assert db.get_frequent_authors() == []
    assert db.get_format_data() == []
    assert db.get_pub_year_data() == []
    assert db.get_top_books_unweighted() == []
    assert db.get_top_books_weighted() == []
    assert db.get_top_authors_unweighted() == []
    assert db.get_top_authors_weighted() == []
    assert db.get_ratings_per_num_ratings() == []