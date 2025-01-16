# Используем базовый образ Python (ARM-совместимый, если нужно для Raspberry Pi)
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт Flask
EXPOSE 5000

# Команда запуска
CMD ["python", "main.py"]
