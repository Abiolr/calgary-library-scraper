import pytest
from src import LibraryDB, Book, Charts

def test_format_distribution_chart(populated_db, query, chart, image_file_path):
    assert chart.format_distribution(populated_db.get_format_data(), query, image_file_path)

def test_pub_year_distribution_chart(populated_db, query, chart, image_file_path):
    assert chart.pub_year_distribution(populated_db.get_pub_year_data(), query, image_file_path)

def test_most_frequent_authors_chart(populated_db, query, chart, image_file_path):
    assert chart.most_frequent_authors(populated_db.get_frequent_authors(), query, image_file_path)

def test_ratings_per_num_ratings_chart(populated_db, query, chart, image_file_path):
    assert chart.ratings_per_num_ratings(populated_db.get_ratings_per_num_ratings(), query, image_file_path)