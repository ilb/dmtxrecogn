# Указываем базовый образ
FROM python:3.6

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y libdmtx0b libdmtx-dev libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем все файлы проекта в рабочую директорию
COPY . .

# Устанавливаем watchdog и другие зависимости проекта
RUN pip install .["test"]

# Запускаем команду по умолчанию при запуске контейнера
CMD ["python", "setup.py", "run"]
