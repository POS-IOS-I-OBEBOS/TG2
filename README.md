# Telegram Excise Stamp OCR Bot

Бот для Telegram, который распознает акцизные марки на фотографиях и возвращает текст с помощью OCR.space. Проект можно развернуть на [Render](https://dashboard.render.com/).

## Возможности

- Команда `/start` с кратким описанием.
- Поддержка помощи через `/help`.
- Прием фотографий и отправка распознанного текста с OCR.space.
- Настройка языка распознавания через переменную окружения `OCR_LANGUAGE`.

## Локальный запуск

1. Установите Python 3.10+ и создайте виртуальное окружение.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Экспортируйте переменные окружения (опционально):
   ```bash
   export TELEGRAM_BOT_TOKEN="<ваш_бот_токен>"  # можно ввести при запуске
   export OCR_SPACE_API_KEY="<ключ_OCR_space_или_helloworld>"
   export OCR_LANGUAGE="rus"  # опционально, по умолчанию eng
   export BOT_LOG_FILE="logs/bot.log.txt"  # опционально, путь к файлу логов
   ```
4. Запустите бота и при необходимости введите токен в командной строке:
   ```bash
   python -m bot.main
   ```
5. Логи работы сохраняются в файл `bot.log.txt` (или путь из `BOT_LOG_FILE`).

## Развертывание на Render

1. Создайте новый Worker-сервис на Render и подключите репозиторий.
2. Render автоматически прочитает файл `render.yaml` и настроит сборку:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m bot.main`
3. Укажите переменные окружения в настройках Render:
   - `TELEGRAM_BOT_TOKEN`
   - `OCR_SPACE_API_KEY`
   - `OCR_LANGUAGE` (опционально)
4. Сохраните настройки и запустите сервис. Worker начнет polling Telegram и будет готов принимать фотографии.

## Переменные окружения

| Переменная              | Назначение                                                  |
| ----------------------- | ----------------------------------------------------------- |
| `TELEGRAM_BOT_TOKEN`    | Токен Telegram-бота (обязательная).                         |
| `OCR_SPACE_API_KEY`     | Ключ OCR.space (`helloworld` — публичный тестовый ключ).    |
| `OCR_LANGUAGE`          | Код языка для OCR (напр. `eng`, `rus`).                     |
| `BOT_LOG_FILE`          | Путь к файлу логов (по умолчанию `bot.log.txt`).            |

## Лицензия

Проект распространяется под лицензией MIT.
