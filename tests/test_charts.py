"""test_charts.py - Unit tests for chart generation functionality.

Tests the Charts class methods for creating various data visualizations
from library database statistics including pie charts, line plots,
bar charts, and scatter plots.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

import pytest
from src import LibraryDB, Book, Charts

def test_format_distribution_chart(populated_db, query, chart, image_file_path):
    """Test generation of format distribution pie chart.
    
    Args:
        populated_db: Database fixture with sample data.
        query: Test query string fixture.
        chart: Charts instance fixture.
        image_file_path: Temporary image file path fixture.
    """
    assert chart.format_distribution(populated_db.get_format_data(), query, image_file_path)

def test_pub_year_distribution_chart(populated_db, query, chart, image_file_path):
    """Test generation of publication year distribution line chart.
    
    Args:
        populated_db: Database fixture with sample data.
        query: Test query string fixture.
        chart: Charts instance fixture.
        image_file_path: Temporary image file path fixture.
    """
    assert chart.pub_year_distribution(populated_db.get_pub_year_data(), query, image_file_path)

def test_most_frequent_authors_chart(populated_db, query, chart, image_file_path):
    """Test generation of most frequent authors horizontal bar chart.
    
    Args:
        populated_db: Database fixture with sample data.
        query: Test query string fixture.
        chart: Charts instance fixture.
        image_file_path: Temporary image file path fixture.
    """
    assert chart.most_frequent_authors(populated_db.get_frequent_authors(), query, image_file_path)

def test_ratings_per_num_ratings_chart(populated_db, query, chart, image_file_path):
    """Test generation of ratings vs. review count scatter plot.
    
    Args:
        populated_db: Database fixture with sample data.
        query: Test query string fixture.
        chart: Charts instance fixture.
        image_file_path: Temporary image file path fixture.
    """
    assert chart.ratings_per_num_ratings(populated_db.get_ratings_per_num_ratings(), query, image_file_path)