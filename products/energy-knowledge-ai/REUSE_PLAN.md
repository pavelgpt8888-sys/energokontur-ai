# Reuse Plan — Energy Knowledge AI BY

## Donor project

Private repository: `pavelgpt8888-sys/book-dialogue-rag`.

The donor already contains a FastAPI/Docker/PostgreSQL+pgvector-oriented RAG skeleton with separated modules for API, ingestion, retrieval, generation, monitoring and security.

## Reuse, do not duplicate

Candidate components to inspect and adapt:

- application bootstrap / FastAPI health and config;
- Docker / Dokploy deployment pattern;
- database/session configuration;
- ingestion interfaces;
- retrieval interfaces;
- generation provider abstraction;
- validation / no-answer behavior;
- monitoring hooks;
- test structure and static checks.

## Energy-specific new work

Must be implemented specifically for this product:

- `energodoc.by` source adapter;
- `minenergo.gov.by` source adapter;
- `energystrategy.by` source adapter;
- legal/access classifier (`public_fulltext`, `metadata_only`, etc.);
- document registry schema;
- version/relation graph;
- hybrid BM25 + vector retrieval;
- metadata/date/status filters;
- citation resolver to exact source/card/page/section;
- regulatory change detector;
- energy eval dataset;
- web UI for Ask / Find document / Compare / What changed.

## Rule

Copying code is not automatic. Each donor component must be reviewed for fit, tests and licensing/ownership. Prefer extraction into a reusable internal core rather than maintaining two diverging copies when practical.
