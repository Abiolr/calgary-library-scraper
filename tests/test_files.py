import pytest
import os
from unittest.mock import mock_open, patch
from src import LibraryDB, write_to_file, export_as_csv
from .sample import library_items_sample

def test_write_to_file(populated_db):
    """Test writing library data to text files"""
    query = "test_query"
    
    # Mock the file operations
    with patch("builtins.open", mock_open()) as mocked_file:
        write_to_file(populated_db, query)
        
        # Check that files were opened for writing
        assert mocked_file.call_count == 2
        
        # Get all write calls
        write_calls = []
        for call in mocked_file.return_value.write.call_args_list:
            write_calls.append(call[0][0])
        
        # Verify content contains expected sections
        content = "".join(write_calls)
        assert "ALL LIBRARY ITEMS" in content
        assert "LIBRARY RESULTS: test_query" in content
        assert "Format Distribution:" in content
        assert "Publication Year Distribution:" in content
        assert "Most Frequent Authors:" in content
        assert "Top Rated Authors (Unweighted):" in content
        assert "Top Rated Authors (Bayesian Weighted):" in content
        assert "Top Rated Books (Unweighted):" in content
        assert "Top Rated Books (Bayesian Weighted):" in content

def test_write_to_file_empty_db(db):
    """Test writing with empty database"""
    query = "empty_test"
    
    with patch("builtins.open", mock_open()) as mocked_file:
        write_to_file(db, query)
        
        # Should still attempt to write files
        assert mocked_file.call_count == 2

def test_write_to_file_exception_handling(populated_db):
    """Test exception handling in write_to_file"""
    query = "test_query"
    
    # Mock file operations to raise an exception
    with patch("builtins.open", side_effect=Exception("File error")):
        # Should not raise exception, should handle it gracefully
        try:
            write_to_file(populated_db, query)
            # If we get here, exception was handled
            assert True
        except Exception:
            pytest.fail("write_to_file should handle exceptions internally")

def test_export_as_csv(populated_db):
    """Test exporting library data to CSV"""
    
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("csv.writer") as mocked_writer:
            export_as_csv(populated_db)
            
            # Check that file was opened for writing
            mocked_file.assert_called_once_with("results/library_items.csv", "w", newline='')
            
            # Check that CSV writer was created and used
            mocked_writer.assert_called_once()
            mocked_writer.return_value.writerow.assert_called_once()

def test_export_as_csv_empty_db(db):
    """Test CSV export with empty database"""
    
    with patch("builtins.open", mock_open()) as mocked_file:
        with patch("csv.writer") as mocked_writer:
            export_as_csv(db)
            
            # Should still attempt to write file
            mocked_file.assert_called_once_with("results/library_items.csv", "w", newline='')
            mocked_writer.assert_called_once()

def test_export_as_csv_exception_handling(populated_db):
    """Test exception handling in export_as_csv"""
    
    # Mock file operations to raise an exception
    with patch("builtins.open", side_effect=Exception("CSV error")):
        # Should not raise exception, should handle it gracefully
        try:
            export_as_csv(populated_db)
            # If we get here, exception was handled
            assert True
        except Exception:
            pytest.fail("export_as_csv should handle exceptions internally")