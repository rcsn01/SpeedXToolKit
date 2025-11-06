# Information Security Policy

This policy sets out high-level security rules for staff and contractors working with SpeedXToolKit and any systems processing customer data.

## 1. Purpose and Scope
- Purpose: define the security expectations, responsibilities, and minimum controls. Scope: all personnel, systems, and data processing activities.

## 2. Acceptable Use Policy
- Company devices must be used for work tasks only. Personal use must not involve customer PHI.
- Prohibited actions: storing PHI in personal cloud storage, sharing credentials, disabling security software.

## 3. Access Control Policy
- Principle of least privilege: access granted only as required.
- Role-based access: developers, operators, support, and administrators have defined access levels.
- User access lifecycle: documented onboarding/offboarding with timely revocation of privileges.

## 4. Password and Authentication Policy
- Passwords: minimum length 12, complexity encouraged; use passphrases.
- MFA: mandatory for all accounts with access to customer data or administrative functions.
- Credential storage: no plaintext credentials in source control; use secret manager.

## 5. Data Handling and Classification
- Data classification levels: Public, Internal, Sensitive (PHI). PHI must be handled per DPA/BAA.
- Data-in-transit: TLS v1.2+ required. Data-at-rest: AES-256 encryption recommended for persisted PHI.

## 6. Logging and Monitoring
- Application logs shall avoid PHI. Access logs retained for incident analysis and limited to required duration.
- Monitoring: alerts for suspicious logins, failed access attempts, and anomalous file operations.

## 7. Incident Response Plan (IRP)
- Detection & reporting: staff must report suspected incidents to the Incident Response Lead immediately.
- Initial response: contain and preserve evidence, assess scope and affected data, notify customers per DPA/BAA timelines (72 hours for GDPR-style incidents).
- Communication: designated spokesperson; preserve confidentiality of the investigation.
- Post-incident: root cause analysis, remediation plan, lessons learned.

## 8. Patch & Vulnerability Management
- Regular patching schedule; critical patches applied within defined SLA (e.g., 7 days).
- Maintain SBOM and scan dependencies regularly.

## 9. Training and Awareness
- Annual security awareness training for all staff, role-specific training for developers/ops handling PHI.

## 10. Physical Security
- Company-issued devices protected by disk encryption; visitor controls for office locations.

## 11. Business Continuity and Backups
- Backups encrypted, access-controlled, and tested periodically for restore capability.

## 12. Policy Review
- Review frequency: annual or after material changes.

## 13. Exceptions
- Any exceptions to this policy must be approved in writing by the CISO or equivalent.
