"""library_db.py - SQLite database management for library items.

Provides database operations and data models for storing and retrieving
Calgary Public Library book information including titles, authors, ratings,
publication years, and other metadata.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

import sqlite3
import sys

class Book:
    """Represents a library book with metadata.
    
    Attributes:
        title (str): Book title including subtitle if available.
        author (str): Author name in "Last, First" format.
        format (str): Book format (BOOK, EBOOK, PAPERBACK, etc.).
        pub_year (int): Publication year.
        rating (float): Average user rating.
        num_ratings (int): Total number of user ratings.
        link (str): Relative URL to book's catalog page.
    """
    
    def __init__(self, title=None, author=None, format=None, pub_year=None, 
                 rating=None, num_ratings=None, link=None):
        """Initialize a Book instance.
        
        Args:
            title (str, optional): Book title.
            author (str, optional): Author name.
            format (str, optional): Book format.
            pub_year (int, optional): Publication year.
            rating (float, optional): Average user rating.
            num_ratings (int, optional): Number of ratings.
            link (str, optional): Catalog page URL.
        """
        self.title = title
        self.author = author
        self.format = format
        self.pub_year = pub_year
        self.rating = rating
        self.num_ratings = num_ratings
        self.link = link

class LibraryDB:
    """SQLite database manager for library items.
    
    Handles all database operations including table creation, data insertion,
    retrieval, and statistical analysis of library book data.
    """
    
    def create_table(self) -> None:
        """Create or recreate the library_items table.
        
        Drops existing table if present and creates a fresh table schema
        with columns for book metadata and calculated ratings.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS library_items;")
            cursor.execute(
                """
                CREATE TABLE library_items (
                    title TEXT,
                    author TEXT,
                    format TEXT,
                    pub_year INTEGER,
                    rating REAL,
                    num_ratings INTEGER,
                    bayesian_avg_rating REAL,
                    link TEXT
                );
                """
            )
            conn.commit()
            conn.close()
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            sys.exit(1)

    def delete_table(self) -> None:
        """Delete the library_items table from database.
        
        Used primarily for cleanup during testing.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS library_items;")
            conn.commit()
            conn.close()
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()

    def add_library_item(self, book: Book) -> None:
        """Insert a book record into the database.
        
        Args:
            book (Book): Book instance containing metadata to insert.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO library_items VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (book.title, book.author, book.format, book.pub_year, 
                book.rating, book.num_ratings, None, book.link)
            )
            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()

    def set_weighted_averages(self) -> None:
        """Calculate and update Bayesian weighted average ratings.
        
        Uses Bayesian averaging with minimum rating threshold of 20
        to provide more reliable ratings for books with few reviews.
        Formula: (v/(v+m)) * R + (m/(v+m)) * C
        Where: v=votes, R=rating, m=minimum votes, C=mean rating
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            cursor.execute("SELECT AVG(rating) FROM library_items WHERE rating IS NOT NULL;")
            C_result = cursor.fetchone()
            C = C_result[0] if C_result and C_result[0] is not None else 0
            m = 20  # minimum ratings required

            cursor.execute("SELECT rowid, rating, num_ratings FROM library_items;")
            items = cursor.fetchall()

            for row in items:
                rowid, R, v = row
                # Skip if rating or num_ratings is None
                if R is None or v is None:
                    continue
                    
                bayesian_avg = round((v / (v + m)) * R + (m / (v + m)) * C, 2)
                cursor.execute(
                    """
                    UPDATE library_items
                    SET bayesian_avg_rating = ?
                    WHERE rowid = ?
                    """,
                    (bayesian_avg, rowid)
                )

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()

    def get_all_library_items(self) -> list:
        """Retrieve all library items from database.
        
        Returns:
            list: List of tuples containing all book records.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM library_items;")
            library_items = cursor.fetchall()
            conn.commit()
            conn.close()
            
            return library_items
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            sys.exit(1)

    def get_item_count(self) -> int:
        """Get total number of items in database.
        
        Returns:
            int: Count of library items, or None if error occurs.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM library_items;")
            item_count = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            
            return item_count
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_frequent_authors(self) -> list:
        """Get authors with most books in collection.
        
        Returns:
            list: Tuples of (author_name, book_count) ordered by frequency.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT author,
                COUNT(author) as author_count
                FROM library_items
                WHERE author IS NOT NULL
                GROUP BY author
                ORDER BY author_count DESC;
                """)
            top_authors = cursor.fetchmany(20)
            conn.commit()
            conn.close()

            return top_authors
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_format_data(self) -> list:
        """Get distribution of book formats in collection.
        
        Returns:
            list: Tuples of (format, count) ordered by frequency.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT format,
                COUNT(format) as format_count
                FROM library_items
                WHERE format IS NOT NULL
                GROUP BY format
                ORDER BY format_count DESC, format;
                """)
            format_data = cursor.fetchall()
            conn.commit()
            conn.close()

            return format_data
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_pub_year_data(self) -> list:
        """Get distribution of publication years in collection.
        
        Returns:
            list: Tuples of (year, count) ordered by year descending.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT pub_year,
                COUNT(pub_year) as year_count
                FROM library_items
                WHERE pub_year IS NOT NULL
                GROUP BY pub_year
                ORDER BY pub_year DESC;
                """)
            pub_year_data = cursor.fetchall()
            conn.commit()
            conn.close()

            return pub_year_data
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_top_books_unweighted(self) -> list:
        """Get highest rated books using raw average ratings.
        
        Returns:
            list: Tuples of (title, author, rating) ordered by rating.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT title, author, rating
                FROM library_items
                WHERE rating IS NOT NULL
                ORDER BY rating DESC;
                """)
            top_books = cursor.fetchmany(10)
            conn.commit()
            conn.close()

            return top_books
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_top_books_weighted(self) -> list:
        """Get highest rated books using Bayesian weighted ratings.
        
        Returns:
            list: Tuples of (title, author, weighted_rating) ordered by rating.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT title, author, bayesian_avg_rating
                FROM library_items
                WHERE bayesian_avg_rating IS NOT NULL
                ORDER BY bayesian_avg_rating DESC;
                """)
            top_books = cursor.fetchmany(10)
            conn.commit()
            conn.close()

            return top_books

        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_top_authors_unweighted(self) -> list:
        """Get authors with highest average ratings (unweighted).
        
        Returns:
            list: Tuples of (author, avg_rating) ordered by rating.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT author, ROUND(AVG(rating), 2) as avg_rating
                FROM library_items
                WHERE rating IS NOT NULL
                GROUP BY author
                ORDER BY avg_rating DESC;
                """)
            top_authors = cursor.fetchmany(10)
            conn.commit()
            conn.close()

            return top_authors

        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None
    
    def get_top_authors_weighted(self) -> list:
        """Get authors with highest Bayesian weighted ratings.
        
        Returns:
            list: Tuples of (author, weighted_rating) ordered by rating.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT author, bayesian_avg_rating
                FROM library_items
                WHERE bayesian_avg_rating IS NOT NULL
                GROUP BY author
                ORDER BY bayesian_avg_rating DESC;
                """)
            top_books = cursor.fetchmany(10)
            conn.commit()
            conn.close()

            return top_books
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

    def get_ratings_per_num_ratings(self) -> list:
        """Get rating and review count data for scatter plot analysis.
        
        Returns:
            list: Tuples of (num_ratings, rating) for visualization.
        """
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT num_ratings, rating
                FROM library_items
                WHERE rating IS NOT NULL
                AND num_ratings IS NOT NULL;
                """)
            ratings_per_num_ratings = cursor.fetchall()
            conn.commit()
            conn.close()

            return ratings_per_num_ratings
        
        except Exception as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
                conn.close()
            
            return None

def prettify(data):
    """Convert list of tuples into formatted ASCII table.
    
    Creates a boxed table with proper alignment and borders
    for displaying tabular data in console output.
    
    Args:
        data (list): List of tuples to format as table.
        
    Returns:
        str: Formatted ASCII table string.
    """
    if not data:
        return "No data"

    # Convert everything to strings
    str_data = [tuple(map(str, row)) for row in data]

    # Find max width for each column
    num_cols = max(len(row) for row in str_data)
    col_widths = [0] * num_cols
    for row in str_data:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(val))

    # Build horizontal border
    horizontal = "+".join("-" * (w + 2) for w in col_widths)
    horizontal = f"+{horizontal}+"

    # Build table rows
    lines = [horizontal]
    for row in str_data:
        pretty_row = " | ".join(val.ljust(col_widths[i]) for i, val in enumerate(row))
        lines.append(f"| {pretty_row} |")
        lines.append(horizontal)

    table = "\n".join(lines)
    return table