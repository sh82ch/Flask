### REST API для сайта объявлений

&nbsp;*Flask*-приложение, которое использует *SQLAlchemy* для соединения с БД *PostgreSQL* и реализует API для управления объявлениями. Оно содержит три эндпоинта:
- `/advertisements` для создания объявления методом POST
- `/advertisements/<int:advertisement_id>` для получения методом *GET* и удаления объявления по *ID* методом *DELETE*


&nbsp;Класс *Advertisement* описывает модель объявления, включающую поля: id, title, description, date_created и owner. id используется в качестве первичного ключа. Поле date_created хранит время создания объявления (в UTC формате) и имеет значение по умолчанию – текущее время.

&nbsp;Метод `create_advertisement()` обрабатывает POST запросы на добавление нового объявления. Он получает JSON из тела запроса и извлекает из него значения полей title, description и owner. Если какие-то из этих полей отсутствуют, сервер вернет ошибку и статус 400. Если все поля присутствуют, объявление будет добавлено в БД методом `db.session.add(advertisement)`.

&nbsp;Метод `get_advertisement()` обрабатывает GET запросы для получения объявления по id. Он получает id из URL, извлекает из БД запись с таким id и возвращает ее в виде JSON.

&nbsp;Метод `delete_advertisement()` обрабатывает DELETE запросы на удаление объявления по его id. Получив id из URL, метод производит его удаление из БД.

&nbsp;В конце файла запускается приложение методом `app.run()`. При запуске также происходит создание всех таблиц в БД, описанных в модели *Advertisement*, за счет использования функции `db.create_all()`.

>Для запуска приложения:
>1) Необходимо установить зависимости, выполнив команду `poetry install`
>2) Запустить файл `app.py`