# last_kyrsov

REST API проект на Django Rest Framework с автоматизированным CI/CD пайплайном и деплоем на удаленный сервер.

## О проекте

Проект представляет собой backend-приложение на Django Rest Framework, которое обеспечивает создание REST API с автоматической документацией, аутентификацией и управлением данными. Проект включает полностью автоматизированный процесс развертывания с использованием GitHub Actions и Docker.

### Основные возможности:
- REST API с полным CRUD функционалом
- Аутентификация и авторизация (JWT или Session)
- Автоматическая документация API (Swagger/ReDoc)
- Админ-панель Django для управления данными
- Автоматическое тестирование при каждом push
- CI/CD пайплайн с деплоем на production сервер

### Использованные технологии

**Backend:** Python 3.10, Django, Django Rest Framework  
**База данных:** PostgreSQL  
**Контейнеризация:** Docker, Docker Compose  
**CI/CD:** GitHub Actions  
**Деплой:** SSH, Docker Hub  
**Инструменты:** pip, venv, git

## Требования

- Python 3.10+
- Docker и Docker Compose (для production)
- Git
- Удаленный сервер с Ubuntu 20.04/22.04 (для деплоя)
- Аккаунт Docker Hub
- GitHub репозиторий

## Локальная установка и запуск

### 1. Клонирование репозитория

  bash
git clone https://github.com/baleksey99/last_kyrsov.git
cd drf_project

### 2. Создание и активация виртуального окружения
Windows:

bash
python -m venv venv
venv\Scripts\activate
Linux/macOS:

bash
python3 -m venv venv
source venv/bin/activate
### 3. Установка зависимостей
bash
pip install -r requirements.txt
### 4. Настройка переменных окружения
Создайте файл .env:

bash
cp .env.example .env
Отредактируйте .env:

ini
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
### 5. Применение миграций и создание суперпользователя
bash
python manage.py migrate
python manage.py createsuperuser
### 6. Запуск сервера разработки
bash
python manage.py runserver
Приложение будет доступно: http://localhost:8000

# Настройка удаленного сервера для деплоя

## Шаг 1: Подготовка сервера
Подключитесь к серверу и выполните:

bash
### Обновление системы
sudo apt update && sudo apt upgrade -y

### Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

### Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

### Добавление пользователя в группу docker
sudo usermod -aG docker $USER

### Перезагрузка сервера (или выход и повторный вход)
sudo reboot

## Шаг 2: Настройка SSH ключей
На локальной машине:

bash
### Создание SSH ключа (если нет)
ssh-keygen -t ed25519 -C "your-email@example.com"

### Копирование ключа на сервер
ssh-copy-id user@your-server-ip

## Шаг 3: Проверка Docker на сервере
После перезагрузки сервера проверьте:

bash
### Проверка установки Docker
docker --version
docker-compose --version

### Проверка прав (не должно требовать sudo)
docker ps


# Настройка GitHub Actions CI/CD
## Шаг 1: Добавление секретов в GitHub
Перейдите в ваш репозиторий на GitHub: Settings → Secrets and variables → Actions → New repository secret

Добавьте следующие секреты:

Секрет	Описание	Пример
DOCKER_HUB_USERNAME	Имя пользователя Docker Hub	john_doe
DOCKER_HUB_ACCESS_TOKEN	Токен доступа Docker Hub	dckr_pat_xxxx
SSH_USER	Имя пользователя на сервере	ubuntu
SERVER_IP	IP адрес сервера	123.456.78.90
SSH_KEY	Приватный SSH ключ	-----BEGIN OPENSSH PRIVATE KEY-----

## Шаг 2: Получение Docker Hub Access Token
Войдите в Docker Hub

Перейдите в Settings → Security → New Access Token

Назовите токен (например, github-actions)

Выберите права: Read, Write, Delete

Скопируйте созданный токен (сохраните его, так как он показывается только один раз)

## Шаг 3: Получение SSH_KEY
На локальной машине выполните:

bash
 Просмотр приватного ключа
cat ~/.ssh/id_ed25519
 или
cat ~/.ssh/id_rsa
Скопируйте всё содержимое, включая:

text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
## Шаг 4: Создание файлов для CI/CD
Dockerfile
Создайте Dockerfile в корне проекта:

dockerfile
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=0

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "drf_project.wsgi:application", "--bind", "0.0.0.0:8000"]
.github/workflows/deploy.yml
Создайте директорию и файл:

yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Create static directory
      run: mkdir -p static
    
    - name: Run tests
      env:
        DB_HOST: localhost
        DB_NAME: testdb
        DB_USER: testuser
        DB_PASSWORD: testpass
      run: |
        python manage.py migrate
        python manage.py test

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_HUB_USERNAME }}
          password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
      
      - name: Build and push Docker image
        run: |
          docker build -t ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }} .
          docker tag ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }} ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest
          docker push ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}
          docker push ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:latest

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - name: Setup SSH
        uses: webfactory/ssh-agent@v0.8.1
        with:
          ssh-private-key: ${{ secrets.SSH_KEY }}
      
      - name: Deploy to server
        run: |
          ssh -o StrictHostKeyChecking=no ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "
            docker pull ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}
            docker stop myapp || true
            docker rm myapp || true
            docker run -d --name myapp -p 80:8000 --restart unless-stopped ${{ secrets.DOCKER_HUB_USERNAME }}/myapp:${{ github.sha }}
            docker image prune -f
          "
requirements.txt
Обновите requirements.txt:

txt
Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-dotenv==1.0.0
whitenoise==6.6.0

# Запуск CI/CD пайплайна
Автоматический запуск
Пайплайн запускается автоматически при:

Push в ветку main

Создании Pull Request в main

# Ручной запуск
Перейдите в ваш репозиторий на GitHub

Нажмите Actions

Выберите workflow CI/CD Pipeline

Нажмите Run workflow

Выберите ветку main и нажмите Run workflow

Мониторинг деплоя
В GitHub Actions:

Перейдите в Actions → выберите запущенный workflow

Следите за выполнением каждого job (test → build → deploy)

Зеленые галочки означают успешное выполнение

# На сервере:

bash
# Подключитесь к серверу
ssh user@your-server-ip

# Проверьте запущенные контейнеры
docker ps

# Посмотрите логи контейнера
docker logs myapp

# Проверьте работу приложения
curl http://localhost:80
Проверка успешного деплоя
После успешного выполнения workflow:

Откройте браузер и перейдите по адресу: http://your-server-ip

Должна открыться главная страница вашего Django приложения

Для доступа к админ-панели: http://your-server-ip/admin

Настройка линтеров
Проект использует:

black — для форматирования кода

isort — для сортировки импортов

flake8 — для проверки стиля кода

Установка инструментов
bash
pip install black isort flake8
Запуск проверок
bash
# Форматирование кода
black .

# Сортировка импортов
isort .

# Проверка стиля кода (исключая venv)
flake8 --exclude venv,.venv,migrations .
Запуск тестов
bash
# Запуск всех тестов
python manage.py test

# Запуск конкретного приложения
python manage.py test myapp

# Запуск с покрытием (если установлен coverage)
coverage run manage.py test
coverage report
Устранение неполадок
Проблема: Permission denied при запуске Docker
bash
# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
# Выйдите и зайдите снова
exit
ssh user@server
Проблема: Ошибка подключения к базе данных в CI
Убедитесь, что в workflow правильно настроены переменные окружения для PostgreSQL сервиса.

Проблема: Контейнер не запускается на сервере
bash
# Проверьте логи
docker logs myapp

# Проверьте, не занят ли порт 80
sudo netstat -tulpn | grep :80
Проблема: GitHub Actions не видит секреты
bash
# Добавьте debug шаг в workflow
- name: Debug secrets
  run: |
    echo "DOCKER_USER exists: ${{ secrets.DOCKER_HUB_USERNAME != '' }}"
    echo "SSH_USER exists: ${{ secrets.SSH_USER != '' }}"
Вклад в проект
Мы приветствуем вклад в проект! Чтобы предложить изменения:

Форкните репозиторий

Создайте ветку для вашей функции (git checkout -b feature/AmazingFeature)

Закоммитьте изменения (git commit -m 'Add AmazingFeature')

Запушьте в ветку (git push origin feature/AmazingFeature)

Откройте Pull Request

Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.

## Контакты
Автор: Алексей

Email: email@example.com

GitHub: baleksey99

## Благодарности
Django Community

GitHub Actions

Docker

Все контрибьюторы проекта

text

Этот `README.md` файл содержит полную информацию о проекте, инструкции по установке, настройке сервера, CI/CD пайплайну и устранению неполадок.