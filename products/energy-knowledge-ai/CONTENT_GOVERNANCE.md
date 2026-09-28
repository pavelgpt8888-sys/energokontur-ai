# Content Governance — Energy Knowledge AI BY

## Purpose
Нормативная база продукта является управляемой базой знаний. Автоматизация и AI помогают собирать и разбирать документы, но доверенная публикация выполняется ответственным человеком.

## Operating model

### Mode A — Customer-managed
Заказчик назначает `Content Curator` (ответственного за нормативную базу).

Curator:
- добавляет документы вручную или принимает найденные системой кандидаты;
- проверяет номер, название, орган, дату и статус;
- связывает редакции;
- подтверждает/отклоняет изменения;
- публикует запись для пользователей;
- архивирует/заменяет устаревшие документы.

### Mode B — Managed Service
Наша поддержка ведёт операционную работу с базой:
- отслеживает новые кандидаты;
- загружает и разбирает документы;
- подготавливает карточки и связи;
- выполняет первичную проверку;
- публикует изменения по согласованной с заказчиком процедуре либо передаёт их на финальное подтверждение его ответственному сотруднику.

Этот режим может входить в отдельный SLA/подписку.

## Workflow

```text
MANUAL UPLOAD / DISCOVERY
        ↓
     CANDIDATE
        ↓
      PARSED
        ↓
  AWAITING REVIEW
        ↓
   ┌────┴────┐
 APPROVE    REJECT
   ↓
APPROVED
   ↓
PUBLISHED
   ↓
users / search / RAG
```

При новой редакции:

```text
new candidate
      ↓
review + version link
      ↓
approve new version
      ↓
publish new version
      ↓
previous version → superseded/archive
```

## Admin UI — minimum

Экран `Нормативная база`:
- таблица документов;
- фильтры по статусу, типу, органу, теме;
- кнопка `Добавить документ`;
- очередь `На проверку`;
- карточка документа;
- загрузка файла или URL;
- metadata editor;
- version relationships;
- preview parsed text;
- source/provenance block;
- `Approve` / `Reject` / `Publish` / `Archive`;
- audit history.

## Roles

### Reader
Ищет документы и задаёт вопросы только по `published` контенту.

### Content Curator
Управляет нормативной базой и публикацией.

### Support Operator
Готовит кандидаты и обновления в managed-service режиме.

### Admin
Управляет пользователями, ролями, настройками источников и политиками публикации.

## Trust rules

1. LLM never publishes content by itself.
2. Unapproved candidate content is excluded from trusted RAG answers.
3. Every published record retains source/provenance.
4. Every approval/publication stores actor + timestamp.
5. Version/status changes are auditable.
6. If document validity is unclear, status remains `unknown` until review.
7. Customer can disable automatic discovery entirely and maintain content manually.

## Commercial implication
Content maintenance is part of the product proposition, not an afterthought.

Potential packages:
- `Platform only` — customer maintains its own knowledge base;
- `Platform + Content Support` — our team maintains the queue and prepares updates;
- `Full Managed Knowledge Service` — continuous maintenance, agreed SLA, periodic quality review and reporting.
