# Используем официальный образ Python
FROM python:3.8

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в рабочую директорию
COPY . .

# Экспонируем порт 80 (или другой, который использует ваше веб-приложение)
EXPOSE 80

# Команда для запуска вашего веб-приложения
CMD ["python", "./main.py"]