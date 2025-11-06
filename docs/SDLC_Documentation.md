# Software Development Life Cycle (SDLC) Documentation

This document collects templates, examples and the minimal artifacts required to demonstrate a disciplined SDLC for product liability defense and quality assurance.

If you need a legal-ready submission (NHS/CRA/etc.) assemble the referenced artifacts per release and attach test evidence (logs, coverage, signed RMF entries).

## 1. Software Requirements Specification (SRS)
- Purpose: describe functional and non-functional requirements, interfaces, and constraints. The SRS is the authoritative source for intended behaviour used by testers and assessors.
Please see:
SpeedXToolKit Version Change Log - Functional Requirements
SpeedXToolKit Version Change Log - Non-Functional Requirements

## 2. Test Plans & Validation Reports
- Test plans must map to RequirementIDs. Use three layers of tests:
  1. Unit tests — validate small code units and parsing logic.
  2. Integration tests — validate the full ingestion -> transform -> output pipeline with representative sample files.
  3. Acceptance tests / Validation tests — verify user-level acceptance criteria and RMF mitigations.

- Validation Report (for each release) should include:
  - Environment (OS, Python version, library versions)
  - Test run date and author
  - Mapping of RequirementID -> TestCaseID -> Result (Pass/Fail)
  - Attachments: logs, screenshots, coverage report, test artifacts (sample input/output)

Templates created in `docs/tests/`:
- `docs/tests/unit_test_plan.md` (unit test scope and coverage targets)
- `docs/tests/integration_test_plan.md` (integration scenarios and sample data sets)
- `docs/tests/validation_report_TEMPLATE.md` (validation evidence template)

## 3. Traceability Matrix
- Purpose: provide evidence that each requirement is implemented and tested. This is essential for audits and product liability defense.
- Maintain `docs/traceability_matrix.csv` (machine readable). Columns recommended:
  - RequirementID, RequirementText, DesignRef, CodeRef, TestRef, TestResult, EvidenceRef, Status

Example CSV header and one row (already created in the repo as a scaffold):
RequirementID,RequirementText,DesignRef,CodeRef,TestRef,TestResult,EvidenceRef,Status
RQ-001,"Accept CSV with header","Design/Parser.md","speedxtoolkit/parser.py::parse","TC-001",Pass,"tests/results/tc-001.log",Implemented

Keep the traceability matrix up to date for each released version.

## 4. Version Change Log (CHANGELOG.md)
- Maintain a human-readable `CHANGELOG.md` at the project root using an established format (e.g., Keep a Changelog). Each release entry should include: version, date, Added/Changed/Fixed sections, and references to issue IDs or commit hashes.

Example entry:
## [3.4.0] - 2025-11-06
### Added
- Input schema validation and checksum support (RQ-010).

### Fixed
- Parser crash on missing trailing newline in CSV (issue #123).

## 5. Release & Validation Process (recommended checklist)
Before publishing a release, complete this checklist and store evidence in `docs/releases/<version>/`:
- [ ] All unit tests pass and coverage meets target.
- [ ] Integration tests for representative data sets pass.
- [ ] Security scans completed (dependency CVE scan) and SBOM updated.
- [ ] RMF hazard items touched by the release reviewed and mitigation evidence attached.
- [ ] Traceability matrix updated and validated.
- [ ] Release artifacts (binary, wheel, container image) are built reproducibly and signed if required.
- [ ] Release notes and `CHANGELOG.md` updated.
- [ ] Approvals: Dev Lead, QA Lead, CISO (or delegated roles) sign-off recorded.

Create `docs/release_checklist.md` as a scaffold for the above and store signed evidence in `docs/releases/<version>/`.

## 6. Artifacts to Keep (evidence repository)
- For each release, collect and archive in `docs/releases/<version>/`:
  - `docs/srs.md` (version snapshot)
  - Traceability matrix snapshot
  - Validation reports and test logs
  - SBOM (SPDX or CycloneDX format)
  - Dependency scan / vulnerability reports
  - Signed RMF hazard acceptance or mitigation evidence
  - Release manifest and changelog entry

## 7. Minimal automation recommendations
- Add CI gates to enforce: linting, unit tests, dependency scanning, SBOM generation, and automatic upload of test artifacts to `docs/releases/<ci_tag>/`.

## 8. Appendices
- A: Example file/dir layout for SDLC artifacts
  - docs/
    - srs.md
    - tests/
      - unit_test_plan.md
      - integration_test_plan.md
      - validation_report_TEMPLATE.md
    - traceability_matrix.csv
    - release_checklist.md
    - releases/
  - CHANGELOG.md

---
The following scaffolding files were created alongside this document (edit them to match your process and then populate with project-specific data):
- `docs/srs.md` (SRS template)
- `docs/tests/unit_test_plan.md`, `docs/tests/integration_test_plan.md`, `docs/tests/validation_report_TEMPLATE.md`
- `docs/traceability_matrix.csv` (scaffold)
- `CHANGELOG.md` (project root template)
- `docs/release_checklist.md` (release & validation checklist)
