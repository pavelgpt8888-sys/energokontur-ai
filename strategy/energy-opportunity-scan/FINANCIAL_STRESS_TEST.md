# Financial stress test: service-led vs low-ticket SaaS vs enterprise product

Date: 2026-09-29. Currency: BYN. Horizon: first 12 months. **All sales quantities, prices, costs and conversion assumptions are scenarios, not observed Belarus market rates or projections.**

## Objective

Find a business model that can pay for delegated development/delivery, the founder's commercial work and its own support. A large gross sector turnover is irrelevant unless the specific buyer can approve an economically justified engagement.

### Reproducible formulas
- Audit revenue = # audits × price.
- Pilot revenue = # pilots × price.
- Managed revenue = average active accounts × monthly fee × active billed months.
- Revenue = audit + pilot + managed.
- Delivery cost = 30% audit revenue + 50% pilot revenue + 40% managed revenue.
- Sales/marketing = 8% of total sales.
- Conditional tax placeholder = 6% of total sales **only for modeling**. Belarus tax treatment, VAT, regime and payroll require accountant verification; do not quote 6% as guaranteed eligibility or actual tax liability.
- Fixed cost varies by scenario.
- Cash profit before founder = revenue – delivery – sales – conditional tax – fixed.
- Economic profit = cash profit – 48,000 BYN/year valuation of founder time (4,000/month, assumption; not necessarily an actual cash expense).

## Scenario inputs and results

| Variable | Conservative | Base | Stretch |
| --- | ---: | ---: | ---: |
| Audits: quantity × price | 4 × 8,000 | 8 × 10,000 | 12 × 12,000 |
| Pilots: quantity × price | 2 × 12,000 | 4 × 20,000 | 6 × 30,000 |
| Managed: avg accounts × price × months | 2 × 1,000 × 6 | 4 × 2,000 × 6 | 7 × 3,000 × 6 |
| **Revenue** | **68,000** | **208,000** | **450,000** |
| Delegated delivery (30/50/40%) | 26,400 | 83,200 | 183,600 |
| Sales 8% | 5,440 | 16,640 | 36,000 |
| Conditional tax placeholder 6% | 4,080 | 12,480 | 27,000 |
| Fixed expenses | 14,000 | 24,000 | 36,000 |
| **Cash profit pre-founder** | **18,080** | **71,680** | **167,400** |
| Founder opportunity cost | 48,000 | 48,000 | 48,000 |
| **Economic profit post-founder** | **−29,920** | **23,680** | **119,400** |

**Check arithmetic:** base = 80k audit + 80k pilot + 48k managed = 208k; subtract 83.2k delivery, 16.64k sales, 12.48k conditional tax and 24k fixed = 71.68k; subtract 48k founder time = 23.68k.

### Critical sensitivity

With the above delivery mix, simplified blended contribution after delivery/sales/placeholder tax ≈46% (varies with actual mix). For fixed cost of 24k/year:
- To **cover business fixed cost plus founder time at 4k/month**, indicative revenue threshold = (24k + 48k)/0.46 ≈ **156,522 BYN/year**, or **13,043 BYN/month**.
- To **fund 10k/month founder compensation** plus 24k fixed, before any unmodeled pay taxes, capital return or working-capital buffer: (24k + 120k)/0.46 ≈ **313,043 BYN/year**, or **26,087 BYN/month**.

This is more useful than saying «SaaS has unlimited scale»: we now have a specific revenue gate and can count how many audits, pilots and retainers are needed.

### Low-ticket standalone SaaS counterexample

Hypothetical vertical SaaS: 60 customers × 100 BYN × average 7 billed months in Year 1 = 42k BYN revenue.

Illustrative direct onboarding = 60 × 150 = 9k; infra = 7.2k; fixed = 12k; selling cost 8% = 3.36k; conditional tax 6% = 2.52k.

Result = **7,920 BYN cash before founder time**, and **−40,080 BYN after founder-time valuation**. Crucially, customer acquisition cost, implementation variation, churn and support may be worse than these assumptions. A 100-BYN subscription requires volume and a cheap distribution channel.

At steady state with contribution 70% and 10k BYN/month fixed cost, break-even customers:
- ARPA 100: 143 accounts;
- ARPA 300: 48 accounts;
- ARPA 2,500: 6 accounts.
Acquisition and one-time costs are not included. This is a mathematical illustration, not actual price discovery.

### Enterprise product counterexample: Energy Knowledge AI BY

Year 1 hypothesis: 2 pilots × 25k + 1 initial annual contract × 30k = 80k revenue.
Development 45k; security/data 15k; infra 9k; COGS/support 25% revenue = 20k; sales 8% = 6.4k; conditional tax 6% = 4.8k.
= **−20,200 BYN cash before founder** and **−68,200 BYN after 48k opportunity cost**.

If a real design partner prepays a pilot or funds data/security integration, the profile changes materially. Do not commit enterprise development solely because an LLM demo works.

## Which vertical can support higher engagement value?

Market hypothesis, subject to buyer quotes:
- Industrial manufacturers, distributors and project contractors can attach an audit/pilot to a measurable cost/profit pool (margin, cash, procurement, uptime); commercial trial ranges in `CROSS_VERTICAL_MARKET_SCAN.md`.
- Banks/insurers/utilities may pay much larger enterprise contracts but need longer pre-sales, vendor onboarding and compliance. Contract size alone is not founder cash.
- Micro-SMB recurring documentation products can be profitable via a partner channel/white-label or full managed service, not necessarily as independent 50–100 BYN SaaS.

## WTP and investment gates

Before funding any product, secure:
1. Baseline of the process from real transaction samples;
2. buyer with budget and responsibility for the measured KPI;
3. at least 2 paid scopes with a repeatable structure;
4. clear implementation cost (time of AI agents is not zero: supervision, review, QA, infrastructure);
5. buyer-approved access and security/data flows;
6. measured post-launch cost-to-serve and willingness to renew.

Model should be re-run with accountant-validated taxes and signed buyer prices before using it in any investment or pricing decision.
