// Добавляем интерактивность кнопкам
document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для кнопок добавления
    document.querySelectorAll('.add-button').forEach(button => {
        button.addEventListener('click', function() {
            const sectionTitle = this.parentElement.querySelector('.section-title').textContent;
            alert(`Добавление новой записи в раздел: ${sectionTitle}`);
        });
    });

    // Обработчик для кнопки редактирования
    document.querySelector('.edit-button').addEventListener('click', function() {
        alert('Редактирование профиля');
    });

    // Обработчики для навигационного меню
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            // Удаляем активный класс у всех ссылок
            document.querySelectorAll('.nav-menu a').forEach(item => {
                item.classList.remove('active');
            });

            // Добавляем активный класс к текущей ссылке
            this.classList.add('active');

            // В реальном приложении здесь будет переход между разделами
            alert(`Переход в раздел: ${this.textContent.trim()}`);
        });
    });
});