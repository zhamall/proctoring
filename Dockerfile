FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости
RUN pip install pytest selenium

# Копируем тесты (если не используете volume)
COPY test_login.py .

# Создаем папку для результатов
RUN mkdir -p test_results

# Запуск тестов (можно переопределить в docker-compose)
CMD ["pytest", "test_login.py", "-v"]