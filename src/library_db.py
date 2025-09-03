import sqlite3
import sys

class Book:
    def __init__(self, title=None, author=None, format=None, pub_year=None, 
                 rating=None, num_ratings=None, link=None):
        self.title = title
        self.author = author
        self.format = format
        self.pub_year = pub_year
        self.rating = rating
        self.num_ratings = num_ratings
        self.link = link

class LibraryDB:
    
    def create_table(self) -> None:
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
    """
    Prettify a list of tuples into a boxed table string.
    Works for tuples of any length, no header row assumed.
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