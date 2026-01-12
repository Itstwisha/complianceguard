# Compliance Framework Mapping

This document explains how ComplianceGuard checks map to industry compliance frameworks.

## CIS Apple macOS 14.0 Benchmark

| Check ID | CIS Control | Level |
|----------|-------------|-------|
| CIS-1.1 | 1.1 Ensure All Apple-Provided Software Is Current | L1 |
| CIS-2.1.1 | 2.1.1 Ensure Firewall Is Enabled | L1 |
| CIS-2.6.1 | 2.6.1 Ensure FileVault Is Enabled | L1 |
| CIS-4.2 | 4.2 Ensure SSH Is Configured Securely | L1 |
| CIS-5.9 | 5.9 Ensure Screen Lock Timeout Is Set | L1 |

**Reference:** CIS Apple macOS 14.0 Benchmark v1.0.0 (November 2023)

## NIST Cybersecurity Framework v1.1

| Check | NIST CSF Category | Subcategory |
|-------|-------------------|-------------|
| Software Updates | PR.IP-12 | A vulnerability management plan is developed and implemented |
| Firewall | PR.AC-5 | Network integrity is protected |
| FileVault | PR.DS-1 | Data-at-rest is protected |
| SSH Config | PR.AC-4 | Access permissions are managed |
| Screen Lock | PR.AC-7 | Users are authenticated |

## ISO/IEC 27001:2022 (Annex A)

| Check | ISO 27001 Control | Control Title |
|-------|-------------------|---------------|
| Software Updates | A.12.6.1 | Management of technical vulnerabilities |
| Firewall | A.13.1.1 | Network controls |
| FileVault | A.10.1.1 | Policy on the use of cryptographic controls |
| SSH Config | A.13.1.1 | Network controls |
| Screen Lock | A.11.2.8 | Unattended user equipment |

---

**Sources:**
- CIS Benchmarks: https://www.cisecurity.org/cis-benchmarks
- NIST CSF: https://www.nist.gov/cyberframework  
- ISO 27001: https://www.iso.org/standard/27001
