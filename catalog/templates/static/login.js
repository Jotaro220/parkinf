function validation(form) {
  function removeError(input) {
    const parent = input.parentNode;
    if (parent.classList.contains("error")) {
      parent.querySelector(".error-label").remove();
      parent.classList.remove("error");
    }
  }


  function createError(input, text) {
    const parent = input.parentNode;
    const errorLabel = document.createElement('label');



    errorLabel.classList.add("error-label");
    errorLabel.textContent = text;

    parent.classList.add("error");

    parent.append(errorLabel);
  }




  let result = true;

  const allInputs = form.querySelectorAll('input');
  for (const input of allInputs) {
    removeError(input);


    //Проверка на минимальную длину строки
    if (input.dataset.minLength) {
      if (input.value.length < input.dataset.minLength) {
        console.log("Ошибка: в поле  " + input.name + " меньше " + input.dataset.minLength + " символов");
        createError(input, `Минимальное кол-во символов: ${input.dataset.minLength} симв`);
        result = false;
      }
    }
    //Проверка на максимальную длину строки
    if (input.dataset.maxLength) {
      if (input.value.length > input.dataset.maxLength) {
        console.log("Ошибка: в поле  " + input.name + " больше " + input.dataset.maxLength + " символов");
        createError(input, `Максимальное кол-во символов: ${input.dataset.maxLength} симв`);
        result = false;
      }
    }



    //Проверка на наличие пробелов в строке
    if (input.dataset.noSpace) {
      if (input.value.indexOf(' ') >= 0) {
        removeError(input);
        console.log("Ошибка: в поле  " + input.name + " не должно быть пробелов");
        createError(input, "В поле не должно быть пробелов");
        result = false;
      }
    }



    //Проверка на пустое поле
    if (input.value == "") {
      removeError(input);
      console.log("Ошибка: поле " + input.name + " не заполнено");
      createError(input, "Поле не заполнено");
      result = false;
    }

    if (input.dataset.noSpace) {
      if (input.value.indexOf(' ') >= 0) {
        removeError(input);
        console.log("Ошибка: в поле  " + input.name + " не должно быть пробелов");
        createError(input, "В поле не должно быть пробелов");
        result = false;
      }
    }

document.getElementById('add-form').addEventListener('submit', function(event) {
  event.preventDefault();
  if (validation(this) == true) {
    const name = document.getElementById("name").value;
    const surname = document.getElementById("surname").value;
    const pass = document.getElementById("psw").value;
    const email = document.getElementById("email").value;
    const login = document.getElementById("login").value;
    console.log(name);
    var formData = {
        username: login,
        name: name,
        surname: surname,
        password: pass,
        email: email
    };
    $.ajax({
        type: "POST",
        url: "create_user", // URL для создания нового пользователя на Django сервере
        data: formData,
        success: function(response) {
            alert('Пользователь успешно!');
          window.location.href = 'car_list';
            // Здесь вы можете выполнить какие-либо дополнительные действия после создания пользователя
        },
        error: function(xhr, status, error) {
            alert('Произошла ошибка при создании.');
            console.error(error);
        }
    });
  }
})
