# Architecture & Product Decisions — Energy Knowledge AI BY

Этот файл фиксирует решения, чтобы последующие агенты не переобсуждали базовые принципы без новых данных.

## ADR-001 — Не обучаем собственную foundation model

**Решение:** использовать готовую LLM, предпочтительно доступную у белорусского провайдера.

**Почему:** корпоративные знания меняются быстрее, чем имеет смысл переобучать веса. Основная задача решается retrieval + RAG.

## ADR-002 — LLM является заменяемым компонентом

**Решение:** backend не должен зависеть от одной конкретной модели/провайдера.

**Следствие:** предусмотреть model adapter interface. Первый кандидат — Qwen у белорусского провайдера; позже можно подключать GLM/другие модели.

## ADR-003 — Retrieval quality важнее размера LLM

**Решение:** сначала добиться качественного hybrid retrieval, metadata filters и reranking, затем подключать генерацию.

## ADR-004 — No source, no confident answer

**Решение:** если система не нашла достаточных подтверждений, она должна отказаться от уверенного ответа.

## ADR-005 — Citations are mandatory

**Решение:** каждый существенный вывод должен быть связан с конкретным источником/фрагментом.

## ADR-006 — Version awareness is core product functionality

**Решение:** хранить статус и связи редакций документов с первых версий продукта, а не добавлять это позже как косметическую функцию.

## ADR-007 — Не строим новую СЭД

**Решение:** продукт является AI/knowledge layer поверх существующих СЭД, 1С, файловых серверов и баз.

## ADR-008 — Не покупаем GPU до появления подтверждённой нагрузки

**Решение:** MVP и первые пилоты использовать LLM/GPU-инфраструктуру белорусских провайдеров. Dedicated/on-premise GPU появляется только при коммерческой необходимости.

## ADR-009 — Public demo before enterprise integration

**Решение:** сначала создать демонстрационный продукт на легально доступных отраслевых документах, затем идти на discovery в Минэнерго/ГПО «Белэнерго».

## ADR-010 — First meeting goal is discovery

**Решение:** цель первой встречи — определить самую ценную AI-задачу и контур пилота, а не продавать заранее весь Enterprise Knowledge AI.

## ADR-011 — Security must be architectural

Enterprise-фаза:

- ACL/RBAC применяется до передачи контекста LLM;
- audit log обязателен;
- минимальные привилегии;
- данные клиента не используются для обучения внешних моделей без явного разрешения;
- вариант полностью закрытого контура должен оставаться архитектурно возможным.

## ADR-012 — Build narrow vertical slice first

Первая сквозная цепочка:

```text
public document
→ ingestion
→ registry
→ hybrid search
→ reranker
→ LLM
→ citation
→ web UI
```

Не строить заранее agents, 1С/СЭД connectors, сложный model router и полный enterprise security stack.

## ADR-013 — Primary product metric

Основная продуктовая метрика: **Time-to-Verified-Answer**.

Дополнительно измерять cost per verified answer (стоимость подтверждённого ответа), retrieval recall, citation accuracy и abstention accuracy.

## ADR-014 — Product ownership split

Архитектурно разделять:

- `Enterprise Knowledge Core` — универсальное ядро;
- `Energy Pack` — энергетическая онтология, metadata, evals и сценарии;
- `Customer adapters` — интеграции и конфигурации конкретного заказчика.
