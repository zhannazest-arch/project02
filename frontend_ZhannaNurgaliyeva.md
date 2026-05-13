# Role

**Frontend Agent — UniSearch University Aggregator**

Отвечает за весь пользовательский интерфейс приложения: отображение университетов,
фильтрацию, пагинацию, детальные страницы и AI-чат виджет.
Стек: React 18 + Vite + TailwindCSS + React Router v6.

---

# System Rules

## Роль AI

- Строить и поддерживать React-компоненты в рамках существующей архитектуры проекта
- Взаимодействовать с Backend исключительно через слой `src/api/index.js`
- Отображать данные университетов, фильтры, требования к поступлению и ответы AI-советника
- Обеспечивать отзывчивый (responsive) UI без нарушения текущей дизайн-системы (Tailwind + Inter)

## Ограничения

- Не обращаться напрямую к базе данных (SQLite) — только через REST API (`/api/*`)
- Не хранить бизнес-логику в компонентах — вся логика запросов в `src/api/index.js`
- Не использовать глобальный state-менеджер (Redux, Zustand и т.д.) — только `useState` / `useEffect`
- Не подключать сторонние UI-библиотеки без явного согласования (shadcn, MUI и т.д.)
- Версии зависимостей фиксированы в `package.json` — не обновлять без причины

## Чего делать нельзя

- Нельзя делать прямые fetch-запросы к `http://localhost:8000` внутри компонентов — только через `api.*`
- Нельзя рендерить чувствительные данные (токены, ключи) на клиенте
- Нельзя изменять `vite.config.js` proxy без синхронизации с Backend
- Нельзя удалять или переименовывать существующие роуты (`/`, `/university/:id`) без обновления `App.jsx`
- Нельзя изменять структуру пропсов компонентов без обновления всех мест использования

## Формат ответов

- Компоненты — функциональные, именованные (`export default function ComponentName`)
- Стили — исключительно через Tailwind CSS utility-классы, без inline-стилей
- Иконки — только из `lucide-react`
- Импорты — в порядке: React → Router → Lucide → внутренние (`../api`, `../components`)
- Нет `console.log` в продакшн-коде
- Каждый новый компонент — отдельный файл в `src/components/` или `src/pages/`

---

# MCP & Tools

## Какие MCP подключены

| MCP | Источник | Назначение |
|-----|----------|-----------|
| **University Feed MCP** | `backend/mcp/university_feed.json` | Обогащение ответов AI-чата данными из внешнего источника: дедлайны, % зачисления, стипендии |

> Frontend не обращается к MCP напрямую. MCP-данные приходят уже встроенными
> в поле `message` ответа `POST /api/chat` — в виде форматированного текстового блока
> с маркером `📋 Из внешнего источника (MCP-feed)`.

## Какие tools может вызывать AI

| Tool / API метод | Эндпоинт | Описание |
|-----------------|----------|----------|
| `api.getUniversities(params)` | `GET /api/universities` | Список университетов с фильтрами (country, specialty, search, page) |
| `api.getUniversity(id)` | `GET /api/universities/:id` | Полная карточка университета + требования к поступлению |
| `api.getCountries()` | `GET /api/universities/countries` | Список стран для фильтра |
| `api.getSpecialties()` | `GET /api/universities/specialties` | Список специальностей для фильтра |
| `api.chat(messages)` | `POST /api/chat` | Отправка истории диалога AI-советнику |

---

# Subagents (если есть)

## ChatWidget → Backend SubAgent

**Назначение:**
`ChatWidget.jsx` не содержит собственной логики подбора университетов.
Вместо этого он передаёт полную историю сообщений на бэкенд (`POST /api/chat`),
где работает `SubAgent` (`backend/ai/sub_agent.py`).

**Когда вызывается:**
- При каждой отправке сообщения пользователем в чат-виджете
- При первом открытии виджета (автоматически отправляется приветствие `"Привет!"`)
- При клике на подсказку-кнопку (`"Computer Science в США"`, `"Медицина в Европе"` и др.)

**Что возвращает SubAgent фронтенду:**

```json
{
  "message": "string (markdown-текст с результатами + MCP-блок)",
  "universities": [ UniversityListItem ] | null
}
```

`ChatWidget` рендерит `message` как текст с поддержкой `**bold**`,
а `universities` — как мини-карточки `UniMiniCard` со ссылкой на `/university/:id`.

---

# Output Contracts

## API Response — `/api/universities` (список)

```json
{
  "items": [
    {
      "id": 1,
      "name": "string",
      "country": "string",
      "city": "string",
      "ranking": 1,
      "image_url": "string | null",
      "tuition_min": 55000,
      "tuition_max": 60000,
      "students_count": 11574,
      "specialties": [{ "id": 1, "name": "string" }]
    }
  ],
  "total": 15,
  "page": 1,
  "pages": 2
}
```

## API Response — `/api/universities/:id` (детальная страница)

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

## API Request — `POST /api/chat`

```json
{
  "messages": [
    { "role": "user",      "content": "string" },
    { "role": "assistant", "content": "string" }
  ]
}
```

## JSX — структура компонентов

```
src/
├── App.jsx                   — Router + Header + ChatWidget
├── pages/
│   ├── HomePage.jsx          — фильтры, сетка карточек, пагинация
│   └── UniversityPage.jsx    — детальная страница + AdmissionSection
├── components/
│   ├── Header.jsx
│   ├── UniversityCard.jsx    — props: { university: UniversityListItem }
│   ├── FilterBar.jsx         — props: { search, country, specialty, ... }
│   ├── Pagination.jsx        — props: { page, pages, onChange }
│   └── ChatWidget.jsx        — props: none (самодостаточный)
└── api/
    └── index.js              — все fetch-обёртки
```

## Роутинг

| Путь | Компонент | Описание |
|------|-----------|----------|
| `/` | `HomePage` | Главная — список + фильтры |
| `/university/:id` | `UniversityPage` | Детальная страница университета |
