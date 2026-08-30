from pydantic import BaseModel, Field
from typing import List, Set
from urllib.parse import urlparse

class EvidenceValidationResult(BaseModel):
    valid: bool
    accepted_urls: List[str]
    rejected_urls: List[str]
    warnings: List[str]

class EvidenceIntegrityValidator:
    @staticmethod
    def _normalize_url(url: str) -> str:
        """
        Normalize URLs by removing trailing slashes, fragments, and resolving http/https.
        """
        try:
            parsed = urlparse(url.lower().strip())
            domain = parsed.netloc
            path = parsed.path.rstrip('/')
            query = parsed.query
            return f"{domain}{path}?{query}"
        except:
            return url.lower().strip().rstrip('/')

    @staticmethod
    def validate_urls(claimed_urls: List[str], retrieved_urls: List[str]) -> EvidenceValidationResult:
        normalized_retrieved = {EvidenceIntegrityValidator._normalize_url(url) for url in retrieved_urls}
        
        accepted = []
        rejected = []
        warnings = []
        
        for url in claimed_urls:
            if url == "MODEL_KNOWLEDGE":
                continue
                
            norm = EvidenceIntegrityValidator._normalize_url(url)
            if norm in normalized_retrieved:
                accepted.append(url)
            else:
                rejected.append(url)
                warnings.append(f"REJECTED HALLUCINATED URL: {url} was not in retrieved search results.")
                
        return EvidenceValidationResult(
            valid=len(rejected) == 0,
            accepted_urls=accepted,
            rejected_urls=rejected,
            warnings=warnings
        )
