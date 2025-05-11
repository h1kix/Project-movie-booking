# Cinema Booking Application

Система бронирования киносеансов – это приложение для выбора фильмов, бронирования мест в зале и управления бронями. Проект реализован с использованием многослойной архитектуры: клиентская часть (GUI на Python с использованием Tkinter и ttkbootstrap), серверная часть (REST‑API на Flask с ORM‑поддержкой через SQLAlchemy) и база данных PostgreSQL.

---

## Краткое описание

Приложение позволяет пользователю:
- Просматривать список фильмов.
- Выбирать зал и место для бронирования с визуальным интерфейсом.
- Оформлять бронь, после чего данные автоматически сохраняются в базе данных.
- Отменять существующие бронирования.

Серверная часть реализует REST‑эндпоинты для работы с фильмами и бронированиями, а база данных хранит информацию о фильмах, залах, местах и бронированиях с обеспечением целостности данных (например, уникальные ограничения, внешние ключи). Клиентская часть отправляет запросы к серверу и отображает результаты пользователю.

---

## Использованные библиотеки

**Серверная часть:**
- **Flask** – веб-фреймворк для построения REST‑API.
- **SQLAlchemy** – ORM для работы с базой данных.
- **psycopg2‑binary** – драйвер для подключения к PostgreSQL.

**Клиентская часть:**
- **Tkinter** – стандартная библиотека для создания графического интерфейса.
- **ttkbootstrap** – набор тем и виджетов для современного оформления интерфейса.
- **requests** – HTTP‑библиотека для отправки запросов к серверу.

**Прочее:**
- **pgAdmin4** – инструмент для управления базой данных PostgreSQL (используется при разработке и отладке).

---

## Архитектура приложения и интеграция модулей

### Общая архитектура

Приложение реализовано по многослойной архитектуре:
- **Клиентский слой (View):**  
  Реализован на Python с использованием Tkinter совместно с ttkbootstrap для создания современного дизайна. Этот слой отображает окна, собирает ввод пользователя (например, выбор фильма, зала, места) и отправляет HTTP‑запросы к серверной части.
- **Серверный слой (Controller & Model):**  
  Реализован с использованием Flask для создания REST‑API. Контроллеры (организованные через Blueprints) получают HTTP‑запросы, работают с моделями (определёнными через SQLAlchemy) и возвращают данные в формате JSON.
- **База данных (Data):**  
  PostgreSQL используется для хранения информации о фильмах, залах, местах и бронированиях. Структура базы данных определяется с помощью DDL‑скриптов, включающих таблицы `movies`, `auditoriums`, `seats` и `bookings`.

### Применяемые шаблоны проектирования

- **Model-View-Controller (MVC):**  
  Чёткое разделение ответственности между интерфейсом (View), бизнес‑логикой и обработчиками HTTP‑запросов (Controller), и слоями доступа к данным (Model).
- **Active Record (ORM):**  
  Модели (`Movie`, `Booking`, `Auditorium`, `Seat`) реализованы как классы SQLAlchemy с методами для сериализации (например, `to_dict()`).
- **RESTful API:**  
  Сервер реализует эндпоинты для обработки HTTP‑запросов посредством декораторов Flask.
- **Dependency Injection:**  
  Объект контроллера (например, `MovieController`) передаётся в представления для облегчения тестирования и переиспользования компонентов.
- **Observer (Event-Driven Programming):**  
  Клиентский интерфейс реагирует на события (например, выбор места, нажатие кнопок) и обновляет отображение через обратные вызовы.

### Внутренние стандарты и оформление кода

- Код оформляется согласно [PEP 8](https://www.python.org/dev/peps/pep-0008/) и [PEP 257](https://www.python.org/dev/peps/pep-0257/).
- Используются внутренние корпоративные стандарты (например, модульность, именование переменных, структурирование проекта) и, при необходимости, соответствие отраслевым стандартам и ГОСТ.
- Все зависимости регистрируются в файле `requirements.txt` и управляются через менеджер пакетов pip.

---

## Скрипт создания базы данных (DDL)

sql
-- Создание базы данных
CREATE DATABASE cinema_db;
\connect cinema_db;

## Таблица movies
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT
);
CREATE INDEX idx_movies_title ON movies(title);

-- Таблица auditoriums
CREATE TABLE auditoriums (
    id SERIAL PRIMARY KEY
);

## Таблица seats
CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    row INT NOT NULL CHECK (row > 0),
    number INT NOT NULL CHECK (number > 0),
    auditorium_id INT NOT NULL,
    CONSTRAINT fk_auditorium FOREIGN KEY (auditorium_id)
        REFERENCES auditoriums(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_seat UNIQUE (row, number, auditorium_id)
);

## Таблица bookings
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    movie_id INT NOT NULL,
    seat_id INT NOT NULL,
    CONSTRAINT fk_movie FOREIGN KEY (movie_id)
        REFERENCES movies(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_seat FOREIGN KEY (seat_id)
        REFERENCES seats(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_booking UNIQUE (movie_id, seat_id)
);

## Дополнительные индексы
CREATE INDEX idx_booking_movie ON bookings(movie_id);
CREATE INDEX idx_booking_seat ON bookings(seat_id);
## Инструкции по запуску

### Предварительные требования:

Python 3.7+

PostgreSQL (версия 10 и выше)

Установленный менеджер пакетов pip

### Установка
Клонируйте репозиторий

bash
git clone https://github.com/your_username/cinema-booking.git
cd cinema-booking
Установите зависимости

bash
pip install -r requirements.txt
Или устанавливайте библиотеки вручную:

bash
pip install flask sqlalchemy psycopg2-binary requests ttkbootstrap
Настройте базу данных

Убедитесь, что PostgreSQL установлен и запущен (стандартный порт: 5432).

Создайте базу данных:

sql
CREATE DATABASE cinema_db;
Отредактируйте файл конфигурации подключения (например, database.py) в соответствии с настройками вашей системы.

### Запуск приложения и серверной части

Перейдите в директорию server/.

Запустите Flask-сервер:

bash
python app.py
Сервер будет слушать подключения по адресу: http://localhost:5000/.

Запуск клиентской части
Перейдите в директорию client/.

Запустите GUI‑приложение:

bash
python views.py
Откроется окно интерфейса, где можно выбрать фильм, перейти к залу и оформить/отменить бронь.

## Интеграция сторонних модулей

### В проекте использовались следующие сторонние модули:

Flask – для построения REST‑API.

SQLAlchemy и psycopg2‑binary – для работы с базой данных PostgreSQL.

requests – для отправки HTTP‑запросов из клиентской части.

ttkbootstrap – для стилизации графического интерфейса.

Tkinter – для создания GUI.

## Заключение
Cinema Booking Application демонстрирует стабильное взаимодействие клиентской части с серверным API и базой данных. В приложении используется современный интерфейс, многослойная архитектура и проверенные шаблоны проектирования (MVC, Active Record, RESTful API). Тщательное тестирование и отладка обеспечивают целостность данных, корректную работу всех модулей и удобство дальнейшего масштабирования проекта.
