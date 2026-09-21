---
name: security-audit
description: Use for a read-only threat hunt with architecture mapping, coverage ledger, independent refutation and structured findings.
---
# Security audit
Adapted from Cloudflare's public MIT `security-audit-skill` (reviewed 2026-09-21).
Use guidance mode for focused questions; use full-audit mode only when the user
requests an audit or report artifacts. Follow six phases: recon and trust
boundaries, ledger-guided hunting, independent refutation, schema-validated
findings, independent record verification, and neutral report. Cover web/auth,
client, AI/MCP, memory/binary and supply chain. The parent owns the ledger and
report files; hunters have isolated scratch directories. Run target-controlled
code only in an OS-enforced, offline, resource-limited sandbox. Never exploit
production, expose secrets, install dependencies, or modify source.
