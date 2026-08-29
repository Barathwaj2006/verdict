from pydantic import BaseModel
from typing import List
from duckduckgo_search import DDGS

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source_domain: str

class ResearchTool:
    def search(self, query: str) -> List[SearchResult]:
        raise NotImplementedError

class DuckDuckGoSearchProvider(ResearchTool):
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 3) -> List[SearchResult]:
        results = []
        try:
            raw_results = self.ddgs.text(query, max_results=max_results)
            for r in raw_results:
                domain = r.get("href", "").split("/")[2] if "href" in r else "unknown"
                results.append(SearchResult(
                    title=r.get("title", ""),
                    url=r.get("href", ""),
                    snippet=r.get("body", ""),
                    source_domain=domain
                ))
        except Exception as e:
            print(f"Search provider failed for query '{query}': {e}")
        return results
