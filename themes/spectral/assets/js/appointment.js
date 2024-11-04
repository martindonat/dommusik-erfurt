$(function() {
$.ajax({
    url: "documents/Kalender_Termine.csv",
    async: false,
    success: function (csvd) {
        data = $.csv.toArrays(csvd);
    },
    dataType: "text",
    complete: function () {
        // call a function on complete 
		let i = 1;
		let nbrAppointement = 0;
		let today = new Date();
		let html = "";
		while (i < data.length) {
			
			//
			
			appointment = new Date(data[i][0].replace(/(.*)\.(.*)\.(.*)/, '$3-$2-$1'));
			if (appointment > today){
				html += '<li class="icon solid fa-music">';
                html += '<h3>'+ data[i][0] +'</h3>';
				html += '<p><b>'+ data[i][1] + ' Uhr '+ data[i][2] + '</b><br />'+ data[i][3] + '</p>';
				html += '</li>';
				nbrAppointement++;
			}
			i++
			if (nbrAppointement === 4) {
				break;
			}
		}
		$('#appointment').html(html);
    }
});
});
