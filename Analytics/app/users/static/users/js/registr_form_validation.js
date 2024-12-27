// Функция для отображения ошибок
const displayError = (fieldId, errorMessage) => {
  const errorElement = document.getElementById(`${fieldId}_error`);
  errorElement.textContent = errorMessage;
  errorElement.style.visibility = errorMessage ? "visible" : "hidden";
};

// Функция для валидации поля "Имя"
const validateName = () => {
  const name = document.getElementById("name").value.trim();
  if (name.length < 2) {
    displayError("name", "The name must be at least 2 characters.");
    return false;
  } else {
    displayError("name", "");
    return true;
  }
};

// Функция для валидации поля "Email"
const validateEmail = () => {
  const email = document.getElementById("email").value.trim();
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    displayError("email", "Please enter a valid email address.");
    return false;
  } else {
    displayError("email", "");
    return true;
  }
};

// Функция для валидации поля "Пароль"
const validatePassword = () => {
  const password = document.getElementById("password").value;
  if (password.length < 8) {
    displayError("password", "The password must be at least 8 characters.");
    return false;
  } else {
    displayError("password", "");
    return true;
  }
};

// Функция для валидации поля "Подтверждение пароля"
const validateConfirmPassword = () => {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  if (password !== confirmPassword) {
    displayError("confirm_password", "Passwords don't match");
    return false;
  } else {
    displayError("confirm_password", "");
    return true;
  }
};

// Обработчики событий для валидации при уходе с поля (blur)
document.getElementById("name").addEventListener("blur", validateName);
document.getElementById("email").addEventListener("blur", validateEmail);
document.getElementById("password").addEventListener("blur", validatePassword);
document.getElementById("confirm_password").addEventListener("blur", validateConfirmPassword);

// Деактивация кнопки отправки, если форма невалидна
document.getElementById("form").addEventListener("input", () => {
  const isFormValid = validateName() && validateEmail() && validatePassword() && validateConfirmPassword();
  document.getElementById("submit_button").disabled = !isFormValid;
});

// Обработчик события при отправке формы
document.getElementById("form").addEventListener("submit", function(event) {
  if (!validateName() || !validateEmail() || !validatePassword() || !validateConfirmPassword()) {
    event.preventDefault(); // Останавливаем отправку формы, если есть ошибки
  }
});
