import pandas as pd
import re
from datetime import datetime

# ================= CONFIG =================

# arquivo_entrada = "filtereddata.csv"
# arquivo_saida = "normalizeddata2.csv"
arquivo_entrada = "reclassifieddata.csv"
arquivo_saida = "normalizeddata3.csv"

colunas_multivalor = [
    "funcoes",
    "tipos_jogos",
    "plataformas_desenvolvimento",
    "ferramentas_desenvolvimento",
    "dificuldades_manutencao",
    "testes_jogo",
    "dificuldades_testes",
    "ferramentas_teste",
    "conteudo_testado",
    "tipo_falha",
    "requisito_testes",
    "avaliacao_artefatos",
    "design_validacao",
    "areas_uso_ia",
    "percepcao_uso_ia",
    "consideracoes_finais_classified"
]

# ================= LOAD =================

df = pd.read_csv(arquivo_entrada)

# ================= SPLIT MULTI RESPOSTA =================

def split_respostas(x):
    if pd.isna(x):
        return []
    return [
        i.strip()
        for i in re.split(r"[;,|]", str(x))
        if i.strip()
    ]

for coluna in colunas_multivalor:
    listas = df[coluna].apply(split_respostas)

    opcoes = sorted(set(
        item
        for sublist in listas
        for item in sublist
    ))

    for op in opcoes:
        nome = f"{coluna}__{op}".lower()
        nome = re.sub(r"\W+", "_", nome)

        df[nome] = listas.apply(lambda lst: 1 if op in lst else 0)

df = df.drop(columns=colunas_multivalor)

# ================= FUNÇÃO GENÉRICA FAIXAS =================

def categorizar(valor, faixas):
    if pd.isna(valor):
        return None
    for nome, min_v, max_v in faixas:
        if max_v is None:
            if valor >= min_v:
                return nome
        else:
            if valor >= min_v and valor < max_v:
                return nome
    return None


# ================= IDADE =================

ano_atual = datetime.now().year
df["idade"] = ano_atual - pd.to_numeric(df["year_of_birth"], errors="coerce")

faixas_idade = [
    ("18a30", 18, 30),
    ("30a40", 30, 40),
    ("40a50", 40, 50),
    ("50a60", 50, 60),
    ("60a80", 60, 80),
    ("80+", 80, None),
]

df["idade_faixa"] = df["idade"].apply(lambda v: categorizar(v, faixas_idade))


# ================= EXPERIENCIA =================

exp = pd.to_numeric(df["anos_experiencia"], errors="coerce")

faixas_exp = [
    ("0a5", 0, 5),
    ("5a10", 5, 10),
    ("10a20", 10, 20),
    ("20a30", 20, 30),
    ("30a40", 30, 40),
    ("40a50", 40, 50),
    ("50+", 50, None),
]

df["experiencia_faixa"] = exp.apply(lambda v: categorizar(v, faixas_exp))


# ================= PROJETOS =================

proj = pd.to_numeric(df["qtd_projetos"], errors="coerce")

faixas_proj = [
    ("0a5", 0, 5),
    ("5a10", 5, 10),
    ("10a20", 10, 20),
    ("20a30", 20, 30),
    ("30a50", 30, 50),
    ("50+", 50, None),
]

df["projetos_faixa"] = proj.apply(lambda v: categorizar(v, faixas_proj))


# ================= COUNTRY NORMALIZATION =================

def normalize_country(c):
    if pd.isna(c):
        return "Other"

    c = str(c).strip().upper()

    if c in ["BR"]:
        return "Brazil"

    if c in ["US"]:
        return "USA"

    if c in ["DE"]:
        return "Germany"

    if c in ["UK"]:
        return "United Kingdom"

    if c in ["FR"]:
        return "France"

    if c in ["CA"]:
        return "Canada"

    return "Other"


df["country_normalized"] = df["country_work"].apply(normalize_country)


# ================= WORLD REGION =================

country_to_region = {
    # North America
    "US": "North America",
    "CA": "North America",

    # Latin America
    "BR": "Latin America",
    "AR": "Latin America",
    "MX": "Latin America",
    "CL": "Latin America",
    "CO": "Latin America",
    "PE": "Latin America",
    "UY": "Latin America",
    "PY": "Latin America",

    # Western Europe
    "UK": "Western Europe",
    "GB": "Western Europe",
    "FR": "Western Europe",
    "DE": "Western Europe",
    "ES": "Western Europe",
    "PT": "Western Europe",
    "IT": "Western Europe",
    "NL": "Western Europe",
    "BE": "Western Europe",
    "IE": "Western Europe",
    "CH": "Western Europe",
    "AT": "Western Europe",
    "UA": "Western Europe",
    "RS": "Western Europe",

    # Europe (other)
    "PL": "Europe",
    "CZ": "Europe",
    "HU": "Europe",
    "RO": "Europe",
    "GR": "Europe",
    "SE": "Europe",
    "NO": "Europe",
    "FI": "Europe",
    "DK": "Europe",

    # Southeast Asia
    "SG": "Southeast Asia",
    "MY": "Southeast Asia",
    "TH": "Southeast Asia",
    "ID": "Southeast Asia",
    "PH": "Southeast Asia",
    "VN": "Southeast Asia",
    "CN": "Southeast Asia",
    "AU":"Southeast Asia",
    "IN": "Southeast Asia",
    "LK": "Southeast Asia",
    "JP": "Southeast Asia",

    # Africa
    "ZA": "Africa",
    "NG": "Africa",
    "EG": "Africa",
    "MA": "Africa",
    "KE": "Africa",
    "GH":"Africa",
    "MG":"Africa",
    "SN":"Africa",
    "CM":"Africa",

    # Middle East
    "IL": "Middle East",
    "AE": "Middle East",
    "SA": "Middle East",
    "TR": "Middle East",
    "IR": "Middle East",
    "QA": "Middle East",
}

df["world_region"] = (
    df["country_work"]
    .astype(str)
    .str.strip()
    .str.upper()
    .map(country_to_region)
    .fillna("Not Informed")
)


# ================= SAVE =================

df.to_csv(arquivo_saida, index=False)

print("Arquivo gerado:", arquivo_saida)