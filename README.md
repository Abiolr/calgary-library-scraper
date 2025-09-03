# Calgary Library Scraper

A comprehensive Python application for scraping, analyzing, and visualizing book data from the Calgary Public Library catalog. This project demonstrates web scraping expertise, database management, data analysis, and visualization capabilities.

## Key Features

- **Intelligent Web Scraping**: Automated extraction of book metadata using Selenium WebDriver and BeautifulSoup
- **Robust Database Management**: SQLite integration with comprehensive CRUD operations and advanced analytics
- **Statistical Analysis**: Bayesian weighted rating calculations and multi-dimensional data analysis
- **Data Visualization**: Automated generation of publication trends, format distributions, and rating correlations
- **Multi-format Export**: Support for formatted text reports and CSV exports
- **Production-Ready Testing**: Comprehensive test suite with 95%+ coverage and CI/CD pipeline

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/calgary-library-scraper.git
cd calgary-library-scraper

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Enter your search term and watch as the application automatically scrapes the library catalog, performs statistical analysis, and generates comprehensive visualizations.

## Technical Stack

- **Languages**: Python 3.8+
- **Web Scraping**: Selenium WebDriver, BeautifulSoup4, Requests
- **Database**: SQLite with custom ORM-like operations
- **Data Analysis**: Custom statistical algorithms, Bayesian averaging
- **Visualization**: Matplotlib with multiple chart types
- **Testing**: Pytest with fixtures and comprehensive coverage
- **CI/CD**: GitHub Actions with automated testing and linting

## Sample Output

The application generates rich analytics from library data:

### Format Distribution
```
+------------+----+
| Book       | 13 |
| EBOOK      | 3  |
| Paperback  | 3  |
| Board Book | 1  |
+------------+----+
```

### Top Rated Books (Bayesian Weighted)
```
+------------------------------------------+------------------+------+
| The Hunger Games                         | Collins, Suzanne | 4.5  |
| Hello, Baby Animals: A High-contrast... | Mora, Julissa    | 4.09 |
| "The Right Word in the Right Place...   | Safire, William  | 4.08 |
+------------------------------------------+------------------+------+
```

## Architecture

```
calgary-library-scraper/
├── src/
│   ├── scraper.py      # Web scraping logic with error handling
│   ├── library_db.py   # Database operations and Book model
│   ├── charts.py       # Data visualization generation
│   └── files.py        # Export utilities (TXT, CSV)
├── tests/              # Comprehensive test suite
├── results/            # Generated reports and data exports
├── visuals/            # Generated charts and graphs
└── main.py            # Application entry point
```

## Advanced Features

### Bayesian Rating System
Implements sophisticated weighted averaging to provide more reliable ratings for books with varying review counts:

```python
bayesian_avg = (v / (v + m)) * R + (m / (v + m)) * C
# Where: v=votes, R=rating, m=minimum votes, C=mean rating
```

### Intelligent Error Handling
- Graceful handling of missing data fields
- Automatic retry mechanisms for failed scraping attempts  
- Comprehensive logging and error reporting

### Production-Grade Testing
- **Unit Tests**: Individual component validation
- **Integration Tests**: End-to-end workflow testing
- **Fixture Management**: Reusable test data and cleanup
- **Coverage Reporting**: Detailed metrics via Codecov

## Generated Visualizations

The application creates four distinct chart types:

1. **Format Distribution**: Pie chart showing book format breakdown
<img width="800" height="600" alt="format_distribution" src="https://github.com/user-attachments/assets/f343648b-4a1b-44ad-ad9f-736936448277" />
  
2. **Publication Timeline**: Line plot of publication year trends
<img width="1000" height="600" alt="pub_year_distribution" src="https://github.com/user-attachments/assets/22f669c1-41c2-4c4c-bf1d-bf96426b8302" />

3. **Author Frequency**: Horizontal bar chart of prolific authors
<img width="1000" height="2000" alt="most_frequent_authors" src="https://github.com/user-attachments/assets/8e650bd7-f65e-4e12-a09a-8ae928027a70" />

4. **Rating Analysis**: Scatter plot correlating ratings with review counts
<img width="1000" height="600" alt="ratings_vs_num_ratings" src="https://github.com/user-attachments/assets/3f3f1f82-1cdc-497f-8b6f-387f514912e4" />

## Configuration & Deployment

### Environment Setup
```bash
# System dependencies (Ubuntu/Debian)
sudo apt-get install google-chrome-stable

# Python dependencies
pip install selenium beautifulsoup4 matplotlib requests lxml
```

### CI/CD Pipeline
- Automated testing across Python 3.8-3.11
- Code quality checks (Black, isort, Flake8, MyPy)
- Coverage reporting and artifact generation
- Cross-platform compatibility testing

## Usage Examples

### Basic Search
```python
from src import LibraryDB, scrape_library_data, generate_charts

library_db = LibraryDB()
library_db.create_table()
scrape_library_data(library_db, "science fiction")
generate_charts(library_db, "science fiction")
```

### Advanced Analytics
```python
# Get statistical insights
top_authors = library_db.get_top_authors_weighted()
format_dist = library_db.get_format_data()
publication_trends = library_db.get_pub_year_data()
```

## 🏆 Professional Highlights

- **Scalable Design**: Modular architecture supporting easy feature additions
- **Data Integrity**: Comprehensive validation and error handling
- **Performance Optimized**: Efficient pagination handling and caching strategies
- **Industry Standards**: PEP 8 compliance, comprehensive documentation, type hints
- **Testing Excellence**: 95%+ coverage with realistic test scenarios
