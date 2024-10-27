# Инструкция для развертывания проекта на сервере

## Подключение к удаленному серверу и создание экрана

1) ## Подключитесь к вашему удаленному серверу.
2) ## Создайте новый экран для запуска проекта:
   ```sh
   screen -S server_lb

3) ## Клонирование репозитория
Клонируйте репозиторий с проектом:

```git clone https://github.com/Stanislav-Kankin/another_webapp_bot.git```

# Установка зависимостей с помощью Poetry


4) ## Перейдите в директорию проекта:
```cd app```
Установите Poetry, если он еще не установлен:
```curl -sSL https://install.python-poetry.org | python3```

5) ## Установите зависимости проекта:
```poetry install```

6) ## Создание нового экрана для запуска ngrok
Выйдите из текущего экрана комбинацией клавиш Ctrl + a + d.
Создайте новый экран для запуска ngrok:
```screen -S server_ng```

7) ## Запуск ngrok
В новом экране запустите ngrok на порту, на котором будет запускаться приложение:
```ngrok http 8000```
Скопируйте полученную ссылку для создания туннеля.

# Настройка конфигурационных файлов
1) ## Перейдите в директорию проекта:
```cd app```, Откройте файл 
config_reader.py и в строке 17 вставьте полученную ссылку в константу WEBAPP_URL:

```WEBAPP_URL: str = "https://<ваша_ссылка>.ngrok-free.app"```

2) ## Откройте файл
```web/templates/index.html``` и в строке 27 вставьте ту же ссылку.

3) ## Настройка переменных окружения
Откройте файл .env и добавьте следующие строки:

```BOT_TOKEN="ваш_токен_бота"```
```DB_URL=sqlite://luckyboxdb.sqlite3```

4) ## Сохранение изменений и отправка на Git
Сохраните все изменения и отправьте их на Git:

```git add .```

```git commit -m "Update config and templates with ngrok URL"```

```git push origin main```

5) ## Обновление проекта и запуск
Перейдите обратно в экран server_lb:

```screen -r server_lb```

Обновите проект:

```git pull```

Запустите проект командой:

```poetry run python __main__.py```

# Проверка работы бота
После запуска бот готов к использованию.

# Примечания
Убедитесь, что у вас установлены все необходимые зависимости и инструменты (git, poetry, ngrok).
Если у вас возникнут проблемы с подключением или запуском, проверьте логи и убедитесь, что все настройки и переменные окружения указаны правильно.