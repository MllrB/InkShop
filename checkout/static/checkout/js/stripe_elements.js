/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

//Delivery form selection
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

//stripe

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create an instance of the card Element.
var card = elements.create('card', {
    style: style,
    hidePostalCode: true
});

card.mount('#card-element');

// handle card validation errors
card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
            `
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// handle form submit
var form = document.getElementById('payment-form');

console.log

form.addEventListener('submit', function(ev) {
    console.log('form submitting')
    ev.preventDefault();


    //disable card entry and form submit button
    card.update({
        'disabled': true
    });
    $('#checkout-submit-btn').attr('disabled', true);

    // get shipping details from active form
    var shippingAddressRef = $('#delivery-addresses').val();
    if (shippingAddressRef == 'None') {
        var shippingFormRef = 'blank-form';
    } else {
        var shippingFormRef = shippingAddressRef;
    }
    var shippingForm = $(`#${shippingFormRef}`);
    var formName = shippingForm.find('input').attr('ID').slice(0, 10);

    function ShippingAddress() {
        this.shippingName = $(`#${formName}contact_name`).val();
        this.shippingPhone = $(`#${formName}contact_phone_number`).val();
        this.shippingLine1 = $(`#${formName}address_line1`).val();
        this.shippingLine2 = $(`#${formName}address_line2`).val();
        this.shippingTownCity = $(`#${formName}town_or_city`).val();
        this.shippingCounty = $(`#${formName}county`).val();
        this.shippingCountry = $(`#${formName}country`).val();
        this.shippingPostCode = $(`#${formName}post_code`).val();
    };

    shippingAddress = new ShippingAddress();

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.default_phone_number.value),
                email: $.trim(form.email.value),
                address: {
                    line1: $.trim(form.billing_address_line1.value),
                    line2: $.trim(form.billing_address_line2.value),
                    city: $.trim(form.billing_town_or_city.value),
                    country: $.trim(form.billing_country.value),
                    state: $.trim(form.billing_county.value),
                }
            }
        },
        shipping: {
            name: $.trim(shippingAddress.shippingName),
            phone: $.trim(shippingAddress.shippingPhone),
            address: {
                line1: $.trim(shippingAddress.shippingLine1),
                line2: $.trim(shippingAddress.shippingLine2),
                city: $.trim(shippingAddress.shippingTownCity),
                country: $.trim(shippingAddress.shippingCountry),
                postal_code: $.trim(shippingAddress.shippingPostCode),
                state: $.trim(shippingAddress.shippingCounty),
            }
        },
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `<span class="icon" role="alert">
                                <i class="fas fa-times"></i>
                                </span>
                                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);

            // $('#payment-form').fadeToggle(100);
            // $('#loading-overlay').fadeToggle(100);
            card.update({
                'disabled': false
            });
            $('#checkout-submit-btn').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});
/*$('#payment-form').fadeToggle(100);
//$('#loading-overlay').fadeToggle(100);

// From using {% csrf_token %} in the form
var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
var postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
};
//var url = '/checkout/cache_checkout_data/';

$.post(url, postData).done(function () {
    
    });
}).fail(function () {
    location.reload();
})*/