"""src package - Calgary Public Library scraper modules.

Main package for the Calgary Library Scraper application providing
database operations, web scraping, data visualization, and file export
functionality for library catalog analysis.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

from .library_db import LibraryDB, Book, prettify
from .scraper import scrape_library_data, _get_driver, _get_target_item_count
from .charts import Charts, generate_charts
from .files import write_to_file, export_as_csv