# Automated Game Testing & Software Engineering Practices Survey — Open Dataset & Analysis

[![License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Dataset Size](https://img.shields.io/badge/Valid%20Respondents-N%20%3D%20231-green.svg)](#dataset-overview)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-yellow.svg)](https://www.python.org/)

## Overview

This repository contains the open dataset, semantic reclassification pipeline, taxonomy mappings, and statistical analysis outputs from an international survey investigating **Software Engineering (SE) practices, automated game testing adoption, complementary Quality Assurance (QA) approaches, and Generative AI tool utilization** among digital game developers.

* **Principal Investigator:** Esdras Caleb Oliveira Silva (PhD Candidate in Computer Science, Federal University of Rio Grande do Norte — UFRN, Brazil)
* **Collection Period:** January 7, 2026 – March 19, 2026
* **Valid Sample Size:** $N = 231$ game developers across 8 world regions
* **Survey Languages:** Multilingual instrument administered in English (`en`: $n = 165$), Brazilian Portuguese (`pt-BR`: $n = 60$), and Spanish (`es`: $n = 6$)

### Research Questions Addressed

The dataset and statistical outputs are organized around four primary Research Questions (RQs):

1. **RQ1 (Testing Adoption & Demographics):** How does the adoption of automated testing vary across geographic regions, developer seniority, team structure, educational background, and experience?
2. **RQ2 (Automated Testing vs. SE Practices):** How does automated testing adoption relate to broader software engineering practices (version control, continuous integration, design patterns, software modeling, and prototyping)?
3. **RQ3 (Complementary QA Approaches):** What game design validation methods, artifact evaluation strategies, and testing workflows do developers rely on alongside—or instead of—automated testing?
4. **RQ4 (AI Tool Utilization):** In which development domains are game developers applying Generative AI tools, and how do those applications correlate with ethical, artistic, and technical concerns?

---

## Repository Structure

```text
survey_automatestests_questionsReclassifiy/
├── filtereddata.csv                 # Pre-filtered, anonymized input survey responses
├── reclassifieddatanew.csv          # Main processed dataset (N = 231 valid rows, 212 variables)
├── statistical_analysis_by_rq.csv   # Statistically significant pairwise chi-square & Cramér's V results (115 associations)
├── reclassify_csv.py                # Data cleaning, one-hot encoding, LLM-assisted reclassification, and feature engineering script
├── mapingssurvey.json               # Controlled vocabulary and taxonomy mappings for multi-select & open-ended responses
├── finalremarks.json                # Thematic classification schema for open-ended closing remarks
├── llm_cache.json                   # Deterministic cache of LLM-assisted classifications for full reproducibility
└── README.md                        # Dataset documentation and codebook

```

> **Note on Visualizations:** Static charts and figures generated from these tables are maintained externally for manuscript preparation and are not bundled in this repository. All visualizations can be reproduced directly from `reclassifieddatanew.csv` and `statistical_analysis_by_rq.csv`.

---

## Dataset Overview & Codebook (`reclassifieddatanew.csv`)

The primary analytical file `reclassifieddatanew.csv` comprises **231 valid respondent records** across **212 columns**.

> ⚠️ **Important Loading Note:** Row index `231` (the final line of the CSV) contains an aggregate summary footer row where `uid` is `NaN` (e.g., `no_use_tests = 226`). Always filter by valid respondent IDs when loading the dataset:
> ```python
> import pandas as pd
> df = pd.read_csv("reclassifieddatanew.csv").dropna(subset=["uid"])
> 
> ```
> 
> 

### 1. Metadata & Respondent Demographics (`Columns 0–16`, `194–199`)

* **Identifiers & Timing:** `uid` (anonymized UUIDv4), `date` (ISO-8601 timestamp), `language` (browser locale), `form_language` (`en`, `pt-BR`, `es`), `time` (completion duration).
* **Geography:** `country_work` (raw country input), `country_normalized`, and `world_region` (`Latin America`: 78, `North America`: 68, `Western Europe`: 47, `Southeast Asia`: 12, `Not Informed`: 10, `Europe`: 9, `Africa`: 5, `Middle East`: 2).
* **Age & Experience:** `year_of_birth`, `idade`, `idade_faixa` (`18a30`, `30a40`, `40a50`, `50a60`, `60a80`), `anos_experiencia`, `experiencia_faixa` (`0a5`, `5a10`, `10a20`, `20a30`, `30a40`, `40a50`), `qtd_projetos`, `projetos_faixa`.
* **Education & Team Context:** `formacao`, `area_formacao`, `situacao` (employment/hobbyist status), `situacao_equipe` (`individual`, `pequena`, `media`, `grande`, `muito_grande`, `varia`), `duracao_projetos`.

### 2. Core Software Engineering Practices (`Columns 21–26`)

Six ordinal categorical variables capturing adoption levels across core SE practices:

* `uso_praticas_controle_versao` (Version Control)
* `uso_praticas_padroes_design` (Design Patterns)
* `uso_praticas_modelagem_projeto` (Software Modeling)
* `uso_praticas_prototipacao` (Prototyping)
* `uso_praticas_testes_automatizados` (Automated Testing)
* `uso_praticas_integracao_continua` (Continuous Integration / CI)

**Response Scale:**

| Raw Value | Meaning |
| --- | --- |
| `sempre_uso` | Always use |
| `uso_as_vezes` | Use sometimes |
| `ja_tentou` | Tried in the past |
| `prefere_outros` | Prefer other methods |
| `nao_util` | Consider not useful |
| `nao_conhece` | Unfamiliar / Do not know |

### 3. Reclassified & Multi-Hot Encoded Variables (`Columns 41–193`)

Multi-select questions and open-ended `"_outro"` (Other) responses were normalized into binary indicator columns (`0` = absent, `1` = present) using `mapingssurvey.json` and `finalremarks.json`:

| Prefix | Domain | # Cols | Examples of Encoded Categories |
| --- | --- | --- | --- |
| `funcoes__*` | Developer Roles | 13 | `programador`, `game_designer`, `qa`, `artista`, `produtor`, `tec_lead` |
| `tipos_jogos__*` | Game Genres | 12 | `action`, `adventure`, `rpg`, `strategy`, `educational_games`, `cozy_games` |
| `plataformas_desenvolvimento__*` | Target Platforms | 9 | `pc`, `mobile`, `web`, `console_psx`, `console_xbox`, `console_nintendo`, `xr` |
| `ferramentas_desenvolvimento__*` | Game Engines & Tech | 11 | `unity`, `godot`, `unreal`, `gamemaker`, `framework_baixo_nivel`, `propria_corporativa` |
| `dificuldades_manutencao__*` | Maintenance Challenges | 10 | `mudancas_escopo`, `mudancas_quebram`, `prazo_curto`, `codigo_dificil`, `sem_boas_praticas` |
| `testes_jogo__*` | Game Testing Approaches | 5 | `exploratorio`, `roteiro`, `automatizado`, `agentes`, `performance` |
| `dificuldades_testes__*` | Automated Testing Barriers | 12 | `criacao_dificil`, `falta_tempo_prazo`, `elementos_subjetivos`, `limitacoes_tecnicas_engine` |
| `ferramentas_teste__*` | Testing Frameworks/Tools | 7 | `unity`, `godot_test_plugin`, `unreal`, `frameworks_gerais_software`, `ci_cd_devops` |
| `conteudo_testado__*` | Tested Game Layers | 8 | `componentes`, `integracao_e2e`, `cenarios`, `performance`, `simulacao`, `teste_fumaca` |
| `tipo_falha__*` | Bug & Failure Categories | 10 | `crash`, `desempenho_estabilidade`, `stuck`, `balanceamento`, `corretude_fisica` |
| `requisito_testes__*` | Test Execution Triggers | 5 | `nova_funcionalidade`, `atualizacao`, `proxima_fase`, `nunca` |
| `avaliacao_artefatos__*` | Artifact Evaluation | 6 | `criterios_definidos`, `testes_formais`, `avaliacao_por_outros`, `avaliacao_subjetiva` |
| `design_validacao__*` | Game Design Validation | 9 | `prototipo_real`, `prototipo_simplificado`, `excel`, `machinations`, `mental` |
| `areas_uso_ia__*` | Generative AI Usage Areas | 12 | `implementacao`, `ideias_criativas`, `conteudo_visual_sonoro`, `planejamento`, `testes` |
| `percepcao_uso_ia__*` | AI Perceptions & Concerns | 12 | `etica_dados`, `confiabilidade_transparencia`, `sem_qualidade`, `perda_visao_artistica` |
| `consideracoes_finais_classified__*` | Thematic Closing Remarks | 12 | `prefer_manal`, `hight_cost`, `no_time`, `autotests_dont_work`, `opinions_on_ai` |

### 4. Engineered Analytical Features (`Columns 200–211`)

Composite variables derived in `reclassify_csv.py` to support cross-group hypothesis testing:

* `no_use_tests`: Binary flag indicating lack of regular automated testing adoption.
* `number_of_roles`: Count of distinct development roles performed by the respondent.
* `Dev` / `OverloadedDev` / `no_use_and_overloaded`: Flags identifying programmers and multi-role ("hat-wearing") developers.
* `senioridade`: Derived professional tier (`Não profissional`: 195, `Profissional Sênior`: 19, `Profissional Pleno`: 13, `Profissional Júnior`: 4).
* `fomationAndDev`: Combined technical background profile (`Self-Taught Dev`: 120, `Formal CS Dev`: 90, `Non-Technical Role`: 21).
* `make_formal_eval` / `make_only_non_formal_eval`: Indicators of formal vs. informal QA evaluation practices.
* `knolege_and_use_tests`: Consolidated awareness and usage index for automated testing.
* `IA_Use`: Binary indicator of active AI tool adoption in game development.
* `Console_dev`: Binary indicator for developers targeting console platforms.

---

## Statistical Analysis Summary (`statistical_analysis_by_rq.csv`)

The file `statistical_analysis_by_rq.csv` reports **115 statistically significant pairwise associations** ($p < 0.05$) identified across the four research questions using Chi-Square tests of independence ($\chi^2$), effect size via **Cramér's V**, and achieved **Statistical Power**:

| Research Question | Significant Pairs | Top Association Example | Cramér's $V$ | $p$-value (`P_Final`) |
| --- | --- | --- | --- | --- |
| **RQ1:** Testing Adoption & Demographics | 8 | `no_use_tests` $\times$ `world_region` | 0.351 | 0.0158 |
| **RQ2:** Automated Testing vs. SE Practices | 25 | `uso_praticas_testes_automatizados` $\times$ `uso_praticas_integracao_continua` | 0.389 | < 0.0001 |
| **RQ3:** Complementary QA Approaches | 62 | `make_formal_eval` $\times$ `design_validacao__prototipo_simplificado` | 0.707 | < 0.0001 |
| **RQ4:** AI Tool Utilization | 20 | `areas_uso_ia__tentou_mas_sem_sucesso` $\times$ `percepcao_uso_ia__sem_resposta` | 0.350 | 0.0095 |

### Schema of `statistical_analysis_by_rq.csv`

* `RQ`: Research question identifier.
* `Base_Column` & `Compare_Column`: Pair of variables tested from `reclassifieddatanew.csv`.
* `Cramers_V`: Effect size metric ($0 \le V \le 1$).
* `Power`: Statistical power ($1 - \beta$) of the test.
* `Chi2`: Pearson's chi-square test statistic ($\chi^2$).
* `P_Final`: Adjusted $p$-value confirming statistical significance ($p < 0.05$).
* `Conclusao`: Human-readable interpretation of association strength.

---

## Reproducibility & Quick Start

### Requirements

* Python 3.10+
* `pandas`, `numpy`, `scipy`

### Running the Reclassification Pipeline

To reproduce `reclassifieddatanew.csv` from `filtereddata.csv` using the cached LLM classifications (`llm_cache.json`) and controlled vocabularies (`mapingssurvey.json`, `finalremarks.json`):

```bash
python reclassify_csv.py

```

### Example Exploratory Snippet

```python
import pandas as pd

# Load valid survey responses
df = pd.read_csv("reclassifieddatanew.csv").dropna(subset=["uid"])
stats = pd.read_csv("statistical_analysis_by_rq.csv")

print(f"Valid respondents: {len(df)}")
print(f"Significant RQ associations: {len(stats)}")
print(stats.groupby("RQ")["Cramers_V"].describe())

```

---

## Ethics, Anonymization & Licensing

* **Anonymization & Privacy:** All respondents participated voluntarily under informed consent. Records are indexed strictly by randomly generated UUIDs (`uid`), and free-text entries were inspected to remove personally identifiable information (PII) prior to publication.
* **Data License:** The datasets (`filtereddata.csv`, `reclassifieddatanew.csv`, `statistical_analysis_by_rq.csv`) and taxonomy JSON files are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
* **Code License:** The processing script (`reclassify_csv.py`) is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## Citation

If you use this dataset, taxonomy, or statistical results in your research, please cite:

```bibtex
@misc{silva2026automatedgametesting,
  author       = {Silva, Esdras Caleb Oliveira},
  title        = {Survey on Automated Game Testing, Software Engineering Practices, and AI Utilization: Open Dataset and Reclassification Pipeline},
  year         = {2026},
  publisher    = {GitHub},
  institution  = {Federal University of Rio Grande do Norte (UFRN)},
  url          = {[https://github.com/EsdrasCaleb/survey_automatestests_questionsReclassifiy](https://github.com/EsdrasCaleb/survey_automatestests_questionsReclassifiy)}
}

```
