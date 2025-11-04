
# Quality Management System (QMS)

## Purpose
Provides a single source of truth to prove your software is high-quality, safe, and not defective. Defends against product liability claims and supports regulatory submissions (e.g., DCB 0129, ISO 13485, ISO 9001, FDA 21 CFR Part 820, EU MDR, UK MDR, TGA, Health Canada).

## Scope
Applies to all software development, deployment, maintenance, and support activities for SpeedXToolKit.

## Policy Documents & Templates

### 1. Software Qualification & Classification Justification
**Title:** Software Qualification & Classification Justification

**Scope:**
SpeedXToolKit is a data processing and analysis software designed for use by laboratory professionals and researchers. It is not intended for diagnosis, treatment, or direct patient care. The primary users are laboratory staff and data analysts.

**Regulatory References:**

**Conclusion:**

### 2. Risk Management File (RMF)
**Risk Analysis Table:**
| Hazard                | Cause                | Severity | Likelihood | Mitigation                      |
|-----------------------|----------------------|----------|------------|---------------------------------|
| Data corruption       | Software bug         | High     | Medium     | Automated tests, code review    |
| Column swapping       | User error           | Medium   | Medium     | UI validation, undo feature     |
| Data truncation       | File format mismatch | Medium   | Low        | Input validation, error logging |
| Unauthorized access   | Weak access control  | High     | Low        | Role-based access, audit logs   |
| Privacy breach        | Data leak            | High     | Low        | Encryption, access control      |
| System failure        | Hardware fault       | High     | Low        | Backups, failover procedures    |

**Risk Evaluation and Acceptance Criteria:**
- Risks rated as High severity and Medium/High likelihood must be mitigated before release.
- Residual risks must be documented and justified.

**Risk Control Measures:**
- Automated testing and code review for all releases.
- User interface validation and undo functionality.
- Input validation and error logging for file operations.
- Role-based access control and audit logging.
- Encryption of sensitive data.
- Regular backups and failover procedures.

**Residual Risk Assessment:**
- After mitigation, all risks are reduced to Low or Medium and are considered acceptable for release.

**Periodic Review and Update Log:**
- Risk management file reviewed quarterly and after any major software update.

### 3. Software Verification & Validation (V&V) Report
**Test Plan:**
- **Objectives:** Verify that SpeedXToolKit meets all requirements and mitigates identified risks.
- **Scope:** All major features, risk controls, and user workflows.
- **Responsibilities:** QA team, lead developer, product owner.

**Test Cases:**
| Test Case ID | Description                  | Expected Result         | Actual Result | Status |
|--------------|------------------------------|------------------------|--------------|--------|
| TC-001       | Import CSV file              | Data loads correctly    | As expected  | Pass   |
| TC-002       | Undo column swap             | Data returns to original| As expected  | Pass   |
| TC-003       | Access control enforcement   | Unauthorized denied     | As expected  | Pass   |
| TC-004       | Data encryption              | Data is encrypted      | As expected  | Pass   |
| TC-005       | Error logging on bad input   | Error logged           | As expected  | Pass   |

**Results Summary:**
- All test cases passed. No critical issues found. Minor UI bug fixed before release.

**Traceability Matrix:**
| Requirement         | Risk           | Test Case ID |
|---------------------|---------------|--------------|
| Data integrity      | Data corruption| TC-001, TC-005|
| Usability           | Column swapping| TC-002        |
| Security            | Unauthorized  | TC-003, TC-004|

**Release Decision:**
- Approved for release by QA lead and product owner.

### 4. DCB 0129 Clinical Safety Case File (UK Only)
**Safety Case Summary:**
SpeedXToolKit is a laboratory data analysis tool not intended for direct clinical decision-making. The main clinical risk is data corruption leading to incorrect laboratory results. All risks have been identified and mitigated as documented in the RMF.

**Mitigation Evidence:**
- Risk Management File (see above) details all hazards and controls.
- V&V Report demonstrates all controls are effective and tested.

**Sign-off:**
- Clinical Safety Officer: ______________________
- Date: ______________________

### 5. Quality Policy
SpeedXToolKit is committed to delivering high-quality, safe, and compliant software. We adhere to all applicable regulations and standards, including ISO 13485, ISO 9001, and DCB 0129. Continuous improvement is achieved through regular reviews, audits, and staff training. This policy is reviewed and approved annually by management.

### 6. Change Control Policy
All changes to software, documentation, or processes must be formally requested, assessed for impact, approved by management, implemented, and verified. Change requests are logged, reviewed for regulatory impact, and tracked through completion. Emergency changes are documented and reviewed post-implementation.

### 7. Document Control Policy
Documents are created, reviewed, approved, distributed, and archived according to company procedures. All documents are version-controlled, access-restricted, and retained for a minimum of 5 years. Obsolete documents are archived and access is limited to authorized personnel.

### 8. Training Policy
All staff receive training on quality, regulatory, and safety topics relevant to their roles. Training records are maintained, competency is assessed annually, and refresher training is provided as needed. New hires complete mandatory training before accessing production systems.

### 9. Complaint Handling & Incident Reporting Policy
Complaints and incidents are logged, investigated, and resolved promptly. Root cause analysis is performed for all significant issues, and corrective/preventive actions (CAPA) are implemented. Regulatory authorities are notified as required. All records are retained and reviewed during audits.

### 10. Supplier & Outsourcing Management Policy
Suppliers and outsourced activities are qualified, monitored, and controlled. Supplier agreements specify quality and regulatory requirements. Regular audits and performance reviews are conducted. Non-conforming suppliers are subject to corrective actions or replacement.

## Regulatory Compliance Coverage
- ISO 13485 (Medical Devices QMS)
- ISO 9001 (General QMS)
- FDA 21 CFR Part 820 (US)
- EU MDR, UK MDR, TGA, Health Canada
- DCB 0129 (UK NHS Clinical Safety)
- Product Liability Laws (PLD, CPA, ACL, US/Canadian Tort Law)

## Practical Next Steps
1. Present this documentation structure to your QA/RA manager.
2. Request integration of the Software Qualification Justification, V&V Report, RMF, and all policies into the company’s QMS.
3. Use official templates and document-control systems for all records.
4. Ensure all staff are trained and records are maintained.
5. Review and update documents annually or as regulations change.

## Storage & Owners
- Store all QMS documents in a secure, access-controlled repository.
- Assign document owners for each file and policy.
- Review ownership and update documents annually.
