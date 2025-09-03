"""charts.py - Data visualization module for library analytics.

Generates matplotlib charts and graphs from library database statistics
including format distribution pie charts, publication timeline plots,
author frequency analysis, and rating correlation visualizations.
"""

__author__ = "Abiola Raji"
__version__ = "1.0"
__date__ = "2025-09-03"

import matplotlib.pyplot as plt
from .library_db import LibraryDB

class Charts:
    """Chart generation class for library data visualization.
    
    Provides methods to create various chart types from library database
    statistics including pie charts, line plots, bar charts, and scatter plots.
    """
    
    def format_distribution(self, format_data: list, query: str, file_path: str) -> bool:
        """Generate pie chart showing distribution of book formats.
        
        Args:
            format_data (list): Tuples of (format_name, count).
            query (str): Search query used in chart title.
            file_path (str): Output path for saved chart image.
            
        Returns:
            bool: True if chart created successfully, False otherwise.
        """
        try:
            labels, values = zip(*format_data)

            plt.figure(figsize=(8, 6))
            plt.pie(
                values,
                labels=labels,
                autopct='%1.1f%%',
                startangle=140,
            )

            plt.title(f"Format Distribution: '{query}'", fontsize=14, weight='bold')
            plt.legend(labels, title="Formats", bbox_to_anchor=(1, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            return True

        except Exception as e:           
            print(f"Could not create {file_path}: {e}")
            return False

    def pub_year_distribution(self, pub_year_data: list, query: str, file_path: str) -> bool:
        """Generate line chart showing publication year distribution over time.
        
        Args:
            pub_year_data (list): Tuples of (year, count).
            query (str): Search query used in chart title.
            file_path (str): Output path for saved chart image.
            
        Returns:
            bool: True if chart created successfully, False otherwise.
        """
        try:
            years, counts = zip(*pub_year_data)  # sort by year

            plt.figure(figsize=(10, 6))
            plt.plot(years, counts, linestyle="-", linewidth=2)

            plt.title(f"Publication Year Distribution: '{query}'", fontsize=14, weight="bold")
            plt.xlabel("Publication Year")
            plt.ylabel("Number of Items")
            plt.xticks(rotation=45)
            plt.grid(True, linestyle="--", alpha=0.6)

            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            return True
        
        except Exception as e:           
            print(f"Could not create {file_path}: {e}")
            return False

    def most_frequent_authors(self, frequent_authors_data: list, query: str, file_path: str) -> bool:
        """Generate horizontal bar chart of most prolific authors.
        
        Args:
            frequent_authors_data (list): Tuples of (author_name, book_count).
            query (str): Search query used in chart title.
            file_path (str): Output path for saved chart image.
            
        Returns:
            bool: True if chart created successfully, False otherwise.
        """
        try:
            authors, counts = zip(*reversed(frequent_authors_data))

            plt.figure(figsize=(10, len(authors)))
            bars = plt.barh(authors, counts, color="skyblue")

            plt.title(f"Most Frequent Authors: '{query}'", fontsize=14, weight="bold")
            plt.xlabel("Number of Items")

            for bar in bars:
                plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                        str(int(bar.get_width())), va="center", fontsize=9)

            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            return True
        
        except Exception as e:            
            print(f"Could not create {file_path}: {e}")
            return False

    def ratings_per_num_ratings(self, ratings_per_num_ratings_data: list, query: str, file_path: str) -> bool:
        """Generate scatter plot correlating rating scores with review counts.
        
        Args:
            ratings_per_num_ratings_data (list): Tuples of (num_ratings, avg_rating).
            query (str): Search query used in chart title.
            file_path (str): Output path for saved chart image.
            
        Returns:
            bool: True if chart created successfully, False otherwise.
        """
        try:
            num_ratings, avg_ratings = zip(*ratings_per_num_ratings_data)

            plt.figure(figsize=(10, 6))
            plt.scatter(num_ratings, avg_ratings, alpha=0.6, edgecolors="k")

            plt.title(f"Average Rating vs. Number of Ratings: '{query}'", fontsize=14, weight="bold")
            plt.xlabel("Number of Ratings")
            plt.ylabel("Average Rating")
            plt.grid(True, linestyle="--", alpha=0.6)

            plt.tight_layout()
            plt.savefig(file_path)
            plt.close()

            return True
        
        except Exception as e:
            print(f"Could not create {file_path}: {e}")
            return False

def generate_charts(library_db: LibraryDB, query: str) -> None:
    """Generate all chart types for library data analysis.
    
    Creates and saves four different chart visualizations:
    - Format distribution pie chart
    - Publication year timeline
    - Most frequent authors bar chart  
    - Rating vs review count scatter plot
    
    Args:
        library_db (LibraryDB): Database instance containing library data.
        query (str): Search query used in chart titles.
    """
    charts = Charts()
    charts.format_distribution(library_db.get_format_data(), query, "visuals/format_distribution.png")
    charts.pub_year_distribution(library_db.get_pub_year_data(), query, "visuals/pub_year_distribution.png")
    charts.most_frequent_authors(library_db.get_frequent_authors(), query, "visuals/most_frequent_authors.png")
    charts.ratings_per_num_ratings(library_db.get_ratings_per_num_ratings(), query, "visuals/ratings_vs_num_ratings.png")