# Role

**Backend Agent — UniSearch University Aggregator**

Отвечает за REST API, бизнес-логику, базу данных и AI-слой приложения.
Стек: FastAPI + SQLAlchemy + SQLite + Pydantic v2.
Запускается на `http://localhost:8000`. Swagger UI: `http://localhost:8000/docs`.

---

# System Rules

## Роль AI

- Обрабатывать HTTP-запросы от Frontend через REST API (`/api/*`)
- Хранить и предоставлять данные университетов, специальностей, требований к поступлению
- Анализировать пользовательские запросы через SubAgent и возвращать рекомендации
- Обогащать ответы данными из внешнего MCP-источника (JSON feed)
- Автоматически создавать и заполнять БД при первом запуске (seed)

## Ограничения

- Все модели данных строго типизированы через Pydantic v2 (`model_config = {"from_attributes": True}`)
- Каждый роутер изолирован в `routers/` — не дублировать логику между роутерами
- Вся работа с БД — только через функции в `crud.py`, не напрямую из роутеров
- CORS разрешён только для `localhost:5173` и `localhost:3000`
- Конфигурация БД — только через `database.py`, путь `sqlite:///./universities.db`
- Seed выполняется идемпотентно: два отдельных блока — университеты и admission (проверка `count() == 0`)

## Чего делать нельзя

- Нельзя делать синхронные блокирующие I/O-операции внутри async-эндпоинтов без `run_in_executor`
- Нельзя хранить состояние запроса в глобальных переменных роутеров
- Нельзя возвращать модели SQLAlchemy напрямую — только через Pydantic-схемы
- Нельзя изменять схему БД без удаления `universities.db` и пересева (нет миграций Alembic)
- Нельзя добавлять новые эндпоинты вне `routers/` — только через `app.include_router()`
- Нельзя изменять `ADMISSIONS` dict в `seed.py` во время выполнения — он мутируется при `pop()`, использовать `.get()` вместо `.pop()`

## Формат ответов

- Все эндпоинты возвращают JSON, задекларированный через `response_model=`
- HTTP 404 — через `HTTPException(status_code=404, detail="...")`
- Пагинация — через `UniversitiesResponse` (items, total, page, pages)
- Поля `Optional` — явно указаны в схемах, дефолт `None`
- Логи запуска — через `print()` в `seed.py` и `mcp_client.py`

---

# MCP & Tools

## Какие MCP подключены

| MCP | Файл | Источник данных | Назначение |
|-----|------|----------------|-----------|
| **University Feed MCP** | `ai/mcp_client.py` | `mcp/university_feed.json` | Обогащение ответов AI-чата внешними данными: % зачисления, дедлайны подачи, стипендии — независимо от SQL |

**Принцип работы MCP:**
- `MCPClient` загружает `mcp/university_feed.json` один раз при импорте модуля
- Метод `get_context(intent, limit)` фильтрует записи по странам и специальностям из `Intent`
- Метод `format_context(context)` форматирует результат в markdown-блок
- MCP-блок добавляется **после** SQL-результатов в ответе `POST /api/chat`
- Данные MCP **не пересекаются** с данными SQL — это дополнительный слой контекста

## Какие tools может вызывать Backend

| Tool | Модуль | Описание |
|------|--------|----------|
| `crud.get_universities()` | `crud.py` | Список университетов с фильтрами + пагинация |
| `crud.get_university()` | `crud.py` | Единичная запись по ID со всеми связями |
| `crud.get_countries()` | `crud.py` | Distinct список стран |
| `crud.get_specialties()` | `crud.py` | Все специальности из справочника |
| `crud.get_universities_by_filters()` | `crud.py` | Фильтрация для AI-советника (страны, специальности, бюджет) |
| `SubAgent.analyze(messages)` | `ai/sub_agent.py` | Разбор истории чата → структурированный `Intent` |
| `MCPClient.get_context(intent)` | `ai/mcp_client.py` | Получение внешнего контекста по Intent |
| `MCPClient.format_context(context)` | `ai/mcp_client.py` | Форматирование MCP-данных в markdown |
| `seed()` | `seed.py` | Первичное заполнение БД (вызывается в lifespan) |

---

# Subagents

## SubAgent — IntentAnalyzerAgent

**Файл:** `ai/sub_agent.py`

**Назначение:**
Единственная ответственность — разбор пользовательских сообщений и извлечение
структурированного намерения (`Intent`). Не знает о БД, не делает запросов.

**Возвращает:**
```python
@dataclass
class Intent:
    intent: str        # "find_university" | "greeting" | "clarify" | "more_info" | "unknown"
    countries: list[str]
    specialties: list[str]
    budget: Optional[int]
    confidence: float  # 0.0 – 1.0
```

**Когда вызывается:**
- При каждом `POST /api/chat` — до обращения к БД и MCP
- Анализирует **всю историю** диалога (все user-сообщения), не только последнее
- Накапливает контекст: если в первом сообщении "германия", а во втором "IT" — Intent содержит оба

**Алгоритм:**
1. Проходит по всем `msg.role == "user"` сообщениям
2. Для каждого вызывает `_extract(text)` → (countries, specialties, budget)
3. Классифицирует намерение через `_classify()` по последнему сообщению
4. Считает `confidence` (0.5 за specialty + 0.35 за country + 0.15 за budget)
5. Возвращает merged `Intent`

**Поддерживаемые языки:** русский + английский (словари `_COUNTRY_MAP`, `_SPECIALTY_MAP`)

---

# Output Contracts

## Эндпоинты API

### `GET /api/universities`

**Query params:** `country`, `specialty`, `search`, `page` (def. 1), `limit` (def. 12)

```json
{
  "items": [
    {
      "id": 1,
      "name": "Massachusetts Institute of Technology",
      "country": "USA",
      "city": "Cambridge, MA",
      "ranking": 1,
      "image_url": "string | null",
      "logo_url": "string | null",
      "tuition_min": 55000,
      "tuition_max": 60000,
      "students_count": 11574,
      "specialties": [{ "id": 1, "name": "Computer Science" }]
    }
  ],
  "total": 15,
  "page": 1,
  "pages": 2
}
```

### `GET /api/universities/{id}`

```json
{
  "id": 1,
  "name": "string",
  "country": "string",
  "city": "string",
  "description": "string | null",
  "website": "string | null",
  "ranking": 1,
  "founded_year": 1861,
  "tuition_min": 55000,
  "tuition_max": 60000,
  "students_count": 11574,
  "specialties": [{ "id": 1, "name": "string" }],
  "admission": {
    "id": 1,
    "description": "string | null",
    "min_gpa": 3.9,
    "language_requirement": "string | null",
    "exams": [
      {
        "id": 1,
        "exam_name": "SAT",
        "min_score": "1500",
        "max_score": "1600",
        "notes": "string | null"
      }
    ]
  }
}
```

### `GET /api/universities/countries`

```json
["Australia", "Canada", "China", "France", "Germany", "Japan",
 "Russia", "Singapore", "Switzerland", "UK", "USA"]
```

### `GET /api/universities/specialties`

```json
[
  { "id": 1, "name": "Architecture" },
  { "id": 2, "name": "Arts" }
]
```

### `POST /api/chat`

**Request:**
```json
{
  "messages": [
    { "role": "user",      "content": "Computer Science в Германии" },
    { "role": "assistant", "content": "..." }
  ]
}
```

**Response:**
```json
{
  "message": "markdown-текст с результатами + MCP-блок (если есть)",
  "universities": [
    {
      "id": 10,
      "name": "Technical University of Munich",
      "country": "Germany",
      "city": "Munich",
      "ranking": 37,
      "tuition_min": 0,
      "tuition_max": 2000,
      "specialties": [{ "id": 3, "name": "Computer Science" }]
    }
  ]
}
```

## Схема БД

| Таблица | Ключевые поля |
|---------|--------------|
| `universities` | id, name, country, city, ranking, tuition_min, tuition_max, students_count, image_url, website, founded_year |
| `specialties` | id, name (unique) |
| `university_specialties` | university_id FK, specialty_id FK (many-to-many) |
| `admission_requirements` | id, university_id FK (unique), description, min_gpa, language_requirement |
| `admission_exams` | id, requirement_id FK, exam_name, min_score, max_score, notes |

## MCP Feed Contract

**Файл:** `mcp/university_feed.json`

```json
[
  {
    "university": "string",
    "country": "string",
    "specialties": ["string"],
    "acceptance_rate": "string",
    "application_deadline": "string",
    "scholarships": ["string"],
    "tags": ["string"]
  }
]
```

## Структура модулей

```
backend/
├── main.py             — FastAPI app, lifespan (create_all + seed), CORS, include_router
├── database.py         — engine, SessionLocal, Base, get_db()
├── models.py           — University, Specialty, AdmissionRequirement, AdmissionExam
├── schemas.py          — Pydantic v2 схемы (UniversityOut, AdmissionRequirementOut, ChatResponse...)
├── crud.py             — все DB-запросы (get_universities, get_university, get_countries...)
├── seed.py             — UNIVERSITIES[], ADMISSIONS{}, seed() с двумя идемпотентными блоками
├── routers/
│   ├── universities.py — GET /api/universities, /countries, /specialties, /{id}
│   └── chat.py         — POST /api/chat → advisor.generate_response()
├── ai/
│   ├── advisor.py      — generate_response(): SubAgent → SQL → MCP → строит ответ
│   ├── sub_agent.py    — SubAgent, Intent dataclass, keyword extraction + classification
│   └── mcp_client.py  — MCPClient, загрузка feed, get_context(), format_context()
└── mcp/
    └── university_feed.json — 15 записей: acceptance_rate, deadlines, scholarships, tags
```
