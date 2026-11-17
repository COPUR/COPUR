# `COPUR-portfolio` — SWOT Zayıflık / Tehdit Giderme Backlog'u (`BG-01` .. `BG-10`)

Bu backlog, `program-manager` SWOT analizinde tespit edilen zayıf yönleri (**W1–W5**) ve tehditleri (**T1–T3**) gidermek üzere TOGAF ADM BDAT döngüsü (`business-architect` → `data-architect` → `application-architect` → `technology-architect`) ile türetilmiştir. Tam mimari spesifikasyon: [TOGAF_ADM_PLAN.md](./TOGAF_ADM_PLAN.md).

---

## Önceliklendirilmiş İyileştirme Matrisi

| Backlog ID | Öncelik | Giderilen SWOT (W/T) | Sahip TOGAF Fazı | Hedef Dosyalar / Bileşenler | Dalga & Kabul Kapısı | Durum |
|---|---|---|---|---|---|---|
| **BG-01** | **P0** | **W1, T2** | Faz B + Faz C (Veri) | `catalog/portfolio-catalog.json`, `README.md`, `PROJECTS.md`, `docs/index.html` — 3 dokümandaki repo kaymalarının (`loan-lifecycle-core`, `accounts-ledger-service`, `iac-cicd-templates`, `adr-runbooks`, `ai-agent-protocols`, `EV_PNC_docs`) tek SSOT ile uzlaştırılması | Dalga 1–2 (`VAL-03`, `VAL-04`, `GATE-01/02`) | `DONE` |
| **BG-02** | **P0** | **W1** | Faz B + Faz C (Uygulama) | `PROJECTS.md`, `docs/index.html`, `README.md` — 4 Yönetici Alanı × 10 Ürün Paketi taksonomisi; Kart 9'un **Suite 9 (EV Telemetry & CAN)** ve **Suite 10 (Serverless News & Observability)** olarak ayrılması; çift `Product 3.2` ve mükerrer `redbank-agentive-framework` hatalarının giderilmesi | Dalga 1–2 (`VAL-01`, `VAL-02`, `GATE-02`) | `DONE` |
| **BG-03** | **P0** | **W1, W4** | Faz D (Teknoloji) | `scripts/publish-portfolio.sh`, `README.md`, `COPUR/COPUR.github.io` — Pages çıktısının canlı kök `https://copur.github.io/` adresine hizalanması ve çift-repo senkronu | Dalga 3 (`GATE-06`, `GATE-07`) | `DONE` |
| **BG-04** | **P0** | **W2, T1** | Faz B + Faz C (Uygulama) | `catalog/portfolio-catalog.json` (`proofLinks[]`), `briefs/*.md`, `docs/briefs/*.html` — Her suite için en az 1 doğrulanabilir derin kanıt linki (quickstart, testkit, C4/ADR özeti) | Dalga 2 (`VAL-07`, `GATE-01/02`) | `DONE` |
| **BG-05** | **P1** | **W2, T1** | Faz B | `OPF-Agentive-Platform` ADR/benchmark referansı, `PROJECTS.md`, `docs/index.html` — `>80% pgvector` gibi güçlü metriklerin ölçüm/ADR derin linkine bağlanması veya niteliksel ifadeyle kalibrasyonu | Dalga 2 (`FF-01`, `GATE-01`) | `DONE` |
| **BG-06** | **P1** | **W3, T1** | Faz B + Faz C (Veri/Uyg.) | `MasruFi_Framework` (`PRIVATE`), `OPF V3/V4`, `EA-Agentive-Platform-v3`, `RedBank` — Kapalı amiral gemileri için kod sızdırmadan redakte C4/ADR özetleri (`PRIVATE`/`IN_DESIGN` için sıfır hyperlink) | Dalga 1–2 (`VAL-04`, `VAL-05`, `FF-03`) | `DONE` |
| **BG-07** | **P1** | **W3, W5** | Faz B + Faz C (Uygulama) | `docs/index.html`, `PROJECTS.md`, `README.md` — 4 katmanlı ürün olgunluk rozetleri (`Runnable K8s / CLI Demo`, `Public Reference Baseline`, `Contract-First Ecosystem`, `Governed Private Enterprise Baseline`) | Dalga 2 (`VAL-08`, `GATE-02`) | `DONE` |
| **BG-08** | **P1** | **W4, T3** | Faz D (Teknoloji) | `scripts/publish-portfolio.sh` — `--dry-run`, `-m`, `--skip-verify-github`, `--offline` bayrakları ve iCloud kilit hatalarına (`mmap` / `index.lock`) karşı `/tmp` APFS çift-repo staging | Dalga 3 (`FF-06`, `GATE-06`, `GATE-07`) | `DONE` |
| **BG-09** | **P1** | **W5** | Faz C (Uygulama) | `docs/index.html` — 4 Domain filtresi, olgunluk seçici, anlık arama, Enterprise Engineering Standards matrisi, SEO/OpenGraph/Twitter meta ve sıfır `innerHTML` vanilla JS | Dalga 2 (`FF-04`, `GATE-03`) | `DONE` |
| **BG-10** | **P2** | **T2, W4** | Faz D + Faz G | `.github/workflows/hygiene.yml`, `scripts/build-portfolio.py`, `tests/test_*.py` — `gh api --paginate` ile 171+ repo ölçeği (`--limit 200` sınırını kaldırma), `unittest` mimari sınır testleri ve tek kaynak `HygieneScanner` | Dalga 1–3 (`FF-05`, `GATE-03/04/05`) | `DONE` |

---

## Uygulama Dalgaları ve Kabul Kriterleri

### Dalga 1 — SSOT Katalog, Şema, Python Stdlib Derleyici ve Birim Testleri (`BG-01`, `BG-02`, `BG-06`, `BG-10`)
- **Artefaktlar:** `catalog/portfolio-catalog.schema.json`, `catalog/portfolio-catalog.json`, `scripts/build-portfolio.py`, `scripts/portfolio_compiler/`, `tests/test_*.py`, güncellenmiş `.gitignore`.
- **Kabul Kriteri:** `python3 scripts/build-portfolio.py --check --offline --strict-hygiene` ve `python3 -m unittest discover -s tests -p "test_*.py" -v` çıkış kodu `0` verir; `VAL-01..VAL-09` ihlali yoktur.

### Dalga 2 — Çift-Artefakt Kanıt Özetleri & 4×10 Etkileşimli Vitrin (`BG-01`, `BG-02`, `BG-04`, `BG-05`, `BG-06`, `BG-07`, `BG-09`)
- **Artefaktlar:** `briefs/*.md`, `docs/briefs/*.html`, `docs/.nojekyll`, yeniden üretilen `README.md`, `PROJECTS.md`, `docs/index.html`.
- **Kabul Kriteri:** Üç yüzeyde tam `4 × 10` yapısal tutarlılık; her suite'te en az 1 geçerli `proofLinks[]`; `PRIVATE`/`IN_DESIGN` öğelerde 0 tıklanabilir URL; `--check --verify-github --strict-verification --strict-hygiene` çıkış kodu `0`.

### Dalga 3 — iCloud-Güvenli Çift-Repo CI/CD & Canlı Yayın (`BG-03`, `BG-08`, `BG-10`)
- **Artefaktlar:** `scripts/publish-portfolio.sh`, `.github/workflows/hygiene.yml`, `COPUR/COPUR` + `COPUR/COPUR.github.io` senkronu.
- **Kabul Kriteri:** `./scripts/publish-portfolio.sh --dry-run` temiz geçer; canlı yayında `COPUR/COPUR` (`main`) ve `COPUR/COPUR.github.io` (`main`) eşitlenir; `https://copur.github.io/` HTTP 200 döner.

### Sonraki Güvenlik Denetimi (`0security` — Dalga 3 Sonrası Opsiyonel)
- Kaydedilen [zero-security](file:///Users/alicopur/.gemini/config/plugins/book-skills/skills/zero-security/SKILL.md) skill'i üzerinden diğer repolarda `0 scan . --module deps` / `deps-fix`, MCP endpoint & prompt-injection taramaları ve CI SARIF entegrasyonu.
