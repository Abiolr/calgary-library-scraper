"""conftest.py - Pytest configuration and fixtures for testing.

Provides reusable test fixtures for database instances, sample data,
and temporary file management to support comprehensive testing
of the Calgary Library Scraper application.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

import pytest
import os
from src import LibraryDB, Book, Charts
from .sample import library_items_sample
from main import remove_file

@pytest.fixture
def db():
    """Create clean test database instance.
    
    Yields:
        LibraryDB: Fresh database instance with empty table.
        
    Cleanup:
        Deletes test table after test completion.
    """
    test_db = LibraryDB()
    test_db.create_table()
    print("Created table for testing")

    yield test_db

    test_db.delete_table()
    print("Deleted test table")

@pytest.fixture
def populated_db():
    """Create test database populated with sample data.
    
    Yields:
        LibraryDB: Database instance pre-loaded with test book records.
        
    Cleanup:
        Deletes test table after test completion.
    """
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
    """Create sample Book instance for testing.
    
    Returns:
        Book: Pre-configured book object with test data.
    """
    return Book("The Hobbit", "Tolkien, J.R.R.", "BOOK", 1937, 4.25, 2150000, "/catalog/12345")

@pytest.fixture
def query():
    """Provide test search query string.
    
    Returns:
        str: Generic test query for chart titles and reports.
    """
    return "test"

@pytest.fixture
def chart():
    """Create Charts instance for visualization testing.
    
    Returns:
        Charts: Chart generator instance for testing visualizations.
    """
    return Charts()

@pytest.fixture
def image_file_path():
    """Provide temporary image file path with automatic cleanup.
    
    Yields:
        str: Path for temporary test image file.
        
    Cleanup:
        Removes test image file after test completion.
    """
    test_image = "visuals/test.png"
    yield test_image
    remove_file(test_image)