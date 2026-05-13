"""
MCPClient — Model Context Protocol Client

Provides university enrichment data from an external JSON feed,
completely independent of the SQL database.

In production this feed URL would point to a real external API or
a subscribed MCP server. Here it reads from mcp/university_feed.json
as a lightweight simulation of an external MCP data source.
"""

import json
import os
from typing import Optional

from ai.sub_agent import Intent

_FEED_PATH = os.path.join(os.path.dirname(__file__), "../mcp/university_feed.json")


class MCPClient:
    """
    MCP (Model Context Protocol) client.

    Responsibilities:
    - Load external university feed on startup (not from SQL)
    - Filter the feed by the structured Intent provided by SubAgent
    - Format enrichment snippets (deadlines, scholarships, acceptance rate)
      to append to advisor responses
    """

    SOURCE = "external JSON feed (mcp/university_feed.json)"

    def __init__(self) -> None:
        self._feed: list[dict] = self._load()

    def get_context(self, intent: Intent, limit: int = 3) -> list[dict]:
        """
        Return MCP feed entries relevant to the given intent.
        Matches by country and specialty; if neither is set, returns top entries.
        """
        results: list[dict] = []

        for item in self._feed:
            match_country = (
                not intent.countries
                or item.get("country") in intent.countries
            )
            match_specialty = (
                not intent.specialties
                or any(s in item.get("specialties", []) for s in intent.specialties)
            )
            if match_country and match_specialty:
                results.append(item)
            if len(results) >= limit:
                break

        return results

    def format_context(self, context: list[dict]) -> Optional[str]:
        """Render MCP context entries as a markdown-style text snippet."""
        if not context:
            return None

        lines = ["\n📋 **Из внешнего источника (MCP-feed):**\n"]
        for item in context:
            lines.append(f"**{item['university']}** ({item.get('country', '')})")
            if item.get("acceptance_rate"):
                lines.append(f"  • Конкурс: {item['acceptance_rate']}")
            if item.get("application_deadline"):
                lines.append(f"  • Дедлайн: {item['application_deadline']}")
            if item.get("scholarships"):
                scholarships = item["scholarships"][:2]
                lines.append(f"  • Стипендии: {', '.join(scholarships)}")
            lines.append("")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Private
    # ------------------------------------------------------------------

    def _load(self) -> list[dict]:
        try:
            with open(_FEED_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"[MCPClient] Loaded {len(data)} entries from {self.SOURCE}")
                return data
        except FileNotFoundError:
            print(f"[MCPClient] Feed not found at {_FEED_PATH}, running without MCP context")
            return []
        except json.JSONDecodeError as e:
            print(f"[MCPClient] Feed parse error: {e}")
            return []
