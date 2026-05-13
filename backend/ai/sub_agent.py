"""
SubAgent — Intent Analyzer Agent

Responsible for parsing conversational messages and returning a structured
Intent object: intent type, countries, specialties, budget, confidence.

This is a focused single-purpose sub-agent that decouples entity extraction
from the main advisor logic.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Intent dataclass — structured output of the sub-agent
# ---------------------------------------------------------------------------

@dataclass
class Intent:
    intent: str                          # "find_university" | "greeting" | "clarify" | "unknown"
    countries: list[str] = field(default_factory=list)
    specialties: list[str] = field(default_factory=list)
    budget: Optional[int] = None
    confidence: float = 0.0              # 0.0 – 1.0

    def has_context(self) -> bool:
        return bool(self.countries or self.specialties)

    def summary(self) -> str:
        parts = []
        if self.specialties:
            parts.append(f"specialties={self.specialties}")
        if self.countries:
            parts.append(f"countries={self.countries}")
        if self.budget:
            parts.append(f"budget=${self.budget:,}")
        return f"Intent({self.intent}, {', '.join(parts)}, confidence={self.confidence:.2f})"


# ---------------------------------------------------------------------------
# Keyword maps
# ---------------------------------------------------------------------------

_COUNTRY_MAP: dict[str, str] = {
    "usa": "USA", "united states": "USA", "america": "USA", "american": "USA",
    "uk": "UK", "britain": "UK", "england": "UK", "british": "UK",
    "germany": "Germany", "german": "Germany",
    "france": "France", "french": "France",
    "japan": "Japan", "japanese": "Japan",
    "china": "China", "chinese": "China",
    "russia": "Russia", "russian": "Russia",
    "canada": "Canada", "canadian": "Canada",
    "australia": "Australia", "australian": "Australia",
    "singapore": "Singapore",
    "switzerland": "Switzerland", "swiss": "Switzerland",
    # Russian
    "сша": "USA", "америка": "USA",
    "германия": "Germany",
    "франция": "France",
    "япония": "Japan",
    "китай": "China",
    "россия": "Russia",
    "канада": "Canada",
    "австралия": "Australia",
    "сингапур": "Singapore",
    "швейцария": "Switzerland",
    "великобритания": "UK", "англия": "UK",
}

_SPECIALTY_MAP: dict[str, str] = {
    "computer science": "Computer Science", "cs": "Computer Science",
    "software": "Computer Science", "programming": "Computer Science",
    "программирование": "Computer Science", "информатика": "Computer Science",
    "it": "Computer Science", "ит": "Computer Science",
    "ai": "Artificial Intelligence", "artificial intelligence": "Artificial Intelligence",
    "machine learning": "Artificial Intelligence", "ml": "Artificial Intelligence",
    "искусственный интеллект": "Artificial Intelligence", "ии": "Artificial Intelligence",
    "engineering": "Engineering", "инженерия": "Engineering", "инженер": "Engineering",
    "medicine": "Medicine", "medical": "Medicine",
    "медицина": "Medicine", "врач": "Medicine",
    "business": "Business", "mba": "Business",
    "бизнес": "Business", "менеджмент": "Business",
    "economics": "Economics", "economic": "Economics",
    "экономика": "Economics", "экономист": "Economics",
    "law": "Law", "legal": "Law",
    "право": "Law", "юрист": "Law", "юриспруденция": "Law",
    "mathematics": "Mathematics", "math": "Mathematics",
    "математика": "Mathematics", "математик": "Mathematics",
    "physics": "Physics", "физика": "Physics",
    "humanities": "Humanities", "гуманитарные": "Humanities",
    "arts": "Arts", "искусство": "Arts",
    "architecture": "Architecture", "архитектура": "Architecture",
}

_GREETING_TOKENS = {
    "hello", "hi", "hey", "привет", "здравствуй", "здравствуйте",
    "добрый", "хай", "sup",
}

_BUDGET_PATTERNS = [
    r"(\d+)\s*k\b",
    r"\$\s*(\d+)",
    r"(\d+)\s*тысяч",
    r"(\d+)\s*000\b",
    r"бюджет[^\d]*(\d+)",
    r"budget[^\d]*(\d+)",
]


# ---------------------------------------------------------------------------
# SubAgent
# ---------------------------------------------------------------------------

class SubAgent:
    """
    Single-responsibility sub-agent: converts raw message history into a
    structured Intent. Does NOT query any database or external service.
    """

    NAME = "IntentAnalyzerAgent"
    VERSION = "1.0"

    def analyze(self, messages: list) -> Intent:
        """
        Analyze the full conversation history and return a merged Intent.
        Accumulates entities across all user turns for context continuity.
        """
        all_countries: list[str] = []
        all_specialties: list[str] = []
        all_budgets: list[int] = []
        last_user_text = ""

        for msg in messages:
            if msg.role != "user":
                continue
            last_user_text = msg.content
            c, s, b = self._extract(msg.content)
            all_countries.extend(c)
            all_specialties.extend(s)
            if b:
                all_budgets.append(b)

        countries = list(dict.fromkeys(all_countries))
        specialties = list(dict.fromkeys(all_specialties))
        budget = min(all_budgets) if all_budgets else None

        intent_type = self._classify(last_user_text, countries, specialties, messages)
        confidence = self._score(countries, specialties, budget)

        return Intent(
            intent=intent_type,
            countries=countries,
            specialties=specialties,
            budget=budget,
            confidence=confidence,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _extract(self, text: str) -> tuple[list[str], list[str], Optional[int]]:
        t = text.lower()

        countries: list[str] = []
        for kw, val in _COUNTRY_MAP.items():
            if kw in t and val not in countries:
                countries.append(val)

        specialties: list[str] = []
        for kw, val in _SPECIALTY_MAP.items():
            if kw in t and val not in specialties:
                specialties.append(val)

        budget: Optional[int] = None
        for pat in _BUDGET_PATTERNS:
            m = re.search(pat, t)
            if m:
                val = int(m.group(1))
                budget = val * 1000 if val < 500 else val
                break

        return countries, specialties, budget

    def _classify(
        self,
        text: str,
        countries: list[str],
        specialties: list[str],
        messages: list,
    ) -> str:
        t = text.lower()
        tokens = set(t.split())

        if len(messages) == 1 and tokens & _GREETING_TOKENS:
            return "greeting"
        if countries or specialties:
            return "find_university"
        if any(w in t for w in ["подробн", "расскаж", "больше", "detail", "more", "tell me"]):
            return "more_info"
        if tokens & _GREETING_TOKENS:
            return "greeting"
        return "clarify"

    def _score(
        self,
        countries: list[str],
        specialties: list[str],
        budget: Optional[int],
    ) -> float:
        score = 0.0
        if specialties:
            score += 0.5
        if countries:
            score += 0.35
        if budget:
            score += 0.15
        return round(min(score, 1.0), 2)
