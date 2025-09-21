 document.addEventListener('DOMContentLoaded', function() {
            const taskCheckboxes = document.querySelectorAll('.task-checkbox');

            taskCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('click', function() {
                    this.classList.toggle('checked');
                    if (this.classList.contains('checked')) {
                        this.innerHTML = '<i class="fas fa-check"></i>';
                    } else {
                        this.innerHTML = '';
                    }
                });
            });

            setInterval(() => {
                // Здесь может быть код для обновления данных с сервера
                console.log('Обновление данных...');
            }, 30000);
        });