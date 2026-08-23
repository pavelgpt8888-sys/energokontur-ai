# Source Registry — Energy Knowledge AI BY

## Purpose

This registry defines trusted and candidate sources for the Phase 0 ingestion pipeline.

Critical rule: LLM output is never authoritative by itself. Status (`active`, `replaced`, `expired`), effective dates, amendment/replacement relationships and legal applicability require evidence from a trusted source. If evidence is insufficient, store `unknown` and route to review.

## Tier A — trusted metadata / provenance sources

### energystrategy.by / ОАО «Экономэнерго»

**Role:** primary structured source for metadata on energy-sector technical normative documents (ТКП and related publications), including approval act, effective date, replacement relationships and amendment information.

**Observed useful fields:**
- document title;
- document number;
- issuing authority;
- approval act number/date;
- effective date;
- `взамен` / replaced-document relationship;
- explicit cancellation notices;
- amendment / reissue information;
- subject/category;
- source page URL.

**Important limitation:** many official technical normative texts have reproduction/distribution restrictions. For public demo, treat this source primarily as a trusted metadata/provenance registry unless storage/use rights to the full text are confirmed.

**Automation strategy:**
1. Crawl normative catalog and news/update posts.
2. Detect newly published/reissued documents.
3. Extract metadata deterministically where possible.
4. Use LLM only for normalization/classification and candidate relation extraction.
5. Validate critical relations against explicit source phrases such as `ВЗАМЕН`, `ОТМЕНЕН`, `с учетом Изменения`, `вступает в силу`.
6. Persist source URL + retrieval timestamp + evidence text hash.

**Examples confirmed during research:**
- ТКП 290-2026: approved by Ministry of Energy resolution No. 15 of 15.05.2026; effective 17.08.2026; replaces ТКП 290-2023; separate publication explicitly says the 2023 document is cancelled from 17.08.2026.
- ТКП 427-2022: reissued with Amendment No. 1 approved 30.12.2024; amendment effective 10.03.2025.
- ТКП 339-2022: reissued with Amendment No. 1 approved 21.05.2025; effective 01.08.2025.
- ТКП 608-2025: effective 01.04.2025; replaces ТКП 608-2017.

## Tier A candidates requiring connector verification

### Ministry of Energy of the Republic of Belarus

**Desired role:** authoritative source for ministry resolutions, official notices, sector policy and public documents.

**Status:** candidate; direct crawler endpoints and stable index paths still need discovery/verification.

**Target fields:**
- act number/date;
- title;
- publication date;
- effective date;
- linked attachments;
- amendment/repeal information;
- official URL.

### National legal information system / official legal publication source

**Desired role:** authoritative confirmation for legal acts and effective dates that govern or amend energy-sector documents.

**Status:** candidate; automatic-access mechanism and licensing/usage conditions need verification.

## Tier B — sector / enterprise sources

### ГПО «Белэнерго»

**Desired role:** public standards, notices, technical publications and later — customer-provided internal standards during pilot.

**Status:** public-source structure still to be mapped. Internal content must only be ingested under customer authorization and ACL.

### Customer internal systems

Examples: 1С:Документооборот, СЭД, shared folders, databases, internal portals.

**Role:** pilot/enterprise knowledge layer.

**Rule:** no crawling without explicit customer authorization. Preserve original ACL and provenance.

## Document trust model

Each document record must include:

- `document_id`
- `title`
- `document_type`
- `number`
- `issuer`
- `approval_date`
- `effective_from`
- `effective_to`
- `status` (`active`, `replaced`, `expired`, `unknown`)
- `replaces[]`
- `replaced_by[]`
- `amendments[]`
- `source_url`
- `source_tier`
- `retrieved_at`
- `evidence_hash`
- `rights_mode` (`metadata_only`, `fulltext_allowed`, `customer_authorized`, `unknown`)
- `validation_state` (`verified`, `needs_review`, `unknown`)

## Rights / storage policy for demo

Before storing full text, classify each source/document:

1. **metadata_only** — keep metadata, public excerpt where lawful, link to source;
2. **fulltext_allowed** — full text may be stored/indexed under confirmed terms;
3. **customer_authorized** — full text supplied by customer for internal processing;
4. **unknown** — do not ingest full text until reviewed.

## Phase 0 next actions

1. Build source adapter for `energystrategy.by` catalog + update posts.
2. Create `source_registry` and `documents` schemas.
3. Ingest first 100 trusted metadata records.
4. Build deterministic rules for `ВЗАМЕН`, `ОТМЕНЕН`, `с учетом Изменения`, effective-date extraction.
5. Add LLM-assisted normalization with confidence + evidence trace.
6. Create 30+ retrieval/versioning eval questions.
7. Map Ministry of Energy and Belenergo public endpoints.
8. Only after stable ingestion: connect embeddings, hybrid retrieval and Qwen.
