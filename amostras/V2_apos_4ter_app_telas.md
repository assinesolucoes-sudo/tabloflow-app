# V2 · Telas do App após Sessão 4-ter

Documento descreve, em markdown, como cada tela do app Streamlit é renderizada
após a refatoração de Sessão 4-ter (D-175 · D-177 · D-178). Screenshots reais
ficam capturáveis via `streamlit run src/app_v2.py` + navegador; este arquivo
consolida o QUE é renderizado em cada momento.

## Legenda

- Cada bloco `### Tela N` descreve o estado da tela em um instante.
- Sidebar fica vazia em TODAS as telas (D-178 · TED migrou para expander).
- Expander "⚙️ Configurações avançadas" aparece após upload; fica colapsado por default.

---

## Tela 1 · Etapa "Reconhecer estrutura" · TED colapsado no topo

```
┌─────────────────────────────────────────────────────────────────────────┐
│ V2 · Análise Comparativa entre Referências                              │
│ [Objetivo da Visão] [Aplicar modelo] [Salvar modelo] [Nova análise]     │
│ ──────────────────────────────────────────────────────────────────────  │
│ ▶ 1·Escolher arquivo  ✅ 2·Reconhecer estrutura  · 3·...  · 4·...  · ...│
│                                                                          │
│ ▼ ⚙️ Configurações avançadas                        (colapsado default)  │
│                                                                          │
│ ### Reconhecer estrutura                                                 │
│ Indique como a comparação está organizada na sua base.                  │
│                                                                          │
│ (○) Cada lado em uma coluna distinta (ex: Orçado e Realizado ...)       │
│ (●) Os dois lados empilhados em uma coluna identificadora                │
│                                                                          │
│ Coluna discriminadora: [ Mes ▾ ]                                         │
│ 2 valor(es) único(s) detectado(s) na coluna 'Mes'                        │
│                                                                          │
│ Comparar de (valor 1): [ 2025-01 ▾ ]                                     │
│ Comparar com (valor 2): [ 2025-02 ▾ ]                                    │
│                                                                          │
│ Rótulos amigáveis — como os dois lados aparecerão no Excel               │
│ Como chamar este lado (Origem): [ Janeiro 2025         ]                │
│ Como chamar este lado (Comparado): [ Fevereiro 2025     ]                │
│                                                                          │
│ [← Voltar]              [Próximo · Configurar análise]                   │
└─────────────────────────────────────────────────────────────────────────┘
 Sidebar: (vazia · D-178)
```

**Mudanças em relação à sessão anterior:**
- Sidebar anteriormente continha TED (4 number_inputs + paleta); agora **vazia**.
- Expander no topo com label `⚙️ Configurações avançadas` começa **colapsado**.

---

## Tela 2 · Etapa "Agrupar" · TED expander aberto

```
┌─────────────────────────────────────────────────────────────────────────┐
│ V2 · Análise Comparativa entre Referências                              │
│ ──────────────────────────────────────────────────────────────────────  │
│ ✅ 1 ✅ 2 ✅ 3 ▶ 4·Agrupar  · Revisar                                   │
│                                                                          │
│ ▲ ⚙️ Configurações avançadas                                   (aberto)  │
│   Edições aqui afetam apenas a leitura qualitativa do Resumo Executivo. │
│   Os cálculos principais (Diferença, Variação %, Classificação) não     │
│   são afetados.                                                          │
│                                                                          │
│   Limite de estabilidade           Limite de valores na coluna de comp. │
│   [    0.0100       ]              [      50       ]                    │
│   (variações menores são estável)  (acima sugere filtragem)             │
│                                                                          │
│   Limite de nulos massivos         Limite de variação extrema           │
│   [     0.20        ]              [    10.00      ]                    │
│   (acima sinaliza qualidade)       (maiores são destacadas)             │
│                                                                          │
│ ### Agrupar                                                              │
│ Defina por quais dimensões a comparação será feita.                     │
│                                                                          │
│ Agrupar por (1 a 9 dimensões):                                           │
│ [ Loja × ] [ Produto × ] [+ adicionar ...]                              │
│                                                                          │
│ Como consolidar valores quando há múltiplas linhas por combinação?       │
│ (●) Soma   (○) Média   (○) Máximo   (○) Mínimo   (○) Contagem            │
│                                                                          │
│ ✓ Estimativa: 50 linhas no resultado.                                   │
│                                                                          │
│ [← Voltar]              [Próximo · Revisar e executar]                   │
└─────────────────────────────────────────────────────────────────────────┘
 Sidebar: (vazia · D-178)
```

**Nota:** Rótulos dos 4 thresholds em **user-facing**. SEM `Δ%`, SEM `C.5`,
SEM `TED`, SEM `pct`. Help de cada campo em microcopy curto (vocabulário v2).

---

## Tela 3 · Resultado da análise (D-177 · microanálise executiva)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ V2 · Análise Comparativa entre Referências                              │
│ ──────────────────────────────────────────────────────────────────────  │
│ ✅ 1 ✅ 2 ✅ 3 ✅ 4 ▶ Revisar                                            │
│                                                                          │
│ ▼ ⚙️ Configurações avançadas                        (colapsado)         │
│                                                                          │
│ # 📊 Resultado da análise                                                │
│ Análise comparativa entre Janeiro 2025 e Fevereiro 2025                 │
│ · gerada em 24/04/2026 às 16:25                                         │
│                                                                          │
│ ### Números principais                                                   │
│ ┌──────────────────┬──────────────────┬──────────────┬──────────────┐   │
│ │ Total · Janeiro  │ Total · Fevereiro│ Diferença    │ Variação %   │   │
│ │ 2025             │ 2025             │              │              │   │
│ │                  │                  │              │              │   │
│ │ R$ 1.234.567,00  │ R$ 1.400.000,00  │ R$ 165.433,00│  13,40%      │   │
│ │                  │                  │ ↑ 13,40%     │              │   │
│ └──────────────────┴──────────────────┴──────────────┴──────────────┘   │
│                                                                          │
│ ### Como os casos se distribuem                                          │
│ ┌──────────────────────────┬──────┬────────────┐  ┌─────────────────┐   │
│ │ Categoria                │ Casos│ Participação│  │                 │   │
│ ├──────────────────────────┼──────┼────────────┤  │ ██████████ 68%  │   │
│ │ Presente nos dois lados  │   41 │     68,33% │  │ ███     25%     │   │
│ │ Ausente no comparado     │   15 │     25,00% │  │ █       5%      │   │
│ │ Sem valor na origem      │    3 │      5,00% │  │ ▪       1,67%   │   │
│ │ Sem valor no comparado   │    1 │      1,67% │  │                 │   │
│ └──────────────────────────┴──────┴────────────┘  └─────────────────┘   │
│                                                                          │
│ ### Variações em destaque                                                │
│ ┌────────┬────────┬─────────────────┬──────────────┬──────────┬────────┐│
│ │ Loja   │ Produto│ Valor · Janeiro │ Valor · Fev  │ Diferença│ Var %  ││
│ ├────────┼────────┼─────────────────┼──────────────┼──────────┼────────┤│
│ │ SP01   │ X      │ R$ 50.000,00    │ R$ 75.000,00 │ 25.000,00│ 50,00% ││
│ │ RJ02   │ Y      │ R$ 100.000,00   │ R$ 60.000,00 │-40.000,00│-40,00% ││
│ │ ...                                                                   ││
│ └────────┴────────┴─────────────────┴──────────────┴──────────┴────────┘│
│                                                                          │
│ ┌──────────────────────────────────────┐                                │
│ │ Barras horizontais (cores por sinal) │                                │
│ │ SP01·X  ████████████████ +25000,00   │                                │
│ │ RJ02·Y  ████████ -40000,00           │                                │
│ │ ...                                  │                                │
│ └──────────────────────────────────────┘                                │
│                                                                          │
│ ### Leitura qualitativa                                                  │
│ A comparação indica melhoria geral na maior parte dos casos.            │
│                                                                          │
│ ⓘ A análise gerou 2 avisos estruturais. Nenhum bloqueio foi escapado.   │
│                                                                          │
│ ▼ Ver detalhes do diagnóstico                                            │
│                                                                          │
│ ────────────────────────────────────────────────────────────             │
│ [← Voltar]  [Paleta: Azul ▾]  [📥 Baixar Excel]                         │
│                                                                          │
│ [🔄 Nova análise]                                                        │
└─────────────────────────────────────────────────────────────────────────┘
 Sidebar: (vazia · D-178)
```

**Pontos removidos que existiam antes (D-177 · D-162 superada):**
- ❌ `st.json(resumo.bloco_N.model_dump())` · era 6 expandidos com JSON cru
- ❌ Checklist "Item 1 · V2-A01 · contagem_categoria" · etc
- ❌ Botão "Ir para Validação Visual"
- ❌ Botão "Visão aprovada"
- ❌ Gate B.4 no download

**Elementos novos:**
- ✅ 4 `st.metric` com formato monetário/percentual BR
- ✅ Tabela de distribuição + `st.bar_chart`
- ✅ Tabela de top variações + `st.bar_chart` horizontal
- ✅ Prosa user-facing de leitura qualitativa
- ✅ Rodapé com Paleta dropdown + Download na mesma linha

---

## Tela 4 · Troca de paleta no rodapé (P-3 fix · D-175)

Sequência de 3 cliques trocando paleta:

```
Estado inicial · paleta_selecionada = "Azul"
  Rodapé: [← Voltar]  [Paleta: Azul ▾]  [📥 Baixar Excel]

Clique 1 · usuário clica no selectbox · muda para "Verde"
  → st.session_state["paleta_selecionada"] = "Verde"
  → Download é regenerado com cache key "caminho_excel_Verde_<id(v2)>"
  → Arquivo Excel tem estilo TableStyleMedium4 (verde)
  Rodapé: [← Voltar]  [Paleta: Verde ▾]  [📥 Baixar Excel]

Clique 2 · usuário troca para "Vinho"
  → st.session_state["paleta_selecionada"] = "Vinho"
  → Novo arquivo em cache "caminho_excel_Vinho_<id(v2)>"
  → TableStyleMedium3 aplicado
  Rodapé: [← Voltar]  [Paleta: Vinho ▾]  [📥 Baixar Excel]

Clique 3 · volta para "Azul"
  → Cache hit na chave "caminho_excel_Azul_<id(v2)>" (já gerada antes)
  → Arquivo original servido · sem reprocessar
  Rodapé: [← Voltar]  [Paleta: Azul ▾]  [📥 Baixar Excel]
```

**Correção do bug P-3:** antes, `paleta_aplicada` era congelado em
`v2.config_usada["paleta_aplicada"]` no momento da execução do motor.
Agora a paleta é lida de `st.session_state.get("paleta_selecionada", ...)`
**no momento do clique no download** (`_render_botao_download_excel`).

Cache por chave composta `caminho_excel_{paleta}_{id(v2)}` garante que
arquivos com paletas diferentes fiquem lado a lado sem regenerar.

---

## Tela 5 · Botão Baixar ao lado da paleta (layout final)

Comparativo lado-a-lado antes × depois:

```
ANTES (D-162 · sessão 4 · canceled):
  Tela Resultado:       [Baixar Excel]  [Ir para Validação Visual]  [Nova]
  Tela Checklist:       Itens V2-A01..V2-A04 ☐☐☐☐  → [Visão aprovada]
  Paleta:               Sidebar (global)

DEPOIS (D-175 · D-177 · D-178 · sessão 4-ter):
  Tela Resultado:       [← Voltar]  [Paleta ▾]  [Baixar Excel]
                        [Nova análise]
  Checklist:            REMOVIDO (tela e conceito absorvidos)
  Paleta:               Rodapé da tela Resultado · trocável in-place
```

O resultado é que o usuário leigo abre o app, configura a análise em 4
etapas, chega na tela **Resultado da análise**, lê a microanálise em tela
(sem código técnico), escolhe a paleta que prefere e **baixa** — zero
obstáculo, zero gate, zero JSON cru.
