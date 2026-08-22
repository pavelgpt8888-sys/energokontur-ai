# Roadmap — Energy Knowledge AI BY

## Phase 0 — Discovery & source audit

Цель: подтвердить, что демонстрационную базу можно собрать легально и достаточно качественно.

- [ ] составить список публичных энергетических источников Беларуси;
- [ ] классифицировать права использования: full text / metadata only / link only;
- [ ] собрать первые 100–300 документов/карточек;
- [ ] определить типы документов и обязательные metadata;
- [ ] собрать 30–50 реальных demo questions;
- [ ] проверить предложения белорусских LLM/GPU-провайдеров и API.

## Phase 1 — Retrieval prototype

Цель: научиться надёжно находить правильный документ без генеративного слоя.

- [ ] parser pipeline;
- [ ] OCR integration для сканов;
- [ ] document registry;
- [ ] structural chunking;
- [ ] keyword/BM25 search;
- [ ] vector search;
- [ ] hybrid retrieval;
- [ ] reranker;
- [ ] metadata/version filters;
- [ ] retrieval evals.

**Gate:** правильный источник в top results ≥90% на контрольной выборке.

## Phase 2 — Answering & citations

- [ ] интеграция Qwen/другой LLM белорусского провайдера;
- [ ] context builder;
- [ ] grounded-answer prompt;
- [ ] citation mapping;
- [ ] citation validator;
- [ ] abstention logic;
- [ ] answer evals.

**Gate:** citation accuracy ≥95%, система не отвечает уверенно без доказательств.

## Phase 3 — Demo web app

- [ ] авторизация demo-user;
- [ ] экран «Спросить»;
- [ ] «Найти документ»;
- [ ] карточка источника;
- [ ] статус документа;
- [ ] «Сравнить редакции»;
- [ ] «Что изменилось»;
- [ ] базовый audit log;
- [ ] подготовка демонстрационных сценариев.

**Gate:** 15-минутный показ работает без ручного вмешательства разработчика.

## Phase 4 — Ministry / Belenergo discovery

Цель встречи: не продавать весь Enterprise, а определить лучший первый пилот.

- [ ] показать public demo;
- [ ] выявить 3 главные AI-задачи;
- [ ] понять существующие СЭД/1С/БД и владельцев данных;
- [ ] определить ограничения ИБ;
- [ ] выбрать подразделение/процесс;
- [ ] получить 100–200 реальных вопросов;
- [ ] согласовать критерии успешного пилота.

## Phase 5 — Customer pilot

Ориентир:

- 5 000–20 000 документов;
- 50–100 пользователей;
- одна предметная область;
- 2–5 предметных экспертов;
- измеримый baseline по времени поиска.

Добавить:

- [ ] customer ingestion;
- [ ] SSO/LDAP при необходимости;
- [ ] RBAC/ACL;
- [ ] закрытое размещение;
- [ ] enterprise audit;
- [ ] feedback loop;
- [ ] pilot analytics.

## Phase 6 — Enterprise rollout

- [ ] connectors к СЭД;
- [ ] connectors к 1С;
- [ ] file-server connectors;
- [ ] version graph;
- [ ] regulatory change monitoring;
- [ ] impact analysis;
- [ ] conflict detection;
- [ ] SLA/monitoring;
- [ ] multi-department rollout.

## Phase 7 — Advanced AI

Только после подтверждённого спроса:

- [ ] model router;
- [ ] GLM/другая сильная open-weight модель для тяжёлого анализа/coding;
- [ ] workflow agents;
- [ ] safe actions with human approval;
- [ ] отраслевые аналитические сценарии.

## Productization rule

Каждая клиентская доработка оценивается как:

1. universal core — должна попасть в Enterprise Knowledge Core;
2. energy-specific — должна попасть в Energy Pack;
3. customer-specific — остаётся адаптером/конфигурацией клиента.

Цель: от 60% custom / 40% product у первого клиента перейти к 10–20% custom / 80–90% product после серии внедрений.
