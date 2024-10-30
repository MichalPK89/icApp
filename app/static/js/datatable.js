$(document).ready(function () {
    console.log("Page is ready, finding tables with class 'display'");

    // Iterate through all tables with the class "display"
    $('table.display').each(function () {
        const tableId = $(this).attr('id') || 'default-table';
        const url = $(this).data('url');
        const tableBodyId = $(this).find('tbody').attr('id') || 'default-tbody';
        const loadingContainerId = '#lc_' + tableId;

        console.log(`Found table with data-url: ${url}, tbody ID: ${tableBodyId}`);

        // Call fetchTableData for each table
        fetchTableData(url, tableBodyId, $(this), loadingContainerId);

        function fetchTableData(url, tableBodyId, tableElement, loadingContainerId) {
            console.log(`Fetching data from URL: ${url}`);


            $(loadingContainerId).show();
            tableElement.hide();


            fetch(url, { method: 'GET', headers: { 'Content-Type': 'application/json' } })
                .then(response => {
                    console.log("Received response:", response);
                    return response.json();
                })
                .then(data => {
                    console.log("Fetched data:", data);


                    $(loadingContainerId).hide();
                    tableElement.show();


                    let tbody = document.getElementById(tableBodyId);
                    tbody.innerHTML = '';  // Clear existing rows

                    if (data.rows.length > 0) {
                        let headers = Object.keys(data.rows[0]);
                        console.log("Headers generated from data:", headers);

                        // Clear existing thead and create new one
                        tableElement.find('thead').empty();

                        // Create and append header row
                        let thead = '<tr>';
                        headers.forEach(header => {
                            thead += `<th>${header}</th>`;
                        });
                        thead += '</tr>';
                        tableElement.find('thead').append(thead);

                        // Create filter row
                        let filterRow = `<tr id="filterTable-${tableId}">`;
                        console.log(filterRow);
                        headers.forEach(header => {
                            filterRow += `<th><input type="text" placeholder="${header}" style="width: 100%"></th>`;
                        });
                        filterRow += '</tr>';
                        tableElement.find('thead').append(filterRow); // Append filter row

                        // Populate the table body with fetched data
                        data.rows.forEach(row => {
                            let tableRow = '<tr>';
                            headers.forEach(header => {
                                tableRow += `<td>${row[header] || ''}</td>`;
                            });
                            tableRow += '</tr>';
                            tbody.innerHTML += tableRow;
                        });

                        console.log("Table rows generated successfully.");
                    } else {
                        console.log("No rows found in data.");
                    }




                    // Initialize DataTable with export options
                    const newTable = tableElement.DataTable({
                        responsive: true,
                        scrollY: '500px',  // Set table height
                        scrollCollapse: true,  // Allow table to shrink if there's less data
                        paging: true,  // Enable paging
                        pageLength: 50,  // Set default rows per page
                        autoWidth: false,  // Disable auto column width
                        dom: 'Bfrtip',  // Add export buttons (CSV/Excel)
                        buttons: [
                            {
                                extend: 'csvHtml5',
                                text: 'Export CSV',
                                bom: true,  // Include UTF-8 BOM for encoding
                                filename: tableId,
                                fieldSeparator: ';',
                                customize: function (csv) {
                                    // Customize CSV to include headers
                                    const headers = tableElement.find('thead tr:eq(0) th').map(function () {
                                        return $(this).text();
                                    }).get();
                                    // Convert rows to CSV format, skipping second row
                                    const dataRows = tableElement.find('tbody tr:not(:eq(1))').map(function () {
                                        return $(this).find('td').map(function () {
                                            return $(this).text();
                                        }).get().join(";");
                                    }).get().join("\n");

                                    // Concatenate headers and data rows into CSV
                                    csv = headers.join(";") + "\n" + dataRows;
                                    return csv;
                                }
                            },
                            {
                                extend: 'excelHtml5',
                                text: 'Export Excel',
                                filename: tableId,
                                title: '',  // Avoid pulling in the base title
                                customize: function (xlsx) {
                                    var sheet = xlsx.xl.worksheets['sheet1.xml'];
                                    var headers = tableElement.find('thead tr:eq(0) th').map(function () {
                                        return $(this).text();
                                    }).get();

                                    // Add headers explicitly to the first row in the sheet XML
                                    var headerRow = '<row r="1">';
                                    headers.forEach((header, index) => {
                                        const cellRef = String.fromCharCode(65 + index) + "1";  // Convert index to Excel column letters (A, B, C...)
                                        headerRow += `<c t="inlineStr" r="${cellRef}"><is><t>${header}</t></is></c>`;
                                    });
                                    headerRow += '</row>';

                                    // Insert headers as the first row in the worksheet XML
                                    $(sheet).find('sheetData').prepend(headerRow);

                                    // Remove empty rows that may appear before the header row
                                    $('row', sheet).each(function (index) {
                                        if (index > 0 && $(this).find("c").length === 0) {
                                            $(this).remove();
                                        }
                                    });
                                },
                                exportOptions: {
                                    rows: ':not(:eq(1))',  // Exclude the filter row if it's the second row
                                    columns: ':visible'    // Export only visible columns
                                }
                            }
                        ]
                    });

                    // Apply individual column filters
                    newTable.columns().every(function (index) {
                        $(`#filterTable-${tableId} th input`).eq(index).on('keyup change', function () {
                            newTable
                                .column(index)
                                .search(this.value)
                                .draw();
                        });
                    });

                    console.log("DataTable initialized successfully.");
                })
                .catch(error => {
                    console.error('Error during data fetching:', error);
                });
        }
    });
});