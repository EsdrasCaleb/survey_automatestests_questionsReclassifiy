import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, MonteCarloMethod
from statsmodels.stats.power import GofChisquarePower

# ==================================
# CONFIGURATION
# ==================================
CSV_FILE = "normalizeddatacalc.csv"

DEMOGRAPHICS = [
    "idade_faixa", "world_region", "formacao","formacao_normalized", "area_formacao","experiencia_faixa",
    "projetos_faixa","situacao","situacao_equipe","duracao_projetos","funcoes__animacao","papeis_total",
	"funcoes__artista",	"funcoes__artista_som",	"funcoes__design_ux",	"funcoes__game_designer",
    "funcoes__level_designer",	"funcoes__marketing",	"funcoes__outro",	"funcoes__produtor",
    "funcoes__programador",	"funcoes__qa",	"funcoes__roteiro_narrativa",	"funcoes__tec_lead","tipo_jogo_total",
    "tipos_jogos__action",	"tipos_jogos__adventure",	"tipos_jogos__artificial_life_puzzle",
    "tipos_jogos__construction_management",	"tipos_jogos__online",	"tipos_jogos__outro",	"tipos_jogos__rpg",
    "tipos_jogos__sports",	"tipos_jogos__strategy",	"tipos_jogos__vehicle_sim","plataformas_total",
    "plataformas_desenvolvimento__console_nintendo",	"plataformas_desenvolvimento__console_psx",
    "plataformas_desenvolvimento__console_xbox",	"plataformas_desenvolvimento__mobile",
    "plataformas_desenvolvimento__outro",	"plataformas_desenvolvimento__pc",	"plataformas_desenvolvimento__web",
    "plataformas_desenvolvimento__xr",	"ferramentas_desenvolvimento__framework_baixo_nivel","ferramentas_total",
    "ferramentas_desenvolvimento__gamemaker",	"ferramentas_desenvolvimento__godot",
    "ferramentas_desenvolvimento__nada",	"ferramentas_desenvolvimento__outro",
    "ferramentas_desenvolvimento__propria_corporativa",	"ferramentas_desenvolvimento__propria_pessoal",
    "ferramentas_desenvolvimento__rpgmaker",	"ferramentas_desenvolvimento__unity",
    "ferramentas_desenvolvimento__unreal","ferramentas_teste_total",
    "ferramentas_teste__godot_test_plugin",	"ferramentas_teste__nenhuma",
    "ferramentas_teste__outro",	"ferramentas_teste__unity",	"ferramentas_teste__unreal"



]

TARGET_QUESTIONS = {
    "RQ1: Practices": [
        "uso_praticas_controle_versao",
        "uso_praticas_padroes_design",
        "uso_praticas_modelagem_projeto",
        "uso_praticas_prototipacao",
        "uso_praticas_testes_automatizados",
        "uso_praticas_integracao_continua",
        "dificuldades_manutencao__codigo_dificil",	"dificuldades_manutencao__comunicacao_dificil",
        "dificuldades_manutencao__mudancas_escopo",	"dificuldades_manutencao__mudancas_quebram",
        "dificuldades_manutencao__outro",	"dificuldades_manutencao__prazo_curto",
        "dificuldades_manutencao__sem_boas_praticas",	"dificuldades_manutencao__sem_dificuldades",
        "design_validacao__excel",	"design_validacao__machinations",	"design_validacao__mental",
        "design_validacao__nenhum",	"design_validacao__outro",	"design_validacao__prototipo_real",
        "design_validacao__prototipo_simplificado",


    ],
    "RQ2: Testing": [
        "tipo_falha__balanceamento",	"tipo_falha__corretude_fisica",	"tipo_falha__crash",
        "tipo_falha__desempenho_estabilidade",	"tipo_falha__outro",	"tipo_falha__stuck",
        "tipo_falha__visual_multimidia","testes_jogo__agentes",	"testes_jogo__automatizado",
        "testes_jogo__exploratorio",	"testes_jogo__outro",	"testes_jogo__roteiro",
        "dificuldades_testes__criacao_dificil",	"dificuldades_testes__entendimento_frameworks",
        "dificuldades_testes__integracao_dificil",	"dificuldades_testes__nao_encontram_erros_reais",
        "dificuldades_testes__nunca_usei",	"dificuldades_testes__outro",	"dificuldades_testes__preferencia_humanos",
        "conteudo_testado__cenarios",	"conteudo_testado__componentes",	"conteudo_testado__nao_uso",
        "conteudo_testado__outro",	"conteudo_testado__performance",	"conteudo_testado__simulacao",
        "conteudo_testado__teste_fumaca","etapa_testes","requisito_testes__atualizacao",
        "requisito_testes__nova_funcionalidade",	"requisito_testes__nunca",
        "requisito_testes__outro",	"requisito_testes__proxima_fase","avaliacao_artefatos__avaliacao_por_outros",
        "avaliacao_artefatos__avaliacao_subjetiva",	"avaliacao_artefatos__criterios_definidos",
        "avaliacao_artefatos__outro",	"avaliacao_artefatos__testes_formais"


    ],
    "RQ3: LLMs": [
        "areas_uso_ia__ainda_nao_usei",	"areas_uso_ia__conteudo_visual_sonoro",
        "areas_uso_ia__ideias_criativas",	"areas_uso_ia__implementacao",	"areas_uso_ia__nao_usarei",
        "areas_uso_ia__outro",	"areas_uso_ia__planejamento",	"areas_uso_ia__testes",
        "areas_uso_ia__validacao",	"percepcao_uso_ia__confiabilidade_transparencia",	"percepcao_uso_ia__etica_dados",
        "percepcao_uso_ia__outro",	"percepcao_uso_ia__privacidade",	"percepcao_uso_ia__sem_preocupacoes",
        "percepcao_uso_ia__substituicao"

    ]
}

power_calc = GofChisquarePower()

def chi_square_power(n, effect_size, dof, alpha=0.05):

    return power_calc.power(
        effect_size=effect_size,
        nobs=n,
        alpha=alpha,
        n_bins=dof + 1
    )

def cramers_v(table):
    chi2 = chi2_contingency(table)[0]
    n = table.sum().sum()
    phi2 = chi2 / n
    r, k = table.shape
    return np.sqrt(phi2 / min(k - 1, r - 1))


def get_demographic_group(name):
    # Grupos por Prefixo
    if name.startswith("funcoes__") or name in ["papeis_total"]: return "Professional Roles"
    if name.startswith("tipos_jogos__") or name in ["tipo_jogo_total"]: return "Game Genres"
    if name.startswith("plataformas_desenvolvimento__") or name in ["plataformas_total"]: return "Target Platforms"
    if name.startswith("ferramentas_desenvolvimento__") or name in ["ferramentas_total"]: return "Dev Tools/Engines"
    if name.startswith("ferramentas_teste__") or name in  ["ferramentas_teste_total"]: return "Testing Tools"

    # Grupos por Nome Específico
    if name in ["formacao", "formacao_normalized", "area_formacao"]: return "Academic Background"
    if name in ["experiencia_faixa", "projetos_faixa"]: return "Professional Experience"
    if name in ["idade_faixa", "world_region"]: return "Personal Demographics"
    if name in ["situacao", "situacao_equipe", "duracao_projetos"]: return "Project/Team Structure"

    return "Other"

def get_question_group(name):
    if name.startswith("uso_praticas_"): return "Core SE Practices"
    if name.startswith("dificuldades_manutencao__"): return "Maintenance Challenges"
    if name.startswith("design_validacao__"): return "Design Validation"
    if name.startswith("tipo_falha__"): return "Failure Types"
    if name.startswith("testes_jogo__"): return "Testing Methods"
    if name.startswith("dificuldades_testes__"): return "Testing Barriers"
    if name.startswith("conteudo_testado__"): return "Testing Scope"
    if name.startswith("requisito_testes__"): return "Test Triggers"
    if name.startswith("avaliacao_artefatos__"): return "Artifact Evaluation"
    if name.startswith("areas_uso_ia__"): return "AI/LLM Application Areas"
    if name.startswith("percepcao_uso_ia__"): return "AI/LLM Perception/Ethics"
    return name

# Armazenamento para o resumo final
stats_results = []

df = pd.read_csv(CSV_FILE)

# ==================================
# EXECUTION ENGINE
# ==================================

for rq_name, questions in TARGET_QUESTIONS.items():
    for q_col in questions:
        for d_col in DEMOGRAPHICS:

            # 1. Criação da Tabela
            table = pd.crosstab(df[d_col], df[q_col])
            if table.size == 0 or table.shape[0] < 2 or table.shape[1] < 2:
                print("Skipping: Table too small for analysis.")
                continue

            # 2. Cálculos Base
            chi2, p_classical, dof, expected = chi2_contingency(table)
            expected_df = pd.DataFrame(expected, index=table.index, columns=table.columns)
            residuals = (table - expected_df) / np.sqrt(expected_df)
            v_cramer = cramers_v(table)

            n_obs = table.to_numpy().sum()

            power = chi_square_power(
                n_obs,
                v_cramer,
                dof
            )

            # 3. Verificação de Premissas (Criterio de Cochran)
            small_cells = (expected_df < 5).sum().sum()
            total_cells = expected_df.size
            ratio = small_cells / total_cells

            # 4. Monte Carlo (se necessário)
            mc = MonteCarloMethod(n_resamples=10000)
            # ADICIONADO: correction=False para evitar o conflito com Monte Carlo
            res_mc = chi2_contingency(table, correction=False, method=mc)
            p_mc = res_mc.pvalue

            final_p = p_mc if ratio > 0.2 else p_classical
            p_source = "Monte Carlo" if ratio > 0.2 else "Classical"

            if final_p < 0.05:
                print("\n" + "=" * 80)
                print(f"TEST: {d_col} vs {q_col} ({rq_name})")
                print("=" * 80)
                print("\n>>> RESULT: SIGNIFICANT ASSOCIATION DETECTED")
                print(f"Assumptions: {small_cells}/{total_cells} cells < 5 ({ratio:.1%}) -> Using {p_source}")
                print(f"Statistical Power: {power:.3f}")
                # =========================
                # IMPRESSÃO DO RELATÓRIO DETALHADO
                # =========================
                # print("\n--- SAMPLE BALANCE & PROPORTIONS ---")
                # print(table.div(table.sum(axis=1), axis=0).round(3))
                print("\n--- OBSERVED ---")
                print(table)

                print("\n--- EXPECTED ---")
                print(expected_df.round(2))

                print("\n--- TOP CONTRIBUTIONS (Residuals) ---")
                top_res = residuals.stack().sort_values(ascending=False)
                print(f"Over-represented (+):\n{top_res.head(3)}")
                print(f"Under-represented (-):\n{top_res.tail(3)}")

                print("\n--- METRICS ---")
                print(f"Chi2: {chi2:.4f} | Cramer's V: {v_cramer:.4f}")
                print(f"P-classical: {p_classical:.3e} | P-MonteCarlo: {p_mc:.3e}")
                # Salva para o ranking final
                stats_results.append({
                    "RQ": rq_name,
                    "Demographic": d_col,
                    "Cramers_V": v_cramer,
                    "Question": q_col,
                    "Power": power,
                    "Chi2": chi2,
                    "P-classical": p_classical,
                    "P-MonteCarlo": p_mc,
                    "ratio":ratio
                })
            # else:
            #     print("\n>>> RESULT: NOT SIGNIFICANT")

# ==================================
# FINAL SUMMARY: IMPACT RANKING
# ==================================

print("\n\n" + "#" * 60)
print(" FINAL IMPACT RANKING BY RESEARCH QUESTION ")
print("#" * 60)

results_df = pd.DataFrame(stats_results)

if not results_df.empty:
    df_export = pd.DataFrame(stats_results)

    # Salvamos em CSV
    # index=False evita que o pandas crie uma coluna extra de números
    #df_export.to_csv("statistical_analysis.csv", index=False, encoding='utf-8')

    # 1. Agregação completa: Média, Mediana, Desvio Padrão e Contagem
    # Nota: 'std' (Standard Deviation) é o desvio padrão no Pandas
    ranking = results_df.groupby(['RQ', 'Demographic']).agg(
        mean_v=('Cramers_V', 'mean'),
        median_v=('Cramers_V', 'median'),
        std_v=('Cramers_V', 'std'),
        count=('Cramers_V', 'count'),
        mean_power=('Power', 'mean'),
        median_power=('Power', 'median'),
        std_power=('Power', 'std')
    ).reset_index()

    # Onde houver apenas 1 questão significante, o desvio padrão será NaN.
    # Vamos preencher com 0.0 para o relatório ficar limpo.
    ranking = ranking.fillna(0)

    # 2. Ordenação: Prioridade para Consistência (count), depois Força (mean_v)
    ranking = ranking.sort_values(
        by=['RQ', 'count', 'mean_v', 'mean_power'],
        ascending=[True, False, False, False]
    )

    print("\n" + "#" * 105)
    print(f"{'FINAL AGGREGATED IMPACT REPORT':^105}")
    print("#" * 105)

    for rq in TARGET_QUESTIONS.keys():
        total_q = len(TARGET_QUESTIONS[rq])
        rq_rank = ranking[ranking['RQ'] == rq]

        print(f"\n>>> {rq.upper()}")
        print("-" * 105)
        # Cabeçalho da Tabela
        print(
            f"{'Demographic Factor':<30} | {'Consist.':<8} | {'Cramér V (μ ± σ)':<22} | {'Power (μ ± σ)':<22} | {'Med. V'} | {'Med. Power'}")
        print("-" * 105)

        if rq_rank.empty:
            print(f"{'No significant factors found.':^105}")
        else:
            for _, row in rq_rank.iterrows():
                count_sig = int(row['count'])

                # Formatação μ ± σ (Média ± Desvio Padrão)
                v_metric = f"{row['mean_v']:.3f} ± {row['std_v']:.3f}"
                p_metric = f"{row['mean_power']:.3f} ± {row['std_power']:.3f}"
                consistency = f"{count_sig}/{total_q}"

                print(
                    f"  {row['Demographic']:<28} | {consistency:^8} | {v_metric:<22} | {p_metric:<22} | {row['median_v']:.3f} | {row['median_power']:.3f}")

    print("-" * 105)

    # ============================================================
    # RELATÓRIO DE IMPACTO POR GRUPOS TEMÁTICOS (DEMO vs QUESTÕES)
    # ============================================================

    results_df['Demo_Group'] = results_df['Demographic'].apply(get_demographic_group)
    results_df['Question_Group'] = results_df['Question'].apply(get_question_group)

    # 2. Agregação por Grupo de Demografia
    # Aqui vemos quantas questões únicas DE CADA TIPO o grupo demográfico afeta
    group_summary = results_df.groupby(['RQ', 'Demo_Group']).agg(
        unique_questions=('Question', 'nunique'),
        unique_q_groups=('Question_Group', 'nunique'),
        mean_v=('Cramers_V', 'mean'),
        std_v=('Cramers_V', 'std'),
        mean_p=('Power', 'mean'),
        std_p=('Power', 'std')
    ).reset_index().fillna(0)

    # Ordenação
    group_summary = group_summary.sort_values(['RQ', 'unique_questions'], ascending=[True, False])

    # Exportação para CSV (opcional)
    group_summary.to_csv("thematic_impact_summary.csv", index=False)
    # 1. Garantir que as colunas de mapeamento existem
    results_df['Demo_Group'] = results_df['Demographic'].apply(get_demographic_group)
    results_df['Question_Group'] = results_df['Question'].apply(get_question_group)

    # 2. Agregação por RQ, Grupo Demográfico E Subgrupo de Questão
    subgroup_ranking = results_df.groupby(['RQ', 'Demo_Group', 'Question_Group']).agg(
        unique_questions=('Question', 'nunique'),
        mean_v=('Cramers_V', 'mean'),
        std_v=('Cramers_V', 'std'),
        mean_p=('Power', 'mean'),
        std_p=('Power', 'std')
    ).reset_index().fillna(0)

    # 3. Ordenação para facilitar a leitura no artigo
    subgroup_ranking = subgroup_ranking.sort_values(
        by=['RQ', 'Demo_Group', 'unique_questions'],
        ascending=[True, True, False]
    )

    # Exportação para CSV
    subgroup_ranking.to_csv("detailed_subgroup_analysis.csv", index=False)

    print("\n" + "#" * 135)
    print(f"{'DETAILED IMPACT ANALYSIS: DEMOGRAPHIC GROUPS vs QUESTION SUB-GROUPS':^135}")
    print("#" * 135)

    for rq in TARGET_QUESTIONS.keys():
        print(f"\n>>> {rq.upper()}")
        print("-" * 135)
        # Cabeçalho formatado
        print(
            f"{'Demographic Group':<25} | {'Question Sub-Group':<25} | {'Reach':<12} | {'Cramér V (μ ± σ)':<25} | {'Power (μ ± σ)':<25}")
        print("-" * 135)

        rq_sub = subgroup_ranking[subgroup_ranking['RQ'] == rq]

        if rq_sub.empty:
            print(f"{'No significant patterns found.':^135}")
        else:
            current_demo_group = ""
            for _, row in rq_sub.iterrows():
                # Lógica para não repetir o nome do grupo demográfico na mesma RQ (deixa a tabela mais limpa)
                display_demo = row['Demo_Group'] if row['Demo_Group'] != current_demo_group else ""
                current_demo_group = row['Demo_Group']

                # Para o Reach, precisamos saber quantas questões existem NO TOTAL naquele subgrupo
                # Vamos filtrar TARGET_QUESTIONS para contar quantas questões pertencem a este Question_Group
                total_in_subgroup = sum(
                    1 for q in TARGET_QUESTIONS[rq] if get_question_group(q) == row['Question_Group'])
                reach_str = f"{int(row['unique_questions'])}/{total_in_subgroup}"

                v_metric = f"{row['mean_v']:.3f} ± {row['std_v']:.3f}"
                p_metric = f"{row['mean_p']:.3f} ± {row['std_p']:.3f}"

                if display_demo != "":
                    print(
                        f"{display_demo:<25} | {row['Question_Group']:<25} | {reach_str:^12} | {v_metric:<25} | {p_metric:<25}")
                else:
                    # Se for o mesmo grupo demográfico, coloca um recuo para as outras categorias
                    print(f"{'':<25} | {row['Question_Group']:<25} | {reach_str:^12} | {v_metric:<25} | {p_metric:<25}")

    print("-" * 135)
    print("Detailed subgroup report saved to 'detailed_subgroup_analysis.csv'")
else:
    print("\nNo significant results to aggregate.")