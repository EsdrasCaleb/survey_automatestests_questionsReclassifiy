import os
import re
import time
import pandas as pd
import numpy as np
import json
import requests
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURAÇÃO DE ALTERNÂNCIA DE MODELO
# ==========================================
# Mude para True para usar o Gemma local ou False para usar o Mistral (com timeout)
USAR_GEMMA = False

# Arquivo onde o cache das requisições será armazenado
CACHE_FILE = "llm_cache.json"


# ==========================================
# GERENCIAMENTO DE CACHE JSON
# ==========================================
def carregar_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                print(f"📦 Cache carregado com sucesso de '{CACHE_FILE}'!")
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Erro ao ler arquivo de cache: {e}. Iniciando um cache novo.")
    return {}


def salvar_cache(cache_data):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Erro ao salvar o cache no disco: {e}")


# ==========================================
# CHAMADAS AOS MODELOS (MISTRAL & GEMMA)
# ==========================================
MODEL_NAME = "google/gemma-4-E2B-it-qat-mobile-transformers"
gemma_generator = None


def ask_gemma(prompt):
    global gemma_generator

    if gemma_generator is None:
        try:
            print("🤖 Inicializando pipeline do Gemma local na GPU...")
            gemma_generator = pipeline(
                "text-generation",
                model=MODEL_NAME,
                device_map="auto"
            )
        except Exception as e:
            print(f"⚠️ Não foi possível usar device_map (GPU). Carregando na CPU... Erro: {e}")
            gemma_generator = pipeline(
                "text-generation",
                model=MODEL_NAME,
                device=-1  # Força o uso da CPU
            )

    messages = [{"role": "user", "content": prompt}]
    outputs = gemma_generator(
        messages,
        max_new_tokens=1024,
        temperature=0.1
    )
    return outputs[0]["generated_text"][-1]["content"]


def ask_mistral(prompt, model="mistral-large-latest"):
    # Espera recomendada para evitar atingir o Rate Limit (Too Many Requests)
    print("⏳ Aguardando 60 segundos para respeitar o limite da API (Rate Limit)...")
    time.sleep(60)

    response = requests.post(
        "https://api.mistral.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ.get('MISTRAL_API_KEY')}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"}  # Força o Mistral a retornar JSON puro, evitando markdown
        },
        timeout=300
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def ask_llm(prompt):
    """
    Roteador inteligente que decide qual modelo chamar com base na configuração global.
    """
    if USAR_GEMMA:
        print("🔮 Chamando Gemma local...")
        return ask_gemma(prompt)
    else:
        print("☁️ Chamando Mistral API...")
        return ask_mistral(prompt)


# ==========================================
# CONFIGURAÇÃO DOS MODELOS DO HUGGING FACE
# ==========================================
# print("Carregando modelo de embeddings para deduplicação...")
# embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

CATEGORIES_MAPPING = {
    "area_formacao_outro": [
        "Computer Science, Information Systems, and Software-Focused Engineering (Computer Engineering, Software Engineering, Telecommunications, Networking)",
        "Engineering (other fields)",
        "Game Design / Digital Game Development",
        "Graphic Design / Visual Arts / Animation",
        "Music / Audio Production",
        "Communication / Digital Media / Multimedia",
        "Self-taught (no formal education in the field)",
        #novas
        "Other STEM",
        "Other Humanities and Social Sciences",
        "Other Biological Sciences"
    ],
    "situacao_outro": [
        "I work full-time at a game industry company",
        "I work part-time at a game industry company",
        "I develop games as a freelancer/contractor regularly",
        "I develop independent games in my spare time (hobbyist/unpaid or occasional revenue)",
        "I develop games occasionally, in one-off or collaborative projects (e.g., Game Jams)",
        #novos
        "I worked full-time at a game industry company",
        "I develop games as part of academic or educational activities",
        "I do not develop games, only follow industry news and consumption trends",
        "I work full-time at a adjacent game industry company"
    ],
    "situacao_equipe_outro":[
        "Work alone (individual projects)",
        "In a Small Team (2 to 15 people)",
        "In a Medium Team (15 to 60 people)",
        "In a Large Team (60 to 120 people)",
         "In a Very Large Team (120+ people)",
        "It varies quite a bit from project to project",
        "I work independently and do not have direct contact with the project team"
    ],
    "funcoes_outro":[
        "Programmer",
        "Visual Artist",
        "UI/UX Designer",
        "Scriptwriting/Narrative",
        "Tech Lead",
        "Marketing/Publishing",
        "Game Designer",
        "Level Designer",
        "Tester (QA)",
        "Sound Artist / Composer",
        "Animator",
        "Producer"
    ],
    "tipos_jogos_outro": [
        "Action Games",
        "Strategy Games",
        "Role-Playing Games",
        "Sports Games",
        "Vehicle Simulations",
        "Construction and Management Simulations",
        "Adventure Games",
        "Idle and Puzzle Games",
        "Online Gaming"
# --- Novas Categorias ---
        "Casual, Cozy, and Social Games",
        "Educational and Serious Games",
        "Unspecified"
    ],
    "plataformas_desenvolvimento_outro": [
        "PC (Windows, Linux, Mac)",
        "Web (browsers)",
        "Mobile devices (Android, iOS)",
        "Sony Consoles / PlayStation",
        "Microsoft Consoles / Xbox",
        "Nintendo Consoles",
        "Virtual / Augmented Reality (XR)",
        "Retro Consoles",
        "Board/Card Games"
    ],
    "ferramentas_desenvolvimento_outro": [
        "Unity",
        "Unreal",
        "Godot",
        "Game Maker",
        "RPG Maker",
        "Low-level framework (LOVE, MonoGame, Heaps, etc.)",
        "Custom Engine (Proprietary, made by me)",
        "Custom Engine (Proprietary, made by the company)",
        "I do not use game engines (programming with basic libs like SDL)",
# --- Novas Categorias ---
        "Other Game Engines (Construct, GDevelop, Defold, Ren'Py, Cryengine, etc.)",
        "Unspecified"
    ],
    "dificuldades_testes_outro": [
        "Difficulty understanding how testing tools work.",
        "Complication integrating tests into the project workflow.",
        "The feeling that manual tests are more practical or efficient.",
        "Difficult to develop and keep the tests up-to-date.",
        "Perception that automated tests do not find the \"bugs that matter\".",
        "I have never tried using automated tests.",
    # --- Novas Categorias ---
        "Lack of time, strict deadlines, or unfavorable cost-benefit ratio.",
        "Difficulty testing subjective elements (\"game feel\", player experience) or non-deterministic gameplay.",
        "Technical limitations of the game engine, architecture, or visual scripting (e.g., Unity, Blueprints).",
        "Team limitations (difficulty training team members or getting them on board).",
        "None"
    ],
    "testes_jogo_outro":[
        "Exploratory testing — I play freely and observe if there are glitches or strange behaviors",
        "Scripted testing — I follow a list of steps or a checklist to verify specific features",
        "Automated testing — I use tools or scripts to test parts of the game without manual intervention",
        "Simulated agents — I use bots or scripts that mimic player behavior to test the game",
        "Performance Tests"
    ],
    "ferramentas_teste_outro": [
        "Unity Test Framework",
        "Unreal Functional Testing Framework / Gauntlet",
        "A Godot Test Framework Plugin (e.g., GUT or gdUnit)",
        "I have never used automated testing tools"
        # --- Novas Categorias ---
        "Custom, In-house, or Proprietary Testing Tools (including custom bots)",
        "General Software Testing Frameworks (NUnit, Jest, Pytest, Rust/C++ units, Playwright, etc.)",
        "CI/CD and DevOps Automation Tools (GitHub Actions, TeamCity, SonarQube, etc.)"
    ],
    "conteudo_testado_outro": [
        "Isolated components — I verify if specific parts of the code work correctly independently (Unit Testing)",
        "Basic performance — I evaluate load times, frame rate (FPS), or resource consumption",
        "Specific game scenarios — I simulate gameplay situations to check if the game responds as expected",
        "Smoke tests — I only check if the game starts and runs without critical crashes",
        "Simulation — I simulate a player's behavior through an agent",
        "I do not use automated tests"
        # --- Novas Categorias ---
        "Integration and End-to-End (E2E) Testing — I test how multiple components, sub-systems, or features work together.",
        "Backend, Server, and External Services — I test APIs, databases, server logic, or network services outside the game client."
    ],
    "tipo_falha_outro": [
        "Stuck — player gets stuck without being able to exit (Softlock)",
        "Crash — game closes, freezes, or hangs",
        "Visual glitches or strange audio noises",
        "Performance drops or framerate instability",
        "Collision errors and physics",
        "Game balance outside the planned level (too easy, too hard, or inconsistent)"
        # --- Novas Categorias ---
        "Networking, Sync, Backend, and Infrastructure Issues (e.g., replication, server downtime, security)",
        "Core Design Flaws, Boring Gameplay Loops, or Lack of Player Engagement",
        "Business, Monetization, and Financial Risks",
        "Not Applicable (e.g., out-of-scope roles, meta-responses, personal motivation)"
    ],
    "etapa_testes_outro":[
      "Before implementing the feature — I follow a test-driven approach (Test-Driven Development)",
      "During or right after implementing the feature — I write tests along with the code",
      "After creating a functional prototype — I test when I already have something playable or testable",
      "Only at the end of the project, during the review phase",
      "I do not use automated tests",
      "When there is time or opportunity — without a defined step in the process",
        # --- Novas opções adicionadas para viabilizar a escolha única ---
        "It depends on the project/system, or I use a hybrid approach (combination of phases)",
        "I do not know, or I am not the person responsible for implementing tests",
        "Invalid response, critique of the survey, or out of scope"
    ],
    "requisito_testes_outro": [
        "To accept contributions from collaborators (e.g., pull requests)",
        "To allow the project to advance to the next phase (alpha, beta)",
         "To start the development of a new feature",
        "They are not a mandatory requirement in projects",
        # --- Novas opções adicionadas para viabilizar a escolha única ---
    ],
    "avaliacao_artefatos_outro": [
        "I use previously defined criteria (e.g., style, clarity, audience suitability)",
        "I rely on informal or subjective evaluation, without a structured evaluation process",
        "I perform formal tests with users or specific tools",
        "The evaluation is done mainly by other people on the team",
        # --- Novas Categorias ---
        "Informal external feedback (e.g., sharing with friends, online communities like Reddit)",
        "Not yet evaluating"
    ],
    "design_validacao_outro": [
        "Through simplified playable prototypes (digital or analog)",
        "With physical or real-world simulations (e.g., with people, objects, role-playing)",
        "Using spreadsheets to simulate systems or balancing",
        "Using specific tools (e.g., Machinations)",
        "I mentally simulate scenarios and interactions",
        "I usually implement directly without prior design validation."
    # --- Novas Categorias ---
        "Writing documents, mind maps, diagrams, or narrative explorations",
        "Discussions, meetings, or feedback from team members and clients",
        "Unspecified"
    ],
    "areas_uso_ia_outro": [
        "To generate creative ideas (e.g., characters, mechanics, narratives, dialogues)",
        "To create visual or audio content (e.g., concept art, voices, soundtracks, effects)",
        "To assist in implementation (e.g., writing or reviewing code, suggesting technical solutions)",
        "To plan or structure the game (e.g., documentation, system architecture, balancing)",
        "To create or suggest automated tests (e.g., generating test cases, validation scripts)",
        "To review or validate game features (e.g., finding bugs, checking logic)",
        "I haven't used AI yet, but I am curious or interested",
        "I do not use AI in my game projects and do not intend to.",
        # --- Novas Categorias ---
        "Research, Learning, and Understanding Documentation (e.g., advanced search, explaining code, math)",
        "Prototyping, Tooling, and Placeholders (e.g., quick scripts, temporary programmer art)",
        "Text Refinement and Localization (e.g., spellchecking, translation, thesaurus)",
        "Tried but found unhelpful"

    ],
    "percepcao_uso_ia_outro": [
        "Unauthorized use of data and ethical issues (copyright, authorship, credits, plagiarism)",
        "Privacy concerns: my inputs might be reused without control",
        "Fear that professionals in the field will be replaced by AI",
        "Lack of transparency and difficulty verifying the originality or reliability of what AI produces",
        "Ethics in AI use (e.g., authorship, credits, plagiarism)",
        "I have no significant concerns at the moment"
        # --- Novas Categorias ---
        "Low quality output, technical debt, bugs, and increased review time (e.g., 'AI Slop')",
        "Loss of human skills, cognitive debt, and over-reliance on AI",
        "Loss of artistic intent, lack of originality, and poor creative control",
        "Environmental and ecological impacts (e.g., power consumption)",
        "Security vulnerabilities and safety risks of AI agents",
        "Negative public perception and potential reputation damage",
        "Do not want answer"
    ],
    "consideracoes_finais": [
        "1. Preference for manual testing & human playtesting (self, friends, team, or community)",
        "2. Scope & resource constraints (solo developers, small teams, short cycles, or game jams)",
        "3. Time, budget, or delivery constraints (rushed timelines leave no room for testing)",
        "4. High cost-of-maintenance & fragility of automated tests (frequent code/UI/gameplay changes)",
        "5. Games as a subjective/artistic medium (untestable 'feel', focus on fun, TDD doesn't fit gameplay)",
        "6. Technical difficulty of testing in standard engines (Unity/Unreal limitations, mocking complexities)",
        "7. Successful, active use, or practical implementation of automated testing/CI-CD pipelines",
        "8. Curiosity, optimism, or interest in adopting automated testing (including AI agent testing)",
        "9. Opinions on Generative AI (Ethical concerns, 'slop', anti-AI policies, or positive productivity tool)",
        "10. Critique of software engineering dogmas/buzzwords (SOLID, Clean Code, TDD as mindless overhead)",
        "11. Meta-feedback on the survey, personal backgrounds, or industry rants",
        "Placeholder responses"
    ],
    "dificuldades_manutencao_outro": [
        "Code becomes difficult to understand over time",
        "Making changes causes unexpected errors in other parts of the game (regressions)",
        "Communication difficulties among team members",
        "Lack of time or tight deadlines",
        "Changes in scope or features in the middle of the project",
        "Absence of good software engineering practices",
        "I do not face significant difficulties in this aspect",
        # --- Novas Categorias ---
        "Technology, engine, framework, and tool limitations",
        "Maintaining focus and motivation"
    ],
}

# Carrega o CSV primeiro para sabermos as colunas reais
df = pd.read_csv('filtereddata.csv')

# Filtra apenas as colunas mapeadas que REALMENTE existem no arquivo CSV
columns_to_process = []
for col in CATEGORIES_MAPPING.keys():
    if col in df.columns:
        columns_to_process.append(col)
    else:
        print(f"⚠️ Aviso: A coluna '{col}' mapeada no script não foi encontrada no CSV e será pulada.")

# Remova a linha 'df = pd.read_csv('normalizeddata.csv')' que estava lá embaixo no processamento principal,
# já que agora carregamos o DataFrame aqui em cima.


# ==========================================
# LLM COM CONTEXTO DINÂMICO
# ==========================================
def ask_llm_to_split_and_translate(text, column_name, known_options):
    """
    Extrai os conceitos das respostas diretamente em inglês usando o modelo configurado.
    """
    response_text = "failed"
    if (
            pd.isna(text)
            or str(text).strip() == ""
            or str(text).lower() in ["outro", "other", "nan"]
    ):
        return []

    prompt = f"""
You are an expert academic data annotator.

Analyze the following game development survey response and extract its core concept(s) directly in English.

Only split the response into multiple separate concepts if it contains more than one independent tool, answer, or idea.

You are provided with a pool of existing valid categories:

{json.dumps(known_options, indent=2)}

Rules:

1. If a concept matches or is semantically equivalent to one of the existing options, you MUST return exactly the existing option string.
2. If it does not fit any existing option, create a concise English label.
3. Return ONLY valid JSON.
4. Do not include explanations.

Output format:

{{
  "concepts": [
    "Concept 1",
    "Concept 2"
  ]
}}

Column:
{column_name}

Response:
{text}
"""

    try:
        response_text = ask_llm(prompt)

        # Regex blindada para remover envoltórios de Markdown (```json ... ```) se existirem
        cleaned_response = re.sub(r"^```(?:json)?\s*|\s*```$", "", response_text.strip(), flags=re.IGNORECASE)

        response_data = json.loads(cleaned_response)
        return response_data.get("concepts", [str(text)])

    except Exception as e:
        print(
            f"Erro no processamento para '{text}': {e}. Resposta crua: {response_text}\n\n Aplicando fallback por vírgulas.")
        cleaned = (
            str(text)
            .replace(" e ", ", ")
            .replace(" and ", ", ")
            .split(",")
        )
        return [c.strip().title() for c in cleaned if c.strip()]



# Inicializa/Carrega o cache do arquivo JSON
cache = carregar_cache()

print("Iniciando Reclassificação Inteligente + Deduplicação por Cosseno...")

for col in columns_to_process:
    print(f"\n>>> Processando coluna: {col}")
    new_col_name = f"{col}_reclass"

    pre_existing = CATEGORIES_MAPPING[col]
    all_new_concepts = set()  # Guarda conceitos novos temporariamente para alimentar o pool dinâmico
    row_results = {}  # Guarda o mapeamento temporário [index] -> lista_de_conceitos

    # Garante estrutura no cache para esta coluna
    if col not in cache:
        cache[col] = {}

    for idx, row in df.iterrows():
        original_text = row[col]
        original_text_str = str(original_text).strip()

        # Condição de parada/pulo para células vazias
        if (
                pd.isna(original_text)
                or original_text_str == ""
                or original_text_str.lower() in ["outro", "other", "nan"]
        ):
            row_results[idx] = []
            continue

        # CHECAGEM DO CACHE: Se já processamos este texto exato nesta coluna, pula a LLM!
        if original_text_str in cache[col]:
            print(f"  ✨ [Cache Hit] Linha {idx}: Reaproveitando resposta de '{original_text_str[:30]}...'")
            concepts = cache[col][original_text_str]
        else:
            # O pool enviado junta as opções base com as novas descobertas acumuladas até aqui
            current_pool = pre_existing + list(all_new_concepts)

            # Executa a requisição (seja Mistral API ou Gemma local)
            # concepts = ask_llm_to_split_and_translate(original_text, col, current_pool)
            concepts = "FILL"
            # Grava no cache e salva imediatamente no arquivo JSON
            cache[col][original_text_str] = concepts
            salvar_cache(cache)

        # Mesmo vindo do cache, precisamos computar 'all_new_concepts' para o agrupamento por cosseno no fim da coluna
        if concepts:
            for c in concepts:
                if c not in pre_existing:
                    all_new_concepts.add(c)
            row_results[idx] = concepts
        else:
            row_results[idx] = []

    # Agrupamento final por Cosseno > 0.90 de novos conceitos descobertos
#     new_concepts_list = list(all_new_concepts)
#     merge_map = {}
#
#     if len(new_concepts_list) > 1:
#         print(f" Analisando {len(new_concepts_list)} novos conceitos gerados para agrupamento...")
#         embeddings = embedding_model.encode(new_concepts_list, convert_to_tensor=True)
#
#         visited = set()
#         for i in range(len(new_concepts_list)):
#             if i in visited:
#                 continue
#             for j in range(i + 1, len(new_concepts_list)):
#                 if j in visited:
#                     continue
#
#                 similarity = util.cos_sim(embeddings[i], embeddings[j])[0][0].item()
#
#                 if similarity >= 0.90:
#                     print(
#                         f"   [Merge > 0.90]: '{new_concepts_list[j]}' unificado em -> '{new_concepts_list[i]}' (Sim: {similarity:.3f})")
#                     merge_map[new_concepts_list[j]] = new_concepts_list[i]
#                     visited.add(j)
#             visited.add(i)
#
#     # Reconstrução final da coluna mesclando os sinônimos
#     df[new_col_name] = df[col].astype(str)
#
#     for idx, concepts in row_results.items():
#         if not concepts:
#             continue
#
#         final_sanitized = []
#         for c in concepts:
#             sanitized_concept = merge_map.get(c, c)
#             final_sanitized.append(sanitized_concept)
#
#         df.at[idx, new_col_name] = ", ".join(list(set(final_sanitized)))
#
# # Salva a planilha final atualizada
# output_filename = "normalizeddata_reclassified.csv"
# df.to_csv(output_filename, index=False)
# print(f"\n Processo concluído com sucesso! Arquivo salvo como: '{output_filename}'")