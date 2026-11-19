from collections import Counter, defaultdict
import json
import re
import pandas as pd

# Mapeamento de quais opções são consideradas NOVAS CATEGORIAS em cada coluna
NEW_CATEGORIES = {
    "area_formacao_outro": [
        "Other STEM",
        "Other Humanities and Social Sciences",
        "Other Biological Sciences",
    ],
    "situacao_outro": [
        "I worked full-time at a game industry company",
        "I develop games as part of academic or educational activities",
        (
            "I do not develop games, only follow industry news and consumption"
            " trends"
        ),
        "I work full-time at a adjacent game industry company",
    ],
    "funcoes_outro": [],
    "tipos_jogos_outro": [
        "Casual, Cozy, and Social Games",
        "Educational and Serious Games",
        "Unspecified",
    ],
    "plataformas_desenvolvimento_outro": [],
    "ferramentas_desenvolvimento_outro": [
        (
            "Other Game Engines (Construct, GDevelop, Defold, Ren'Py, Cryengine,"
            " etc.)"
        ),
        "Unspecified",
    ],
    "dificuldades_testes_outro": [
        "Difficulty understanding how testing tools work.",
        "Complication integrating tests into the project workflow.",
        "The feeling that manual tests are more practical or efficient.",
        "Difficult to develop and keep the tests up-to-date.",
        "Perception that automated tests do not find the \"bugs that matter\".",
        "I have never tried using automated tests.",
        "Lack of time, strict deadlines, or unfavorable cost-benefit ratio.",
        "Difficulty testing subjective elements (\"game feel\", player experience) or non-deterministic gameplay.",
        "Technical limitations of the game engine, architecture, or visual scripting (e.g., Unity, Blueprints).",
        "Team limitations (difficulty training team members or getting them on board).",
        "None"
    ],
    "ferramentas_teste_outro": [
        (
            "Custom, In-house, or Proprietary Testing Tools (including custom"
            " bots)"
        ),
        (
            "General Software Testing Frameworks (NUnit, Jest, Pytest, Rust/C++"
            " units, Playwright, etc.)"
        ),
        (
            "CI/CD and DevOps Automation Tools (GitHub Actions, TeamCity,"
            " SonarQube, etc.)"
        ),
    ],
    "conteudo_testado_outro": [
        (
            "Integration and End-to-End (E2E) Testing — I test how multiple"
            " components, sub-systems, or features work together."
        ),
        (
            "Backend, Server, and External Services — I test APIs, databases,"
            " server logic, or network services outside the game client."
        ),
    ],
    "tipo_falha_outro": [
        (
            "Networking, Sync, Backend, and Infrastructure Issues (e.g.,"
            " replication, server downtime, security)"
        ),
        (
            "Core Design Flaws, Boring Gameplay Loops, or Lack of Player"
            " Engagement"
        ),
        "Business, Monetization, and Financial Risks",
        (
            "Not Applicable (e.g., out-of-scope roles, meta-responses, personal"
            " motivation)"
        ),
    ],
    "etapa_testes_outro": [
        (
            "It depends on the project/system, or I use a hybrid approach"
            " (combination of phases)"
        ),
        (
            "I do not know, or I am not the person responsible for implementing"
            " tests"
        ),
        "Invalid response, critique of the survey, or out of scope",
    ],
    "avaliacao_artefatos_outro": [
        (
            "Informal external feedback (e.g., sharing with friends, online"
            " communities like Reddit)"
        ),
        "Not yet evaluating",
    ],
    "design_validacao_outro": [
        "Writing documents, mind maps, diagrams, or narrative explorations",
        "Discussions, meetings, or feedback from team members and clients",
        "Unspecified",
    ],
    "areas_uso_ia_outro": [
        (
            "Research, Learning, and Understanding Documentation (e.g., advanced"
            " search, explaining code, math)"
        ),
        (
            "Prototyping, Tooling, and Placeholders (e.g., quick scripts,"
            " temporary programmer art)"
        ),
        (
            "Text Refinement and Localization (e.g., spellchecking, translation,"
            " thesaurus)"
        ),
        "Tried but found unhelpful",
    ],
    "percepcao_uso_ia_outro": [
        (
            "Low quality output, technical debt, bugs, and increased review"
            " time (e.g., 'AI Slop')"
        ),
        "Loss of human skills, cognitive debt, and over-reliance on AI",
        "Loss of artistic intent, lack of originality, and poor creative control",
        "Environmental and ecological impacts (e.g., power consumption)",
        "Security vulnerabilities and safety risks of AI agents",
        "Negative public perception and potential reputation damage",
        "Do not want answer",
    ],
    "dificuldades_manutencao_outro":[
        "Technology, engine, framework, and tool limitations",
        "Maintaining focus and motivation"
    ]
}


def load_json(filepath):
    """Carrega um arquivo JSON informando a codificação UTF-8."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_desc_to_key_map(categories_json):
    """Inverte o JSON de categorias para mapear descrições para as chaves curtas."""
    desc_to_key = {}
    for col, mapping in categories_json.items():
        desc_to_key[col] = {v.strip(): k for k, v in mapping.items()}
    return desc_to_key


def normalize_categories(mapped_val):
    """Garante que o valor do remapeamento seja uma lista de strings limpas."""
    if isinstance(mapped_val, str):
        return [mapped_val.strip()]
    elif isinstance(mapped_val, list):
        return [item.strip() for item in mapped_val if isinstance(item, str)]
    return []


def update_base_column(current_val, new_keys, outro_keyword="outro"):
    """Remove 'outro' e adiciona as novas chaves sem duplicar."""
    if pd.isna(current_val):
        existing_items = []
    elif isinstance(current_val, str):
        existing_items = [
            x.strip() for x in re.split(r"[,;]", current_val) if x.strip()
        ]
    else:
        existing_items = [str(current_val).strip()]

    # Remove 'outro'
    filtered_items = [
        item
        for item in existing_items
        if item.lower() != outro_keyword.lower()
    ]

    # Adiciona as novas chaves
    for key in new_keys:
        if key not in filtered_items:
            filtered_items.append(key)

    return ", ".join(filtered_items)


def process_reclassification(
    csv_path, categories_json_path, remapping_json_path, output_csv_path
):
    print("⏳ Carregando dados e arquivos JSON...")
    df = pd.read_csv(csv_path)
    categories = load_json(categories_json_path)
    remapping = load_json(remapping_json_path)

    desc_to_key = build_desc_to_key_map(categories)

    # Prepara conjunto de novas categorias para busca rápida
    new_categories_set = {
        col: {item.strip() for item in items}
        for col, items in NEW_CATEGORIES.items()
    }

    # Contadores
    modified_count = 0
    new_category_counts = defaultdict(Counter)
    total_new_assignments = 0

    # Processa cada coluna presente no mapa de remapeamento
    for outro_col, response_map in remapping.items():
        if outro_col not in df.columns:
            continue

        # Trata o caso de consideracoes_finais e similares
        if outro_col.startswith("consideracoes_finais"):
            target_col = "consideracoes_finais_classified"
            is_new_column = True
        else:
            target_col = outro_col.replace("_outro", "")
            is_new_column = False

        # Se for criar uma nova coluna, inicializa com None se ainda não existir
        if is_new_column and target_col not in df.columns:
            df[target_col] = None
        elif not is_new_column and target_col not in df.columns:
            continue

        col_desc_map = desc_to_key.get(outro_col, {})

        # Varre cada linha do CSV
        for idx in df.index:
            raw_response = df.at[idx, outro_col]

            if pd.isna(raw_response):
                continue

            raw_response_str = str(raw_response).strip()

            if raw_response_str in response_map:
                mapped_descriptions = normalize_categories(
                    response_map[raw_response_str]
                )

                reclassified_keys = []
                for desc in mapped_descriptions:
                    desc_clean = desc.strip()

                    # Contabiliza se for uma categoria NOVA
                    if desc_clean in new_categories_set.get(outro_col, set()):
                        new_category_counts[outro_col][desc_clean] += 1
                        total_new_assignments += 1

                    # Mapeia para a chave curta
                    reclassified_keys.append(
                        col_desc_map.get(desc_clean, desc_clean)
                    )

                if reclassified_keys:
                    if is_new_column:
                        # Em nova coluna, salva diretamente as chaves sem mesclar/filtrar 'outro'
                        df.at[idx, target_col] = ", ".join(reclassified_keys)
                    else:
                        current_base_val = df.at[idx, target_col]
                        updated_val = update_base_column(
                            current_base_val, reclassified_keys
                        )
                        df.at[idx, target_col] = updated_val

                    modified_count += 1

    # Salva o resultado
    df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

    # 📊 EXIBIÇÃO DO RELATÓRIO DE CONTAGEM
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE USO DAS NOVAS CLASSIFICAÇÕES")
    print("=" * 60)

    if not new_category_counts:
        print("Nenhuma nova classificação foi atribuída.")
    else:
        for outro_col, counts in new_category_counts.items():
            base_col = (
                "consideracoes_finais_classified"
                if outro_col.startswith("consideracoes_finais")
                else outro_col.replace("_outro", "")
            )
            print(f"\n🔹 Coluna Alvo: {base_col} (origem: {outro_col})")
            print(f"   Subtotal nesta coluna: {sum(counts.values())} usos")
            for cat_name, count in counts.items():
                print(f"   • [{count:3d}x] {cat_name}")

    print("\n" + "-" * 60)
    print(f"✅ Processamento concluído com sucesso!")
    print(f"📋 Total de registros atualizados no CSV: {modified_count}")
    print(
        f"🎯 Total de atribuições a NOVAS categorias: {total_new_assignments}"
    )
    print(f"💾 Arquivo salvo em: {output_csv_path}")
    print("=" * 60)


if __name__ == "__main__":
    process_reclassification(
        csv_path="filtereddata.csv",
        categories_json_path="mapingssurvey.json",
        remapping_json_path="llm_cache.json",
        output_csv_path="reclassifieddata.csv",
    )