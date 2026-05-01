## D4 — Findings SAST

| ID | Outil | Service | Fichier | Règle | Sévérité | Statut |
|----|-------|---------|---------|-------|----------|--------|
| S-01 | Bandit | user-service | app.py:68 | B104 hardcoded_bind_all_interfaces | Medium | Faux positif — nosec ajouté |
| S-02 | Bandit | product-service | app.py:49 | B104 hardcoded_bind_all_interfaces | Medium | Faux positif — nosec ajouté |
| S-03 | Bandit | notification-service | app.py:29 | B104 hardcoded_bind_all_interfaces | Medium | Faux positif — nosec ajouté |
| S-04 | Semgrep | order-service | index.js | — | — | 0 findings |
| S-05 | Semgrep | payment-service | index.js | — | — | 0 findings |
| S-06 | Semgrep | inventory-service | index.js | — | — | 0 findings |

## D4 — Findings Container Scanning (Trivy)

| ID | Image | OS Base | CVE | Sévérité | Library | Fix |
|----|-------|---------|-----|----------|---------|-----|
| T-01 | inventory-service | debian 12.13 | CVE-2026-0861 | CRITICAL | libc-bin/glibc | Migrer vers node:20-alpine |
| T-02 | order-service | debian 12.13 | CVE-2026-0861 | HIGH | libc-bin/glibc | Migrer vers node:20-alpine |
| T-03 | payment-service | debian 12.13 | CVE-2026-0861 | HIGH | libc-bin/glibc | Migrer vers node:20-alpine |
| T-04 | user-service | debian 13.4 | — | — | — | Clean ✅ |
| T-05 | product-service | debian 13.4 | — | — | — | Clean ✅ |
| T-06 | notification-service | debian 13.4 | — | — | — | Clean ✅ |