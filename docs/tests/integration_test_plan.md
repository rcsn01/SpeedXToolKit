# Integration Test Plan (template)

Purpose: validate end-to-end scenarios from ingestion to output.

- Test owner: [name]
- Test environment: staging server or local reproducible env

Integration scenarios (examples):
- TC-001: Ingest sample hospital CSV, apply mapping, produce output matching canonical file.
- TC-002: Large file streaming test (10k rows) to validate memory usage and performance.

Each scenario should include input sample, mapping file, expected output, and pass/fail criteria.
