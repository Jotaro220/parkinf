const ratingButtons = document.querySelectorAll('.rating-buttons');
ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        // Получаем значение рейтинга из data-атрибута кнопки
        const value = parseInt(event.target.dataset.value)
        const carId = parseInt(event.target.dataset.car)
        const ratingSum = button.querySelector('.rating-sum');
        // Создаем объект FormData для отправки данных на сервер
        const formData = new FormData();
        // Добавляем id статьи, значение кнопки
        formData.append('car_id', carId);
        formData.append('value', value);
        // Отправляем AJAX-Запрос на сервер
        fetch("/catalog/rating", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            // Обновляем значение на кнопке
            ratingSum.textContent = data.rating_sum;
        })
        .catch(error => console.error(error));
    });
});
function show()
{   const carId = parseInt(document.querySelector('.btn-primary').dataset.car);

    const ratingSum = document.querySelector('.rating-sum');
    var formData = {
        car_id: carId,
    };
    $.ajax({
        type: "POST",
        url: "/catalog/upload-rating",
        data: formData,
        cache: false,
        success: function(data){
            ratingSum.textContent = data.rating;
        }
    });
}


$(document).ready(function(){

    show();
    setInterval('show()',1000);
});

// https://codething.ru/ajax.php
// javascript запуск fetch по таймеру