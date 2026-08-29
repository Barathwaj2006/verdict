import re

class DuplicateQueryProtector:
    @staticmethod
    def _normalize_query(query: str) -> str:
        # Lowercase, remove extra whitespace, remove common punctuation
        q = query.lower()
        q = re.sub(r'[^\w\s]', '', q)
        q = re.sub(r'\s+', ' ', q)
        return q.strip()

    @staticmethod
    def filter_queries(queries: list[str], executed_queries: set[str]) -> tuple[list[str], list[str]]:
        unique_queries = []
        duplicate_queries = []
        
        for q in queries:
            norm = DuplicateQueryProtector._normalize_query(q)
            if norm in executed_queries:
                duplicate_queries.append(q)
            else:
                executed_queries.add(norm)
                unique_queries.append(q)
                
        return unique_queries, duplicate_queries
