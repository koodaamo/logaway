$(document).ready(function() {

    var table = $('#entries').DataTable();

	var connection = new autobahn.Connection({
	   url: 'ws://localhost:8888',
	   realm: 'logging'}
	);

	connection.onopen = function (session) {
	   function onevent1(args) {
	   		entry = args[0];
	   		var row = [entry.created, entry.name, entry.levelname, entry.msg];
	   		var rowNode = table.row.add(row).draw().node();
			$(rowNode).css('color', 'black').animate({ 'color':'rgba(0,255,0)' });
	   }
	   session.subscribe('logging', onevent1);
	};

	connection.open();

} );

