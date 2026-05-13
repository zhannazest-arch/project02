import re
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
import crud
import models
from ai.sub_agent import SubAgent
from ai.mcp_client import MCPClient

# Module-level singletons — instantiated once at import time
_sub_agent = SubAgent()
_mcp_client = MCPClient()

COUNTRY_KEYWORDS: dict[str, str] = {
    "usa": "USA",
    "united states": "USA",
    "america": "USA",
    "american": "USA",
    "uk": "UK",
    "britain": "UK",
    "england": "UK",
    "british": "UK",
    "germany": "Germany",
    "german": "Germany",
    "france": "France",
    "french": "France",
    "japan": "Japan",
    "japanese": "Japan",
    "china": "China",
    "chinese": "China",
    "russia": "Russia",
    "russian": "Russia",
    "canada": "Canada",
    "canadian": "Canada",
    "australia": "Australia",
    "australian": "Australia",
    "singapore": "Singapore",
    "switzerland": "Switzerland",
    "swiss": "Switzerland",
    "сша": "USA",
    "америка": "USA",
    "германия": "Germany",
    "франция": "France",
    "япония": "Japan",
    "китай": "China",
    "россия": "Russia",
    "канада": "Canada",
    "австралия": "Australia",
    "сингапур": "Singapore",
    "швейцария": "Switzerland",
    "великобритания": "UK",
    "англия": "UK",
}

SPECIALTY_KEYWORDS: dict[str, str] = {
    "computer science": "Computer Science",
    "cs": "Computer Science",
    "software": "Computer Science",
    "programming": "Computer Science",
    "программирование": "Computer Science",
    "информатика": "Computer Science",
    "it": "Computer Science",
    "ит": "Computer Science",
    "ai": "Artificial Intelligence",
    "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Artificial Intelligence",
    "ml": "Artificial Intelligence",
    "искусственный интеллект": "Artificial Intelligence",
    "ии": "Artificial Intelligence",
    "engineering": "Engineering",
    "инженерия": "Engineering",
    "инженер": "Engineering",
    "medicine": "Medicine",
    "medical": "Medicine",
    "медицина": "Medicine",
    "врач": "Medicine",
    "business": "Business",
    "mba": "Business",
    "бизнес": "Business",
    "менеджмент": "Business",
    "economics": "Economics",
    "economic": "Economics",
    "экономика": "Economics",
    "экономист": "Economics",
    "law": "Law",
    "legal": "Law",
    "право": "Law",
    "юрист": "Law",
    "юриспруденция": "Law",
    "mathematics": "Mathematics",
    "math": "Mathematics",
    "математика": "Mathematics",
    "математик": "Mathematics",
    "physics": "Physics",
    "физика": "Physics",
    "физик": "Physics",
    "humanities": "Humanities",
    "гуманитарные": "Humanities",
    "arts": "Arts",
    "art": "Arts",
    "искусство": "Arts",
    "architecture": "Architecture",
    "архитектура": "Architecture",
}

GREETINGS = [
    "hello", "hi", "hey", "привет", "здравствуй", "здравствуйте",
    "добрый день", "добрый вечер", "доброе утро", "хай",
]

WELCOME_MESSAGE = (
    "Привет! 👋 Я помогу подобрать университет.\n\n"
    "Расскажите немного о себе:\n"
    "- **Какую специальность** хотите изучать?\n"
    "- **В какой стране** хотели бы учиться?\n"
    "- Есть предпочтения по **стоимости обучения**?\n\n"
    "Например: *«Хочу изучать Computer Science в Германии»*"
)


def _extract_entities(
    text: str,
) -> Tuple[List[str], List[str], Optional[int]]:
    t = text.lower()

    countries: List[str] = []
    for kw, country in COUNTRY_KEYWORDS.items():
        if kw in t and country not in countries:
            countries.append(country)

    specialties: List[str] = []
    for kw, spec in SPECIALTY_KEYWORDS.items():
        if kw in t and spec not in specialties:
            specialties.append(spec)

    budget: Optional[int] = None
    patterns = [
        r"(\d+)\s*k\b",
        r"\$\s*(\d+)",
        r"(\d+)\s*тысяч",
        r"(\d+)\s*000\b",
        r"бюджет[^\d]*(\d+)",
        r"budget[^\d]*(\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, t)
        if m:
            val = int(m.group(1))
            budget = val * 1000 if val < 500 else val
            break

    return countries, specialties, budget


def generate_response(
    messages: list, db: Session
) -> Tuple[str, List[models.University]]:
    if not messages:
        return WELCOME_MESSAGE, []

    last = messages[-1].content

    # --- Greeting shortcut (before sub-agent call) ---
    if len(messages) == 1 and any(g in last.lower() for g in GREETINGS):
        return WELCOME_MESSAGE, []

    # ----------------------------------------------------------------
    # Sub-agent: structured intent analysis
    # Replaces the manual per-message loop over _extract_entities()
    # ----------------------------------------------------------------
    intent = _sub_agent.analyze(messages)

    countries = intent.countries
    specialties = intent.specialties
    budget = intent.budget

    if intent.intent == "greeting":
        return WELCOME_MESSAGE, []

    if intent.has_context():
        # --- SQL: primary university results ---
        unis = crud.get_universities_by_filters(
            db,
            countries=countries or None,
            specialties=specialties or None,
            max_tuition=budget,
            limit=5,
        )

        if not unis:
            return (
                "По вашим критериям ничего не нашлось. 😕\n\n"
                "Попробуйте расширить поиск — например, другую страну или специальность.",
                [],
            )

        parts = []
        if specialties:
            parts.append(f"**{', '.join(specialties)}**")
        if countries:
            parts.append(f"в **{', '.join(countries)}**")
        if budget:
            parts.append(f"до **${budget:,}/год**")

        header = "По вашим критериям"
        if parts:
            header += " (" + ", ".join(parts) + ")"

        lines = [f"нашёл **{len(unis)}** подходящих университетов:\n"]
        for i, u in enumerate(unis, 1):
            tuition = (
                f"${u.tuition_min:,}–${u.tuition_max:,}/год"
                if u.tuition_min
                else "уточнить"
            )
            rank_str = f" · #{u.ranking}" if u.ranking else ""
            lines.append(f"{i}. **{u.name}** ({u.city}){rank_str} — {tuition}")

        lines.append("\n💡 Нажмите на карточку университета для подробностей.")
        response = f"{header}: {chr(10).join(lines)}"

        # ----------------------------------------------------------------
        # MCP layer: append external enrichment (deadlines, scholarships)
        # Data comes from JSON feed — NOT from the SQL database
        # ----------------------------------------------------------------
        mcp_context = _mcp_client.get_context(intent, limit=2)
        mcp_snippet = _mcp_client.format_context(mcp_context)
        if mcp_snippet:
            response += mcp_snippet

        return response, unis

    # Guide user toward giving more info
    if not specialties and not countries:
        return (
            "Расскажите, что вас интересует!\n\n"
            "Например: *«Computer Science в США»* или *«медицина в Европе»*",
            [],
        )
    if not specialties:
        return (
            "Отлично! Какую **специальность** хотите изучать?\n"
            "Например: Computer Science, Engineering, Medicine, Business...",
            [],
        )
    return (
        f"Понял, интересует **{', '.join(specialties)}**.\n"
        "В какой **стране** хотели бы учиться?",
        [],
    )
