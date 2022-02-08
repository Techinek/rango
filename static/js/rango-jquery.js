$("#about-btn").removeClass('btn-primary').addClass('btn-success');

$('#about-btn').click(function () {
    msgStr = $('#msg').html();
    msgStr = msgStr + ' ooo, fancy!';
    $('#msg').html(msgStr);
});