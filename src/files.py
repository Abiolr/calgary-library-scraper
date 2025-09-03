"""files.py - File export utilities for library data.

Handles exporting library database contents to various file formats
including formatted text reports and CSV files for data analysis
and archival purposes.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

from .library_db import LibraryDB, prettify
import csv

def write_to_file(library_db: LibraryDB, query: str) -> None:
    """Export library data to formatted text files.
    
    Creates two text files:
    1. library_items.txt - All items in tabular format
    2. library_results.txt - Statistical analysis and rankings
    
    Args:
        library_db (LibraryDB): Database instance containing library data.
        query (str): Search query used in report headers.
    """
    try:
        with open("results/library_items.txt", "w") as file:
            file.write(f"ALL LIBRARY ITEMS\n")
            all_library_items = library_db.get_all_library_items()
            file.write(prettify(all_library_items))
    
    except Exception as e:
        print(f"Error writing to file: {e}")

    try:
        with open("results/library_results.txt", "w") as file:
            file.write(f"\nLIBRARY RESULTS: {query}\n")
            file.write("\n\nFormat Distribution:\n")

            format_data = library_db.get_format_data()
            file.write(prettify(format_data))
            
            file.write("\n\nPublication Year Distribution:\n")
            pub_year_data = library_db.get_pub_year_data()
            file.write(prettify(pub_year_data))

            file.write("\n\nMost Frequent Authors:\n")
            frequent_authors_data = library_db.get_frequent_authors()
            file.write(prettify(frequent_authors_data))

            file.write("\n\nTop Rated Authors (Unweighted):\n")
            top_authors_unweighted_data = library_db.get_top_authors_unweighted()
            file.write(prettify(top_authors_unweighted_data))

            file.write("\n\nTop Rated Authors (Bayesian Weighted):\n")
            top_authors_weighted_data = library_db.get_top_authors_weighted()
            file.write(prettify(top_authors_weighted_data))

            file.write("\n\nTop Rated Books (Unweighted):\n")
            top_books_unweighted_data = library_db.get_top_books_unweighted()
            file.write(prettify(top_books_unweighted_data))

            file.write("\n\nTop Rated Books (Bayesian Weighted):\n")
            top_books_weighted_data = library_db.get_top_books_weighted()
            file.write(prettify(top_books_weighted_data))
        
    except Exception as e:
        print(f"Error writing to file: {e}")

def export_as_csv(library_db: LibraryDB) -> None:
    """Export all library items to CSV format.
    
    Creates a comma-separated values file containing all book records
    suitable for spreadsheet analysis or data processing.
    
    Args:
        library_db (LibraryDB): Database instance containing library data.
    """
    try:
        with open("results/library_items.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(library_db.get_all_library_items())
    
    except Exception as e:
        print(f"Error writing to file: {e}")