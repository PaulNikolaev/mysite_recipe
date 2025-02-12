 # Проект ["Cайта рецептов на Django" (https://mysiterecipe.ru)](https://mysiterecipe.ru) 

 ## Описание

 Проект "Сайт рецептов на Django" разработан с использованием технологий фрэймворка Django и Bootstrap. Это приложение дает возможность регистрации на сайте, добавления и управления рецептами авторизованными пользователями, просмотр рецептов других пользователей

## Возможности приложения управления учетными записями пользователей

Это приложение предоставляет функции для управления учетными записями пользователей с возможностью регистрации, авторизации, редактирования профиля и восстановления пароля:

### 1. **Просмотр профиля**
   - Пользователи могут просматривать информацию о своем профиле, включая связанные категории рецептов. Для этого используется представление `ProfileDetailView`, которое отображает профиль пользователя и его данные.
   
### 2. **Редактирование профиля**
   - Пользователи могут обновить свой профиль, включая информацию о себе и своей учетной записи. Это реализовано через представление `ProfileUpdateView`, которое использует формы для обновления данных и транзакции для атомарности операции.
   
### 3. **Регистрация**
   - Новый пользователь может зарегистрироваться на сайте, заполнив форму регистрации. После успешной регистрации пользователю показывается сообщение о подтверждении. Это реализовано через представление `UserRegisterView`.
   
### 4. **Авторизация и выход**
   - Пользователи могут войти в систему, используя форму авторизации, и выйти через представления `UserLoginView` и `UserLogoutView`. После успешной авторизации отображается приветственное сообщение.
   
### 5. **Изменение пароля**
   - Пользователи могут изменить свой пароль с помощью формы `CustomPasswordChangeView`, доступной только после входа в систему. Логирование отслеживает изменение пароля.
   
### 6. **Восстановление пароля**
   - Пользователи могут запросить восстановление пароля по электронной почте через представление `CustomPasswordResetView`. Им будет отправлено письмо с инструкциями по восстановлению пароля.
   
### 7. **Подтверждение сброса пароля**
   - После получения инструкции по восстановлению пароля, пользователи могут установить новый пароль с помощью формы `CustomPasswordResetConfirmView`.

---

### Дополнительные особенности:
- **Логирование**: Все действия пользователей, такие как регистрация, авторизация и изменения профиля, логируются для отслеживания событий.
- **Категории рецептов**: Все представления добавляют в контекст категории рецептов, что позволяет пользователям легко переходить к нужным разделам на сайте.
- **Сообщения об успехе**: После успешных действий (например, регистрации или изменения пароля) пользователи получают соответствующие уведомления об успехе.

--- 

Таким образом, приложение предоставляет полный набор функционала для работы с учетными записями пользователей на сайте, обеспечивая удобный интерфейс для управления профилем и безопасности.


## Возможности приложения для работы с рецептами

Это приложение предоставляет возможности для создания, просмотра, редактирования и удаления рецептов, ингредиентов и этапов приготовления. Также присутствует функция поиска рецептов по названию с использованием триграммного сходства.

### 1. **Просмотр рецептов**
   - **Главная страница**: Просмотр списка всех рецептов на главной странице с пагинацией.
   - **Просмотр рецепта**: Детальный просмотр конкретного рецепта, включая описание, ингредиенты и шаги приготовления.

### 2. **Поиск рецептов**
   - **Поиск по названию**: Возможность поиска рецептов по названию с использованием триграммного сходства для точности результатов.

### 3. **Категории рецептов**
   - Рецепты можно фильтровать по категориям, с отображением всех рецептов, относящихся к конкретной категории.

### 4. **Создание рецепта**
   - Пользователи могут создавать новые рецепты с помощью формы. После создания рецепта автором является текущий пользователь.
   
### 5. **Редактирование рецепта**
   - Пользователи могут редактировать свои рецепты, обновляя информацию о них, включая название, описание и ингредиенты.

### 6. **Удаление рецепта**
   - Возможность удалить рецепт, если он был создан текущим пользователем. При удалении рецепта генерируется предупреждающее сообщение.

### 7. **Управление ингредиентами рецепта**
   - **Добавление ингредиента**: Пользователи могут добавлять ингредиенты в рецепт.
   - **Редактирование ингредиента**: Возможность редактировать уже добавленные ингредиенты.
   - **Удаление ингредиента**: Удаление ингредиентов из рецепта.
   
### 8. **Управление этапами приготовления**
   - **Добавление этапа приготовления**: Пользователи могут добавлять шаги приготовления в рецепт.
   - **Редактирование этапа**: Возможность редактировать существующие этапы приготовления.
   - **Удаление этапа**: Удаление шагов приготовления из рецепта.

### 9. **Мои рецепты**
   - Список рецептов, добавленных текущим пользователем. Возможность просматривать, редактировать и удалять свои рецепты.

### 10. **Ошибки и их обработка**
   - **404 ошибка**: Страница не найдена, с логированием ошибки.
   - **500 ошибка**: Внутренняя ошибка сервера, с подробным сообщением для пользователей.
   - **403 ошибка**: Ошибка доступа, если пользователю запрещен доступ к странице.

---

### Дополнительные особенности:
- **Логирование**: Все действия (создание, редактирование, удаление рецептов и ингредиентов) логируются.
- **Формы**: Для создания и редактирования рецептов, ингредиентов и этапов используются формы с валидацией данных.
- **Пагинация**: Для удобства пользователя данные рецепты разбиваются на страницы.
- **Авторизация**: Все действия, связанные с созданием, редактированием и удалением рецептов, доступны только авторизованным пользователям.

--- 

Таким образом, приложение обеспечивает полный функционал для работы с рецептами, позволяя пользователям удобно добавлять, редактировать и удалять рецепты и их составляющие.

---

# Приложение на [FastAPI для работы с базой данных Django (https://mysiterecipe.ru/api/docs)](https://mysiterecipe.ru/api/docs)

Приложение на FastAPI, которое работает с базой данных, созданной в Django, имеет следующие возможности:

### 1. Подключение к базе данных
Приложение использует SQLAlchemy для подключения к базе данных PostgreSQL, параметры которой считываются из переменных окружения. Подключение к базе данных проверяется на старте приложения с выводом сообщения об успешном подключении или ошибке.

### 2. Модели данных
- **Category**: Модель для категорий рецептов с полями: `id` — уникальный идентификатор категории, `title` — название категории, `slug` — слаг для категории, `description` — описание категории.
- **Recipe**: Модель для рецептов с полями: `id`, `title`, `slug`, `description` — идентификатор, название, слаг и описание рецепта, `cooking_time`, `servings`, `thumbnail`, `status` — время приготовления, количество порций, изображение и статус рецепта, `category_id` — ссылка на категорию рецепта.
- **Ingredient**: Модель для ингредиентов рецепта с полями: `id`, `title`, `amount`, `quantity` — идентификатор, название ингредиента, количество и единица измерения, `recipe_id` — ссылка на рецепт.

### 3. API эндпоинты

- **Получение всех категорий**: возвращает список всех категорий.
- **Получение рецептов по ингредиенту**: возвращает все рецепты, содержащие указанный ингредиент.
- **Получение всех опубликованных рецептов**: возвращает список всех опубликованных рецептов.
- **Получение рецептов по категории**: возвращает все рецепты из указанной категории.
- **Получение рецепта по названию**: возвращает рецепт по частичному совпадению в названии.

### 4. Интерфейс и функциональность
Использование FastAPI позволяет эффективно обрабатывать запросы, обеспечивая асинхронное взаимодействие с базой данных через SQLAlchemy. Приложение возвращает данные в формате JSON, что удобно для взаимодействия с фронтенд-приложениями. Применение зависимостей для подключения к базе данных гарантирует, что каждый запрос будет выполнен в рамках транзакции.

### 5. Ошибки и обработка исключений
Все ошибки (например, не найденные категории или рецепты) обрабатываются с помощью `HTTPException`, возвращая соответствующие статус-коды и сообщения об ошибках.

---

Это приложение на FastAPI позволяет эффективно интегрировать функционал для работы с данными, созданными в Django, и обеспечивать доступ к рецептам, категориям и ингредиентам через API.

---

# Развертывание проекта

Проект состоит из нескольких сервисов, которые включают Django, FastAPI и PostgreSQL, все управляемые через Docker Compose. Также используется Nginx для проксирования запросов.

### Структура проекта

Проект имеет следующую структуру:
- `app_django/` — код приложения Django.
- `app_fastapi/` — код приложения FastAPI.
- `.env` — переменные окружения для разработки.
- `.env.prod` — переменные окружения для продакшн.
- `docker-compose.yaml` — Docker Compose для разработки.
- `docker-compose.prod.yaml` — Docker Compose для продакшн.
- `requirements.txt` — зависимости проекта.
- `nginx/` — конфигурация Nginx и SSL.
- `init-scripts/` — скрипты для начальной настройки базы данных.


### Конфигурация окружения

Перед началом работы, необходимо настроить переменные окружения в файле `.env.prod`, который должен содержать секреты и параметры подключения, такие как секретный ключ, параметры базы данных и настройки почты.

### Развертывание

#### 1. Сборка и запуск контейнеров

Для запуска Docker Compose используйте команду с указанием конфигурации для продакшн окружения. Это автоматически соберёт контейнеры и запустит их в фоновом режиме.

#### 2. Подключение к базе данных

PostgreSQL будет доступен на порту 5432. Убедитесь, что все переменные окружения, включая параметры базы данных, корректно настроены в `.env.prod`.

#### 3. Инициализация базы данных

При первом запуске контейнера с PostgreSQL сервис автоматически выполнит начальную настройку базы данных с помощью скриптов, находящихся в директории `init-scripts`.

#### 4. Настройка Nginx

Nginx будет использовать конфигурацию из папки `nginx`. Важно настроить проксирующие запросы для Django и FastAPI. Также добавьте SSL сертификаты для продакшн версии.

#### 5. Дополнительные настройки

- **Кэширование**: В конфигурации Django укажите параметры для кэширования и логирования.
- **Переменные окружения**: Убедитесь, что все переменные для почты, базы данных и других сервисов корректно указаны в `.env.prod`.

---

