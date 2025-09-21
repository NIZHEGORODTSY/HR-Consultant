document.addEventListener('DOMContentLoaded', function() {
            // Анимация прогресс-баров
            const progressBars = document.querySelectorAll('.progress-fill');

            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0';

                setTimeout(() => {
                    bar.style.width = width;
                }, 500);
            });

            // Анимация кругового прогресса
            const circleProgress = document.querySelector('.circle-progress');
            setTimeout(() => {
                circleProgress.style.strokeDashoffset = '70';
            }, 500);

            // Имитация обновления данных
            setInterval(() => {
                // Здесь может быть код для обновления данных с сервера
                console.log('Обновление данных прогресса...');
            }, 30000);
        });