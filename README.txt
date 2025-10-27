# FWRI Key Card Access Tracker
*A lightweight browser-based application for reviewing and filtering facility access records.*

---

## Overview
This project was developed as part of application design exercise for the Data Administration Analyst for the Florida Fish
and Wildlife Conservation Commission  
It simulates how security staff and administrators at the Florida Wildlife Research Institute (FWRI) could efficiently search and review building access events.

The application loads data from JSON files (representing database tables) and allows users to:

- Filter entries by **employee name** and/or **date range**
- Display **employee details**, **access timestamps**, and **security camera snapshots**
- View results interactively in a web-based DataTable

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-------------|----------|
| **Backend** | Flask (Python) | Web server, routing, data processing |
| **Data** | JSON + PyLinq | Simulated database and query operations |
| **Frontend** | HTML, Bootstrap, jQuery, DataTables.js | Interactive UI and filtering |
| **Language** | Python 3.11 | Core business logic and data transformation |

---

## Design Approach: My Take on MVC
While this project doesn’t use a full framework like Django, I structured it around **Model-View-Controller (MVC)** principles to keep logic separated and maintainable.

- **Model:**  
  The *data and transformation layer* in `src/services/`.  
  It loads JSON files (Employees, KeyCardEntries, Images, Categories) and uses PyLinq to perform in-memory joins and transformations, mimicking SQL queries.

- **View:**  
  The HTML interface (`src/views/index.html`) and the JavaScript logic (`src/static/entries.js`).  
  Responsible for rendering data, handling filters, and making AJAX requests to the backend.

- **Controller:**  
  Flask route handlers in `src/controllers/routes.py`.  
  They act as the bridge between frontend requests and backend services — receiving query parameters, calling business logic, and returning responses.


> 💡 This structure kept the project easy to reason about and test, even as features like filtering and validation were added.

---

## Core Features
- **Interactive Filtering:** Search by name, date, or both (partial matching supported)  
- **Image Rendering:** Displays base64-encoded security camera snapshots inline  
- **Date Validation:** Prevents invalid date ranges (e.g., start > end)  
- **Formatted Output:** Dates displayed in `MM/DD/YYYY HH:MM:SS` format  
- **Clean Separation of Logic:** Modularized business rules, data joining, and frontend rendering  

---

## How It Works
1. Flask loads data from JSON into Python dictionaries.  
2. PyLinq performs multi-table joins to simulate SQL queries.  
3. The resulting dataset is flattened for JSON serialization.  
4. The frontend fetches data via AJAX and populates the DataTable dynamically.  
5. Filters are sent as query parameters (`name`, `start_date`, `end_date`) to the `/api/entries` endpoint.

---

