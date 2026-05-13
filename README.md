# UniSearch — Агрегатор университетов

Fullstack приложение для поиска, фильтрации и подбора университетов с AI-советником.

## Стек

| Слой | Технологии |
|------|-----------|
| Frontend | React 18 + Vite + TailwindCSS + React Router |
| Backend | FastAPI + SQLAlchemy + SQLite |
| UI-иконки | Lucide React |
| AI-чат | Встроенный советник (без внешних API) |

## Возможности

- **Список университетов** — карточки с фото, рейтингом, стоимостью и специальностями
- **Фильтры** — по стране, специальности, поиск по названию
- **Пагинация** — постраничная навигация
- **Страница университета** — полная информация, описание, статистика
- **Требования к поступлению** — минимальный GPA, языковые требования, список экзаменов с минимальными баллами
- **AI-чат** — плавающий виджет, понимает запросы на русском и английском, рекомендует университеты по стране / специальности / бюджету
- **15 университетов** в базе: MIT, Stanford, Oxford, Cambridge, ETH Zurich, NUS, Toronto, Peking, Melbourne, TU Munich, Sorbonne, Tokyo, МГУ, ВШЭ, ИТМО

## Запуск

### 1. Backend

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload --port 8000
```

> API: http://localhost:8000  
> Swagger-документация: http://localhost:8000/docs

База данных создаётся и заполняется автоматически при первом запуске.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

> Приложение: http://localhost:5173

## Структура проекта

```
project02/
├── backend/
│   ├── main.py                  # FastAPI app, CORS, lifespan
│   ├── database.py              # SQLAlchemy engine + session
│   ├── models.py                # University, Specialty, AdmissionRequirement, AdmissionExam
│   ├── schemas.py               # Pydantic схемы запросов/ответов
│   ├── crud.py                  # Запросы к БД
│   ├── seed.py                  # Начальные данные (15 университетов + требования)
│   ├── routers/
│   │   ├── universities.py      # GET /api/universities, /countries, /specialties, /{id}
│   │   └── chat.py              # POST /api/chat
│   ├── ai/
│   │   └── advisor.py           # Keyword-based AI советник (ru + en)
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── vite.config.js           # Proxy /api → localhost:8000
    ├── tailwind.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── api/
        │   └── index.js         # Fetch-обёртки для всех эндпоинтов
        ├── components/
        │   ├── Header.jsx
        │   ├── UniversityCard.jsx
        │   ├── FilterBar.jsx
        │   ├── Pagination.jsx
        │   └── ChatWidget.jsx   # Плавающий AI-чат
        └── pages/
            ├── HomePage.jsx     # Список + фильтры + пагинация
            └── UniversityPage.jsx  # Детальная страница + требования к поступлению
```

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/universities` | Список университетов (фильтры: country, specialty, search, page) |
| GET | `/api/universities/{id}` | Полная информация об университете + требования к поступлению |
| GET | `/api/universities/countries` | Список стран |
| GET | `/api/universities/specialties` | Список специальностей |
| POST | `/api/chat` | AI-советник (принимает историю переписки) |
| GET | `/api/health` | Проверка работоспособности |

## База данных

| Таблица | Описание |
|---------|----------|
| `universities` | Основная информация об университете |
| `specialties` | Справочник специальностей |
| `university_specialties` | Связь many-to-many |
| `admission_requirements` | Требования к поступлению (GPA, язык) |
| `admission_exams` | Экзамены с минимальными баллами |
