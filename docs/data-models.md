# Data Models (Pydantic / TypeScript)

```python
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ClaimStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    INSUFFICIENT = "INSUFFICIENT"

class Claim(BaseModel):
    claim_id: str
    statement: str
    evidence: str
    source: str
    originating_agent: str
    confidence: float
    status: ClaimStatus
    verification_status: Optional[str] = None
    related_research_round: int

class ResearchMission(BaseModel):
    assigned_agent: str
    brief: str

class Challenge(BaseModel):
    challenge_id: str
    claim_id: str
    challenge_type: str
    argument: str

class VerificationResult(BaseModel):
    claim_id: str
    is_verified: bool
    new_status: ClaimStatus
    reasoning: str

class Verdict(BaseModel):
    summary: str
    decision: str
    key_evidence: List[Claim]
    caveats: List[str]
```
