# Release & Validation Checklist

Use this checklist for every release and store completed evidence in `docs/releases/<version>/`.

- [ ] Update `CHANGELOG.md` and bump version tag
- [ ] Update `docs/srs.md` snapshot (if requirements changed)
- [ ] Run unit tests and attach results (`docs/releases/<version>/tests/unit/`)
- [ ] Run integration tests and attach results (`docs/releases/<version>/tests/integration/`)
- [ ] Generate SBOM and store (`docs/releases/<version>/sbom/`)
- [ ] Run dependency vulnerability scan; resolve or document exceptions
- [ ] Update `docs/traceability_matrix.csv` and attach snapshot
- [ ] RMF hazard items: review mitigations touched by this change; update RMF and sign off
- [ ] Security review: CISO or delegate sign-off
- [ ] QA validation report completed and signed
- [ ] Tag release in VCS and attach release artifacts and checksums

Record approvers and dates in `docs/releases/<version>/approvals.txt`.
