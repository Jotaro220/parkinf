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

    // Проверка на совпдаение паролей
    if (document.getElementById("psw-repeat") != null) {


      if (document.getElementById("psw").value != document.getElementById("psw-repeat").value) {
        removeError(document.getElementById("psw"));
        removeError(document.getElementById("psw-repeat"));
        console.log("Ошибка: пароли не совпадают");
        createError(document.getElementById("psw"), "Пароли не совпадают");
        createError(document.getElementById("psw-repeat"), "Пароли не совпадают");
        result = false;
      }
    }
    
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

    //Проверка на первую заглавную букву, ее единственность, в строке нет цифр
    if (input.dataset.name) {
      if (input.value.charAt(0) === input.value.charAt(0).toLowerCase()) {
        removeError(input);
        console.log("Ошибка: в поле  " + input.name + " первая буква должна быть заглавной");
        createError(input, "Первая буква должна быть заглавной");
        result = false;
      }

      for (let i = 1; i < input.value.length; i++) {
        if (input.value.charAt(i) === input.value.charAt(i).toUpperCase()) {
          removeError(input);
          console.log("Ошибка: в поле  " + input.name + " буквы должны быть строчными");
          createError(input, "Все кроме первой буквы должны быть строчными");
          result = false;
          break;
        }
      }
      if (/^[A-ZА-ЯЁ]+$/i.test(input.value) == false) {
        removeError(input);
        console.log("Ошибка: в поле  " + input.name + " недействительные символы");
        createError(input, "В поле должны быть только буквы");
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



    // Проверка email
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (input.dataset.validEmail) {
      if (re.test(input.value) == false) {
        removeError(input);
        console.log("Ошибка: в поле  " + input.name + " почта введена неверно");
        createError(input, "Почта введена неверно.");
        result = false;
      }
  
    }
    

  }
  return result;
}
if (document.getElementById('registration-form') != null){
document.getElementById('registration-form').addEventListener('submit', function(event) {
   event.preventDefault();
   if (validation(this) == true) {
     const name = document.getElementById("name").value;
     const surname = document.getElementById("surname").value;
     const pass = document.getElementById("psw").value;
     const email = document.getElementById("email").value;
     const login = document.getElementById("login").value;
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
}
else{
document.getElementById('login-form').addEventListener('submit', function(event) {
  event.preventDefault();
  if (validation(this) == true) {
    const pass = document.getElementById("psw").value;
    const login = document.getElementById("login").value;
    var formData = {
        username: login,
        password: pass,
    };
    $.ajax({
        type: "POST",
        url: "login_user",
        data: formData,
	headers: {'X-CSRFToken': csrftoken},
        success: function(response) {
            alert('Пользователь успешно авторизирован!');
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
}
