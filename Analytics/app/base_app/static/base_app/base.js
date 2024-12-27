// для подсвеч активных ссылок открт
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
  link.addEventListener('click', () => {
    // Удаляем класс active у всех ссылок
    navLinks.forEach(link => link.classList.remove('active'));
    // Добавляем класс active к текущей ссылке
    link.classList.add('active');
  });
});
// для подсвеч активных ссылок закрыт

// Для подсветки активных ссылок в sidebar-href
const navLinksSidebar = document.querySelectorAll('.sidebar-href');
navLinksSidebar.forEach(link => {
  link.addEventListener('click', () => {
    // Удаляем класс active у всех ссылок
    navLinksSidebar.forEach(link => link.classList.remove('active'));
    // Добавляем класс active к текущей ссылке
    link.classList.add('active');
  });
});


