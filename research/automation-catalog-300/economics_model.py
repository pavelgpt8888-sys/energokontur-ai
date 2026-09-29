#!/usr/bin/env python3
"""Monthly unit-economics model for the Belarus product candidates (BYN).

Every number below is an assumption to be replaced with interview data.
Run: python3 economics_model.py  -> prints markdown tables used in ECONOMICS_BY.md
"""
from dataclasses import dataclass, field, replace

MONTHS = 36
FOUNDER_MONTHLY = 4000          # opportunity cost of the founder's time (≈ average salary in Minsk)
TAX_RATE = 0.06                 # assumption: simplified tax regime on revenue; HTP residents pay ~1%
BASE_INFRA = 250                # VPS, storage, domains, monitoring
ACCOUNTING = 250                # accounting and legal support
SETUP_ONE_OFF = 1300            # contracts, offer, brand, landing page (month 1)
DEV_COST = 8000                 # middle developer, employer cost per month
CS_COST = 3800                  # sales / customer success manager, employer cost per month
FOCUS = 0.7                     # combined path: a small team sells three products -> 70% of standalone pace


@dataclass
class Stream:
    """Recurring subscription stream."""
    name: str
    start: int                  # first month with sales
    price: float                # BYN per unit per month
    new_first: float            # new units in the first sales month
    new_step: float             # monthly increase of new units
    new_max: float              # cap of new units per month
    churn: float                # monthly churn
    var_cost: float = 1.0       # AI + storage per active unit per month
    partner_share: float = 0.0  # share of revenue coming via partners
    partner_fee: float = 0.0    # commission paid to partners on that revenue


@dataclass
class OneOff:
    """One-off paid service (document packages, checks, norms under a key)."""
    name: str
    price: float
    cost: float                 # external expert time, AI, per order
    schedule: list              # [(from_month, orders_per_month), ...]


@dataclass
class Plan:
    name: str
    streams: list
    oneoffs: list
    staff: list                 # [(from_month, monthly_cost, label)]
    marketing: list             # [(from_month, monthly_cost)]
    lumps: list = field(default_factory=list)   # [(month, cost, label)]


def orders_at(schedule, m):
    n = 0
    for frm, per in schedule:
        if m >= frm:
            n = per
    return n


def run(plan: Plan):
    active = {s.name: 0.0 for s in plan.streams}
    cum_cash = cum_full = 0.0
    min_cash = min_full = 0.0
    breakeven = None
    payback = None
    rows = []
    for m in range(1, MONTHS + 1):
        rev = var = partner = 0.0
        units = 0.0
        for s in plan.streams:
            if m >= s.start:
                new = min(s.new_max, s.new_first + s.new_step * (m - s.start))
                active[s.name] = active[s.name] * (1 - s.churn) + new
            r = active[s.name] * s.price
            rev += r
            var += active[s.name] * s.var_cost
            partner += r * s.partner_share * s.partner_fee
            units += active[s.name]
        mrr = rev
        for o in plan.oneoffs:
            n = orders_at(o.schedule, m)
            rev += n * o.price
            var += n * o.cost
        staff = sum(c for frm, c, _ in plan.staff if m >= frm)
        mkt = 0.0
        for frm, c in plan.marketing:
            if m >= frm:
                mkt = c
        lump = sum(c for mm, c, _ in plan.lumps if mm == m) + (SETUP_ONE_OFF if m == 1 else 0)
        cost = var + partner + staff + mkt + lump + BASE_INFRA + ACCOUNTING + rev * TAX_RATE
        profit = rev - cost
        cum_cash += profit
        cum_full += profit - FOUNDER_MONTHLY
        min_cash = min(min_cash, cum_cash)
        min_full = min(min_full, cum_full)
        if breakeven is None and m > 3 and profit - FOUNDER_MONTHLY >= 0:
            breakeven = m
        if payback is None and m > 3 and cum_full >= 0:
            payback = m
        rows.append(dict(m=m, rev=rev, mrr=mrr, units=units, cost=cost, profit=profit,
                         cum_cash=cum_cash, cum_full=cum_full,
                         per={s.name: (active[s.name], active[s.name] * s.price) for s in plan.streams}))
    year = lambda y: sum(r["rev"] for r in rows[(y - 1) * 12: y * 12])
    return dict(name=plan.name, rows=rows, invest_cash=-min_cash, invest_full=-min_full,
                breakeven=breakeven, payback=payback, y1=year(1), y2=year(2), y3=year(3),
                mrr24=rows[23]["mrr"], mrr36=rows[35]["mrr"], units24=rows[23]["units"],
                cum36_full=rows[35]["cum_full"])


# ---------------------------------------------------------------- candidates

def plan_A(k="base"):
    """A. Energy manager: TER norms, 4-energy-saving report, RIAS preparation."""
    p = dict(base=(150, 12, 0.015, [(4, 2), (10, 4)]),
             pess=(100, 6, 0.025, [(4, 1), (10, 2)]),
             opt=(200, 20, 0.010, [(4, 3), (10, 6)]))[k]
    price, cap, churn, sched = p
    return Plan(
        name=f"А · {k}",
        streams=[Stream("subs", start=4, price=price, new_first=2, new_step=1, new_max=cap, churn=churn,
                        var_cost=3, partner_share=0.3, partner_fee=0.2)],
        oneoffs=[OneOff("норма ТЭР под ключ", price=1500, cost=300, schedule=sched)],
        staff=[(1, 1500, "методолог 0,5 ставки"), (7 if k != "pess" else 9, DEV_COST, "разработчик"),
               (12, CS_COST, "продажи и сопровождение")],
        marketing=[(4, 600), (12, 1000)],
        lumps=[(10, 12000, "защита информации и ПДн")],
    )


def plan_B(k="base"):
    """B. Electrical facilities under TKP 181-2023: outsourcer cabinet, in-house orgs, document packages."""
    p = dict(base=(22, 100, 0.025, [(3, 4), (7, 8), (13, 12)]),
             pess=(18, 40, 0.035, [(3, 2), (7, 4), (13, 6)]),
             opt=(25, 200, 0.020, [(3, 6), (7, 12), (13, 18)]))[k]
    arpu, cap, churn, sched = p
    return Plan(
        name=f"Б · {k}",
        streams=[Stream("objects", start=3, price=arpu, new_first=15, new_step=10, new_max=cap, churn=churn,
                        var_cost=0.4)],
        oneoffs=[OneOff("пакет документов или допуск", price=450, cost=60, schedule=sched)],
        staff=[(1, 1500, "методолог 0,5 ставки"), (8, DEV_COST, "разработчик"), (10, CS_COST, "продажи и сопровождение")],
        marketing=[(3, 700), (10, 1200)],
        lumps=[(9, 12000, "защита информации и ПДн")],
    )


def plan_C(k="base"):
    """C (В). Executive documentation and method statements for electrical installation companies."""
    p = dict(base=(300, 8, 0.020, [(5, 6), (11, 15)]),
             pess=(220, 4, 0.030, [(5, 3), (11, 7)]),
             opt=(400, 15, 0.015, [(5, 9), (11, 22)]))[k]
    price, cap, churn, sched = p
    return Plan(
        name=f"В · {k}",
        streams=[Stream("companies", start=5, price=price, new_first=2, new_step=1, new_max=cap, churn=churn,
                        var_cost=8)],
        oneoffs=[OneOff("техкарта или ППР", price=250, cost=40, schedule=sched)],
        staff=[(1, 1500, "методолог ПТО 0,5 ставки"), (4, DEV_COST, "разработчик"), (12, CS_COST, "продажи и сопровождение")],
        marketing=[(5, 800), (12, 1200)],
        lumps=[(11, 12000, "защита информации и ПДн")],
    )


def plan_D(k="base"):
    """D (Г). Pre-expertise checks of electrical design sections against Belarusian norms."""
    p = dict(base=(450, 6, 0.015, [(6, 8), (12, 25)]),
             pess=(300, 3, 0.025, [(6, 4), (12, 12)]),
             opt=(600, 10, 0.010, [(6, 12), (12, 38)]))[k]
    price, cap, churn, sched = p
    return Plan(
        name=f"Г · {k}",
        streams=[Stream("orgs", start=6, price=price, new_first=1, new_step=0.5, new_max=cap, churn=churn,
                        var_cost=15)],
        oneoffs=[OneOff("проверка раздела", price=150, cost=10, schedule=sched)],
        staff=[(1, 2000, "методолог-проектировщик 0,5 ставки"), (3, DEV_COST, "разработчик"),
               (14, CS_COST, "продажи и сопровождение")],
        marketing=[(6, 800), (14, 1200)],
        lumps=[(12, 12000, "защита информации и ПДн")],
    )


def plan_path(k="base"):
    """Recommended path on one core: B from month 3, A from month 7, C from month 15; shared team."""
    b, a, c = plan_B(k), plan_A(k), plan_C(k)
    shift = lambda s, start: replace(s, start=start)
    sh_sched = lambda sched, d: [(m + d, n) for m, n in sched]
    return Plan(
        name=f"Путь Б→А→В · {k}",
        streams=[b.streams[0],
                 replace(shift(a.streams[0], 7), new_max=a.streams[0].new_max * FOCUS),
                 replace(shift(c.streams[0], 15), new_max=c.streams[0].new_max * FOCUS)],
        oneoffs=[b.oneoffs[0],
                 replace(a.oneoffs[0], schedule=sh_sched(a.oneoffs[0].schedule, 3)),
                 replace(c.oneoffs[0], schedule=sh_sched(c.oneoffs[0].schedule, 10))],
        staff=[(1, 1500, "методолог-энергетик 0,5 ставки"), (6, DEV_COST, "разработчик 1"),
               (9, CS_COST, "продажи и сопровождение"), (10, 1500, "методолог ПТО 0,5 ставки"),
               (13, DEV_COST, "разработчик 2")],
        marketing=[(3, 700), (9, 1200), (15, 1800)],
        lumps=[(9, 15000, "защита информации и ПДн")],
    )


def plan_path_fast(k="base"):
    """Same path, but a developer from month 1: A sells from month 5, C from month 11."""
    base = plan_path(k)
    a_s, c_s = base.streams[1], base.streams[2]
    sh = lambda sched, d: [(m + d, n) for m, n in sched]
    return replace(
        base, name=f"Путь Б→А→В с разработчиком с 1-го мес. · {k}",
        streams=[base.streams[0], replace(a_s, start=5), replace(c_s, start=11)],
        oneoffs=[base.oneoffs[0], replace(base.oneoffs[1], schedule=sh(base.oneoffs[1].schedule, -2)),
                 replace(base.oneoffs[2], schedule=sh(base.oneoffs[2].schedule, -4))],
        staff=[(1, 1500, "методолог-энергетик 0,5 ставки"), (1, DEV_COST, "разработчик 1"),
               (7, CS_COST, "продажи и сопровождение"), (8, 1500, "методолог ПТО 0,5 ставки"),
               (10, DEV_COST, "разработчик 2")],
    )


def fmt(x):
    return f"{x:,.0f}".replace(",", " ")


def main():
    results = []
    for f in (plan_A, plan_B, plan_C, plan_D, plan_path, plan_path_fast):
        for k in ("pess", "base", "opt"):
            results.append(run(f(k)))
    print("| Вариант | Вложить деньгами | Вложить с учётом вашего времени | Выход в плюс (мес.) | "
          "Возврат вложений (мес.) | Выручка 1-й год | 2-й год | 3-й год | Подписка в месяц на 24-й мес. | "
          "Итог за 36 мес. с учётом вашего времени |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in results:
        be = r["breakeven"] or "> 36"
        pb = r["payback"] or "> 36"
        print(f"| {r['name']} | {fmt(r['invest_cash'])} | {fmt(r['invest_full'])} | {be} | {pb} | {fmt(r['y1'])} | "
              f"{fmt(r['y2'])} | {fmt(r['y3'])} | {fmt(r['mrr24'])} | {fmt(r['cum36_full'])} |")
    print("\nПлатящие единицы на 24-й и 36-й месяц (базовые сценарии):\n")
    for r in results:
        if r["name"].endswith("base"):
            u24 = ", ".join(f"{k}: {v[0]:.0f}" for k, v in r["rows"][23]["per"].items())
            u36 = ", ".join(f"{k}: {v[0]:.0f}" for k, v in r["rows"][35]["per"].items())
            print(f"- {r['name']}: 24 мес. — {u24}; 36 мес. — {u36}")
    base = run(plan_path("base"))
    print("\nБазовый путь по кварталам (BYN):\n")
    print("| Квартал | Выручка | Затраты | Результат | Накопленный итог с учётом вашего времени |")
    print("|---|---:|---:|---:|---:|")
    for q in range(12):
        rs = base["rows"][q * 3:(q + 1) * 3]
        print(f"| {q + 1} | {fmt(sum(x['rev'] for x in rs))} | {fmt(sum(x['cost'] for x in rs))} | "
              f"{fmt(sum(x['profit'] for x in rs))} | {fmt(rs[-1]['cum_full'])} |")


# ------------------------------------------------ price check and state sector (28.09.2026)

def plan_B_real():
    """B with observed outsourcer prices (50-150 BYN per client per month): tool ≈ 8 BYN per object."""
    b = plan_B("base")
    return replace(b, name="Б · реальные цены (8 BYN за объект)", streams=[replace(b.streams[0], price=8)])


def plan_A_real():
    """A with observed consultant floor (norms from 300 BYN): 100 BYN/month, norms under key 800 BYN."""
    a = plan_A("base")
    return replace(a, name="А · реальные цены (100 BYN/мес, нормы 800 BYN)",
                   streams=[replace(a.streams[0], price=100)],
                   oneoffs=[replace(a.oneoffs[0], price=800, cost=200)])


def plan_path_real():
    p = plan_path("base")
    return replace(p, name="Путь Б→А→В · реальные цены",
                   streams=[replace(p.streams[0], price=8), replace(p.streams[1], price=100), p.streams[2]],
                   oneoffs=[p.oneoffs[0], replace(p.oneoffs[1], price=800, cost=200), p.oneoffs[2]])


def plan_gov(k="base"):
    """State sector: A for medium/large state enterprises priced under 100 base units per deal
    (own-funds procurement rule from 11.07.2026), B for district centers serving budget organizations."""
    a_price, a_cap, a_churn, a_one = dict(base=(250, 8, 0.01, [(5, 2), (11, 4)]),
                                          pess=(180, 4, 0.02, [(5, 1), (11, 2)]),
                                          opt=(330, 12, 0.008, [(5, 3), (11, 6)]))[k]
    b_price, b_cap, b_one = dict(base=(180, 3, [(4, 1), (10, 2)]),
                                 pess=(120, 1.5, [(4, 0.5), (10, 1)]),
                                 opt=(220, 5, [(4, 2), (10, 3)]))[k]
    return Plan(
        name=f"Госсектор: А крупным + Б для ЦОДБО · {k}",
        streams=[Stream("A_enterprises", start=5, price=a_price, new_first=1, new_step=0.5, new_max=a_cap,
                        churn=a_churn, var_cost=4, partner_share=0.2, partner_fee=0.2),
                 Stream("B_centers", start=4, price=b_price, new_first=0.5, new_step=0.25, new_max=b_cap,
                        churn=0.01, var_cost=6)],
        oneoffs=[OneOff("нормы под ключ крупному", price=2500, cost=500, schedule=a_one),
                 OneOff("перевод зданий ЦОДБО на ТКП 181-2023", price=1500, cost=250, schedule=b_one)],
        staff=[(1, 1500, "методолог-энергетик 0,5 ставки"), (6, DEV_COST, "разработчик"),
               (10, CS_COST, "продажи и сопровождение госсектора")],
        marketing=[(4, 600), (10, 1000)],
        lumps=[(8, 15000, "размещение на beCloud, защита информации")],
    )


def print_price_check():
    plans = [plan_B("base"), plan_B_real(), plan_A("base"), plan_A_real(), plan_path("base"), plan_path_real(),
             plan_gov("pess"), plan_gov("base"), plan_gov("opt")]
    print("\nСверка с реальными ценами и госсектор:\n")
    print("| Вариант | Вложить деньгами | С вашим временем | Выход в плюс | Возврат | Выручка 3-го года | Подписки в мес. на 24-й |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for plan in plans:
        r = run(plan)
        print(f"| {r['name']} | {fmt(r['invest_cash'])} | {fmt(r['invest_full'])} | {r['breakeven'] or '> 36'} | "
              f"{r['payback'] or '> 36'} | {fmt(r['y3'])} | {fmt(r['mrr24'])} |")


# ------------------------------------------------ services instead of SaaS (28.09.2026)
# Price anchors: Bitrix24 integrator in Minsk 72.80 BYN per norm-hour, 1C programmers from 30 BYN/h,
# Russian AI integrators: RAG assistant 150-200k RUB (≈5.4-7.2k BYN) in 3-8 weeks, support 20-30k RUB/month.

ENGINEER_COST = 5500            # automation engineer (n8n / Python / LLM), employer cost per month
SUPPORT_VAR = 70                # hosting and model calls per supported client per month
LEARN = 0.06                    # each repeat of a package cuts its hours by 6% until the floor
BACKLOG_LOSS = 0.25             # share of waiting orders lost each month while there is no capacity


@dataclass
class Package:
    """Fixed-scope service package; hours fall with every repeat as modules get reused."""
    name: str
    price: float
    hours_first: float
    hours_min: float
    cost: float                 # transcription, LLM, travel per order


DIAG = Package("экспресс-диагностика", price=2000, hours_first=30, hours_min=18, cost=80)
PILOT = Package("пилот одного процесса", price=4200, hours_first=80, hours_min=45, cost=250)
ROLLOUT = Package("внедрение", price=14000, hours_first=220, hours_min=140, cost=800)


HIRE_BACKLOG = 60               # an engineer joins after a month with at least 60 hours of work left undone
SALES_GATE = 6                  # a sales manager joins only after 6 delivered pilots (the offer is proven)


@dataclass
class Hire:
    earliest: int               # not before this month
    cost: float
    hours: float                # delivery hours added; for a manager - founder hours freed from selling
    label: str
    sales: bool = False         # a sales manager brings extra leads; others join only when overloaded
    forced: bool = False        # hired on the earliest month regardless of load (capital-backed plan)


@dataclass
class Product:
    """Product built from the most repeated package; starts only after enough paid pilots."""
    earliest: int               # not before this month
    gate: float                 # pilots delivered before a developer is hired for the product
    streams: list               # [(months after the developer starts, Stream)]
    min_profit: float = DEV_COST  # and the last 3 months must earn at least this per month
    lump: float = 15000         # beCloud placement and information security, two months after start
    marketing: float = 1600     # monthly, from the first sales month
    founder_shift: float = 30   # founder delivery hours moved to the product


@dataclass
class ServicesPlan:
    name: str
    leads: list                 # [(from_month, diagnostics sold per month)] by the founder
    direct_pilots: list         # [(from_month, pilots sold without diagnostics)]
    diag_to_pilot: float        # share of diagnostics that turn into a pilot
    pilot_to_impl: float        # share of pilots that turn into a full rollout
    to_support: float           # share of pilots that stay on paid support
    support_price: float        # BYN per client per month
    support_hours: float        # delivery hours per supported client per month
    support_churn: float
    lag_pilot: int = 1          # months from diagnostics to pilot
    lag_impl: int = 2           # months from pilot to rollout
    price_k: float = 1.0        # multiplier for package prices
    founder_hours: float = 90   # founder delivery hours per month; the rest is sales and admin
    hires: list = field(default_factory=list)       # [Hire], taken in order when overloaded
    manager_leads: float = 0.0  # extra diagnostics per month once a sales manager works
    manager_direct: float = 0.0  # extra direct pilots per month once a sales manager works
    marketing: list = field(default_factory=list)   # [(from_month, monthly_cost)]
    tools: list = field(default_factory=list)       # [(from_month, monthly_cost)] GPU rent, licences
    product: Product = None
    profit_gate: bool = True    # False: capital pays for hires, only the workload decides


def run_services(p: ServicesPlan):
    keys = (("impl", ROLLOUT), ("pilot", PILOT), ("diag", DIAG))
    queue = {k: 0.0 for k, _ in keys}
    done = {k: [0.0] * (MONTHS + 1) for k, _ in keys}
    repeats = {k: 0.0 for k, _ in keys}
    arrived = support = 0.0
    pending, team = list(p.hires), []
    pr, prod_start, active = p.product, None, {}
    overloaded = False
    cum_cash = cum_full = min_cash = min_full = 0.0
    breakeven = payback = None
    rows = []
    for m in range(1, MONTHS + 1):
        trailing = sum(r["profit"] for r in rows[-3:]) / 3 if len(rows) >= 3 else 0.0
        for h in [h for h in pending if h.forced and m >= h.earliest]:
            team.append((m, h))
            pending.remove(h)
        affordable = lambda need: trailing >= need or not p.profit_gate
        for h in pending:
            if m >= h.earliest and (repeats["pilot"] >= SALES_GATE and affordable(FOUNDER_MONTHLY + h.cost)
                                    if h.sales else overloaded and affordable(FOUNDER_MONTHLY)):
                team.append((m, h))
                pending.remove(h)
                break
        if pr and prod_start is None and m >= pr.earliest and repeats["pilot"] >= pr.gate \
                and trailing >= pr.min_profit:
            prod_start = m
        selling = any(h.sales for _, h in team)
        new = dict(diag=orders_at(p.leads, m) + (p.manager_leads if selling else 0),
                   pilot=orders_at(p.direct_pilots, m) + (p.manager_direct if selling else 0)
                   + (p.diag_to_pilot * done["diag"][m - p.lag_pilot] if m - p.lag_pilot >= 1 else 0),
                   impl=p.pilot_to_impl * done["pilot"][m - p.lag_impl] if m - p.lag_impl >= 1 else 0)
        for k in queue:
            queue[k] += new[k]
            arrived += new[k]
        cap = p.founder_hours - (pr.founder_shift if prod_start else 0) + sum(h.hours for _, h in team)
        sup_hours = support * p.support_hours
        free = max(0.0, cap - sup_hours)
        hours = {k: max(pk.hours_min, pk.hours_first * (1 - LEARN) ** repeats[k]) for k, pk in keys}
        need = sum(queue[k] * hours[k] for k, _ in keys)
        share = 1.0 if need <= free else free / need   # short of hours -> every queue served pro rata
        overloaded = need - free >= HIRE_BACKLOG
        rev = support * p.support_price
        mrr = rev
        var = support * SUPPORT_VAR
        used = min(cap, sup_hours)
        for k, pk in keys:
            n = queue[k] * share
            done[k][m] = n
            repeats[k] += n
            used += n * hours[k]
            queue[k] = (queue[k] - n) * (1 - BACKLOG_LOSS)
            rev += n * pk.price * p.price_k
            var += n * pk.cost
        support = support * (1 - p.support_churn) + p.to_support * done["pilot"][m]
        staff = sum(h.cost for _, h in team)
        extra = orders_at(p.marketing, m) + orders_at(p.tools, m)
        lump = SETUP_ONE_OFF if m == 1 else 0
        if prod_start:
            staff += DEV_COST
            lump += pr.lump if m == prod_start + 2 else 0
            extra += pr.marketing if m >= prod_start + min(off for off, _ in pr.streams) else 0
            for off, s in pr.streams:
                if m >= prod_start + off:
                    step = m - prod_start - off
                    active[s.name] = active.get(s.name, 0.0) * (1 - s.churn) + min(s.new_max, s.new_first + s.new_step * step)
                a = active.get(s.name, 0.0)
                r = a * s.price
                rev += r
                mrr += r
                var += a * s.var_cost + r * s.partner_share * s.partner_fee
        cost = var + staff + extra + lump + BASE_INFRA + ACCOUNTING + rev * TAX_RATE
        profit = rev - cost
        cum_cash += profit
        cum_full += profit - FOUNDER_MONTHLY
        min_cash = min(min_cash, cum_cash)
        min_full = min(min_full, cum_full)
        if breakeven is None and m > 3 and profit - FOUNDER_MONTHLY >= 0:
            breakeven = m
        if cum_full < 0:
            payback = None      # a product dip can push the total below zero again; count the last crossing
        elif payback is None and m > 3:
            payback = m
        rows.append(dict(m=m, rev=rev, mrr=mrr, cost=cost, profit=profit, cum_full=cum_full,
                         support=support, load=used / cap if cap else 0.0,
                         heads=1 + len(team) + (1 if prod_start else 0)))
    served = sum(sum(v) for v in done.values())
    year = lambda y: sum(r["rev"] for r in rows[(y - 1) * 12: y * 12])
    return dict(name=p.name, rows=rows, invest_cash=max(0.0, -min_cash), invest_full=max(0.0, -min_full),
                breakeven=breakeven, payback=payback, y1=year(1), y2=year(2), y3=year(3),
                mrr24=rows[23]["mrr"], mrr36=rows[35]["mrr"], cum36_full=rows[35]["cum_full"],
                lost=1 - served / arrived if arrived else 0.0, prod_start=prod_start,
                hired=[mm for mm, _ in team], team=[f"{h.label} — {mm}" for mm, h in team])


def services_params(k):
    """Funnel and prices per scenario; leads = diagnostics sold per month."""
    return dict(
        pess=dict(scale=0.5, shift=2, diag_to_pilot=0.35, pilot_to_impl=0.2, to_support=0.45,
                  support_price=350, support_churn=0.05, price_k=0.8, lag_pilot=2, lag_impl=3),
        base=dict(scale=1.0, shift=0, diag_to_pilot=0.5, pilot_to_impl=0.3, to_support=0.6,
                  support_price=450, support_churn=0.03, price_k=1.0, lag_pilot=1, lag_impl=2),
        opt=dict(scale=1.5, shift=0, diag_to_pilot=0.6, pilot_to_impl=0.4, to_support=0.7,
                 support_price=550, support_churn=0.02, price_k=1.15, lag_pilot=1, lag_impl=2),
    )[k]


def _services(k, name, **extra):
    q = services_params(k)
    sc, sh = q.pop("scale"), q.pop("shift")
    return ServicesPlan(name=f"{name} · {k}",
                        leads=[(m + sh, n * sc) for m, n in [(2, 1), (4, 1.5), (9, 2)]],
                        direct_pilots=[(3 + sh, 0.5 * sc)],
                        manager_leads=1.5 * sc, manager_direct=0.5 * sc,
                        support_hours=4, tools=[(2, 300)], **q, **extra)


def plan_services_solo(k="base"):
    """Founder alone: about 90 delivery hours a month, the rest goes to sales and admin."""
    return _services(k, "Услуги соло", marketing=[(2, 300)])


def plan_services_team(k="base"):
    """Same founder funnel; engineers and a sales manager join only when work is left undone."""
    return _services(k, "Услуги с командой", marketing=[(3, 500), (9, 1000)],
                     hires=[Hire(4, ENGINEER_COST, 120, "инженер автоматизации 1"),
                            Hire(8, CS_COST, 20, "продажи и сопровождение", sales=True),
                            Hire(10, ENGINEER_COST, 120, "инженер автоматизации 2"),
                            Hire(16, ENGINEER_COST, 120, "инженер автоматизации 3")])


def plan_services_hybrid(k="base"):
    """Team services; after 6 delivered pilots a developer turns the most repeated package into products."""
    gov = plan_gov(k)
    return replace(plan_services_team(k), name=f"Гибрид: услуги → продукт · {k}",
                   product=Product(earliest=10, gate=6, streams=[(3, gov.streams[0]), (6, gov.streams[1])]))


def print_services():
    print("\nУслуги вместо SaaS:\n")
    print("| Вариант | Вложить деньгами | С вашим временем | Выход в плюс | Возврат | Выручка 1-й год | "
          "2-й год | 3-й год | Повторяющаяся в мес. на 24-й / 36-й | На сопровождении на 24-й | "
          "Найм (мес.) | Продукт с (мес.) | Потеряно заказов |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|")
    for f in (plan_services_solo, plan_services_team, plan_services_hybrid):
        for k in ("pess", "base", "opt"):
            r = run_services(f(k))
            print(f"| {r['name']} | {fmt(r['invest_cash'])} | {fmt(r['invest_full'])} | {r['breakeven'] or '> 36'} | "
                  f"{r['payback'] or '> 36'} | {fmt(r['y1'])} | {fmt(r['y2'])} | {fmt(r['y3'])} | "
                  f"{fmt(r['mrr24'])} / {fmt(r['mrr36'])} | {r['rows'][23]['support']:.0f} | "
                  f"{', '.join(map(str, r['hired'])) or '—'} | {r['prod_start'] or '—'} | {r['lost']:.0%} |")
    for plan in (plan_path_real(), plan_gov("base")):
        r = run(plan)
        print(f"| SaaS для сравнения: {r['name']} | {fmt(r['invest_cash'])} | {fmt(r['invest_full'])} | "
              f"{r['breakeven'] or '> 36'} | {r['payback'] or '> 36'} | {fmt(r['y1'])} | {fmt(r['y2'])} | "
              f"{fmt(r['y3'])} | {fmt(r['mrr24'])} / {fmt(r['mrr36'])} | — | — | — | — |")
    for f in (plan_services_team, plan_services_hybrid):
        r = run_services(f("base"))
        print(f"\n{r['name']}: найм по месяцам — {'; '.join(r['team'])}")
    for f in (plan_services_solo, plan_services_team, plan_services_hybrid):
        r = run_services(f("base"))
        print(f"\n{r['name']} по кварталам (BYN):\n")
        print("| Квартал | Выручка | Из неё повторяющаяся | Затраты | Результат | Человек | "
              "Накопленный итог с учётом вашего времени |")
        print("|---|---:|---:|---:|---:|---:|---:|")
        for q in range(12):
            rs = r["rows"][q * 3:(q + 1) * 3]
            print(f"| {q + 1} | {fmt(sum(x['rev'] for x in rs))} | {fmt(sum(x['mrr'] for x in rs))} | "
                  f"{fmt(sum(x['cost'] for x in rs))} | {fmt(sum(x['profit'] for x in rs))} | {rs[-1]['heads']} | "
                  f"{fmt(rs[-1]['cum_full'])} |")


# ------------------------------------------------ owner income targets (28.09.2026)
# Dividends of Belarusian residents from 2026: 13% up to 350 000 BYN a year, 25% above.

DIV_TAX_LOW, DIV_TAX_HIGH, DIV_LIMIT = 0.13, 0.25, 350000
USN_LIMIT = 3735000             # simplified tax regime revenue cap for 2026


def dividends_net(gross_year):
    return min(gross_year, DIV_LIMIT) * (1 - DIV_TAX_LOW) + max(0.0, gross_year - DIV_LIMIT) * (1 - DIV_TAX_HIGH)


def dividends_gross(net_year):
    low = DIV_LIMIT * (1 - DIV_TAX_LOW)
    return net_year / (1 - DIV_TAX_LOW) if net_year <= low else DIV_LIMIT + (net_year - low) / (1 - DIV_TAX_HIGH)


def plan_studio(k="base"):
    """Capital-backed studio: tech co-founder and energy methodologist from month 1, sales manager
    from month 3, engineers under load, products after 4 pilots without waiting for profit."""
    gov = plan_gov(k)
    q = services_params(k)
    sc, sh = q["scale"], q["shift"]
    return replace(plan_services_team(k), name=f"Студия с капиталом · {k}",
                   leads=[(m + sh, n * sc) for m, n in [(2, 1.5), (4, 2.5), (7, 3)]],
                   hires=[Hire(1, 6000, 60, "технический сооснователь (зарплата ниже рынка + доля)", forced=True),
                          Hire(1, 2500, 60, "методолог-энергетик 0,5 ставки", forced=True),
                          Hire(3, CS_COST, 20, "продажи и сопровождение", sales=True, forced=True),
                          Hire(4, ENGINEER_COST, 120, "инженер автоматизации 1"),
                          Hire(6, ENGINEER_COST, 120, "инженер автоматизации 2"),
                          Hire(10, ENGINEER_COST, 120, "инженер автоматизации 3"),
                          Hire(14, ENGINEER_COST, 120, "инженер автоматизации 4")],
                   marketing=[(2, 1500), (7, 3000)], tools=[(2, 600)],
                   product=Product(earliest=7, gate=4, min_profit=-1e9,
                                   streams=[(3, gov.streams[0]), (6, gov.streams[1])]),
                   profit_gate=False)


def owner_view(r, draw_net=10000):
    """What the owner gets: capital needed to pay yourself draw_net a month from month 1,
    months when profit covers 10k and 30k BYN net, year-3 profit paid out as dividends."""
    draw = dividends_gross(draw_net * 12) / 12
    cum = low = 0.0
    for x in r["rows"]:
        cum += x["profit"] - draw
        low = min(low, cum)
        if x["m"] == 9:
            burn9 = -cum

    def covers(net_month):
        need = dividends_gross(net_month * 12) / 12
        for i in range(2, MONTHS):
            if all(y["profit"] >= need for y in r["rows"][i - 2:]):
                return i - 1
        return None

    p3 = sum(x["profit"] for x in r["rows"][24:36])
    return dict(capital=-low, m10=covers(10000), m30=covers(30000), profit_y3=p3, net_y3=dividends_net(p3),
                rev_y3=r["y3"], cum36=cum, burn9=max(0.0, burn9))


def print_owner_targets():
    print("\nЦели по доходу (10 тыс. BYN на руки с 1-го месяца из капитала, дивиденды 13% / 25%):\n")
    print(f"Нужно прибыли в месяц: на 10 тыс. на руки — {fmt(dividends_gross(120000) / 12)}; "
          f"на 30 тыс. — {fmt(dividends_gross(360000) / 12)}; на 200 тыс. $ в год "
          f"({fmt(200000 * 3.0276)} BYN) — {fmt(dividends_gross(200000 * 3.0276) / 12)}\n")
    print("| Вариант | Капитал, чтобы платить себе 10 тыс. с 1-го мес. | Сгорит, если остановиться на 9-м мес. | "
          "10 тыс. на руки из прибыли с (мес.) | 30 тыс. на руки с (мес.) | Выручка 3-го года | Прибыль 3-го года | "
          "На руки за 3-й год | То же, тыс. $ | Итог за 36 мес. после ваших выплат |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    plans = [plan_services_team("base"), plan_services_hybrid("base")] + \
        [plan_studio(k) for k in ("pess", "base", "opt")] + [plan_services_hybrid("opt")]
    for plan in plans:
        r = run_services(plan)
        o = owner_view(r)
        print(f"| {r['name']} | {fmt(o['capital'])} | {fmt(o['burn9'])} | {o['m10'] or '> 36'} | {o['m30'] or '> 36'} | "
              f"{fmt(o['rev_y3'])} | "
              f"{fmt(o['profit_y3'])} | {fmt(o['net_y3'])} | {o['net_y3'] / 3.0276 / 1000:.0f} | {fmt(o['cum36'])} |")
    r = run_services(plan_studio("base"))
    print(f"\nСтудия с капиталом · base: найм по месяцам — {'; '.join(r['team'])}; продукт с {r['prod_start']}-го мес.")
    print("\n| Квартал | Выручка | Из неё повторяющаяся | Затраты | Прибыль до ваших выплат | Человек |")
    print("|---|---:|---:|---:|---:|---:|")
    for q in range(12):
        rs = r["rows"][q * 3:(q + 1) * 3]
        print(f"| {q + 1} | {fmt(sum(x['rev'] for x in rs))} | {fmt(sum(x['mrr'] for x in rs))} | "
              f"{fmt(sum(x['cost'] for x in rs))} | {fmt(sum(x['profit'] for x in rs))} | {rs[-1]['heads']} |")


if __name__ == "__main__":
    main()
    print_price_check()
    print_services()
    print_owner_targets()
