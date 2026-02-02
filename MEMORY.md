# MEMORY.md — Long-Term Memory

## Identity
- **Name:** Clava
- **Human:** Sasha (Alec Voronovich), @Aleq305, PST timezone
- **Contacts:** Арина (+18579190404) — жена/подруга Саши

## Infrastructure

### ClavAgent (Sub-agent for Moltbook research)
- **VM:** 20.97.238.79 (azureuser)
- **Gateway port:** 18790
- **SSH key:** `~/.openclaw/workspace/.ssh-keys/id_ed25519`
- **Webchat:** `http://127.0.0.1:18790/chat?token=clavagent-secret-token-2026`
- **Hooks token:** `clavagent-hook-token-2026`
- **Moltbook account:** TidalExplorer
- **Reports repo:** https://github.com/Clawabot/clavagent-reports

### Clava (Main agent - this instance)
- **Gateway port:** 18789
- **Browser:** Chrome headless enabled (noSandbox)

## Key Learnings

### 2026-02-01
- ClavAgent восстановлен из backup после потери VM
- SSH ключи нужно хранить в workspace (`~/.openclaw/workspace/.ssh-keys/`)
- При SSH рестарте gateway — нужен явный AZURE_API_KEY в env

### 2026-02-02
- Browser tool требует Chrome + headless + noSandbox на сервере
- ClavAgent webchat требует auth token в URL

## Projects

### Moltbook/Agent Economy Research
- ClavAgent автономно постит и взаимодействует на moltbook.com
- Фокус: Agent Economy, payment rails, Money Transmitter opportunity
- Саша владеет лицензированным Money Transmitter в USA
