# Gap analysis: v2 (500) vs старый каталог v1 (300)

Дата: 2026-09-29.

## Вывод
Старый каталог v1 был сильным по документам, ПТО, эксплуатации, ЭТЛ, CRM, базовой диагностике, охране труда и внутренней автоматизации. Он не был плохим. Но второй независимый проход показывает несколько крупных слоёв, которые были либо представлены одной-двумя идеями, либо практически отсутствовали.

## 12 наиболее заметных пробелов v1

1. **Grid-Enhancing Technologies (GETs).** В v1 был DDLR в отдельном технологическом радаре, но почти не было продуктового слоя: DTR, topology optimisation, dynamic operating envelopes, non-firm connections, APFC decision support, SATA screening, экономика «стоимость/МВт высвобождённой мощности».
2. **Demand flexibility / DERMS / V2G.** В v1 были BESS и управление пиками, но почти отсутствовали агрегаторы гибкости, automated demand response, smart charging, V2G, flexibility contracts и digital flexibility passport.
3. **Grid connection queue / hosting capacity.** Новые идеи: зрелость заявок, поиск «мертвых» проектов, non-firm offers, сценарное усиление сети, инвестиционный backlog.
4. **Data centres и новые крупные нагрузки.** Отдельный класс задач появился из-за роста AI/data-centre demand: grid-readiness, workload shifting, UPS-as-flexibility, large-load planning.
5. **OT cybersecurity + AI governance.** V1 имел инвентаризацию АСУ ТП и аномалии, но почти не было SBOM, supply-chain cyber risk, JIT remote access, model registry, agent action ledger, prompt-injection tests и sandbox для AI.
6. **Regulatory impact management.** V1 имел мониторинг нормативки и AI-ассистента. V2 добавляет change impact на внутренние документы, compliance debt, curator workflow, права на нормативные тексты, requirement graph.
7. **Climate resilience.** Почти отдельная продуктовая категория: flood/heat/ice/storm risk, pre-positioning ресурсов, resilience microgrid, emergency spare sharing, climate stress-test инвестпрограмм.
8. **Advanced project controls / claims.** V1 имел бюджет и кассовые разрывы, но почти не было earned value, change-order detection, notice periods, claims evidence, cost-to-complete и margin-at-completion.
9. **Supply-chain intelligence.** Добавлены lead-time forecasting, supplier risk, total landed cost, serial tracking, remote FAT, дефицитные BOM и риск страны/поставщика.
10. **Simultaneous operations / dynamic safety.** V1 имел наряды и СИЗ. V2 добавляет conflict detection между нарядами, JSA/JHA AI-check, fatigue, skill decay, near-miss intelligence и dynamic competency.
11. **AI-native operating model компании.** Не отдельный бот, а связанный back-office: agents для tender/procurement/contracts/finance/field reports/knowledge с human approval и ROI tracking.
12. **Product packaging / managed services.** V1 был список решений. V2 явно превращает часть идей в продаваемые функции: DLR-as-a-Service, Power Quality-as-a-Service, Compliance-as-a-Service, Executive Documentation-as-a-Service, shared AI back-office и outcome-based pricing.

## Что повторилось
Повторение — полезный сигнал. Независимо снова появились:
- asset passports / health score / predictive maintenance;
- drones + computer vision;
- transformer diagnostics;
- RZA event analysis;
- losses / AMI / power quality;
- electrical-facility compliance;
- ETL reports;
- BIM/CAD automation;
- tender intelligence;
- field reports → documents/tasks;
- executive documentation;
- regulatory assistant;
- management dashboards.

Это означает, что v1 не случайно был сфокусирован на этих областях: они естественно возникают при повторном анализе процессов.

## Что я считаю самыми интересными новыми направлениями для коммерческой проверки

### Быстрые B2B / service-led
- №301 AI-квалификация тендера по реализуемости и марже.
- №307 Автосбор clarification questions.
- №318 RFP-to-solution.
- №331 Подбор эквивалентов с evidence.
- №340 Remote FAT.
- №365 Change-order detector.
- №366 Автосбор доказательств для допработ.
- №385 Матрица «требование → процесс → документ → ответственный».
- №395 Supply-chain cyber risk score.
- №440 Shared/managed AI workflows для компаний.

### Mid-market / промышленность
- №205 Automated demand response для технологических нагрузок.
- №218 Flexibility contract calculator.
- №223 Энергоинтенсивность единицы продукции real-time.
- №229 Сценарии отказа вводов/АВР с оценкой потерь.
- №239 Measurement & Verification экономии.
- №331–340 supply-chain intelligence.
- №421–440 AI-native operating model.

### Enterprise / энергосистема
- №82 Hosting capacity на фидере.
- №101–120 GETs.
- №181 Hosting Capacity Map.
- №187 Queue maturity scoring.
- №193–200 сетевые investment analytics.
- №201–220 DER/BESS/flexibility.
- №401–420 data centres / large loads.

## Что НЕ делать автоматически
- Не считать все 500 отдельными продуктами.
- Не делать AI там, где хватает интеграции/правил.
- Не допускать agentic AI к safety-critical/OT action без отдельного risk model, testbed и human approval.
- Не строить бизнес-кейс для Беларуси из глобального тренда без локального WTP.
- Не считать совпадение с IEA/DOE подтверждением локального рынка — это только указатель технологического направления.

## Gate v3
Следующий разумный проход — не ещё 500 идей, а scoring всех 500 и старых 300 по единой матрице, затем интервью по 10–20 наиболее коммерчески сильным кластерам.
