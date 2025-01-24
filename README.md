
# [Wheesh](https://wheesh.ru)

## О проекте

**Wheesh** – это веб-приложения для создания списков желаний и возможности поделиться ими с кем угодно.

**Приложение помогает:**

- Просто и быстро ***создавать списки желаний*** (вишлисты).
- ***Бронировать*** подарки в чужих вишлистах.
- Делиться своими вишлистами с помощью удобных ***коротких ссылок***.

## Установка

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/DatPill/wheesh.git
    cd wheesh
    ```

2. **Настройте окружение:**
    Убедитесь, что у вас установлен Python 3.12 или новее. Затем создайте виртуальное окружение.
   - *Для Linux/MacOS:*

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

   - *Для Windows:*

    ```bash
    python -m venv .venv
    venv\Scripts\activate
    ```

3. **Установите зависимости:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настройте переменные окружения:**

    Для запуска необходимо создать `.env` файл

    - *Linux/MacOS:*

    ```bash
    cp .env.example .env
    ```

    - *Windows:*

    ```bash
    copy .env.example .env
    ```

    После чего необходимо открыть файл `.env` и задать все необходимые перменные окружения.

    ---

    Создать DJANGO_SECRET_KEY можно командой:

    - *Linux/MacOS:*

    ```bash
    python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

    - *Windows:*

    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ```

5. **Запустите систему:**

    Для запуска используйте Docker Compose:

    ```bash
    docker-compose up
    ```

6. **Проверьте систему:**

   Перейдите в браузер и откройте интерфейс сайт (обычно доступен по адресу `http://localhost:8000`).

## Roadmap

- [x] Реализовать возможность бронирования подарков
- [ ] Адаптировать под мобильные устройства
- [ ] Переписать фронтенд на VueJS/React
- [ ] Подключить Telegram-бота
- [ ] Подключить Telegram Mini App
- [ ] Добавить режим тайного санты
- [ ] Добавить возможность создания нескольких вишлистов на аккаунте
- [ ] Добавить возможность напоминания о мероприятии вишлиста
- [ ] Реализовать совместные вишлисты
