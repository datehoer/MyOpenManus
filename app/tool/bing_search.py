import asyncio
from typing import List
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
from app.tool.base import BaseTool

class BingSearch(BaseTool):
    name: str = "bing_search"
    description: str = """Perform a Bing search and return a list of relevant links。
Use this tool when you need to find information on the web, get up-to-date data, or research specific topics.
The tool returns a list of URLs that match the search query.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "(required) The search query to submit to Bing."
            },
            "num_results": {
                "type": "integer",
                "description": "(optional) The number of search results to return. Default is 10.",
                "default": 10
            }
        },
        "required": ["query"]
    }

    async def execute(self, query: str, num_results: int = 10) -> List[str]:
        """
        Execute a Bing search and return a list of URLs.
        Args:
            query (str): The search query to submit to Bing.
            num_results (int, optional): The number of search results to return. Default is 10.
        Returns:
            List[str]: A list of URLs matching the search query.
        """

        def sync_search():
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            url = f'https://www.cn.bing.com/search?q={quote(query)}'
            links = []

            for page in range(0, num_results // 10 + 1):
                resp = requests.get(
                    f'{url}&first={page * 10}',
                    headers=headers,
                    timeout=10
                )
                soup = BeautifulSoup(resp.text, 'html.parser')

                for result in soup.select('.b_algo'):
                    link = result.find('a', href=True)
                    if link and 'href' in link.attrs:
                        links.append(link['href'])
                        if len(links) >= num_results:
                            return links
            rst = links[:num_results]
            return rst

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_search)