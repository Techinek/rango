$(document).ready(function () {
    $('#like_btn').click(function () {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like-category/',
            {'category_id': categoryIdVar},
            function (data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });
});

$(document).ready(function () {
    $('#search-input').keyup(function () {
        var query;
        query = $(this).val();

        $.get('/rango/suggest/',
            {'suggestion': query},
            function (data) {
                $('#categories-listing').html(data);
            }
        )
    })
})