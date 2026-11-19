import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import MonteCarloMethod

from rq1tests import TESTS

CSV_FILE = "normalizeddatacalc.csv"


# ==================================
# CONFIGURE TESTS HERE
# ==================================


TESTS = [

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"
        }
    },
{
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {"type": "categorical",
              "column": "uso_praticas_controle_versao"
        }
    },
]


# ==================================
# HELPERS
# ==================================

def cramers_v(table):
    chi2 = chi2_contingency(table)[0]
    n = table.to_numpy().sum()
    r, c = table.shape
    return np.sqrt(chi2 / (n * min(r - 1, c - 1)))


def extract_variable(df, spec):

    # variável categórica simples (ex: formacao)
    if spec["type"] == "categorical":
        return df[spec["column"]].astype(str)

    # soma de colunas (one-hot ou múltiplas flags)
    if spec["type"] == "sum":
        return df[spec["columns"]].fillna(0).sum(axis=1)

    raise Exception("Unknown type")

def build_test_name(x, y):

    def label(spec):

        if spec["type"] == "categorical":
            return spec["column"]

        if spec["type"] == "sum":
            if(len(spec["columns"])>1):
                return "sum_" + str(len(spec["columns"]))
            else:
                return spec["columns"][0]


    return f"{label(x)}_vs_{label(y)}"


# ==================================
# RUN
# ==================================

df = pd.read_csv(CSV_FILE)

for test in TESTS:

    name = build_test_name(test["x"], test["y"])

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    x = extract_variable(df, test["x"])
    y = extract_variable(df, test["y"])

    table = pd.crosstab(x, y)

    chi2, p, dof, expected = chi2_contingency(table)

    mc = MonteCarloMethod(
        n_resamples=10000
    )

    result = chi2_contingency(
        table,
        correction=False,
        method=mc
    )

    p_mc = result.pvalue

    effect = cramers_v(table)

    expected_df = pd.DataFrame(
        expected,
        index=table.index,
        columns=table.columns
    )

    residuals = (table - expected_df) / np.sqrt(expected_df)

    # =========================
    # BALANCEAMENTO (IMPORTANTE)
    # =========================

    row_balance = table.sum(axis=1)
    col_balance = table.sum(axis=0)

    print("\n--- SAMPLE BALANCE ---")

    print("\nRow distribution (X):")
    print(row_balance)

    print("\nColumn distribution (Y):")
    print(col_balance)

    print("\nNormalized row proportions:")
    print(table.div(row_balance, axis=0).round(3))

    # =========================
    # OBSERVED / EXPECTED
    # =========================

    print("\n--- OBSERVED ---")
    print(table)

    print("\n--- EXPECTED ---")
    print(expected_df.round(2))

    # =========================
    # RESÍDUOS (QUEM CAUSA O EFEITO)
    # =========================

    print("\n--- TOP CONTRIBUTIONS (Residuals) ---")

    top_residuals = (
        residuals
        .stack()
        .sort_values(ascending=False)
    )

    print("\nPositive (over-represented):")
    print(top_residuals.head(5))

    print("\nNegative (under-represented):")
    print(top_residuals.tail(5))

    # =========================
    # MÉTRICAS GLOBAIS
    # =========================

    print(f"\nchi2 = {chi2:.4f}")
    print(f"Classical p = {p:.3e}")
    print(f"Monte Carlo p = {p_mc:.3e}")

    print(f"dof = {dof}")
    print(f"Cramer's V = {effect:.4f}")

    # =========================
    # VALIDAÇÃO DO TESTE
    # =========================

    small_cells = (expected_df < 5).sum().sum()
    total_cells = expected_df.size

    print("\n--- TEST ASSUMPTIONS ---")
    print(
        f"Cells with expected < 5: "
        f"{small_cells}/{total_cells}"
    )

    ratio = small_cells / total_cells
    final_p = p
    p_source = "Classical"

    if ratio > 0.2:
        print("WARNING: χ² may be unreliable (too many small expected counts)")
        final_p = p_mc
        p_source = "Monte Carlo"
    else:
        print("χ² assumptions acceptable")

    # =========================
    # CONCLUSÃO
    # =========================

    print("\n--- CONCLUSION ---")

    print(
        f"Decision based on {p_source} p-value"
    )

    if final_p < 0.05:
        print(
            "Significant association detected"
        )

    else:
        print(
            "No significant association detected"
        )

print("""
============================================================
STATISTICAL ANALYSIS REPORT
============================================================

This report applies Pearson's Chi-Squared Test of Independence
to evaluate associations between categorical variables.

KEY CONCEPTS:

- Observed table:
  Real distribution of responses in the dataset.

- Expected table:
  Distribution expected if variables were independent.

- Chi-square (χ²):
  Measures global deviation between observed and expected.

- p-value:
  Probability of observing such deviation under independence.
  p < 0.05 suggests evidence of association.

- Cramér's V:
  Effect size (strength of association):
    ~0.1 = small
    ~0.3 = moderate
    ~0.5 = strong

- Standardized residuals:
  Cell-level contribution:
    > +2  : stronger than expected
    < -2  : weaker than expected

- Sample imbalance:
  Unequal marginal distributions across categories.
  Does NOT invalidate χ², but affects interpretation and power.

============================================================
""")