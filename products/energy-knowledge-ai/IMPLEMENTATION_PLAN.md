# Energy Knowledge AI BY — Implementation Plan v0.1

Дата старта: 2026-08-23

## Цель
За минимальный разумный срок получить живой, устойчивый демонстрационный продукт для показа Минэнерго Республики Беларусь / ГПО «Белэнерго», а затем без переписывания ядра перейти к закрытому пилоту на документах заказчика.

## Принцип
Не строим весь Enterprise заранее. Делаем вертикальный срез end-to-end:

public/legal energy sources -> ingestion -> document registry -> hybrid retrieval -> reranker -> Belarus-hosted LLM -> grounded answer -> citation -> web UI -> eval.

LLM является заменяемым компонентом. Основной продукт — document intelligence, retrieval, version/status awareness, citations, access control и evaluation.

---

## Сводные сроки

### Demo v0.1 — 10–15 рабочих дней
Можно уверенно показывать руководителю: вопрос -> подтверждённый ответ -> источник -> документ.

### Pilot-ready v0.2 — 4–6 недель от старта
Можно принять ограниченный набор внутренних документов заказчика, дать доступ тестовой группе и измерять KPI.

### Production-ready v1.0 — 8–12 недель от старта
При отсутствии тяжёлых интеграций и нестандартных требований ИБ.

### Enterprise rollout — дополнительно 6–12+ недель
Зависит от СЭД/1С/AD/LDAP, требований ИБ, аттестации, количества филиалов и объёма legacy-документов.

---

# Phase 0 — Source & Legal Discovery
Срок: 1–2 рабочих дня

## Задачи
- составить реестр официальных и легально используемых источников;
- разделить metadata-only, full-text allowed и restricted sources;
- выбрать 100–300 документов/карточек для первого набора;
- определить 30–50 демонстрационных/eval вопросов;
- определить типы документов и обязательные metadata.

## Результат
- `SOURCE_REGISTRY.md`;
- первый corpus manifest;
- eval questions v0;
- правила использования источников.

## Gate
Нельзя массово ingest'ить документы, пока не понятен правовой статус источника.

---

# Phase 1 — Ingestion & Document Registry
Срок: 2–3 рабочих дня

## Задачи
- загрузка PDF/DOCX/HTML/text;
- извлечение текста;
- OCR fallback для сканов;
- нормализация;
- chunking с сохранением структуры;
- metadata extraction;
- document registry;
- связи `replaces / replaced_by / amends / active`.

## Минимальная схема документа
- id;
- title;
- type;
- number;
- issuer;
- issue_date;
- effective_from;
- effective_to;
- status;
- source_url;
- source_type;
- access_level;
- predecessor/successor;
- checksum/version.

## Результат
100–300 качественно обработанных документов/карточек.

---

# Phase 2 — Retrieval Core
Срок: 2–3 рабочих дня

## Задачи
- lexical/BM25 search;
- vector search;
- metadata filters;
- reciprocal rank fusion или аналогичный hybrid merge;
- reranker;
- status/version filters;
- retrieval API.

## KPI
- correct source Top-5 >= 90% на eval set;
- deprecated/replaced document не должен выигрывать у действующего без явного запроса пользователя.

---

# Phase 3 — RAG Answer Engine + Belarus LLM
Срок: 1–2 рабочих дня

## Задачи
- OpenAI-compatible provider adapter, если поддерживается;
- Qwen/другая доступная LLM белорусского провайдера;
- context builder;
- grounded answer policy;
- citation generation;
- abstention policy;
- confidence/evidence checks;
- логирование model/version/latency/token usage.

## Ключевое правило
No evidence -> no confident answer.

## KPI
- citation accuracy >= 95%;
- unsupported confident claims — 0 на критическом eval-наборе;
- ответ должен позволять открыть первоисточник.

---

# Phase 4 — Demo Web UI
Срок: 2–3 рабочих дня

## Основные режимы
1. Спросить.
2. Найти документ.
3. Сравнить редакции.
4. Что изменилось?

## Экран ответа
- краткий ответ;
- confidence/evidence state;
- источники;
- название/номер/статус документа;
- фрагмент доказательства;
- кнопка «Открыть источник».

## Не делаем сейчас
- сложный кабинет администратора;
- полноценный RBAC;
- красивую аналитику;
- агенты;
- 1С/СЭД интеграции.

---

# Phase 5 — Evaluation & Demo Hardening
Срок: 2–3 рабочих дня

## Набор тестов
- 10 exact document lookup;
- 10 semantic questions;
- 10 multi-source questions;
- 10 version/status questions;
- 10 no-answer/adversarial questions.

## Проверяем
- retrieval recall;
- citation accuracy;
- answer faithfulness;
- abstention;
- latency;
- broken source links;
- duplicate/outdated documents;
- prompt injection in documents.

## Definition of Demo Ready
- Top-5 source recall >= 90%;
- citation accuracy >= 95%;
- no-answer работает;
- 10–15 заранее подготовленных killer scenarios проходят end-to-end;
- нет ручного вмешательства во время демонстрации;
- demo может быть поднято повторно из README/runbook.

---

# Demo checkpoint
Ориентир: конец 2-й / начало 3-й рабочей недели.

После этого уже можно назначать встречу в Минэнерго/Белэнерго.

Не ждём Enterprise v1.0 для первой встречи.

---

# Phase 6 — Pilot Discovery
Срок: 3–5 рабочих дней совместно с заказчиком

## Нужно от заказчика
- одна предметная область;
- 5k–20k документов или репрезентативная выборка;
- 100–200 реальных вопросов;
- 2–5 предметных экспертов;
- IT owner;
- ИБ owner;
- 20–100 пилотных пользователей.

## Выход
- утверждённый Pilot Scope;
- security/data-flow схема;
- KPI baseline;
- коммерческое предложение.

---

# Phase 7 — Pilot v0.2
Срок: 2–4 недели

## Добавляем
- private document ingestion;
- базовый RBAC/ACL;
- tenant/customer separation;
- audit log;
- admin ingestion screen;
- document refresh/update;
- feedback buttons;
- telemetry;
- eval на реальных вопросах;
- deployment в согласованном белорусском контуре.

## Pilot KPI
- source retrieval >= 90%;
- citation accuracy >= 95%;
- снижение median Time-to-Verified-Answer не менее 50%;
- critical ACL leakage = 0;
- critical hallucination on protected eval = 0.

---

# Phase 8 — Production v1.0
Срок: ещё 3–6 недель

## Добавляем по необходимости
- AD/LDAP/SSO;
- enterprise RBAC/ACL sync;
- HA/backup/monitoring;
- retention policies;
- SIEM/audit export;
- disaster recovery;
- document source connectors;
- formal security review;
- load/performance testing;
- support/SLA runbook.

---

# Phase 9 — Enterprise modules
После подтверждённого спроса.

## Module A — Regulatory Change Monitor
Новый документ -> поиск затронутых внутренних документов -> отчёт.

## Module B — Document Impact Analysis
Оценка потенциального влияния нового нормативного требования.

## Module C — Conflict Detection
Поиск потенциальных противоречий между внутренними и внешними документами.

## Module D — Drafting Assistant
Подготовка проектов документов только с evidence/citations и human approval.

## Module E — Model Router
Qwen для обычного knowledge workload; более сильные reasoning/code models (включая GLM) только для дорогих/сложных задач.

---

# Команда / способ разработки

Для Demo v0.1 допустима маленькая AI-assisted команда:
- product/architecture — ChatGPT;
- implementation — Codex/Claude Code;
- review/eval/security — независимый второй агент/модель;
- человек — product owner + проверка источников/связей и приёмка.

Не тратим GitHub Actions на каждый мелкий commit. Основные тесты локально, CI — на PR/checkpoints.

---

# Главные риски сроков

1. Право на использование/полный текст нормативных документов.
2. Сильно плохое качество PDF/сканов.
3. Отсутствие нормального API у выбранного белорусского LLM-провайдера.
4. Качество metadata/version relations.
5. Желание добавить Enterprise-функции до подтверждения спроса.
6. Требования ИБ конкретного заказчика — главный источник неопределённости после demo.

---

# Что не является блокером для Demo
- отсутствие собственной GPU;
- отсутствие GLM;
- отсутствие доступа к Минэнерго;
- отсутствие 1С-интеграции;
- отсутствие миллионов документов.

---

# Практический календарь при старте 2026-08-23

## Неделя 1
Sources/legal -> corpus -> ingestion -> registry -> retrieval skeleton.

## Неделя 2
Hybrid retrieval -> reranker -> Qwen provider -> citations -> first UI -> eval loop.

## Неделя 3 (buffer/polish)
Version comparison -> hardening -> security checks -> killer demo scenarios -> meeting-ready build.

При хорошем прохождении источников и API демо может стать готовым в конце 2-й недели; 3-я неделя — резерв качества, а не обязательное ожидание.

---

# Коммерческий переход

Demo -> discovery meeting -> paid pilot -> department deployment -> enterprise rollout.

Первая встреча продаёт не enterprise contract, а доступ к Pilot Discovery и небольшой реальной выборке данных.
