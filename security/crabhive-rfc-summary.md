# Crabhive Security RFC Summary

Source: https://x.com/crabhive/status/2018144604822847964
Full guide: https://github.com/40verse/TETSU/blob/main/docs/security/CRABHIVE-TETSU-MINIMAL-SECURITY-ENHANCEMENTS-RFC-GUIDE.md

## The Iron Crab Principle
> "Harden the shell first, then grant capabilities."

- All security modules enabled by default
- Explicit opt-out required for relaxed security
- Zero-trust is the floor, not the ceiling

## Five Security Modules

### 1. Input Sanitization
- Unicode normalization (NFC)
- Control character stripping
- Bidirectional override detection
- Base64 payload flagging
- Suspicious pattern warnings

### 2. Rate Limiting
- Per-session limits
- Per-tool limits (exec tighter than message)
- Cooldown periods on violations
- Exempt tools for safe operations

### 3. Structured Audit Logging
- Structured JSON format
- Correlation IDs across requests
- Configurable sinks (file, console, webhook)
- ISO 8601 timestamps with actor attribution

### 4. Session Isolation
- Three levels: strict/standard/relaxed
- Ownership validation on every call
- Timeout enforcement
- Concurrent session limits
- Tool state clearing

### 5. Hook Execution Hardening
- Enforced timeouts with SIGKILL
- Payload size limits
- Schema validation
- Output sanitization (strip ANSI, control chars)
- Error containment

## Threat Matrix

| Threat | Module | Mitigation |
|--------|--------|------------|
| Prompt injection | Sanitization | Pattern detection, warnings |
| Unicode attacks | Sanitization | NFC normalization |
| ANSI injection | Sanitization + Hooks | Control char stripping |
| Resource exhaustion | Rate Limiting | Hierarchical limits |
| Session hijacking | Session Isolation | Ownership validation |
| State leakage | Session Isolation | Isolation levels |
| Hook attacks | Hook Hardening | Timeouts, sandboxing |
| Forensic gaps | Audit Logging | Structured events |

## Implementation Priority

1. **Phase 1 (Now):** Input Sanitization + Rate Limiting
2. **Phase 2 (Next):** Structured Audit Logging
3. **Phase 3 (After):** Session Isolation + Hook Security
