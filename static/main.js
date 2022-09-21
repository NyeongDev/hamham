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
            window.location.reload()
        }
    });
}

// 리뷰 리스트
function show_reviews() {
    $('#cards-box').empty()
    $.ajax({
        type: 'GET',
        url: '/api/reviews',
        data: {},
        success: function (response) {
            let rows = response['reviews']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let desc = rows[i]['desc']

                let temp_html = ``
                $('#cards-box').append(temp_html)
            }
        }
    })
}