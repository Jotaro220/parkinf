document.getElementById('dateStart').valueAsDate = new Date();
document.getElementById("dateStart").min = new Date().toISOString().split("T")[0];
document.getElementById('dateEnd').valueAsDate = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
  document.getElementById('dateEnd').min = new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toISOString().split("T")[0];

  document.getElementById("dateStart").addEventListener('change',function (){

    if (document.getElementById("dateEnd").valueAsDate <= document.getElementById("dateStart").valueAsDate){
    document.getElementById('dateEnd').valueAsDate = new Date(new Date(this.value).getTime() + 24 * 60 * 60 * 1000);
    document.getElementById("dateEnd").min = new Date(new Date(this.value).getTime() + 24 * 60 * 60 * 1000);
    }

    var str = document.getElementById('payment').textContent.split(/[s*=]+/);
    var price = str[0];
    const date1 = new Date(this.value);
    const date2 = new Date(document.getElementById('dateEnd').value);
    let Difference_In_Time = date2.getTime() - date1.getTime();
    let dates = Math.round(Difference_In_Time / (1000 * 3600 * 24));
    var sum = dates * price;
    document.getElementById('payment').textContent = price+' * '+dates+' = '+sum;
  });


document.getElementById("dateEnd").addEventListener('change',function (){

  var str = document.getElementById('payment').textContent.split(/[s*=]+/);
  var price = str[0];
  const date1 = new Date(document.getElementById('dateStart').value);
  const date2 = new Date(this.value);
  let Difference_In_Time = date2.getTime() - date1.getTime();
  let dates = Math.round(Difference_In_Time / (1000 * 3600 * 24));
  var sum = dates * price;
  document.getElementById('payment').textContent = price+' * '+dates+' = '+sum;
});


document.getElementById('order-form').addEventListener('submit', function(event) {
  event.preventDefault();
    const carId = parseInt(document.querySelector('.btn-order').dataset.car);
    console.log(carId); 
    const dateStart = document.getElementById("dateStart").value;
    const dateEnd = document.getElementById("dateEnd").value;
    const address = document.getElementById("adress").value;
    var str = document.getElementById('payment').textContent.split('=');
    var cost = str[1]; 
    var formData = {
	    carId: carId,
        dateStart: dateStart,
        dateEnd:  dateEnd,
	    address: address,
	    cost: cost,
    };
    $.ajax({
        type: "POST",
        url: "/catalog/order_car", // URL для создания нового пользователя на Django сервере
        data: formData,
        headers: {'X-CSRFToken': csrftoken},
        success: function(response) {
            alert('Пользователь успешно авторизирован!');
//          window.location.href = 'car_list';
        },
        error: function(xhr, status, error) {
            alert('Произошла ошибка при создании.');
            console.error(error);
        }
    });
})