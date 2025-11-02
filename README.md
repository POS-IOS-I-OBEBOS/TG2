# Telegram Excise Stamp OCR Bot

Этот проект содержит Telegram-бота, который распознаёт текст на фотографиях
акцизных марок с помощью EasyOCR. Бот предназначен для запуска на платформе
[Render](https://dashboard.render.com/), но его также можно запускать локально.

## Возможности

- Команды `/start` и `/help` с кратким описанием.
- Приём фотографий от пользователя и распознавание текста на изображении.
- Настраиваемые языки OCR через переменную окружения `OCR_LANGUAGES`.

## Требования

- Python 3.10+
- Токен Telegram-бота (переменная окружения `TELEGRAM_BOT_TOKEN`).

## Установка локально

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Создайте файл `.env` (или экспортируйте переменные окружения другим способом)
со значением токена:

```bash
export TELEGRAM_BOT_TOKEN="<ваш токен бота>"
# Опционально: языки и использование GPU
export OCR_LANGUAGES="ru,en"
export OCR_USE_GPU="false"
```

Запустите бота:

```bash
python -m bot.main
```

## Деплой на Render

1. Создайте новый **Private Service** типа *Worker* в Dashboard Render.
2. Укажите репозиторий с этим проектом.
3. На вкладке **Environment** добавьте переменную `TELEGRAM_BOT_TOKEN` со
   значением токена вашего бота.
4. При необходимости добавьте `OCR_LANGUAGES` (например, `ru,en`) и
   `OCR_USE_GPU` (`true` или `false`).
5. В поле **Start Command** задайте:

   ```bash
   python -m bot.main
   ```

После деплоя Render будет автоматически запускать воркер, и бот начнёт обрабатывать
входящие сообщения.

## Структура проекта

```
.
├── bot
│   ├── __init__.py
│   ├── config.py        # Загрузка настроек из окружения
│   ├── handlers.py      # Telegram-хэндлеры
│   ├── main.py          # Точка входа
│   └── ocr.py           # Функции OCR
├── requirements.txt
└── README.md
```
