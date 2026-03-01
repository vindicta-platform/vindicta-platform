"""MCP Server for RAG rules retrieval (FR-005).

Implements the standard Model Context Protocol server interface,
exposing ``search_40k_rules`` tool for Vindicta agents to query
rules from the local ChromaDB vector store.

The server uses protocol-based dependency injection for the storage
layer, enabling testing without ChromaDB/Ollama.
"""

from __future__ import annotations

import logging
from typing import Any

from vindicta_foundation.models.rag import AgentQuery
from vindicta_foundation.rag_pipeline.storage import RulesStorage

logger = logging.getLogger(__name__)


class McpToolHandler:
    """Handler for MCP tool calls.

    Processes ``search_40k_rules`` requests by querying the
    local storage layer and returning formatted results.
    """

    def __init__(self, storage: RulesStorage) -> None:
        self._storage = storage

    def search_40k_rules(
        self,
        query_text: str,
        agent_id: str = "unknown",
        n_results: int = 5,
    ) -> dict[str, Any]:
        """Search for 40k rules by natural language query.

        This is the primary tool exposed via the MCP protocol.

        Args:
            query_text: Natural language search string.
            agent_id: Identifier of the calling agent.
            n_results: Max results to return.

        Returns:
            Dict with ``results`` list and ``query`` metadata.
        """
        # Validate the query via our model
        query = AgentQuery(
            query_text=query_text,
            agent_id=agent_id,
        )

        logger.info(
            "Agent %s searching: %s",
            query.agent_id,
            query.query_text[:80],
        )

        results = self._storage.search(
            query=query.query_text,
            n_results=n_results,
        )

        return {
            "results": results,
            "query": {
                "text": query.query_text,
                "agent_id": query.agent_id,
                "timestamp": query.timestamp.isoformat(),
            },
            "count": len(results),
        }

    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Return MCP-compatible tool definitions.

        This follows the MCP tool schema format so any
        MCP-compliant client can discover and use the tool.
        """
        return [
            {
                "name": "search_40k_rules",
                "description": (
                    "Search Warhammer 40k rules from local database. "
                    "Returns relevant rules excerpts with version history."
                ),
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query_text": {
                            "type": "string",
                            "description": "Natural language search query",
                        },
                        "agent_id": {
                            "type": "string",
                            "description": "Calling agent identifier",
                            "default": "unknown",
                        },
                        "n_results": {
                            "type": "integer",
                            "description": "Max results to return",
                            "default": 5,
                        },
                    },
                    "required": ["query_text"],
                },
            }
        ]
