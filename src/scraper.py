"""scraper.py - Web scraping module for Calgary Public Library catalog.

Handles automated data extraction from the Calgary Public Library's online
catalog using Selenium WebDriver and BeautifulSoup for HTML parsing.
Extracts book metadata including titles, authors, ratings, and publication details.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

from bs4 import BeautifulSoup
from selenium import webdriver
from .library_db import LibraryDB, Book
from urllib.parse import urlencode
from selenium.webdriver.chrome.options import Options
import re
import requests
import sys

def _get_driver(headless=True):
    """Initialize and configure Chrome WebDriver instance.
    
    Args:
        headless (bool): Run browser in headless mode. Default True.
        
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.
        
    Raises:
        SystemExit: If driver initialization fails.
    """
    try:
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        return driver
    
    except:
        print("Unable to get driver")
        sys.exit(1)

def _get_target_item_count(url: str, query: str) -> int:
    """Determine total number of search results available.
    
    Makes initial request to catalog search page to extract the total
    number of items matching the search query.
    
    Args:
        url (str): Base URL for library catalog search.
        query (str): Search term to look up.
        
    Returns:
        int: Total number of items found for the search query.
        
    Raises:
        SystemExit: If unable to retrieve or parse result count.
    """
    params = {
            'query': query,
            'searchType': 'tag',
            'locked': 'true',
            'f_FORMAT': 'BK|EBOOK|GRAPHIC_NOVEL|LPRINT|BOARD_BK|PAPERBACK',
        }
    
    try:
        url = f"{url}?{urlencode(params)}"
        raw_html = requests.get(url).text
        soup = BeautifulSoup(raw_html, 'lxml')
        try:
            target_item_count = int(soup.find('span', class_='cp-pagination-label').text.split()[4].replace(',',''))
        except:
            target_item_count = 0

        return target_item_count
    
    except:
        print("Could not scrape target amount")
        sys.exit(1)

def scrape_library_data(library_db: LibraryDB, query: str) -> None:
    """Scrape library catalog data and populate database.
    
    Main scraping function that iterates through search result pages,
    extracts book metadata from each item, and stores it in the database.
    Handles pagination automatically and calculates Bayesian weighted ratings.
    
    Args:
        library_db (LibraryDB): Database instance to store scraped data.
        query (str): Search term for library catalog lookup.
        
    Raises:
        SystemExit: If no results found or scraping fails.
    """
    try:
        driver = _get_driver(headless=True)
        page_number = 1
        base_url = "https://calgary.bibliocommons.com/v2/search"
        target_item_count = _get_target_item_count(base_url, query)
        if target_item_count == 0:
            print(f"No results found for '{query}'. Please try another search term.")
            sys.exit(1)

        prev_item_count = 0
        while library_db.get_item_count() < target_item_count:
            print(f"Scraping page {page_number}... (collected {library_db.get_item_count()}/{target_item_count})")
            params = {
                'query': query,
                'searchType': 'tag',
                'locked': 'true',
                'f_FORMAT': 'BK|EBOOK|GRAPHIC_NOVEL|LPRINT|BOARD_BK|PAPERBACK',
                'page': page_number
            }
            
            url = f"{base_url}?{urlencode(params)}"
            driver.get(url)
            library_html = driver.page_source
            soup = BeautifulSoup(library_html, 'lxml')
            book_cards = soup.find_all('div', class_='cp-search-result-item-content')

            for book_card in book_cards:
                book = Book()
                book.title = book_card.find('span', class_='title-content').text
                try:
                    subtitle = book_card.find('span', class_='cp-subtitle').text
                    book.title += f": {subtitle}"
                except:
                    pass
                try:
                    author = book_card.find('a', class_='author-link').text
                    last, first = author.split(",", 1)
                    last = last.replace(" ", "")
                    first = re.sub(r'\.\s+', '.', first.strip())
                    book.author = f"{last}, {first}"
                except:
                    pass
                try:
                    book.format = book_card.find('span', class_='display-info-primary').text.split(', ')[0]
                except:
                    pass
                try:
                    book.pub_year = int(book_card.find('span', class_='display-info-primary').text.split(', ')[1])
                    if book.pub_year < 1000:
                        book.pub_year = None
                except:
                    pass
                try:
                    book.rating = float(book_card.find('span', class_='cp-rating-stars rating-stars').span.text.split(' ')[2])
                    book.num_ratings = int(book_card.find('span', class_='rating-count').text.strip('(,)').split(' ')[0].replace(',',''))
                except:
                    pass
                try:
                    book.link = book_card.find('h2', class_='cp-title').a['href']
                except:
                    pass
                
                library_db.add_library_item(book)
            
            if library_db.get_item_count() == prev_item_count:
                break

            page_number += 1
            prev_item_count = library_db.get_item_count()

        driver.quit()

        if target_item_count != library_db.get_item_count():
            print("Scrape incomplete. Restarting the process...")
            library_db.create_table()
            scrape_library_data(library_db, query)

        library_db.set_weighted_averages()

    except Exception as e:
        print(f"Unable to scrape data: {e}")
        sys.exit(1)