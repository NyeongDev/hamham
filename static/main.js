// 리뷰 포스트
function post() {
    let title = $('#title').val()
    let desc = $('#desc').val()

    $.ajax({
        type: 'POST',
        // enctype: 'multipart/form-data',
        url: '/post/send',
        data: {title_give:title, desc_give:desc},
        success: function (response) {
            alert(response['msg'])
            window.location.href='/';
        }
    });
}