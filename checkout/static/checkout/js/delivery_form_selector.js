$('.delivery-form').hide();

$('#delivery-addresses').change(function() {
    var addressRef = $('#delivery-addresses').val();
    if (addressRef == 'None') {
        $('.delivery-form').hide();
        $('#blank-form').show();
    } else {
        $('#blank-form').hide();
        $('.delivery-form').hide();
        $(`#${addressRef}`).show();
    }

});