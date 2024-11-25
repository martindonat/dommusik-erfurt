$(function() {
    $.ajax({
        url: "documents/Kalender_Termine.csv",
        async: false,
        success: function (csvd) {
            data = $.csv.toArrays(csvd);
        },
        dataType: "text",
        complete: function () {
            let today = new Date();
            let appointments = [];

            // Collect upcoming appointments
            for (let i = 1; i < data.length; i++) {
                let appointmentDate = new Date(data[i][0].replace(/(.*)\.(.*)\.(.*)/, '$3-$2-$1') + ' ' + data[i][1]);
                if (appointmentDate > today) {
                    appointments.push({
                        date: appointmentDate,
                        title: data[i][0],
                        time: data[i][1],
                        details: data[i][2],
                        description: data[i][3]
                    });
                }
            }

            // Sort appointments by date and time
            appointments.sort(function(a, b) {
                return a.date - b.date;
            });

            // Prepare HTML for the first four appointments
            let html = "";
            for (let i = 0; i < Math.min(appointments.length, 4); i++) {
                let appointment = appointments[i];
                html += '<li class="icon solid fa-music">';
                html += '<h3>' + appointment.title + '</h3>';
                html += '<p><b>' + appointment.time + ' Uhr ' + appointment.details + '</b><br />' + appointment.description + '</p>';
                html += '</li>';
            }

            $('#appointment').html(html);
        }
    });
});
