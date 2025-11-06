# Data Protection Impact Assessment (DPIA)

Use this DPIA for GDPR/UK data protection assessments. Fill in project-specific details for each deployment.

## 1. Project and Controller Details
- Project name: SpeedXToolKit (data processing for labs/hospitals)
- Controller: [Customer Name]
- Processor: [Company Name]

## 2. Description of Processing
- Purpose: transform, validate, and reformat laboratory CSV files to customer-specified schemas. No automated clinical interpretation performed.
- Data categories: patient identifiers, demographics, laboratory test results, accession numbers, timestamps.
- Processing operations: ingestion, validation, mapping, output generation, optional storage for audit/troubleshooting.

## 3. Necessity and Proportionality
- Data minimization: only requested columns are processed; optional pseudonymization available. Default is local processing to avoid unnecessary transfers.
- Retention: configurable retention policy; recommended minimal retention of temporary files (e.g., 7 days) unless customer instructs otherwise.

## 4. Risks to Data Subjects
- Risk: unauthorized access to PHI (impact: severe)
- Risk: accidental disclosure via logs or mis-delivered files (impact: severe)
- Risk: data mismatch or corruption leading to misattributed results in downstream systems (impact: medium)

## 5. Mitigations
- Access controls, encryption in transit and at rest, least-privilege architecture.
- Operational mitigations: staff training, strict logging policies, test suites and validation checks, checksum validations, schema validation on input files.
- Technical mitigations: input validation, parsing sanity checks, explicit column mapping, unit tests for parser variations.

## 6. Residual Risk Evaluation
- After mitigations, residual risk for unauthorized access is Low-Medium when controls are implemented; for data mismatch residual risk is Low with QA procedures.

## 7. Consultation and Approvals
- Data Protection Officer (DPO) / Responsible person: [Name]
- Approval: signature block and date.

## 8. DPIA Review
- Review schedule: prior to launch and annually thereafter.
