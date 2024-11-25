$(function() {
    $.ajax({
        url: "documents/Kalender_Termine.csv",
        async: true,
        success: function (csvd) {
            data = $.csv.toArrays(csvd);
        },
        dataType: "text",
        complete: function () {
            let i = 1; // Start from the second row
            let today = new Date();
            let html = "";
            let currentYear = ""; // To track the current year
            let currentMonth = ""; // To track the current month

            // German month names
            const monthNames = [
                "Januar", "Februar", "März", "April", "Mai", "Juni", 
                "Juli", "August", "September", "Oktober", "November", "Dezember"
            ];

            // Loop through all data entries
            while (i < data.length) {
                // Convert the date from the first column
                let appointment = new Date(data[i][0].replace(/(.*)\.(.*)\.(.*)/, '$3-$2-$1'));
                
                // Check if the appointment date is in the future
                if (appointment > today) {
                    let year = appointment.getFullYear();
                    let month = appointment.getMonth(); // 0-11 for Jan-Dec
                
                    // Check for a new year
                    if (currentYear !== year) {
                        currentYear = year; // Update currentYear
                        html += `<h1>${year}</h1>`; // Add year header
                    }

                    // Check for a new month
                    if (currentMonth !== month) {
                        currentMonth = month; // Update currentMonth
                        // Add month header
                        html += `<h2>${monthNames[month]}</h2>`;
                        // Start a new table and add header row
                        html += `
                            <table>
                                <thead>
                                    <tr>
                                        <th>Datum</th>
                                        <th>Uhrzeit</th>
                                        <th>Ort</th>
                                        <th>Beschreibung</th>
                                    </tr>
                                </thead>
                                <tbody>`;
                    }

                    // Add appointment details in table row
                    html += `
                        <tr>
                            <td>${data[i][0]}</td>
                            <td>${data[i][1]}</td>
                            <td>${data[i][2]}</td>
                            <td>${data[i][3]}</td>
                        </tr>`;
                }
                i++; // Move to the next row
            }

            // Close the last table's tbody and table tags
            if (currentMonth !== "") {
                html += `
                            </tbody>
                        </table>`;
            }

            // Insert the generated HTML into the appointment element
            $('#appointment').html(html);
        }
    });
});
