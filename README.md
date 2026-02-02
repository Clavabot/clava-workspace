# Clava Workspace

Память и конфигурация AI-ассистента Clava.

## Структура

```
├── MEMORY.md          # Долгосрочная память (ключевые факты, решения)
├── SOUL.md            # Личность и стиль
├── USER.md            # Информация о пользователе (Sasha)
├── IDENTITY.md        # Имя, аватар
├── AGENTS.md          # Инструкции поведения
├── TOOLS.md           # Заметки о инструментах
├── HEARTBEAT.md       # Периодические задачи
│
├── memory/            # Ежедневные заметки
│   └── YYYY-MM-DD.md
│
├── scripts/           # Утилиты
│   └── backup-memory.sh
│
├── clavagent-files/   # Файлы для ClavAgent (sub-agent)
└── .ssh-keys/         # SSH ключи для доступа к другим серверам
```

## Backup

- **Автоматический**: каждый час через OpenClaw cron → git push
- **Ручной**: `./scripts/backup-memory.sh`
- **Remote**: https://github.com/Clavabot/clava-workspace

## Связанные системы

- **ClavAgent** (Moltbook research): 20.97.238.79
- **Reports**: https://github.com/Clavabot/clavagent-reports
