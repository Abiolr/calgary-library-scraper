import time
import os
from src import LibraryDB, scrape_library_data, generate_charts, write_to_file, export_as_csv
    
def get_query() -> str:
    print("Please enter a search term to look up in the Calgary Public Library:")
    query = str(input(">>> "))
        
    return query

def remove_file(file_path: str):
    os.remove(file_path)

if __name__ == "__main__":
    library_db = LibraryDB()
    library_db.create_table()
    query = get_query()

    print("\nStarting library search...")
    scrape_library_data(library_db, query)

    print(f"\nScraped {library_db.get_item_count()} items for '{query}'.")

    print("\nWriting results to 'results/library_items.txt' and 'results/library_results.txt'...")
    write_to_file(library_db, query)
    time.sleep(1)

    print("\nExporting results as csv to results/library_items.csv")
    export_as_csv(library_db)
    time.sleep(1)

    print("\nGenerating charts...")
    generate_charts(library_db, query)
    time.sleep(1)

    print("\nDone! Charts and results have been generated successfully.")