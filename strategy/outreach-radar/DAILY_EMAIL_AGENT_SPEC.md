# Outreach Radar — Daily Personalised Email Agent

Date: 2026-09-29. Status: product/specification draft. This is a **research + drafting agent**, not an autonomous bulk-mailer.

## Goal

Every workday produce a small batch of high-quality outreach opportunities where each message is tied to:
1. a real company signal;
2. a specific role / likely decision-maker;
3. one plausible business-process problem;
4. one bounded diagnostic CTA.

The agent must **not** lead with "AI", "n8n", "agents", "automation platform" or generic transformation language. It sells a conversation around a business problem.

## Daily pipeline

1. **Account discovery**
   - Find 5–15 target companies from approved sources: B2B directories, 1C implementation registry, official company pages, vacancies, procurement notices, project/news pages and manually approved lists.
   - Record source links and date.

2. **Qualification**
   - Segment: manufacturing / industrial distribution / EPC-construction / industrial service / energy-adjacent.
   - Estimate fit on:
     - problem intensity;
     - repeatability;
     - budget-owner accessibility;
     - visible digital trigger;
     - likely economic effect;
     - integration complexity.
   - If evidence is weak, mark `LOW_CONFIDENCE`; do not draft a personalized factual claim.

3. **Pre-discovery brief**
   - What the company sells.
   - Likely customer type.
   - Observed trigger ("new ERP", hiring, expansion, tender activity, product complexity, multi-site operation, etc.).
   - 1–3 **HYPOTHESES**, clearly marked as hypotheses.
   - Likely decision-maker role.
   - One process to discuss first.

4. **Draft outreach message**
   - One personalized email per selected account.
   - 70–130 words.
   - One subject line + one alternate.
   - First sentence must contain a real company-specific observation or neutral context; never fabricated praise.
   - Second paragraph: one **hypothesis**, not a claim.
   - CTA: 15–20 minute diagnostic conversation.
   - No attachment on first touch.
   - No invented case study, metric, customer or relationship.

5. **Human approval**
   - Default status is `DRAFT_REVIEW_REQUIRED`.
   - No sending until a human approves recipient, message and source evidence.
   - Later automation of sending must be a separate explicit decision.

6. **Response / learning loop**
   - Track: sent, opened if lawfully available, replied, positive, negative, wrong person, later, no need, existing vendor, no budget, security/data objection.
   - Update hypothesis and wording weekly.
   - Never infer demand from opens alone.

## Message anatomy

### Subject
Short, specific, non-marketing:
- `[Компания]: вопрос по обработке технических запросов`
- `Вопрос по КП и передаче данных в 1С`
- `[Компания]: где теряется время между заявкой и заказом?`

Avoid:
- "AI для вашего бизнеса"
- "Увеличим прибыль на 30%"
- "Революционная автоматизация"
- fake "Re:" / fake internal thread subjects.

### Body structure
1. **Why you / why now** — one verifiable observation.
2. **Problem hypothesis** — "В компаниях с похожим процессом часто..."
3. **Diagnostic value** — what we can map in 15–20 min.
4. **Low-friction CTA** — ask if relevant / who owns this process.

## Drafting rules

- Russian by default for Belarus prospects unless recipient/company context suggests another language.
- Use recipient's name only when verified.
- Do not write "я изучил вашу компанию" if only one landing page was read.
- Do not say "у вас проблема" without direct evidence. Say "хочу проверить гипотезу".
- Prefer process vocabulary of the company: `КП`, `ПТО`, `снабжение`, `заявка`, `1С`, `CRM`, `исполнительная документация`, etc.
- One email = one pain hypothesis.
- No technology stack unless recipient asks.
- No AI in subject; usually no AI in the first message at all.
- Never promise percentage ROI before baseline.
- Use a concrete diagnostic CTA, not "давайте созвонимся обсудить сотрудничество".

## Output schema for each account

```yaml
company:
company_url:
segment:
source_urls:
signal:
signal_confidence: HIGH | MEDIUM | LOW
decision_maker_role:
decision_maker_name: null | verified name
process_hypothesis:
why_now:
business_metric_to_test:
offer:
subject_1:
subject_2:
email_body:
followup_1:
followup_2:
status: DRAFT_REVIEW_REQUIRED
research_notes:
```

## Initial email template logic

**Do not copy-paste unchanged.** Agent must regenerate from evidence.

Здравствуйте, [Имя].

Увидел, что [проверяемый факт/сигнал о компании]. Хочу проверить одну гипотезу: в компаниях, где [описание процесса], часть времени часто уходит на [ручной переход / ожидание / сверку / подготовку документов].

Если у вас это тоже актуально, могу за 20 минут вместе с вами разложить процесс [точка А → точка Б] и посмотреть, где реально теряются время, заявки или маржа. Без презентации AI и без обязательств по внедрению.

Есть смысл обсудить, или этим у вас занимается другой человек?

Павел

## Follow-up logic

### Follow-up 1 — after ~3 business days
- 35–70 words.
- Add one new useful observation or a sharper question.
- Do not write "Вы видели моё письмо?" alone.

### Follow-up 2 — after ~7–10 business days
- Close the loop politely.
- Ask whether the topic is irrelevant, handled internally, or better revisited later.
- Do not guilt or pressure recipient.

## Daily brief to Pavel

Every morning produce:

```
OUTREACH RADAR — YYYY-MM-DD

Ready for review: N
High-confidence: N
Medium-confidence: N
Not ready / insufficient evidence: N

1. COMPANY
   - Why now:
   - Decision-maker:
   - Pain hypothesis:
   - Evidence:
   - Email:
   - Follow-up 1:
   - Follow-up 2:
   - Recommended action: EMAIL / CALL / RESEARCH_MORE

...
```

Limit to **10 ready-to-contact accounts/day** in the first phase. Quality is more important than volume.

## A/B tests

Test only one variable at a time:
- problem-led subject vs role/process-led subject;
- ask "есть ли это у вас?" vs "кто отвечает за этот процесс?";
- 80-word vs 120-word body;
- first touch email vs phone after evidence-based pre-brief.

Track response/meeting rate by segment, pain and trigger. Do not optimise on vanity metrics.

## First three outreach offers

### A. Technical Quote / Revenue Process
For industrial manufacturers/distributors:
`incoming RFQ → engineer verification → supplier/current price → approved quote → CRM/ERP → order/payment exception`.

### B. Project Margin & Evidence
For EPC/construction/installation:
`scope/tender → project → field changes → evidence → extra work → acts → payment/margin`.

### C. Process Hand-offs Around 1C/ERP
For manufacturers:
`email/Excel/CRM/1C/approvals` where the same data is manually copied or exceptions are invisible.

## Safety / trust guardrails

- Respect applicable communication/privacy rules and recipient opt-outs.
- Keep source provenance.
- No deceptive identity, fake client, fake referral, fabricated trigger or synthetic personal detail.
- No sensitive personal profiling.
- No autonomous mass sending in v1.
- If an account asks not to be contacted, put it on suppression list.
- Store only the minimum business-contact data needed for outreach.

## Success metric

Primary: **qualified conversations with a confirmed costly process**, not number of emails.

Secondary:
- positive reply rate;
- meeting booked rate;
- qualified pain rate;
- paid diagnostic/pilot conversion;
- segment/pain repeatability.

Final goal: discover which problem buyers repeatedly pay to solve, then productize that process.
