import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from statsmodels.stats.power import GofChisquarePower

# ==================================
# CONFIGURAÇÃO
# ==================================
CSV_FILE = "reclassifieddatanew.csv"

TARGET_RELATIONS = {
    "RQ1: Testing Adoption & Demographics": {
        "base_cols": [
            "knolege_and_use",
            "no_use_tests",
            "make_formal_eval",
            "make_only_non_formal_eval",
            "uso_praticas_testes_automatizados",
        ],
        "compare_cols": [
            # Perfil Profissional, Sênior e Sobrecarga
            "senioridade",
            "formacao",
            "area_formacao",
            "fomationAndDev",
            "number_of_roles",
            "DevOverloadedDev",
            "idade_faixa",
            "world_region",
            "experiencia_faixa",
            "projetos_faixa",
            "situacao",
            "situacao_equipe",
            "duracao_projetos",

            # Engines / Ferramentas de Desenvolvimento
            "ferramentas_desenvolvimento__unity",
            "ferramentas_desenvolvimento__unreal",
            "ferramentas_desenvolvimento__godot",

            # Plataformas de Desenvolvimento (Q12 reclassificada)
            "plataformas_desenvolvimento__analog_games",
            "plataformas_desenvolvimento__console_nintendo",
            "plataformas_desenvolvimento__console_psx",
            "plataformas_desenvolvimento__console_retro",
            "plataformas_desenvolvimento__console_xbox",
            "plataformas_desenvolvimento__mobile",
            "plataformas_desenvolvimento__pc",
            "plataformas_desenvolvimento__web",
            "plataformas_desenvolvimento__xr",
            "Console_dev"
        ]
    },
    "RQ2: Automated Testing vs SE Practices": {
        "base_cols": [
            "uso_praticas_testes_automatizados",
            "knolege_and_use",
            "no_use_tests",
            "fomationAndDev",
            "senioridade",
            "area_formacao",
            "fomationAndDev",
            "Console_dev",
            "tipo_falha__balanceamento",
            "tipo_falha__corretude_fisica",
            "tipo_falha__crash",
            "tipo_falha__desempenho_estabilidade",
            "tipo_falha__falhas_design_gameplay_chato",
            "tipo_falha__infraestrutura_rede_sync",
            "tipo_falha__nao_se_aplica",
            "tipo_falha__negocios_monetizacao_financeiro",
            "tipo_falha__stuck",
            "tipo_falha__visual_multimidia"
        ],
        "compare_cols": [
            "uso_praticas_controle_versao",
            "uso_praticas_padroes_design",
            "uso_praticas_modelagem_projeto",
            "uso_praticas_prototipacao",
            "uso_praticas_integracao_continua",
            "uso_praticas_testes_automatizados",
        ]
    },
    "RQ3: Complementary QA Approaches": {
        "base_cols": [
            "no_use_tests",
            "no_use_and_overloaded",
            "make_formal_eval",
            "make_only_non_formal_eval",
            "Console_dev",
            "tipo_falha__balanceamento",
            "tipo_falha__corretude_fisica",
            "tipo_falha__crash",
            "tipo_falha__desempenho_estabilidade",
            "tipo_falha__falhas_design_gameplay_chato",
            "tipo_falha__infraestrutura_rede_sync",
            "tipo_falha__nao_se_aplica",
            "tipo_falha__negocios_monetizacao_financeiro",
            "tipo_falha__stuck",
            "tipo_falha__visual_multimidia"
        ],
        "compare_cols": [
            # Formas de Teste de Jogo (testes_jogo__*)
            "testes_jogo__agentes",
            "testes_jogo__automatizado",
            "testes_jogo__exploratorio",
            "testes_jogo__performance",
            "testes_jogo__roteiro",

            # Validação do Game Design (design_validacao__*)
            "design_validacao__documentos_mapas_diagramas",
            "design_validacao__excel",
            "design_validacao__machinations",
            "design_validacao__mental",
            "design_validacao__nao_especificado",
            "design_validacao__nenhum",
            "design_validacao__prototipo_real",
            "design_validacao__prototipo_simplificado",
            "design_validacao__reunioes_feedback_equipe",

            # Avaliação de Artefatos Criativos (avaliacao_artefatos__*)
            "avaliacao_artefatos__ainda_nao_avalia",
            "avaliacao_artefatos__avaliacao_por_outros",
            "avaliacao_artefatos__avaliacao_subjetiva",
            "avaliacao_artefatos__criterios_definidos",
            "avaliacao_artefatos__feedback_externo_informal",
            "avaliacao_artefatos__testes_formais",

            # Tipos de Falha Priorizados para Evitar (tipo_falha__*)
            "tipo_falha__balanceamento",
            "tipo_falha__corretude_fisica",
            "tipo_falha__crash",
            "tipo_falha__desempenho_estabilidade",
            "tipo_falha__falhas_design_gameplay_chato",
            "tipo_falha__infraestrutura_rede_sync",
            "tipo_falha__nao_se_aplica",
            "tipo_falha__negocios_monetizacao_financeiro",
            "tipo_falha__stuck",
            "tipo_falha__visual_multimidia"
        ]
    },
    "RQ4: AI Tool Utilization": {
        "base_cols": [
            # Campos de Perfil de Teste e IA Geral
            "knolege_and_use",
            "no_use_tests",
            "IA_Use",

            # Todas as Áreas de Uso de IA (Q25 reclassificada)
            "areas_uso_ia__ainda_nao_usei",
            "areas_uso_ia__conteudo_visual_sonoro",
            "areas_uso_ia__ideias_criativas",
            "areas_uso_ia__implementacao",
            "areas_uso_ia__nao_usarei",
            "areas_uso_ia__pesquisa_documentacao_aprendizado",
            "areas_uso_ia__planejamento",
            "areas_uso_ia__prototipagem_placeholders_ferramentas",
            "areas_uso_ia__refinamento_texto_localizacao",
            "areas_uso_ia__tentou_mas_sem_sucesso",
            "areas_uso_ia__testes",
            "areas_uso_ia__validacao"
        ],
        "compare_cols": [
            # Todas as Preocupações/Percepções de IA (Q26 reclassificada)
            "percepcao_uso_ia__confiabilidade_transparencia",
            "percepcao_uso_ia__etica_dados",
            "percepcao_uso_ia__impacto_ambiental",
            "percepcao_uso_ia__perda_de_habilidade",
            "percepcao_uso_ia__perda_visao_artistica",
            "percepcao_uso_ia__privacidade",
            "percepcao_uso_ia__reputacao_opiniao_publica",
            "percepcao_uso_ia__seguranca_vulnerabilidade",
            "percepcao_uso_ia__sem_preocupacoes",
            "percepcao_uso_ia__sem_qualidade",
            "percepcao_uso_ia__sem_resposta",
            "percepcao_uso_ia__substituicao",
            "consideracoes_finais_classified__opinions_on_ai"
        ]
    }
}

power_calc = GofChisquarePower()


def chi_square_power(n, effect_size, dof, alpha=0.05):
    if dof <= 0 or effect_size <= 0:
        return 0.0
    return power_calc.power(
        effect_size=effect_size,
        nobs=n,
        alpha=alpha,
        n_bins=dof + 1
    )


def cramers_v(table):
    chi2 = chi2_contingency(table)[0]
    n = table.sum().sum()
    if n == 0:
        return 0.0
    phi2 = chi2 / n
    r, k = table.shape
    min_dim = min(k - 1, r - 1)
    if min_dim <= 0:
        return 0.0
    return np.sqrt(phi2 / min_dim)


def monte_carlo_chi2(table, n_resamples=10000):
    """Simulação de Monte Carlo robusta para p-valor do Qui-Quadrado."""
    obs_chi2 = chi2_contingency(table, correction=False)[0]
    r_sums = table.sum(axis=1).values
    c_sums = table.sum(axis=0).values
    n = table.values.sum()

    rows = np.repeat(np.arange(len(r_sums)), r_sums)
    cols = np.repeat(np.arange(len(c_sums)), c_sums)

    greater = 0
    for _ in range(n_resamples):
        cols_shuffled = np.random.permutation(cols)
        perm_tab = np.bincount(rows * len(c_sums) + cols_shuffled, minlength=len(r_sums) * len(c_sums)).reshape(
            len(r_sums), len(c_sums))
        exp = np.outer(r_sums, c_sums) / n
        with np.errstate(divide='ignore', invalid='ignore'):
            chi2_stat = np.nan_to_num(np.sum((perm_tab - exp) ** 2 / exp))
        if chi2_stat >= obs_chi2:
            greater += 1
    return greater / n_resamples


def classificar_conclusao(v_cramer, p_val):
    """Gera o texto de conclusão interpretável com base no p-valor e Cramer's V."""
    if p_val >= 0.05:
        return "Sem associação significativa (Hipótese Nula mantida)"

    if v_cramer < 0.10:
        intensidade = "Associação Muito Fraca / Desprezível"
    elif v_cramer < 0.30:
        intensidade = "Associação Fraca"
    elif v_cramer < 0.50:
        intensidade = "Associação Moderada"
    else:
        intensidade = "Associação Forte"

    return f"Existe relação ({intensidade}, V={v_cramer:.3f})"


# ==================================
# MOTOR DE EXECUÇÃO
# ==================================

df = pd.read_csv(CSV_FILE)
stats_results = []

print("Iniciando análise cruzada por RQ...\n")

for rq_name, config in TARGET_RELATIONS.items():
    base_cols = config.get("base_cols", [])
    compare_cols = config.get("compare_cols", [])

    for b_col in base_cols:
        for c_col in compare_cols:
            if b_col == c_col or b_col not in df.columns or c_col not in df.columns:
                continue

            table = pd.crosstab(df[b_col], df[c_col])
            if table.size == 0 or table.shape[0] < 2 or table.shape[1] < 2:
                continue

            # 1. Estatísticas de Base
            chi2, _, dof, _ = chi2_contingency(table)
            v_cramer = cramers_v(table)
            n_obs = table.to_numpy().sum()
            power = chi_square_power(n_obs, v_cramer, dof)

            # 2. P-Valor Direto via Monte Carlo (10.000 reamostragens)
            p_final = monte_carlo_chi2(table, n_resamples=10000)

            # 3. Somente Hipóteses Nulas Rejeitadas (p < 0.05)
            if p_final < 0.05:
                conclusao_txt = classificar_conclusao(v_cramer, p_final)
                stats_results.append({
                    "RQ": rq_name,
                    "Base_Column": b_col,
                    "Compare_Column": c_col,
                    "Cramers_V": v_cramer,
                    "Power": power,
                    "Chi2": chi2,
                    "P_Final": p_final,
                    "Conclusao": conclusao_txt
                })

# ==================================
# RELATÓRIO FINAL E EXPORTAÇÃO
# ==================================

results_df = pd.DataFrame(stats_results)

if not results_df.empty:
    results_df.to_csv("statistical_analysis_by_rq.csv", index=False, encoding='utf-8')

    print("\n" + "#" * 115)
    print(" RESUMO DAS RELAÇÕES SIGNIFICATIVAS POR RESEARCH QUESTION ")
    print("#" * 115)

    for rq in TARGET_RELATIONS.keys():
        rq_df = results_df[results_df["RQ"] == rq]
        print(f"\n>>> {rq.upper()}")
        print("-" * 115)
        print(
            f"{'Base Column':<25} | {'Compare Column':<28} | {'Cramer V':<9} | {'Power':<7} | {'p-Value':<8} | {'Conclusão'}")
        print("-" * 115)

        if rq_df.empty:
            print(f"{'Nenhuma relação significativa encontrada (Hipótese Nula mantida).':^115}")
        else:
            for _, row in rq_df.iterrows():
                print(
                    f"  {row['Base_Column']:<23} | {row['Compare_Column']:<28} | {row['Cramers_V']:<9.3f} | {row['Power']:<7.3f} | {row['P_Final']:<8.4f} | {row['Conclusao']}"
                )

    print("-" * 115)
    print("\nResultados salvos com sucesso no arquivo 'statistical_analysis_by_rq.csv'.")

    # ============================================================
    # EXPLICAÇÃO DAS COLUNAS IMPRESSA NA TELA
    # ============================================================
    print("\n" + "=" * 80)
    print(" DICIONÁRIO E LEGENDA DAS COLUNAS DO RELATÓRIO / CSV ")
    print("=" * 80)
    explicacoes_colunas = {
        "RQ": "Identificador da Questão de Pesquisa (Research Question).",
        "Base_Column": "Variável principal/foco sob análise naquela relação.",
        "Compare_Column": "Variável secundária cruzada com a variável base.",
        "Cramers_V": "Mede a INTENSIDADE da associação entre as duas variáveis categóricas (varia de 0.0 a 1.0).",
        "Power": "Poder estatístico do teste (1 - β). Valores próximos a 1.0 indicam alta capacidade de evitar falsos negativos.",
        "Chi2": "Valor da estatística de teste Qui-Quadrado de independência.",
        "P_Final": "Valor-p (p-value) calculado via simulação de Monte Carlo com 10.000 reamostragens (Significativo se p < 0.05).",
        "Conclusao": "Interpretação direta: declara se existe relação estatisticamente significativa e classifica a força da associação (Fraca, Moderada, Forte) com base no V de Cramer."
    }

    for col, desc in explicacoes_colunas.items():
        print(f"• {col:<15} : {desc}")
    print("=" * 80 + "\n")

else:
    print("\nNenhuma relação estatisticamente significativa foi encontrada.")