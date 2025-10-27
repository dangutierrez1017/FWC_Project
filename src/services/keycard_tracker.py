"""
keycard_tracker.py
------------------
Provides services to retrieve and filter keycard entry data
from the FWRI KeyCard Entry Database through the use of LINQ where.
Supports filtering by employee name and/or date range.

One of the filters can be described by the SQL-like pseudocode:
CREATE PROCEDURE GetKeyCardEntries
    @NameQuery NVARCHAR(100) = NULL,
    @StartDate DATETIME = NULL,
    @EndDate DATETIME = NULL
AS
BEGIN
    SELECT *
    FROM joined_data_full
    WHERE 
        @NameQuery  == EmployeeName AND
        @StartDate <= EntryDateTime AND EntryDateTime <= @EndDate OR

Author: Daniel Gutierrez
Date: 10/22/2025
"""

from datetime import datetime
from .transforming import join_data_full, retrieve_flattened_data

def retrieve_joined_data_full_raw():
    """Retrieve the fully joined data through python list of nested dictionaries."""
    return join_data_full().to_list()

def retrieve_flattened_data_full():
    """Retrieve the fully flattened data through python list of dictionaries."""
    return retrieve_flattened_data(join_data_full())

def retrieve_information_by_name(name_query):
    """
    Retrieve keycard entry information filtered by employee name.
    The search is case-insensitive and matches partial names input
    from the user. Uses LINQ where to filter the joined data.
    Args:
        name_query (str): The name or partial name to filter by.
    Returns:
        list: A list of dictionaries containing the flattened data
    """

    name_query = name_query.lower().strip() #Strip whitespace and convert to lowercase for case-insensitive search

    results = (join_data_full() #Combines first and last name for search
               .where(lambda entry: name_query in (entry['Employee']['FirstName'].lower() + ' ' + entry['Employee']['LastName'].lower())))
    
    return retrieve_flattened_data(results)


def retrieve_information_by_date_range(formatted_start_date, formatted_end_date):
    """
    Retrieve keycard entry information filtered by date range.
    Uses LINQ where to filter the joined data.
    Also that the date format used is in the DateTime format (YYYY-MM-DDTHH:MM:SSZ).
    
    Args:
        formatted_start_date (datetime): The start date for filtering.
        formatted_end_date (datetime): The end date for filtering.
    Returns:
        list: A list of dictionaries containing the flattened data
    
    """

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ" #Example: 2023-10-15T14:30:00Z
    
    results = (join_data_full()
               .where(lambda entry: formatted_start_date <= datetime.strptime(entry['KeyCardEntry']['EntryDateTime'],DATE_FORMAT) <= formatted_end_date))
    
    return retrieve_flattened_data(results)

def retrieve_information_by_both(name_query, formatted_start_date, formatted_end_date):
    """
    Combines the filtering logic of retrieve_information_by_name and
    retrieve_information_by_date_range to filter by both name and date range.

    Args:
        name_query (str): The name or partial name to filter by.
        formatted_start_date (datetime): The start date for filtering.
        formatted_end_date (datetime): The end date for filtering.
    Returns:
        list: A list of dictionaries containing the flattened data
    """

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ" #Example: 2023-10-15T14:30:00Z
    
    results = (join_data_full() #Combines first and last name for search and date range filtering
               .where(lambda entry: name_query in (entry['Employee']['FirstName'].lower() + ' ' + entry['Employee']['LastName'].lower()) 
                      and formatted_start_date <= datetime.strptime(entry['KeyCardEntry']['EntryDateTime'],DATE_FORMAT) <= formatted_end_date))
    return retrieve_flattened_data(results)

def retrieve_information(name_query=None, start_date=None, end_date=None):
    """
    Main function that retrieves keycard entry information based on optional filters:
    employee name, start date, and end date. Utilizes the specific filtering helper
    functions defined above.

    Args:
        name_query (str, optional): The name or partial name to filter by.
        start_date (str, optional): The start date in 'YYYY-MM-DD' format for filtering.
        end_date (str, optional): The end date in 'YYYY-MM-DD' format for filtering.
    Returns:
        list: A list of dictionaries containing the flattened data
    
    """
    DATE_FORMAT_INPUT = "%Y-%m-%d" #Example: 2023-10-15

    results = join_data_full()  

    # Handle date parsing to appropriate datetime objects
    if start_date and not end_date:
        start_date = datetime.strptime(start_date, DATE_FORMAT_INPUT)
        end_date = datetime.max
    elif not start_date and end_date:
        start_date = datetime.min
        end_date = datetime.strptime(end_date, DATE_FORMAT_INPUT)
    elif start_date and end_date:
        start_date = datetime.strptime(start_date, DATE_FORMAT_INPUT)
        end_date = datetime.strptime(end_date, DATE_FORMAT_INPUT)


    # Edge case: If start_date is after end_date, return empty list.
    if start_date and end_date and start_date > end_date:
        return []
    
    # Apply filtering based on provided parameters
    if name_query: 
        if start_date and end_date:
            return retrieve_information_by_both(name_query, start_date, end_date) 
        else:
            return retrieve_information_by_name(name_query)
    else:
        if start_date and end_date:
            return retrieve_information_by_date_range(start_date, end_date)
        else:
            return retrieve_flattened_data_full()
        
    
#TODO: Optimize by reducing the use of helper functions and combining filtering directly here.
