
TESTS = [

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao_normalized"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"
        }
    },
{
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao_normalized"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao_normalized"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao_normalized"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao_normalized"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"
        }
    },

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"
        }
    },
    ## funcao programador
    {
        "x": {
            "type": "sum",
            "columns": [
                "funcoes__programador",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "funcoes__programador",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "funcoes__programador",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "funcoes__programador",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "funcoes__programador",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "funcoes__programador",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"}
    },
    ## area formacao

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "area_formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"
        }
    },
{
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "area_formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "area_formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "area_formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "area_formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"
        }
    },

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "area_formacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"
        }
    },
    ## team size situacao_equipe
{
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao_equipe"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"
        }
    },
{
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao_equipe"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao_equipe"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao_equipe"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao_equipe"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"
        }
    },

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao_equipe"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"
        }
    },
    # situacao
{
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"
        }
    },
{
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"
        }
    },
    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"
        }
    },

    {
        "name": "formacao_vs_controle_versao",

        "x": {
            "type": "categorical",
            "column": "situacao"
        },

        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"
        }
    },
    # desenvolve consoles plataformas_desenvolvimento__console_nintendo	plataformas_desenvolvimento__console_psx	plataformas_desenvolvimento__console_xbox
{
        "x": {
            "type": "sum",
            "columns": [
                "plataformas_desenvolvimento__console_nintendo",
                "plataformas_desenvolvimento__console_psx",
                "plataformas_desenvolvimento__console_xbox",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "plataformas_desenvolvimento__console_nintendo",
                "plataformas_desenvolvimento__console_psx",
                "plataformas_desenvolvimento__console_xbox",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "plataformas_desenvolvimento__console_nintendo",
                "plataformas_desenvolvimento__console_psx",
                "plataformas_desenvolvimento__console_xbox",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "plataformas_desenvolvimento__console_nintendo",
                "plataformas_desenvolvimento__console_psx",
                "plataformas_desenvolvimento__console_xbox",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "plataformas_desenvolvimento__console_nintendo",
                "plataformas_desenvolvimento__console_psx",
                "plataformas_desenvolvimento__console_xbox",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "plataformas_desenvolvimento__console_nintendo",
                "plataformas_desenvolvimento__console_psx",
                "plataformas_desenvolvimento__console_xbox",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"}
    },
    # faz jogos de simulaçãop construção
{
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__construction_management",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__construction_management",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__construction_management",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__construction_management",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__construction_management",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__construction_management",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"}
    },
 # faz jogos de estrategia
{
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__strategy",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__strategy",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__strategy",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__strategy",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__strategy",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__strategy",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"}
    },
 # faz jogos online
{
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_controle_versao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_padroes_design"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_modelagem_projeto"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_prototipacao"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_testes_automatizados"}
    },
    {
        "x": {
            "type": "sum",
            "columns": [
                "tipos_jogos__online",
            ]
        },
        "y": {
            "type": "categorical",
            "column": "uso_praticas_integracao_continua"}
    },
]