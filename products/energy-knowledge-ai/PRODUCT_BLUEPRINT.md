# Product Blueprint v0.1 — Energy Knowledge AI BY

## 1. Product thesis

Energy Knowledge AI BY — интеллектуальный слой над существующими корпоративными и отраслевыми источниками знаний. Он не заменяет СЭД (систему электронного документооборота), 1С, файловые серверы или нормативные базы, а даёт единое окно поиска и анализа с доказательными ссылками на первоисточники.

## 2. Problem

В энергетических организациях знания распределены между нормативными актами, ТКП, инструкциями, приказами, СЭД, 1С, файловыми хранилищами, внутренними порталами и экспертами. Сотрудник часто знает, что «такой документ существует», но тратит время на поиск актуальной редакции и нужного пункта.

## 3. Core outcome

Сократить Time-to-Verified-Answer (время до подтверждённого ответа):

вопрос → релевантный действующий документ → точный пункт/страница → краткий ответ → ссылка на первоисточник.

## 4. First ICP

Первый целевой контур:

- Министерство энергетики Республики Беларусь — discovery и отраслевые задачи;
- ГПО «Белэнерго» — отраслевой/управленческий уровень;
- энергопредприятия — корпоративное внедрение на внутренних документах.

## 5. MVP capabilities

- natural-language Q&A (вопросы обычным языком);
- точный поиск по номеру/дате/названию;
- semantic search (поиск по смыслу);
- hybrid search (точный + смысловой поиск);
- reranking (повторное ранжирование);
- RAG;
- citations (ссылки на источник);
- реестр документов и статус редакции;
- compare revisions (сравнение редакций);
- abstention (отказ от ответа при недостатке доказательств).

## 6. Future enterprise capabilities

- connectors к СЭД, 1С, файловым серверам и БД;
- RBAC/ACL (ролевое и объектное разграничение доступа);
- audit log (журнал действий);
- version graph (граф версий и замен документов);
- regulatory change monitor (мониторинг изменений нормативной базы);
- impact analysis (какие внутренние документы затронуты новым НПА/ТКП);
- conflict detection (поиск потенциальных противоречий);
- drafting assistant (подготовка проектов документов только с подтверждаемыми источниками);
- AI agents (агенты) для последующих безопасных workflow.

## 7. Architecture

```text
User
  ↓
Web UI
  ↓
Authentication
  ↓
Query Router
  ↓
Hybrid Search
  ├─ BM25 / keyword
  ├─ vector search
  └─ metadata filters
  ↓
Reranker
  ↓
Version / validity filter
  ↓
ACL filter (enterprise phase)
  ↓
Context builder
  ↓
LLM from Belarus provider
  ↓
Citation validator
  ↓
Answer + sources
```

## 8. Model strategy

LLM не является ядром продукта.

Базовый слой: Qwen или аналогичная open-weight модель, доступная у белорусского провайдера.

Позже model router (маршрутизатор моделей) может направлять тяжёлый анализ или coding-задачи в GLM/другую сильную open-weight модель при наличии экономического смысла.

## 9. Data model

Минимальная карточка документа:

- document_id;
- title;
- type;
- number;
- issuer;
- date;
- effective_from;
- effective_to;
- status: active / superseded / expired / draft;
- replaces_document;
- replaced_by;
- version;
- source;
- source_url/path;
- access_level;
- checksum;
- ingestion_timestamp.

## 10. Trust rules

1. Нет источника — нет уверенного ответа.
2. Каждое существенное утверждение должно иметь citation.
3. Устаревшие документы не должны автоматически считаться действующими.
4. В enterprise-фазе ACL применяется до передачи контекста LLM.
5. Все ответы должны быть воспроизводимы через audit trail (журнал трассировки).

## 11. Pilot hypothesis

Первый настоящий пилот:

- 1 подразделение/предметная область;
- 5 000–20 000 документов;
- 50–100 пользователей;
- 100–200 реальных вопросов;
- 2–5 предметных экспертов;
- измерение Time-to-Verified-Answer до/после.

Ориентир коммерческой гипотезы пилота: 15–30 тыс. BYN после discovery. Цена не фиксируется до понимания реального объёма и требований ИБ.

## 12. Product economics hypothesis

Доход:

- implementation fee (внедрение);
- annual/monthly platform license (лицензия платформы);
- infrastructure pass-through/markup (инфраструктура);
- connectors;
- advanced modules;
- support/SLA.

Целевой долгосрочный COGS (прямые затраты) — примерно 25–35% выручки сервиса при зрелой платформе; целевая gross margin (валовая маржинальность) — 65–75%. Это гипотеза, подлежащая проверке на тарифах белорусских провайдеров и реальной нагрузке.

## 13. Strategic moat

Защитное преимущество продукта строится не на конкретной LLM, а на:

- качестве ingestion pipeline;
- реестре и версиях документов;
- citations;
- hybrid retrieval;
- evaluation dataset;
- отраслевых metadata и ontology;
- connectors;
- security architecture;
- накопленных шаблонах внедрений.

## 14. North-star metric

**Time-to-Verified-Answer** — время от вопроса пользователя до проверяемого ответа с первоисточником.

Дополнительные метрики:

- retrieval recall;
- citation accuracy;
- answer accuracy;
- abstention accuracy;
- latency;
- cost per verified answer;
- user success rate.

## 15. Productization path

```text
Energy Knowledge Demo
↓
Energy Pilot
↓
Enterprise Knowledge Core
+ Energy Pack
↓
Belenergo / energy enterprises
↓
другие вертикали: industrial / banking / construction / government
```
