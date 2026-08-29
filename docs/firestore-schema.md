# Firestore Schema (M6)

## Collections

### `investigations` (Collection)
- `investigation_id`: string (doc ID)
- `original_objective`: string
- `user_requirements`: string
- `explicit_constraints`: array of strings
- `status`: string ("IN_PROGRESS", "NEEDS_CLARIFICATION", "COMPLETED", "STALLED", "FAILED")
- `current_round`: integer
- `created_at`: timestamp
- `updated_at`: timestamp
- `final_verdict`: object (nullable)
- `termination_reason`: string (nullable)

#### `investigations/{investigation_id}/rounds` (Subcollection)
- `round_number`: integer (doc ID e.g., `round_1`)
- `status`: string
- `started_at`: timestamp
- `completed_at`: timestamp (nullable)
- `lead_plan`: object (serialized LeadPlan)
- `research_batches`: array of objects (serialized ResearchBatch list)
- `skeptic_report`: object (serialized SkepticReport, nullable)
- `verification_results`: array of objects (serialized VerificationResult list)
- `knowledge_gaps`: array of objects (serialized KnowledgeGap list)
- `decision`: string (nullable)

#### `investigations/{investigation_id}/state` (Subcollection)
- `state_id`: string (doc ID e.g., `global_state`)
- `executed_queries`: array of strings (for DuplicateQueryProtector)
