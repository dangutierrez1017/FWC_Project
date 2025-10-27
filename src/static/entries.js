/**
 * entries.js
 * ----------
 * This JS script handles the population and filtering of the keycard entries
 * displayed in the DataTable on the frontend. It fetches data from the backend
 * API endpoint and updates the table based on user input for name and date range.
 * 
 * Dependencies
 * -----------
 * - jQuery
 *      - Although largely replaced by React and pure JS in modern development,
 *        jQuery is still used here for simple integration with DataTables.js
 *        and better code readabilty.
 * - DataTables.Js
 * - Bootstrap5
 * 
 *
 * Author: Daniel Gutierrez
 * Date: 10/25/2025
 */


function displayEntries() {
/**
 * Implements and manages the DataTable displaying keycard entries.
 * Fetches JSON data from Flask API endpoint to fill the table.
 * Sets up filtering based on user input for name and date range.
 * 
 * Also provides basic error handling for invalid date ranges.
 * 
 * @returns {void}
 */

    const table = $('#entriesTable').DataTable({

        // Disables search box that comes with DataTables.js by default
        searching: false,

        // Ajax call to Flask API endpoint to fetch keycard entries data
        ajax: {
            // API endpoint URL
            url: '/api/entries',
            dataSrc: '',

            //Filter parameters sent to backend
            data: function (d) {
                d.name = $('#name').val().trim();
                d.start_date = $('#start_date').val();
                d.end_date = $('#end_date').val();
            }
        },

        // Define table columns and data mapping to JSON fields
        columns: [
            {data:'EntryID'},
            {data:'FirstName'},
            {data:'LastName'},
            {data:'WorkTitle'},
            {data:'EmployeeID'},
            {data:'EmployeeEmail'},
            {data:'EntryDateTime'},
            {
             data: 'ImageData',
             orderable: false, 

                // Function to render image thumbnail in row
             render: function (data, type, row) {
                    // If no image data, return placeholder dash
                if (!data) return '—';

                    // Construct image alt text using image file name
                const preview= `${row.ImageName}.${row.ImageExtension}` 
                return `<img class="thumb" alt=${preview} >`;
                }
            }
        ]
    })

    // Filter submission handler using jQuery
    $('#filterForm').on('submit', function (e) {

        // Prevent form submission to Flask server
        e.preventDefault(); 
        
        const start = $('#start_date').val();
        const end = $('#end_date').val();

        if (start && end) {
            const startDate = new Date(start);
            const endDate = new Date(end);
            
            // Will throw alert if start date is after end date
            if (startDate > endDate) { 
                alert('Start date cannot be later than end date.');
            }
         }  
        
        //Reload table data with new filters 
        table.ajax.reload(); 
    });
}

// Initialize DataTable
document.addEventListener("DOMContentLoaded", displayEntries);
