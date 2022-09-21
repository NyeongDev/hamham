// 리뷰 포스트
function post() {
    let title = $('#title').val()
    let desc = $('#desc').val()

    $.ajax({
        type: 'POST',
        // enctype: 'multipart/form-data',
        url: '/post',
        data: {title:title, desc:desc},
        success: function (response) {
            console.log(response)
            alert(response['msg'])
            window.location.reload()
        }
    });
}

// 리뷰 리스트
function listing() {
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

                let temp_html = `<div class="reviews-card">
                                        <div class="reviews-body">
                                            <h5 class="reviews-title">${title}</h5>
                                            <p class="reviews-desc">${desc}</p>
                                        </div>
                                    </div>`
                $('#cards-box').append(temp_html)
            }
        }
    })
}