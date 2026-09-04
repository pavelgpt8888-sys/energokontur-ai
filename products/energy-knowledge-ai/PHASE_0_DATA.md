# Phase 0 — Data, Sources, Trust and Evaluation

## Objective
Build the trusted data foundation for Energy Knowledge AI BY before UI or model polish.

## Core principle
The system may use AI to discover, classify, extract and compare documents, but authoritative facts such as document status, effective date and replacement relationships must be backed by a trusted source **and approved by a responsible curator before publication into the trusted knowledge base**.

The product must distinguish between:
- discovered candidate;
- parsed candidate;
- awaiting review;
- approved;
- published trusted record.

## Workstreams

### 1. Source registry
Create a whitelist of approved public sources for the first demo.
For each source store:
- source_id
- organization
- base_url
- source_type
- trust_level
- crawl_allowed
- full_text_storage_allowed
- metadata_only
- update_frequency
- notes

Initial target categories:
- Ministry of Energy of the Republic of Belarus
- official/legal publication sources
- sector normative-document portals
- Belenergo public materials
- public pages of energy organizations

### 2. Candidate discovery
Build an optional crawler/parser pipeline that helps the curator:
1. checks approved sources;
2. detects new or changed documents;
3. stores URL, checksum and retrieval timestamp;
4. downloads permitted content or stores metadata/link only;
5. queues documents for parsing;
6. creates a candidate record but **does not publish it automatically**.

Automatic discovery is an assistant function. It is not the authority for the production knowledge base.

### 3. Document processing
For every candidate document:
- extract text;
- OCR only if needed;
- preserve headings, sections, clauses, tables and page references where possible;
- extract candidate metadata using deterministic parsing + LLM-assisted extraction;
- create chunks with structural context;
- prepare a curator-friendly review card.

### 4. Trust validation and human approval
LLM extraction is a proposal, not authority.

Fields requiring source-backed validation:
- document number;
- title;
- issuer;
- publication date;
- effective_from;
- effective_to;
- active/replaced/expired status;
- replaces/replaced_by relationships.

Review policy:
- direct trusted evidence -> pre-fill candidate values;
- conflicting evidence -> flag conflict;
- no authoritative evidence -> unknown;
- curator/support reviewer confirms or corrects fields;
- only approved records become available to trusted RAG answers.

No `active`, `replaced`, `expired`, `replaces`, `replaced_by` status becomes trusted solely because an LLM inferred it.

### 5. Content roles
Minimum roles for v0.1/v0.2:

#### Content Curator (ответственный за нормативную базу)
Can:
- upload/add document;
- review discovered candidate;
- edit metadata;
- set validity/effective dates;
- link versions;
- approve/reject publication;
- archive/supersede a record;
- see audit history.

#### Support Operator (сотрудник поддержки)
Optional managed-service role. Can prepare updates and review candidates according to customer policy.

#### Reader (пользователь)
Can search and ask questions only against published trusted content.

### 6. Document Registry
Minimum schema:
- document_id
- title
- document_type
- number
- issuer
- publication_date
- effective_from
- effective_to
- status: active|replaced|expired|unknown
- workflow_status: candidate|parsed|awaiting_review|approved|published|rejected|archived
- previous_version_id
- next_version_id
- replaces_ids[]
- amended_by_ids[]
- source_url
- source_id
- source_hash
- retrieved_at
- access_level
- topic_tags[]
- raw_file_ref
- parsed_text_ref
- reviewed_by
- reviewed_at
- published_by
- published_at

### 7. Version graph
Maintain explicit relations:
- replaces
- replaced_by
- amends
- amended_by
- based_on
- references

Relations proposed by AI remain candidates until curator approval.

The graph must be queryable before generation so outdated documents can be filtered or clearly marked.

### 8. Initial data population
For the first product version:
- populate the open normative base from trusted public sources as far as legally allowed;
- use automation to accelerate discovery and parsing;
- perform curator review before records are marked trusted/published;
- prioritize document quality and currentness over raw volume.

Initial target: hundreds to several thousand metadata records, depending on accessible open sources and review throughput.

### 9. Eval set
Create 30–50 questions for v0.1:
- 10 exact document retrieval;
- 10 semantic retrieval;
- 10 current-vs-old version questions;
- 5–10 multi-source questions;
- 5–10 unanswerable questions.

Store for each question:
- query
- expected_document_ids
- expected_status
- key evidence
- answerable boolean
- severity if wrong

### 10. Acceptance criteria for Phase 0
- source registry exists;
- trusted records are separated from unapproved candidates;
- curator can approve/reject/update a candidate;
- duplicate detection works by checksum/canonical identity;
- version/status fields are never invented without evidence and approval;
- at least 30 eval questions exist;
- every record retains provenance to its source;
- every publication/change retains reviewer identity and timestamp;
- legal/storage restrictions are recorded per source.

## Deliverables
- `data/source_registry.*`
- `data/document_registry.*`
- candidate discovery/parser skeleton
- curator review workflow
- trust-validation rules
- version graph schema
- first reviewed dataset
- eval dataset
- ingestion/review audit log

## Non-goals
- fully autonomous publication of normative changes;
- production ACL beyond the initial content roles;
- 1C/SED connectors;
- enterprise SSO;
- autonomous agents;
- GLM integration;
- large-scale crawling outside approved sources.

## Definition of done
Phase 0 is complete when the team can demonstrate that a new public energy document can be discovered or manually added, parsed into a candidate, reviewed by a responsible person, published into the trusted registry, linked to its source/version history, and then used in a repeatable retrieval evaluation.
