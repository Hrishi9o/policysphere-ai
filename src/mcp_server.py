"""
Dell Hackathon 2026 - Problem Statement 1
Module: src/mcp_server.py
Standard Model Context Protocol (MCP) Server for Campus Policy Discovery.
Exposes standardized tools for autonomous AI agents, enterprise sidecars,
and desktop assistants (Claude Desktop, Cursor, Antigravity) over JSON-RPC.
"""

import sys
import json
from typing import Dict, Any, List

try:
    from src.retrieve import PolicyRetriever
    from src.answer import AnswerEngine
except ImportError:
    from retrieve import PolicyRetriever
    from answer import AnswerEngine


class CampusPolicyMCPServer:
    """
    Production-grade MCP Tool Provider implementing Model Context Protocol standard.
    """
    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self):
        self.retriever = PolicyRetriever()
        self.answer_engine = AnswerEngine()

    def get_manifest(self) -> Dict[str, Any]:
        """Returns standard MCP tool definitions."""
        return {
            "mcp_version": self.PROTOCOL_VERSION,
            "server_name": "policysphere-campus-discovery-mcp",
            "description": "Standard MCP server exposing autonomous campus policy retrieval and compliance verification tools.",
            "tools": [
                {
                    "name": "search_campus_policies",
                    "description": "Searches official MSRIT academic regulations using Multi-Hypothesis HyDE, vector RAG, and guardrails.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Informal student inquiry (e.g., 'Can I skip lab for a hackathon?')"
                            },
                            "mode": {
                                "type": "string",
                                "enum": ["raw", "hyde", "multi_hyde"],
                                "default": "multi_hyde",
                                "description": "Retrieval mode: raw query baseline, single HyDE, or multi-hypothesis RRF"
                            },
                            "top_k": {
                                "type": "integer",
                                "default": 3,
                                "description": "Number of handbook chunks to retrieve"
                            }
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_policy_by_section",
                    "description": "Retrieves the exact statutory legal handbook text for a given Section ID (e.g. '1.2.0', '6.1.0').",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "section_id": {
                                "type": "string",
                                "description": "Official section clause number (e.g., '1.2.0', '2.1.0', '6.1.0')"
                            }
                        },
                        "required": ["section_id"]
                    }
                },
                {
                    "name": "list_all_policy_sections",
                    "description": "Lists all 25 active policy clauses and categories indexed in the campus handbook.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches tool execution according to MCP specification."""
        if tool_name == "search_campus_policies":
            query = arguments.get("query", "").strip()
            mode = arguments.get("mode", "multi_hyde")
            top_k = arguments.get("top_k", 3)

            if not query:
                return {"error": "Query parameter cannot be empty."}

            if mode == "raw":
                chunks = self.retriever.retrieve_raw(query, top_k=top_k)
                hyde_used = False
            elif mode == "hyde":
                _, chunks, hyde_used = self.retriever.retrieve_hyde(query, top_k=top_k)
            else:
                _, chunks, hyde_used = self.retriever.retrieve_multi_hyde(query, top_k=top_k)

            res = self.answer_engine.generate_answer(query, chunks, hyde_used=hyde_used)
            return {
                "decision": res["decision"],
                "answer": res["answer"],
                "citations": res.get("citations", []),
                "guardrail_status": res.get("guardrail_status", "PASSED"),
                "confidence_score": res.get("confidence_score", 0.0)
            }

        elif tool_name == "get_policy_by_section":
            target_id = arguments.get("section_id", "").strip()
            for sec in self.retriever.sections:
                if sec["section_id"] == target_id:
                    return {
                        "section_id": sec["section_id"],
                        "title": sec["title"],
                        "category": sec["category"],
                        "text": sec["text"],
                        "source": sec.get("source", "data/handbook.md")
                    }
            return {"error": f"Section '{target_id}' not found in official handbook."}

        elif tool_name == "list_all_policy_sections":
            summary = [
                {
                    "section_id": s["section_id"],
                    "title": s["title"],
                    "category": s["category"]
                }
                for s in self.retriever.sections
            ]
            return {
                "total_sections": len(summary),
                "sections": summary
            }

        else:
            return {"error": f"Unknown tool name: '{tool_name}'"}


if __name__ == "__main__":
    server = CampusPolicyMCPServer()
    manifest = server.get_manifest()
    print("=" * 80)
    print(f"MCP SERVER INITIALIZED: {manifest['server_name']}")
    print(f"Protocol Version: {manifest['mcp_version']}")
    print(f"Available Tools: {[t['name'] for t in manifest['tools']]}")
    print("=" * 80)

    # Test tool 1
    test_q = "Can I skip lab for a hackathon?"
    print(f"\n[Testing Tool: search_campus_policies]")
    result = server.call_tool("search_campus_policies", {"query": test_q})
    print(f"Decision: {result['decision']}")
    print(f"Citations: {result['citations']}")

    # Test tool 2
    print(f"\n[Testing Tool: get_policy_by_section ('1.2.0')]")
    sec_info = server.call_tool("get_policy_by_section", {"section_id": "1.2.0"})
    print(f"Title: {sec_info.get('title')}")
