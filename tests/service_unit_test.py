import json
from src.services.transforming import join_data_full, retrieve_flattened_data
from src.services.keycard_tracker import retrieve_information
from py_linq import Enumerable

def test_join_data_full():

    joined = join_data_full().to_list()
    assert "Employee" in joined[0]
    assert "KeyCardEntry" in joined[0]
    assert "Image" in joined[0]
    assert "Category" in joined[0]

def test_flattened_data_format():
    joined = join_data_full()
    flattened = retrieve_flattened_data(joined)
    sample = flattened[0]
    assert "FirstName" in sample
    assert "EntryDateTime" in sample
    assert "ImageData" in sample

def test_retrieve_information_with_name_only(monkeypatch):

    monkeypatch.setattr("src.services.keycard_tracker.join_data_full", lambda: Enumerable([]))
    
    result = retrieve_information(name_query="Jean")
    assert isinstance(result, list)

def test_retrieve_information_with_date_range(monkeypatch):
    monkeypatch.setattr("src.services.keycard_tracker.join_data_full", lambda: Enumerable([]))
    
    start = "2025-09-01"
    end = "2025-09-30"
    result = retrieve_information(start_date=start, end_date=end)
    assert isinstance(result, list)

def test_retrieve_information_start_later_than_end(monkeypatch):
    monkeypatch.setattr("src.services.keycard_tracker.join_data_full", lambda: Enumerable([]))
    
    start = "2025-10-01"
    end = "2025-09-01"
    result = retrieve_information(start_date=start, end_date=end)
    assert result == []

