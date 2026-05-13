# WORKFLOW.md — UniSearch University Aggregator
## Project02 | Zhanna Nurgaliyeva

> **Примечание:** Проект выполнен одним участником, совмещающим роли Frontend Developer, Backend Developer и QA Engineer. Все роли задокументированы отдельно ниже.

> **Замечание:** Выбор технологий frontend-стека (React 18 + Vite + TailwindCSS) был сделан AI-ассистентом (Windsurf / Cascade), а не мной лично. У меня нет опыта работы с этими технологиями. Я формулировала задачи на русском языке, AI генерировал код и архитектуру. Считаю важным указать это явно.

---

## 👥 Команда

| Роль | Участник | Зона ответственности |
|------|----------|---------------------|
| Frontend Developer | Zhanna Nurgaliyeva | UI/UX, компоненты, роутинг, AI-чат виджет |
| Backend Developer | Zhanna Nurgaliyeva | API, БД, AI-слой, MCP, Sub-agent |


---

## 🗂 Структура проекта

```
project02/
├── backend/                    # FastAPI + SQLAlchemy + SQLite
│   ├── ai/
│   │   ├── advisor.py          # Главный AI-модуль
│   │   ├── sub_agent.py        # SubAgent — анализ интентов
│   │   └── mcp_client.py       # MCP Client — внешний контекст
│   ├── mcp/
│   │   └── university_feed.json  # Внешний MCP-источник данных
│   ├── routers/
│   │   ├── universities.py
│   │   └── chat.py
│   ├── models.py / schemas.py / crud.py / seed.py
│   └── main.py
├── frontend/                   # React 18 + Vite + TailwindCSS
│   └── src/
│       ├── pages/
│       │   ├── HomePage.jsx
│       │   └── UniversityPage.jsx
│       ├── components/
│       │   ├── ChatWidget.jsx
│       │   ├── UniversityCard.jsx
│       │   ├── FilterBar.jsx
│       │   └── Pagination.jsx
│       └── api/index.js
├── WORKFLOW.md
├── frontend_ZhannaNurgaliyeva.md
└── backend_ZhannaNurgaliyeva.md
```

---

## ⚙️ Backend Developer — Workflow

### Стек
- **FastAPI** — REST API framework
- **SQLAlchemy ORM** — работа с БД
- **SQLite** — база данных (`universities.db`)
- **Pydantic v2** — валидация данных
- **SubAgent** — анализ пользовательских намерений
- **MCPClient** — внешний источник контекста

---

### Шаг 1 — Проектирование схемы БД (через AI-промпт)

**Промпт:**
```
Создай SQLAlchemy модели для агрегатора университетов.
Нужны таблицы: University, Specialty (many-to-many),
AdmissionRequirement, AdmissionExam.
```

**Результат — схема БД:**

```
universities  ──< university_specialties >── specialties
     │
     └──< admission_requirements
               │
               └──< admission_exams
```

| Таблица | Поля |
|---------|------|
| `universities` | id, name, country, city, ranking, tuition_min/max, students_count, image_url, website, founded_year |
| `specialties` | id, name (unique) |
| `university_specialties` | university_id FK, specialty_id FK |
| `admission_requirements` | id, university_id FK (unique), description, min_gpa, language_requirement |
| `admission_exams` | id, requirement_id FK, exam_name, min_score, max_score, notes |

**Файлы:** `models.py`, `schemas.py`

---

### Шаг 2 — API эндпоинты (через AI-промпт)

**Промпт:**
```
Создай FastAPI роутеры для:
- GET /api/universities (с фильтрами: country, specialty, search, page)
- GET /api/universities/{id} (с admission requirements)
- GET /api/universities/countries
- GET /api/universities/specialties
- POST /api/chat
```

**Реализованные эндпоинты:**

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/universities` | Список + пагинация + фильтры |
| GET | `/api/universities/{id}` | Детали + требования к поступлению |
| GET | `/api/universities/countries` | Справочник стран |
| GET | `/api/universities/specialties` | Справочник специальностей |
| POST | `/api/chat` | AI-советник |
| GET | `/api/health` | Healthcheck |

**Файлы:** `routers/universities.py`, `routers/chat.py`, `crud.py`

---

### Шаг 3 — Seed данных (через AI-промпт)

**Промпт:**
```
Заполни БД 15 реальными университетами мирового уровня.
Для каждого добавь: требования к поступлению, минимальные баллы,
список экзаменов (SAT, IELTS, TOEFL, ЕГЭ и т.д.).
```

**Результат:** 15 университетов × 56 экзаменов  
**Страны:** USA, UK, Germany, France, Japan, China, Russia, Canada, Australia, Singapore, Switzerland

**Файл:** `seed.py`

---

### Шаг 4 — MCP интеграция (через AI-промпт)

**Промпт:**
```
Реализуй MCP слой, который предоставляет данные университетов
из внешнего источника (JSON), не из SQL.
Добавь backend sub-agent для анализа пользовательского запроса
(intent, country, budget, major).
```

**Архитектура MCP + Sub-agent:**

```
POST /api/chat
       │
       ▼
  advisor.py
       ├─► SubAgent.analyze(messages)     — ai/sub_agent.py
       │       └─ Intent { intent, countries, specialties, budget, confidence }
       │
       ├─► crud.get_universities_by_filters()   — SQL запрос
       │
       └─► MCPClient.get_context(intent)   — ai/mcp_client.py
               └─ читает mcp/university_feed.json
                  → дедлайны, стипендии, % зачисления
```

**SubAgent — IntentAnalyzerAgent:**
- Анализирует **всю историю** диалога (накопительный контекст)
- Возвращает `Intent(intent, countries, specialties, budget, confidence)`
- Поддерживает русский + английский язык
- Классифицирует: `find_university` | `greeting` | `clarify` | `more_info`

**MCPClient — внешний источник:**
- Читает `mcp/university_feed.json` (15 записей)
- Фильтрует по `Intent.countries` и `Intent.specialties`
- Добавляет блок `📋 Из внешнего источника (MCP-feed)` в ответ чата
- **Не зависит от SQL** — отдельный слой данных

**Файлы:** `ai/sub_agent.py`, `ai/mcp_client.py`, `mcp/university_feed.json`

---

## 🎨 Frontend Developer — Workflow

### Стек
- **React 18** — UI framework
- **Vite** — сборщик
- **TailwindCSS** — дизайн-система
- **React Router v6** — роутинг
- **Lucide React** — иконки

---

### Шаг 1 — Компоненты (через AI-промпт)

**Промпт:**
```
Создай красивый UI для агрегатора университетов.
React 18 + Vite + TailwindCSS.
Нужны: список карточек, фильтры, пагинация,
детальная страница, AI-чат виджет.
```

**Реализованные компоненты:**

| Компонент | Описание |
|-----------|----------|
| `Header.jsx` | Навигация с логотипом |
| `UniversityCard.jsx` | Карточка с фото, рейтингом, стоимостью, специальностями |
| `FilterBar.jsx` | Поиск + фильтры по стране и специальности + сброс |
| `Pagination.jsx` | Постраничная навигация с ellipsis |
| `ChatWidget.jsx` | Плавающий AI-чат с подсказками и typing-индикатором |

**Запрещённые подходы (не использованы):**
- ❌ Чистый HTML + CSS без дизайн-системы
- ❌ Примитивный UI (кнопка + текст)
- ❌ Inline стили
- ❌ Отдельные CSS файлы вместо Tailwind

---

### Шаг 2 — Страницы (через AI-промпт)

**Промпт:**
```
Создай HomePage с фильтрацией, пагинацией и карточками.
Создай UniversityPage с полной информацией об университете
и секцией требований к поступлению (GPA, языковые тесты, экзамены с баллами).
```

**Страницы:**

| Путь | Компонент | Функциональность |
|------|-----------|-----------------|
| `/` | `HomePage` | Сетка карточек, фильтры, поиск, пагинация, loading/error state |
| `/university/:id` | `UniversityPage` | Фото-шапка, статистика, описание, `AdmissionSection`, специальности, ссылка на сайт |

**AdmissionSection** (добавлена после расширения):
- Карточка минимального GPA (янтарный цвет)
- Карточка языковых требований (синий цвет)
- Таблица экзаменов с минимальными/максимальными баллами и примечаниями

---

### Шаг 3 — API интеграция

**Файл:** `src/api/index.js`

```js
// Все запросы через Vite proxy → localhost:8000
api.getUniversities(params)   // GET /api/universities
api.getUniversity(id)         // GET /api/universities/:id
api.getCountries()            // GET /api/universities/countries
api.getSpecialties()          // GET /api/universities/specialties
api.chat(messages)            // POST /api/chat
```

Proxy настроен в `vite.config.js` — Frontend никогда не хардкодит `localhost:8000`.

---

## 🧪 QA & Workflow Master

### Проверки API

```bash
# Список университетов
GET http://localhost:8000/api/universities

# Детали с admission (проверка MCP + sub-agent)
GET http://localhost:8000/api/universities/1

# Проверка чата с SubAgent + MCP
POST http://localhost:8000/api/chat
Body: {"messages": [{"role": "user", "content": "Computer Science in Germany"}]}
Ожидается: unis > 0, "MCP" in message == True

# Swagger UI
GET http://localhost:8000/docs
```

### Проверка БД после seed

```bash
py -c "
from database import SessionLocal; import models
db = SessionLocal()
print('unis:', db.query(models.University).count())          # 15
print('admissions:', db.query(models.AdmissionRequirement).count())  # 15
print('exams:', db.query(models.AdmissionExam).count())      # 56
db.close()
"
```

### Доказательства использования AI

| Что сгенерировано AI | Файл |
|----------------------|------|
| SQLAlchemy модели (5 таблиц) | `models.py` |
| Pydantic v2 схемы | `schemas.py` |
| CRUD функции с фильтрами | `crud.py` |
| FastAPI роутеры | `routers/` |
| Seed данных (15 университетов + 56 экзаменов) | `seed.py` |
| Sub-agent с Intent dataclass | `ai/sub_agent.py` |
| MCP Client + JSON feed | `ai/mcp_client.py`, `mcp/university_feed.json` |
| React компоненты (5 шт.) | `frontend/src/components/` |
| Страницы с адаптивным UI | `frontend/src/pages/` |
| Документация (3 .md файла) | `WORKFLOW.md`, `frontend_ZhannaNurgaliyeva.md`, `backend_ZhannaNurgaliyeva.md` |

---

## 🚀 Запуск проекта

### Backend
```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload --port 8000
# БД создаётся и заполняется автоматически
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Открыть http://localhost:5173
```

### Проверка
- Сайт: http://localhost:5173
- API: http://localhost:8000
- Документация API: http://localhost:8000/docs

---

## 📌 Итог

| Метрика | Значение |
|---------|----------|
| Университетов в БД | 15 |
| Стран | 11 |
| Специальностей | 12 |
| Экзаменов (admission) | 56 |
| API эндпоинтов | 6 |
| React компонентов | 7 |
| MCP источников | 1 (university_feed.json) |
| Sub-agent'ов | 1 (IntentAnalyzerAgent) |
| AI-сгенерированных файлов | 16+ |
