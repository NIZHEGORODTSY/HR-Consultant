document.addEventListener('DOMContentLoaded', function() {
    // Фильтрация проектов
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Удаляем активный класс у всех кнопок
            filterButtons.forEach(btn => btn.classList.remove('active'));

            // Добавляем активный класс текущей кнопке
            this.classList.add('active');

            const filter = this.textContent.trim();

            // Фильтрация проектов
            projectCards.forEach(card => {
                const status = card.querySelector('.project-status').textContent.trim();

                if (filter === 'Все') {
                    card.style.display = 'block';
                } else if (filter === 'Активные' && status === 'Активный') {
                    card.style.display = 'block';
                } else if (filter === 'Завершенные' && status === 'Завершен') {
                    card.style.display = 'block';
                } else if (filter === 'Мои') {
                    // Здесь можно добавить логику для фильтрации "Мои проекты"
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // Поиск проектов
    const searchInput = document.querySelector('.search-input');

    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();

        projectCards.forEach(card => {
            const title = card.querySelector('.project-title').textContent.toLowerCase();
            const description = card.querySelector('.project-description').textContent.toLowerCase();

            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });

    // Создание нового проекта
    const createProjectBtn = document.querySelector('.create-project-btn');

    createProjectBtn.addEventListener('click', function() {
        alert('Функция создания нового проекта будет реализована здесь');
        // window.location.href = '/projects/create';
    });

    // Действия с проектом
    const actionButtons = document.querySelectorAll('.action-btn');

    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const projectCard = this.closest('.project-card');
            const projectTitle = projectCard.querySelector('.project-title').textContent;
            alert(`Действия с проектом: ${projectTitle}`);
        });
    });

    // Клик по карточке проекта
    projectCards.forEach(card => {
        card.addEventListener('click', function() {
            const projectId = this.getAttribute('data-project-id') || '123';
            window.location.href = `/projects/${projectId}`;
        });
    });

    // Пагинация
    const paginationButtons = document.querySelectorAll('.pagination-btn:not(.disabled)');

    paginationButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('active')) {
                document.querySelector('.pagination-btn.active').classList.remove('active');
                this.classList.add('active');
                alert('Загрузка страницы...');
            }
        });
    });
});