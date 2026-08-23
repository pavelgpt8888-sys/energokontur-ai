# Phase 0 — Data, Sources, Trust and Evaluation

## Objective
Build the trusted data foundation for Energy Knowledge AI BY before UI or model polish.

## Core principle
The system may use AI to discover, classify, extract and compare documents, but authoritative facts such as document status, effective date and replacement relationships must be backed by a trusted source.

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

### 2. Automated discovery
Build a crawler/parser pipeline that:
1. checks approved sources;
2. detects new or changed documents;
3. stores URL, checksum and retrieval timestamp;
4. downloads permitted content or stores metadata/link only;
5. queues documents for parsing.

### 3. Document processing
For every document:
- extract text;
- OCR only if needed;
- preserve headings, sections, clauses, tables and page references where possible;
- extract candidate metadata using deterministic parsing + LLM-assisted extraction;
- create chunks with structural context.

### 4. Trust validation
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

Validation policy:
- high-confidence + direct official evidence -> auto-accept;
- conflicting evidence -> human review queue;
- no authoritative evidence -> unknown, never guessed.

### 5. Document Registry
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

### 6. Version graph
Maintain explicit relations:
- replaces
- replaced_by
- amends
- amended_by
- based_on
- references

The graph must be queryable before generation so outdated documents can be filtered or clearly marked.

### 7. Demo dataset
Phase 0 target:
- first checkpoint: 100 trusted documents/records;
- demo target: 300–1,000 records/documents depending on legal availability;
- prioritize quality and version relationships over raw volume.

### 8. Eval set
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

### 9. Acceptance criteria for Phase 0
- source registry exists;
- at least 100 trusted records ingested;
- duplicate detection works by checksum/canonical identity;
- version/status fields are never invented without evidence;
- at least 30 eval questions exist;
- every record retains provenance to its source;
- legal/storage restrictions are recorded per source.

## Deliverables
- `data/source_registry.*`
- `data/document_registry.*`
- crawler/parser skeleton
- trust-validation rules
- version graph schema
- first trusted dataset
- eval dataset
- ingestion audit log

## Non-goals
- production ACL;
- 1C/S ED connectors;
- enterprise SSO;
- complex UI;
- autonomous agents;
- GLM integration;
- large-scale crawling outside approved sources.

## Definition of done
Phase 0 is complete when the team can demonstrate that a new public energy document can be discovered, parsed, registered, linked to its source, assigned a validated status or `unknown`, and used in a repeatable retrieval evaluation without manual reconstruction of the pipeline.
