# HIPAA Security Risk Analysis (SRA) - Internal Assessment

Purpose: internal assessment of risks to Protected Health Information (PHI) created, received, maintained, or transmitted by [Company Name] when using SpeedXToolKit. Update annually and after major changes.

## 1. Scope
- Systems and services in scope: SpeedXToolKit application, ingestion pipelines, data stores, developer machines that handle customer data, build artifacts, backups.
- PHI in scope: patient identifiers (name, DOB, MRN), test results, accession numbers, contact details, provider details.

## 2. PHI Inventory
- Source: CSV imports provided by customers (labs/hospitals).
- Stored: temporary processing directory, optional persistent output directory if customer configures it.
- Transmitted: over TLS to customer endpoints when configured; local processing by default.

## 3. Threats & Vulnerabilities
List plausible threats and vulnerabilities. Assign an initial likelihood (High/Medium/Low).

- Employee laptop theft — Vulnerability: unencrypted device or credentials stored locally. Likelihood: Medium. Impact: High.
- Ransomware attack on server handling files — Vulnerability: internet-connected server without EDR or patching. Likelihood: Medium. Impact: High.
- Accidental data disclosure via log files — Vulnerability: verbose logging of file contents. Likelihood: Medium. Impact: Medium.
- Data corruption bug in parser causing mismatched columns — Vulnerability: insufficient input validation and unit tests. Likelihood: Medium. Impact: Medium.
- Unauthorized access due to weak access control — Vulnerability: shared credentials, weak password policy. Likelihood: Medium. Impact: High.
- Third-party library vulnerability — Vulnerability: outdated dependency with known CVE. Likelihood: Medium. Impact: High.

## 4. Current Controls
- Encryption: TLS for network transmission; AES-256 recommended for data at rest where persisted.
- Access controls: role-based accounts for cloud services; local processing reduces exposure.
- Logging: application logs redact PHI by default; debug mode must be off in production.
- Backups: encrypted backups with limited retention and access controls.
- Development controls: static analysis, code reviews, unit tests, CI pipeline (if used).
- Physical: secure office policies; company-issued devices for staff handling PHI.

## 5. Risk Assessment Matrix
- For each Threat, document Likelihood, Impact, Risk Level (derived), and Rationale.

Example row:
- Threat: Employee laptop theft
- Likelihood: Medium
- Impact: High
- Risk Level: High
- Rationale: Device may hold cached input files; without disk encryption, PHI exposure likely.

## 6. Mitigation Plan (for Medium/High risks)
- Employee laptop theft
  - Controls to implement: full disk encryption (BitLocker), mandatory device enrollment, remote wipe capability, restrict local storage of PHI, enforce MFA.
  - Owner: IT Manager
  - Target date: [date]

- Ransomware on server
  - Controls: maintain patching schedule, host-based EDR, immutable backups, network segmentation.
  - Owner: IT Manager
  - Target date: [date]

- Logging disclosure
  - Controls: ensure PHI redaction, code review of logging, disable debug in production, redact test data in logs.
  - Owner: Dev Lead
  - Target date: [date]

- Dependency vulnerabilities
  - Controls: maintain SBOM, schedule dependency scans, patch/update policy, subscribe to security advisories.
  - Owner: DevOps
  - Target date: [date]

## 7. Residual Risk and Acceptance
- For each mitigation, note residual risk and acceptance by risk owner.

## 8. Review Schedule
- Review frequency: annually and whenever major changes occur.

## 9. Appendices
- Appendix A: Evidence (encryption settings, training records, certificates)
- Appendix B: Contact list for incident response
