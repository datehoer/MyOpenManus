import httpx
import asyncio
from app.config import config
from app.tool.base import BaseTool
from typing import List


class ExaAi(BaseTool):
    api_key = config.exa_ai.get("api_key")
    if api_key:
        name: str = "exa_ai"
        description: str = """Perform an Exa.ai search and return a list of search result.
Use this tool when you need to find information on the web, get up-to-date data, or research specific topics using Exa.ai's AI-powered search capabilities.
The tool returns a list of Search Result that match the search query."""
        parameters: dict = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "(required) The search query to submit to Exa Ai Search.",
                },
                "num_results": {
                    "type": "integer",
                    "description": "(optional) The number of search results to return. Default is 10.Max is 100.",
                    "default": 10,
                },
            },
            "required": ["query"],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        async def execute(self, query: str, num_results: int = 10) -> List[str]:
            loop = asyncio.get_event_loop()
            proxy = config.default.get("proxy")
            results = await loop.run_in_executor(
                None, lambda: list(httpx.post("https://api.exa.ai/search", headers=self.headers, json={
                "query": query,
                "contents": {
                  "text": True
                },
                "numResults": num_results
            }, proxy=proxy).json()['data']['results']))
            return results

