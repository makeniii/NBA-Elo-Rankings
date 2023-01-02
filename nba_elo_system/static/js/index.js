$(document).ready( function () {
    $('#elo-table').DataTable({
        paging: false,
        info: false,
        "oLanguage": {
            "sSearch": "Team Search: "
        },
        "columns": [
            { "searchable": false },
            null,
            { "searchable": false },
            { "type": "num-fmt", "searchable": false },
            { "type": "num-fmt", "searchable": false },
            { "type": "num-fmt", "searchable": false }
        ]
    });
} );


