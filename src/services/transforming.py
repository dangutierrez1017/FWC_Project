"""
transforming.py
------------------
This module is responsible for transforming and joining FWCI data
through the use of LINQ operations into combined and flattened formats
for easier consumption by other backend and frontend services. The project
specifications require displaying relevant employee and image keycard entry
information in the frontend.

The join can be described by the SQL-like pseudocode:
WITH joined_data_full AS(
    SELECT *
    FROM Employees
    JOIN KeyCardEntries ON Employees.KeyCardId = KeyCardEntries.KeyCardId
    JOIN Images ON KeyCardEntries.SecurityImageId = Images.ImageId
    JOIN Categories ON Images.ImageCategoryId = Categories.categoryId;
)

The flattened data can be described by the SQL-like pseudocode utilizing the above joined_data_full CTE:
SELECT 
    KeyCardEntries.EntryId AS EntryID,
    Employees.FirstName AS FirstName,
    Employees.LastName AS LastName,
    Employees.WorkTitle AS WorkTitle,
    Employees.EmployeeId AS EmployeeID,
    Employees.WorkEmail AS EmployeeEmail,
    KeyCardEntries.EntryDateTime AS EntryDateTime,
    Images.ImageData AS ImageData,
    Images.ImageName AS ImageName,
    Images.ImageExtension AS ImageExtension
FROM joined_data_full;

Author: Daniel Gutierrez
Date: 10/22/2025
"""


from datetime import datetime
from py_linq import Enumerable
from .database_loader import load_employees_json, load_keyCard_Entries, load_images_json, load_categories_json

def join_data_full():
    """
    Converts the loaded JSON data into a py_linq Enumerable and performs
    the necessary LINQ joins to create a comprehensive dataset resembling the FWRI KeyCard Entry Database.

    Returns:
        Enumerable: A py_linq Enumerable containing the fully joined data.
    """
    
    employees_enum = Enumerable(load_employees_json())
    entries_enum = Enumerable(load_keyCard_Entries())
    images_enum = Enumerable(load_images_json())
    categories_enum = Enumerable(load_categories_json())

    joined_data = employees_enum.join(entries_enum, 
                                  lambda emp: emp['KeyCardId'], 
                                  lambda key: key['KeyCardId'], 
                                  lambda result: {'Employee': result[0], 'KeyCardEntry': result[1]})

    joined_data_images = joined_data.join(images_enum,
                                        lambda left: left['KeyCardEntry']['SecurityImageId'],
                                        lambda image: image['ImageId'],
                                        lambda result: {'Employee': result[0]['Employee'],
                                                        'KeyCardEntry': result[0]['KeyCardEntry'],
                                                        'Image': result[1]})

    #Increasingly complex use of lambda functions due to nested json structure
    final_data = joined_data_images.join(categories_enum, 
                                        lambda left: left['Image']['ImageCategoryId'],
                                        lambda category: category['categoryId'],
                                        lambda result: {'Employee': result[0]['Employee'],
                                                        'KeyCardEntry': result[0]['KeyCardEntry'],
                                                        'Image': result[0]['Image'],
                                                        'Category': result[1]})
    return final_data

def retrieve_flattened_data(enum):
    """
    Transforms the joined data Enumerable into a flattened structure
    containing only the relevant fields for display in the frontend
    through the use of LINQ select.

    Args:
        enum (Enumerable): The joined data Enumerable.
    Returns:
        list: A list of dictionaries containing the flattened data.
    """
    flattened_data = enum.select(lambda entry: {
            'EntryID': entry['KeyCardEntry']['EntryId'],
            'FirstName': entry['Employee']['FirstName'],
            'LastName': entry['Employee']['LastName'],
            'WorkTitle': entry['Employee']['WorkTitle'],
            'EmployeeID': entry['Employee']['EmployeeId'],
            'EmployeeEmail': entry['Employee']['WorkEmail'],
            'EntryDateTime': datetime.strptime(entry['KeyCardEntry']['EntryDateTime'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S"),
            'ImageData': entry['Image']['ImageData'],
            'ImageName': entry['Image']['ImageName'],
            'ImageExtension': entry['Image']['ImageExtension'],
            })
    return flattened_data.to_list()