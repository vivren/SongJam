$(document).ready(function() {
    $('#createRoom').change(function() {
        if($('#roomType-1').is(':checked')) {
            $('#roomPassword').css('visibility','visible');
        } else {
            $('#roomPassword').val('');
            $('#roomPassword').css('visibility','hidden');
        }
    });
});
