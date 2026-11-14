"""
Dell Hackathon 2026 - Problem Statement 1
Campus Policy Discovery Assistant: Model Context Protocol (MCP) Interface
Implements standard Model Context Protocol (MCP) tool schemas for Agent-to-Agent discovery.
Evaluated under Dell Technology (25%) Evaluation Matrix.
"""

import json
from typing import Dict, Any, List
from vector_engine import PolicyVectorStore

class CampusPolicyMCPServer:
    """
    Standard Model Context Protocol (MCP) Tool Interface.
    Exposes campus policy discovery and regulatory handbook lookup to autonomous AI agents.
    """

    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self):
        self.vector_store = PolicyVectorStore()

    def get_manifest(self) -> Dict[str, Any]:
        """
        Returns MCP Server tool definitions adhering to the Model Context Protocol standard.
        """
        return {
            "mcp_version": self.PROTOCOL_VERSION,
            "server_name": "dell-campus-policy-discovery-mcp",
            "capabilities": {
                "tools": [
                    {
                        "name": "search_campus_policies",
                        "description": (
                            "Searches the official university academic regulations and policy handbook. "
                            "Uses HyDE (Hypothetical Document Embeddings) to bridge colloquial student queries "
                            "with formal institutional administrative clauses."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The student's inquiry or scenario (can be informal, e.g., 'Can I skip lab for a gig?')"
                                },
                                "use_hyde": {
                                    "type": "boolean",
                                    "default": True,
                                    "description": "Whether to apply HyDE translation before vector retrieval."
                                },
                                "top_k": {
                                    "type": "integer",
                                    "default": 3,
                                    "description": "Number of top matching regulatory clauses to return."
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_clause_by_id",
                        "description": "Fetches the full legalistic regulatory text and constraints of a specific clause ID.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "clause_id": {
                                    "type": "string",
                                    "description": "The official handbook clause ID (e.g., 'ACA-ATT-4.2', 'ACA-LAB-5.3')"
                                }
                            },
                            "required": ["clause_id"]
                        }
                    }
                ]
            }
        }

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP Tool Dispatcher executing tool calls from autonomous agents.
        """
        if tool_name == "search_campus_policies":
            query = arguments.get("query", "")
            use_hyde = arguments.get("use_hyde", True)
            top_k = arguments.get("top_k", 3)

            if use_hyde:
                hyde_doc, results = self.vector_store.search_hyde(query, top_k=top_k)
                return {
                    "tool": "search_campus_policies",
                    "mode": "HyDE_Enhanced",
                    "synthesized_hyde_memo": hyde_doc,
                    "retrieved_clauses": results
                }
            else:
                results = self.vector_store.search_raw(query, top_k=top_k)
                return {
                    "tool": "search_campus_policies",
                    "mode": "Raw_Baseline",
                    "retrieved_clauses": results
                }

        elif tool_name == "get_clause_by_id":
            clause_id = arguments.get("clause_id", "").strip().upper()
            for p in self.vector_store.policies:
                if p["clause_id"].upper() == clause_id:
                    return {
                        "status": "FOUND",
                        "clause": p
                    }
            return {
                "status": "NOT_FOUND",
                "message": f"Clause ID {clause_id} does not exist in the official handbook."
            }

        else:
            return {
                "error": f"Unknown MCP tool: {tool_name}"
            }


if __name__ == "__main__":
    # Test MCP tool calling
    mcp = CampusPolicyMCPServer()
    manifest = mcp.get_manifest()
    print("=" * 80)
    print("MODEL CONTEXT PROTOCOL (MCP) SERVER INITIALIZED")
    print(f"Server Name: {manifest['server_name']} (v{manifest['mcp_version']})")
    print(f"Registered MCP Tools: {[t['name'] for t in manifest['capabilities']['tools']]}")
    print("=" * 80)

    # Call MCP search tool
    sample_call = mcp.call_tool("search_campus_policies", {
        "query": "My band has a gig next Friday, can I skip my lab and make it up later?",
        "use_hyde": True,
        "top_k": 2
    })
    print("\nMCP Tool Execution Result:")
    print(json.dumps(sample_call, indent=2))

