# spec_fundacao.md

**Spec consolidada da Fundação do TabloFlow** · artefato único de design da Fase 1.

Cobertura: contratos de dados (§A) · motor upload (§B) · motor base (§C) · transversais fundamentais (§D) · transversais por família (§E) · transversais de composição (§F) · decisão de roadmap T-CONCAT/M2.STACK (§G · D-135) · exportação (§Exportação) · arquitetura do dataset sintético de fundação (§H) · cobertura por visão (§I) · `casos_esperados.yaml` (§J) · fechamento e transição para F-MOT (§K).

**Origem:** consolidação dos 11 DCVs aprovados da Fase 0 (V2 · V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5 · V6) · 5 princípios derivados formalizados em CONTEXT §9 Camada C · 6 padrões estruturais de produto em CONTEXT §13 · decisões D-122 a D-141.

**Receptividade a IA declarada (D-130):** todos os contratos desta spec são Pydantic BaseModel serializáveis JSON-compatível · enums com valores string explícitos · rastreabilidade por campo estrutural · schema auto-documentado via `Field(..., description=...)`. Nenhuma implementação de IA nesta fase — apenas aptidão declarada.

**Marco · Fundação-Design CONCLUÍDA (20/04/2026).** Próximo bloco operacional: **F-MOT** (prompt consolidado em §K.2 · sessão dedicada Claude Code).

---

## Histórico de produção

Spec consolidada a partir de 3 blocos sequenciais de design (G-FUND · Opção 2 · dividido em 3 partes pela densidade do escopo · confirmado pela Usuária em 20/04/2026). Os 3 blocos foram produzidos no mesmo dia e consolidados no fechamento do Marco Fundação-Design:

- **G-FUND bloco 1** (20/04/2026) · contratos (§A) · motores (§B · §C) · transversais fundamentais (§D) · decisão T-CONCAT/M2.STACK (§G) · decisões emergentes D-133, D-134, D-135 · momentos D-131 resolvidos M1 (negócio · T-CONCAT na Fundação · M2.STACK em M2) e M3 (técnico puro · `tipo_estrutural` no motor_base).
- **G-FUND bloco 2** (20/04/2026) · transversais por família (§E) · transversais de composição (§F) · exportação (§Exportação) · decisões emergentes D-136, D-137, D-138, D-139 · momento D-131 resolvido M2 (negócio · F-EXP bloco único).
- **G-FUND bloco 3** (20/04/2026) · arquitetura do dataset sintético (§H) · cobertura por visão (§I) · `casos_esperados.yaml` canônico (§J) · fechamento e prompt F-MOT (§K) · decisões emergentes D-140, D-141 · nenhuma decisão de negócio (confirmado).

Esta consolidação final (20/04/2026) foi produzida em sessão de alinhamento ALINHA-Fundação-Design→F-MOT como parte do kit de encerramento do Marco. Padrão ALINHA formalizado em D-142 nesta mesma sessão.

---

## Sumário

- [Seção A · Contratos de dados](#seção-a--contratos-de-dados)
- [Seção B · Motor upload](#seção-b--motor-upload)
- [Seção C · Motor base](#seção-c--motor-base)
- [Seção D · Transversais fundamentais](#seção-d--transversais-fundamentais)
- [Seção E · Transversais por família](#seção-e--transversais-por-família)
- [Seção F · Transversais de composição](#seção-f--transversais-de-composição)
- [Seção G · Decisão de roadmap · T-CONCAT e M2.STACK (D-135)](#seção-g--decisão-de-roadmap--t-concat-e-m2stack-d-135)
- [Seção Exportação · `exportacao.py` consolidado](#seção-exportação--exportacaopy-consolidado)
- [Seção H · Arquitetura do dataset sintético de fundação](#seção-h--arquitetura-do-dataset-sintético-de-fundação)
- [Seção I · Cobertura por visão](#seção-i--cobertura-por-visão)
- [Seção J · `casos_esperados.yaml` · artefato canônico de validação](#seção-j--casos_esperadosyaml--artefato-canônico-de-validação)
- [Seção K · Fechamento da Fundação · transição para F-MOT](#seção-k--fechamento-da-fundação--transição-para-f-mot)
- [Referências canônicas](#referências-canônicas)

---

## Seção A · Contratos de dados

### A.1 · Arquitetura geral

Quatro contratos compõem o vocabulário canônico da Fundação:

| Contrato | Produzido por | Consumido por | Natureza |
|---|---|---|---|
| **`UploadResult`** | `motor_upload.py` | `motor_base.py` · Fase 2 via `motor_base` | Metadados de arquivo carregado |
| **`MotorResult`** | `motor_base.py` | Todas as 11 visões (V1..V11) | DataFrame processado + metadados estruturais |
| **`VNResultBase`** (classe abstrata) | `visao_vN.py` (subclasses V{N}Result) | `app_vN.py` · `exportacao.py` | Resultado analítico da visão |
| **`DiagnosticoVN`** (auxiliar via T-DIAG) | Todas as visões + motores | Aba Diagnóstico da exportação | Warnings estruturais unificados |

Todos são Pydantic BaseModel. Todos implementam serialização JSON-compatível. Contratos compartilhados (warning · bloqueio · ajuste de motor · decisão de usuário) aparecem uma única vez.

### A.2 · `UploadResult`

Consolidação de D-007 (`arquivo_bytes`), D-018 (T-DUAL), D-026 (reconhecedor pt-BR/pt-EN), D-130 (receptividade IA).

```python
class UploadResult(BaseModel):
    file_name: str = Field(..., description="Nome do arquivo principal")
    modo_upload: Literal["SIMPLES", "DUAL"] = Field(..., description="T-DUAL · V1/V11 = DUAL · demais = SIMPLES")
    arquivo_unico: Optional[ArquivoInfo] = Field(None, description="Preenchido em modo SIMPLES")
    arquivos_dual: Optional[List[ArquivoInfo]] = Field(None, description="2 entradas em modo DUAL")
    timestamp_upload: datetime
    warnings: List[WarningEstrutural]

class ArquivoInfo(BaseModel):
    caminho_logico: Literal["origem", "comparado", "unico"]
    nome_arquivo: str
    arquivo_bytes: bytes = Field(..., description="D-007 · preservado em memória para motor_base")
    abas_disponiveis: List[str]
    aba_selecionada: str
    formato: Literal["xlsx", "xlsm", "csv", "tsv"]
    preview: Dict[str, List]    # 5 linhas como records · auditoria rápida
    encoding_detectado: Optional[str] = Field(None, description="Relevante para CSV/TSV")
    separador_csv: Optional[str] = Field(None, description="Inferido via csv.Sniffer")
```

**Decisões internas de design (ficam nesta spec · não viram D-XXX):**
- Preview: 5 linhas (herança D-007)
- Encoding CSV default: utf-8 com fallback latin-1 (cp1252) e warning W-U-ENCODING-FALLBACK
- Separador CSV: `csv.Sniffer` sobre primeiros 4KB · fallback `,` · segundo fallback `;` (padrão brasileiro)
- Excel multi-aba: seleção obrigatória antes de motor_base rodar (C.5 · princípio C.3)

### A.3 · `MotorResult`

Consolidação de D-007, D-008 (W-B01 boolean disfarçado), D-026, D-103 (subtipo ID), D-113 (tipo_estrutural com 5 enums), **D-133** (tipo_estrutural sempre computado).

```python
class MotorResult(BaseModel):
    df: pd.DataFrame              # DataFrame completo · D-007 · arbitrary_types_allowed
    column_meta: Dict[str, ColumnMeta]
    modo_upload: Literal["SIMPLES", "DUAL"]
    origem_comparado_map: Optional[Dict[int, Literal["origem", "comparado"]]] = Field(
        None, description="Quando DUAL · mapeia índice de linha ao caminho_logico"
    )
    total_linhas_originais: int
    total_linhas_processadas: int    # após exclusões de parse
    timestamp_processamento: datetime
    warnings: List[WarningEstrutural]
    
    class Config:
        arbitrary_types_allowed = True
    
    def para_contexto_ia(self) -> Dict:
        """D-130 · subset otimizado para contexto IA (sem df bruto, com sumário estatístico)"""
        return {
            "column_meta": {k: v.model_dump() for k, v in self.column_meta.items()},
            "total_linhas": self.total_linhas_processadas,
            "modo_upload": self.modo_upload,
            "amostra_5_linhas": self.df.head(5).to_dict(orient="records"),
            "estatisticas_sumarias": self._resumir_estatisticas(),
            "warnings": [w.model_dump() for w in self.warnings],
        }

class ColumnMeta(BaseModel):
    nome: str
    tipo_tecnico: Literal["int", "float", "string", "bool", "datetime", "object", "mixed"]
    tipo_semantico: Literal["numeric", "boolean", "temporal", "textual", "categorico_baixa_card", "misto"]
    tipo_estrutural: Literal["CATEGORICO_ELEGIVEL", "NUMERICO_CONTINUO", "TEMPORAL", "BOOLEANO", "VAZIO_OU_AMBIGUO"] = Field(
        ..., description="D-113 · D-133 · sempre computado pelo motor_base"
    )
    subtipo_id_detectado: bool = Field(..., description="D-103 · sempre computado em int/string com alta cardinalidade")
    null_count: int
    cardinalidade: int        # valores únicos não-nulos
    eh_candidato_categorico: bool
    padrao_cronologico_detectado: Optional[Literal[
        "ISO_DATE", "PT_BR_DATE", "MONTH_NAME_PT", "MONTH_NAME_EN",
        "COMPACT_MONTHYEAR", "YEAR_ONLY", "Q_TRIMESTRE"
    ]] = Field(None, description="D-026 · 7 padrões reconhecidos · threshold 80%")
    ordem_insercao: int       # índice posicional na base original · auditoria
```

**D-133** formaliza que `tipo_estrutural` e `subtipo_id_detectado` são **sempre computados** pelo motor_base em toda coluna — não lazy, não opcional. Razão: (a) determinismo C.1 · (b) metadados consistentes se usuário trocar de visão · (c) custo O(n) desprezível mesmo em 500K linhas.

### A.4 · `VNResultBase` · padrão genérico

Os 11 DCVs mostram variação grande no resultado analítico específico. `VNResultBase` é classe abstrata que toda `V{N}Result` herda.

```python
class VNResultBase(BaseModel):
    visao_id: Literal["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11"]
    config_usada: Dict[str, Any] = Field(..., description="Config persistível · T-MODELO · TED D-123")
    motor_result_meta: MotorResultMeta
    timestamp_execucao: datetime
    
    # Blocos padronizados presentes em toda visão
    base_analitica: pd.DataFrame = Field(..., description="Padrão BAD · D-124")
    resumo_executivo: ResumoExecutivoPadrao = Field(..., description="6 blocos fixos · D-125")
    coracao_visual: CoracaoVisualRef = Field(..., description="Referência à aba e tipo · D-126")
    
    # Bloqueios e warnings
    bloqueios_disparados: List[BloqueioOperacional] = Field(..., description="Padrão MBO · D-127 · contrato único D-134")
    warnings: List[WarningEstrutural]
    
    # Diagnóstico (alimenta aba Diagnóstico via T-DIAG)
    diagnostico: DiagnosticoVN
    
    class Config:
        arbitrary_types_allowed = True
    
    def para_contexto_ia(self) -> Dict:
        """D-130 · subset para IA (Papel B · leitura em linguagem natural do resultado)"""
        return {
            "visao_id": self.visao_id,
            "config_usada": self.config_usada,
            "resumo_executivo": self.resumo_executivo.model_dump(),
            "coracao_visual": self.coracao_visual.model_dump(),
            "bloqueios_escapados": [b.model_dump() for b in self.bloqueios_disparados if b.escape_acionado],
            "warnings": [w.model_dump() for w in self.warnings],
            "amostra_base_analitica": self.base_analitica.head(20).to_dict(orient="records"),
        }

class ResumoExecutivoPadrao(BaseModel):
    """D-125 · 6 blocos fixos · adaptações via D-073 permitidas preservando a espinha"""
    bloco_1_cabecalho: CabecalhoExecucao
    bloco_2_numeros_ancora: Dict[str, Union[float, int, str]]
    bloco_3_distribuicao: Dict[str, Any]
    bloco_4_elementos_destacados: Dict[str, Any]
    bloco_5_leitura_qualitativa: LeituraQualitativa
    bloco_6_qualidade_estrutural: QualidadeEstrutural

class LeituraQualitativa(BaseModel):
    classificacao_ativa: str
    thresholds_usados: Dict[str, float] = Field(..., description="TED D-123 · editados ou default")
    alguma_leitura_alterada_por_edicao: bool

class CoracaoVisualRef(BaseModel):
    """D-126 · referência declarativa · exportacao.py implementa"""
    nome_aba: str               # "Matriz de Presença" · "Mapa de Grupos" · "Curva Pareto" · etc.
    tipo: Literal["BARRAS", "BARRAS_LINHA", "COLUMN_EMPILHADO_100", "MATRIZ_COLORIDA", "HISTOGRAMA", "TABELA_HEATMAP"]
    capabilities_requeridas: List[str]    # ["formatacao_condicional", "paginacao_grande", "ColumnChart_empilhado"]
```

Cada `V{N}Result` adiciona seus campos específicos nas Specs S-VN da Fase 2 (V4Result adiciona `classificacao_abc` · V6Result adiciona `matriz_cruzamento` · V9Result adiciona `mapa_perfil` · etc.).

### A.5 · `BloqueioOperacional` · contrato único compartilhado (D-134)

**D-134** formaliza que `BloqueioOperacional` é contrato único compartilhado por todas as visões. Materialização arquitetural do padrão MBO (C.D4 · D-127) · aba Diagnóstico consolida bloqueios de qualquer visão sem código específico por visão.

```python
class BloqueioOperacional(BaseModel):
    codigo: str = Field(..., description="Padrão B-VN-DESCRITOR · ex: 'B-V6-EIXO-NUMERICO-CONTINUO'")
    condicao_disparo: str = Field(..., description="Microcopy descritivo · visível ao usuário")
    escapavel: bool
    escape_acionado: Optional[bool] = None
    warning_pos_escape: Optional[str] = Field(None, description="Código do warning permanente quando escape é acionado")
    contexto_disparo: Dict[str, Any] = Field(default_factory=dict, description="Campos relacionados · contagens · valores observados")
```

**Consequência arquitetural:** Specs S-VN declaram a matriz de bloqueios V-específica como lista de dicionários com esses campos. Motor da visão instancia `BloqueioOperacional` preenchido na ordem declarada. `exportacao.py` consome a lista sem conhecer a visão-origem.

### A.6 · `DiagnosticoVN` e T-DIAG

Consolidação de D-017 (Diagnóstico sempre última aba · herança universal) e §A.5 acima.

```python
class DiagnosticoVN(BaseModel):
    # Seção 1 · Ajustes do motor
    ajustes_aplicados: List[AjusteMotor]
    
    # Seção 2 · Warnings por categoria
    warnings_por_categoria: Dict[CategoriaWarning, List[WarningEstrutural]]
    
    # Seção 3 · Decisões do usuário (defaults editados · thresholds editáveis TED · escapes)
    decisoes_usuario: List[DecisaoUsuario]
    
    # Seção 4 · Bloqueios escapados
    bloqueios_informativos: List[BloqueioOperacional]
    
    # Seção 5 · Integridade estrutural
    integridade: IntegridadeEstrutural

class CategoriaWarning(str, Enum):
    INFORMATIVO = "informativo"
    AJUSTE_LEVE = "ajuste_leve"
    ALERTA_ESTRUTURAL_LEVE = "alerta_estrutural_leve"
    ALERTA_ESTRUTURAL = "alerta_estrutural"
    DECISAO_USUARIO = "decisao_usuario"
    ESCAPE_ACIONADO = "escape_acionado"

class WarningEstrutural(BaseModel):
    codigo: str                # "W-V6-EIXO-CARDINALIDADE-P2"
    categoria: CategoriaWarning
    microcopy: str
    contexto: Dict[str, Any]
    linha_referenciada: Optional[int] = None

class AjusteMotor(BaseModel):
    tipo_ajuste: str           # "INTERVALO_AJUSTADO_INICIO" · "LINHA_EXCLUIDA_NULO" · etc.
    linhas_afetadas: int
    descricao: str

class DecisaoUsuario(BaseModel):
    contexto: str              # "threshold_dominante_editado" · "escape_cardinalidade_acionado"
    valor_default: Any
    valor_escolhido: Any
    justificativa_opcional: Optional[str] = None

class IntegridadeEstrutural(BaseModel):
    total_linhas_base_original: int
    total_linhas_processadas: int
    total_linhas_excluidas: int
    motivo_exclusao_por_categoria: Dict[str, int]
```

**Vocabulário fechado:** as 6 categorias de warning cobrem todos os 11 DCVs. Adição de categoria nova é decisão D-XXX.

### A.7 · Receptividade a IA · implementação nos 4 contratos (D-130 ratificada)

3 requisitos concretos materializados:

**Requisito 1 · Serialização JSON-compatível sem perda semântica.** Todo BaseModel tem:
```python
model_config = {
    "use_enum_values": False,   # enum preserva nome: "CATEGORICO_ELEGIVEL", não valor opaco
    "json_encoders": {
        datetime: lambda v: v.isoformat(),
        pd.DataFrame: lambda df: df.to_dict(orient="records"),
    }
}
```

**Requisito 2 · Schema auto-documentado.** Todo campo tem `Field(..., description="...")`. IA externa lê o JSON Schema (`model.model_json_schema()`) e entende o domínio sem necessidade de documentação separada.

**Requisito 3 · Método `.para_contexto_ia()`** em `VNResultBase` e `MotorResult` (ver §A.3 e §A.4 acima) · subset otimizado descartando `df` bruto · mantendo metadados · amostra · warnings · estatísticas sumárias.

**Nenhuma IA é chamada na Fase 1.** Implementação do Papel A (sugestão de configuração pré-execução) + Papel B (leitura em linguagem natural) acontece em bloco IA-Família-A após validação V2+V1+V11.

---

## Seção B · Motor upload

### B.1 · API pública

```python
def processar_upload(
    arquivos: List[ArquivoEntrada],
    modo: Literal["SIMPLES", "DUAL"],
    abas_selecionadas: Dict[str, str],    # {caminho_logico: nome_aba}
) -> UploadResult
```

Modo declarado pelo chamador (app Streamlit sabe se é V1/V11 ou outra visão). Motor não infere modo (C.5).

### B.2 · Modo T-DUAL (D-018)

Modo DUAL aceita dois inputs estruturais equivalentes, padronizados pelo chamador antes de chamar o motor:
- **Formato 1 · 2 arquivos** — `[{path: "origem.xlsx", logico: "origem"}, {path: "comparado.xlsx", logico: "comparado"}]`
- **Formato 2 · 1 arquivo com 2 abas** — `[{path: "dual.xlsx", aba: "Origem", logico: "origem"}, {path: "dual.xlsx", aba: "Comparado", logico: "comparado"}]`

Motor não distingue formatos — trabalha sobre `List[ArquivoEntrada]` de 2 entradas com `caminho_logico` preenchido.

### B.3 · Reconhecedor cronológico pt-BR/pt-EN · 7 padrões (D-026)

Consumido por `column_meta.padrao_cronologico_detectado` via motor_base. Herdado por T-EIXO (D-061) · zero duplicação.

| Padrão | Regex/heurística | Exemplos |
|---|---|---|
| `ISO_DATE` | datetime parsing estrito ISO-8601 | `2024-01-15` · `2024-01-15T10:30:00` |
| `PT_BR_DATE` | `dd/mm/yyyy` · `dd-mm-yyyy` | `15/01/2024` · `15-01-2024` |
| `MONTH_NAME_PT` | nomes de mês em pt (jan · fev · mar ... dez) + ano opcional | `jan/24` · `Janeiro 2024` · `Fev-24` |
| `MONTH_NAME_EN` | nomes de mês em en (Jan · Feb · ... Dec) + ano opcional | `Jan-24` · `January 2024` · `Feb/2024` |
| `COMPACT_MONTHYEAR` | `yyyy-mm` · `yyyymm` · `mm/yyyy` | `2024-01` · `202401` · `01/2024` |
| `YEAR_ONLY` | 4 dígitos 1900-2099 · cardinalidade ≤ 30 | `2020` · `2021` · `2022` |
| `Q_TRIMESTRE` | `Qn` · `Tn` · `n° Trimestre` | `Q1 2024` · `T3/24` · `1º Trimestre` |

**Prioridade em ambiguidade:** ISO_DATE > PT_BR_DATE > COMPACT_MONTHYEAR > MONTH_NAME_PT > MONTH_NAME_EN > Q_TRIMESTRE > YEAR_ONLY.

**Threshold de detecção:** ≥ 80% dos valores não-nulos casam padrão → `tipo_estrutural = TEMPORAL`. Entre 50-79% → `tipo_estrutural = CATEGORICO_ELEGIVEL` + warning W-B-TEMPORAL-PARCIAL.

**Biblioteca de parsing:** `dateutil.parser` com locale pt-BR via pré-normalização regex. `pandas.to_datetime` não é usado diretamente (falha silenciosa em padrões pt-BR).

### B.4 · Detecção de subtipo ID (D-103 · V5 origem · D-112 V6 consumo)

**Heurística:**
```
Coluna é candidato a subtipo ID se E somente se:
  (1) tipo_tecnico in ["int", "string"]
  (2) cardinalidade >= 0.90 * (total_linhas - null_count)
  (3) uma das condições:
      (a) sequência aritmética com diferença constante em ≥ 80% dos valores (int)
      (b) comprimento fixo ≥ 8 dígitos em 100% dos valores (int ou string)
      (c) padrão regex identificado (CPF · CNPJ · UUID · matrícula padrão)
```

**Camada de inferência (M3 da D-131 · resolvido como decisão técnica pura):** detecção roda no **motor_base**, não no motor_upload. Razão: depende de coluna completa, não de amostragem. Preview de 5 linhas é insuficiente para confiabilidade. Consequência de negócio: V11 (que consome subtipo ID para campo-chave de matching) fica disponível na Família A junto com V2 e V1 sem atraso.

### B.5 · Encoding e separadores

- **Excel** (xlsx/xlsm) — engine `openpyxl` · read-only mode para bases grandes
- **CSV/TSV** — tenta utf-8 → fallback latin-1 (cp1252) com W-U-ENCODING-FALLBACK
- **Separador CSV** — `csv.Sniffer` sobre primeiros 4KB · default `,` · fallback `;`

### B.6 · Warnings de motor_upload

- **W-U-ENCODING-FALLBACK** — arquivo CSV lido com fallback latin-1 · INFORMATIVO
- **W-U-SEP-FALLBACK** — separador CSV inferido como `;` após falha de `,` · INFORMATIVO
- **W-U-ARQUIVO-VAZIO** — arquivo sem dados após parse · ALERTA_ESTRUTURAL

---

## Seção C · Motor base

### C.1 · API pública

```python
def processar_base(upload_result: UploadResult) -> MotorResult
```

Consome `UploadResult.arquivo_unico` (modo SIMPLES) ou `UploadResult.arquivos_dual` (modo DUAL · construção de `origem_comparado_map`). Produz DataFrame completo (D-007) + `column_meta` populada para toda coluna.

### C.2 · Heurística completa de `tipo_estrutural` (D-113 · D-133)

Algoritmo canônico (ordem determinística · não trocar ordem):

```python
def classificar_tipo_estrutural(col: pd.Series, meta: ColumnMeta, total_linhas: int) -> TipoEstrutural:
    nulos_pct = meta.null_count / total_linhas
    
    # 1. VAZIO_OU_AMBIGUO · filtro de topo
    if nulos_pct > 0.90:
        return "VAZIO_OU_AMBIGUO"
    if meta.tipo_semantico == "misto":   # > 30% em tipos técnicos divergentes
        return "VAZIO_OU_AMBIGUO"
    
    # 2. BOOLEANO · D-008 (W-B01) + cardinalidade 2 explícita
    if meta.tipo_semantico == "boolean":
        return "BOOLEANO"
    if meta.cardinalidade == 2 and valores_em_conjunto_booleano(col):
        # valores em {0, 1, 0.0, 1.0, "sim", "não", "true", "false", True, False}
        return "BOOLEANO"
    
    # 3. TEMPORAL · reconhecedor pt-BR/pt-EN ≥ 80%
    if meta.padrao_cronologico_detectado is not None:
        return "TEMPORAL"
    
    # 4. NUMERICO_CONTINUO vs CATEGORICO_ELEGIVEL · fronteira principal
    if meta.tipo_tecnico in ["int", "float"]:
        if meta.tipo_tecnico == "float":
            return "NUMERICO_CONTINUO"
        # int
        if meta.subtipo_id_detectado:
            return "CATEGORICO_ELEGIVEL"    # ID é categórico apesar de int
        if meta.cardinalidade > 200:
            return "NUMERICO_CONTINUO"
        return "CATEGORICO_ELEGIVEL"
    
    # 5. String · sempre CATEGORICO_ELEGIVEL
    return "CATEGORICO_ELEGIVEL"
```

Fronteira int "categórico vs contínuo" em **200 valores distintos** — herdada de V6 D-113 · consistência.

### C.3 · Matriz completa `column_meta` por tipo de coluna

| Caso | tipo_tecnico | tipo_semantico | tipo_estrutural | Warnings |
|---|---|---|---|---|
| Texto puro < 50 distintos | string | categorico_baixa_card | CATEGORICO_ELEGIVEL | — |
| Texto puro ≥ 50 distintos | string | textual | CATEGORICO_ELEGIVEL | — |
| Texto com datas pt-BR em 90%+ | string | temporal | TEMPORAL | — |
| Int ≤ 200 distintos | int | numeric | CATEGORICO_ELEGIVEL | — |
| Int > 200 sem padrão ID | int | numeric | NUMERICO_CONTINUO | — |
| Int com subtipo ID | int | numeric | CATEGORICO_ELEGIVEL | W-B-ID-DETECTADO |
| Float sempre | float | numeric | NUMERICO_CONTINUO | — |
| Float em {0.0, 1.0, NaN} | float | boolean | BOOLEANO | W-B01 (D-008) |
| Bool nativo | bool | boolean | BOOLEANO | — |
| Datetime nativo | datetime | temporal | TEMPORAL | — |
| Misto > 30% divergente | object | misto | VAZIO_OU_AMBIGUO | W-B-MISTO |
| > 90% nulos | qualquer | qualquer | VAZIO_OU_AMBIGUO | W-B-QUASE-VAZIO |
| Temporal 50-79% parcial | string | textual | CATEGORICO_ELEGIVEL | W-B-TEMPORAL-PARCIAL |

### C.4 · Warnings de motor_base (vocabulário fechado)

- **W-B01** — Boolean disfarçado detectado · float64 {0, 1, NaN} classificado BOOLEANO · D-008 · INFORMATIVO
- **W-B-MISTO** — Coluna com > 30% de valores em tipos técnicos divergentes · VAZIO_OU_AMBIGUO · ALERTA_ESTRUTURAL
- **W-B-QUASE-VAZIO** — Coluna com > 90% nulos · VAZIO_OU_AMBIGUO · ALERTA_ESTRUTURAL_LEVE
- **W-B-TEMPORAL-PARCIAL** — Padrão cronológico reconhecido em 50-79% (abaixo threshold) · INFORMATIVO
- **W-B-ID-DETECTADO** — Subtipo ID detectado na coluna · INFORMATIVO (consumido por V5 · V6 · V11)

### C.5 · Performance e bloqueios

- **Limite saudável:** 500K linhas (< 30s em máquina padrão) · warning W-B-BASE-GRANDE acima desse limite
- **Limite absoluto:** 2M linhas · bloqueio B-B-BASE-MUITO-GRANDE · sem escape
- **Streaming:** bases > 100K linhas acionam `openpyxl read-only` automaticamente
- **Amostragem para detecção de padrão cronológico:** primeiras 1000 linhas não-nulas ou 10% do total (o que for maior)

---

## Seção D · Transversais fundamentais

Transversais consumidos por **todas ou quase todas** as visões. Nesta seção: **T-AGRUPA · T-DIAG · T-SEMA**. Transversais por família ficam em §E · transversais de composição ficam em §F.

### D.1 · T-AGRUPA

**Contrato canônico com 3 extensões.**

```python
def consolidar_com_modo(
    df: pd.DataFrame,
    agrupadores: List[str],
    regras: Union[
        Literal["soma", "media", "maximo", "minimo", "contagem", "primeiro"],
        Dict[str, Literal["soma", "media", "maximo", "minimo", "contagem", "primeiro"]]
    ],
    modo_base: Literal["TRANSACIONAL", "PRE_AGREGADO"]
) -> Tuple[pd.DataFrame, List[WarningEstrutural]]
```

**Extensão 1 · Reconhecedor cronológico pt-BR/pt-EN** (D-026) — T-AGRUPA consome `column_meta.padrao_cronologico_detectado` para ordenação cronológica de agrupadores temporais · zero reimplementação (o reconhecedor vive em motor_upload/motor_base).

**Extensão 2 · Regra de agregação por métrica** (D-096 · V9 origem) — `regras` aceita string (todas métricas) ou `Dict[metrica, regra]` (regra específica por métrica). Compatibilidade retroativa: V4, V7 usam string; V9 usa dict.

**Extensão 3 · Modo no-op validado** (D-074 V8 origem · D-082 V7 · D-092 V9 · C.D1 CPCO) — quando `modo_base = "PRE_AGREGADO"`, T-AGRUPA não consolida mas valida unicidade de chaves · emite warning estrutural se duplicata encontrada · retorna DataFrame idêntico ao input em caso de unicidade válida.

**Warnings de T-AGRUPA:**
- **W-T-AGRUPA-DUPLICATA-PRE-AGREGADO** — Modo Pré-agregado declarado mas chaves têm duplicatas · ALERTA_ESTRUTURAL
- **W-T-AGRUPA-REGRA-POR-METRICA** — Contrato Dict usado · lista regras efetivas por métrica · INFORMATIVO

**Adaptação V5-específica (D-102):** V5 declara 3 modos próprios sem consolidar valores · **não invoca T-AGRUPA**. Adaptação via D-073.

### D.2 · T-DIAG

**Função · coletor unificado.** T-DIAG não é transformador analítico — é coletor canônico de todos os warnings, ajustes, decisões de usuário e bloqueios escapados. Todas as visões e motores emitem via T-DIAG; consolidação final produz `DiagnosticoVN` para a aba Diagnóstico.

```python
class T_DIAG:
    def __init__(self, visao_id: str):
        self.visao_id = visao_id
        self._warnings: List[WarningEstrutural] = []
        self._ajustes: List[AjusteMotor] = []
        self._decisoes_usuario: List[DecisaoUsuario] = []
        self._bloqueios_escapados: List[BloqueioOperacional] = []
        self._integridade: Optional[IntegridadeEstrutural] = None
    
    def registrar_warning(self, w: WarningEstrutural) -> None: ...
    def registrar_ajuste(self, a: AjusteMotor) -> None: ...
    def registrar_decisao_usuario(self, d: DecisaoUsuario) -> None: ...
    def registrar_bloqueio_escapado(self, b: BloqueioOperacional) -> None: ...
    def setar_integridade(self, i: IntegridadeEstrutural) -> None: ...
    def consolidar(self) -> DiagnosticoVN: ...
```

**Nenhuma visão emite warning direto.** Toda emissão passa por T-DIAG para consolidação canônica · garantia de vocabulário unificado na aba Diagnóstico (D-017 · sempre última aba).

### D.3 · T-SEMA · 2 contratos

**Contrato 1 · Semântica única** (D-067 · V3 origem · consumido V3 · V8):

```python
def classificar_semantica(
    estrutural: Literal["AUMENTOU", "REDUZIU", "ESTAVEL", "NAO_APLICAVEL"],
    semantica: Literal["MAIOR_MELHOR", "MENOR_MELHOR", "NEUTRA"]
) -> str
```

Tabela de mapeamento (determinística):

| Estrutural | MAIOR_MELHOR | MENOR_MELHOR | NEUTRA |
|---|---|---|---|
| AUMENTOU | Melhorou | Piorou | Aumentou |
| REDUZIU | Piorou | Melhorou | Reduziu |
| ESTAVEL | Estável | Estável | Estável |
| NAO_APLICAVEL | Não aplicável | Não aplicável | Não aplicável |

**Contrato 2 · Semântica por métrica com efeito no cálculo** (D-087 · V7 origem · D-095 V9 consumo):

```python
def classificar_semantica_por_metrica(
    resultados: Dict[str, ResultadoMetrica],
    semanticas: Dict[str, Literal["MAIOR_MELHOR", "MENOR_MELHOR", "NEUTRA"]]
) -> Dict[str, str]
```

Em contrato 2, a semântica **afeta o cálculo** — em V9, a Posição é invertida para métricas `MENOR_MELHOR` (menor valor = Pos 1). Isso é tratamento V9-específico que T-SEMA expõe como capability. V7 consome contrato 2 sem inverter (apenas vocabulário).

**Warnings de T-SEMA:**
- **W-T-SEMA-METRICA-SEM-SEMANTICA** — Métrica em contrato 2 sem semântica declarada · default NEUTRA aplicado · INFORMATIVO

---

## Seção E · Transversais por família

Esta seção especifica 5 transversais consumidos por famílias específicas de visões. Diferença vs §D: §D consolidou transversais consumidos por **todas** ou **quase todas** as visões (T-AGRUPA, T-DIAG, T-SEMA); §E consolida transversais com consumo focado por família.

### E.1 · `T-EIXO` · Eixo sequencial ordenado (Família B · V3 · V8)

**Origem canônica:** D-061 (refino DCV-V3) · herança integral em V8 (D-071). Formalizada na Fundação com 3 tipos canônicos e detecção de lacunas dependente do tipo.

**Consumidores:** V3 (primária), V8 (herança integral).

**Contrato de entrada (parâmetros de configuração):**

```python
class ConfigEixo(BaseModel):
    coluna_eixo: str = Field(..., description="Nome da coluna que representa o eixo sequencial")
    tipo_declarado: Literal["TEMPORAL", "ORDINAL", "MANUAL"] = Field(
        ..., description="Declaração final do usuário após default declarado do motor"
    )
    ordem_aplicada: List[str] = Field(
        ..., description="Ordem final dos pontos do eixo · motor propõe default · usuário confirma/edita"
    )
    intervalo_declarado: IntervaloEixo = Field(
        ..., description="De/Até declarado pelo usuário · preservado para auditoria mesmo após ajuste"
    )

class IntervaloEixo(BaseModel):
    de: str = Field(..., description="Ponto inicial declarado · string no vocabulário do eixo")
    ate: str = Field(..., description="Ponto final declarado")
```

**Contrato de saída (enriquecimento do DataFrame + metadados auxiliares):**

```python
class EixoResult(BaseModel):
    tipo_aplicado: Literal["TEMPORAL", "ORDINAL", "MANUAL"]
    tipo_inferido_pelo_motor: Literal["TEMPORAL", "ORDINAL", "MANUAL"]    # auditoria W-V{N}-EIXO-TIPO-INFERIDO
    ordem_aplicada: List[str]
    intervalo_declarado: IntervaloEixo
    intervalo_efetivo: IntervaloEixo                                       # após ajuste-limite
    pontos_no_intervalo: List[str]                                         # ordem final aplicada, recortada pelo intervalo
    pontos_ausentes_detectados: List[str]                                  # apenas TEMPORAL e ORDINAL com prefixo
    deteccao_de_lacuna_disponivel: bool                                    # False em MANUAL e ORDINAL sem prefixo
    densidade_de_lacuna: Optional[float]                                   # % de pontos ausentes · apenas quando disponível
    warnings_gerados: List[WarningEstrutural]
```

**Detecção dos 3 tipos canônicos** (ordem de prioridade quando múltiplos padrões são detectados simultaneamente · TEMPORAL > ORDINAL > MANUAL):

| Tipo | Heurística de detecção | Reconhecedor |
|---|---|---|
| **TEMPORAL** | Cardinalidade ≥ 80% dos valores únicos casa com padrão cronológico | Reconhecedor pt-BR/pt-EN **herdado de D-026 · T-AGRUPA** · datas ISO · datas pt-BR · nomes de meses (Jan/Fev/... · Jan/Feb/...) · anos (YYYY) · Q1-Q4 · "Jan/24" · "2024-01" |
| **ORDINAL com prefixo** | Cardinalidade ≥ 80% dos valores únicos tem prefixo ou sufixo numérico extraível | Regex `^(\d+)[^\d]` OU `[^\d](\d+)$` · aplicado a rótulos como "Etapa 1" · "Fase 3" · "Lote 7" · "1º Trimestre" |
| **ORDINAL sem prefixo** | Declaração explícita pelo usuário (motor não detecta · fallback automático para MANUAL) | Declaração do usuário |
| **MANUAL** | Fallback quando nenhum padrão acima é detectado | Ordem de primeira ocorrência na base |

**Regra de herança zero-duplicação:** o reconhecedor pt-BR/pt-EN do tipo TEMPORAL é o **mesmo módulo** `/src/utils/reconhecedor_cronologico.py` consumido por T-AGRUPA em D-026. Não há reimplementação. Adicionar padrão cronológico novo beneficia T-AGRUPA e T-EIXO simultaneamente.

**Default declarado (padrão D-024) aplicado em 2 pontos:**
1. **Tipo do eixo:** motor detecta padrões na amostragem do `motor_base` · propõe tipo com maior prioridade detectada · usuário confirma ou edita em 1 clique · warning `W-V{N}-EIXO-TIPO-INFERIDO` (informativo) registra aceitação sem edição
2. **Ordem do eixo:** motor propõe ordem conforme tipo aplicado · usuário pode reordenar manualmente · reordenação sobre TEMPORAL/ORDINAL dispara `W-V{N}-EIXO-ORDEM-MANUAL` (informativo · auditoria)

**Detecção de lacunas · dependente do tipo:**

| Tipo | Detecção automática | Referência |
|---|---|---|
| TEMPORAL | ✅ | Sequência canônica derivada do padrão detectado (ex: meses entre De e Até preenchem a sequência Jan, Fev, Mar...) |
| ORDINAL com prefixo numérico | ✅ | Sequência 1, 2, 3, ..., N dos prefixos extraídos |
| ORDINAL sem prefixo | ❌ | Sem referência semântica para inferir sequência canônica |
| MANUAL | ❌ | Ordem é declaração, não inferência |

Quando detecção é feita, `pontos_ausentes_detectados` é preenchido · `densidade_de_lacuna` calculada · warning `W-V{N}-EIXO-LACUNA` (informativo) dispara listando ausentes · `W-V{N}-EIXO-LACUNA-MASSIVA` (alerta · não bloqueio) dispara quando > 30% dos pontos esperados estão ausentes (threshold editável · TED · default 30% · range 10-50%).

**Intervalo declarado vs intervalo efetivo** (auditoria · princípio C.2):
- `intervalo_declarado` é preservado em T-MODELO e na aba Parâmetros · o que o usuário configurou literalmente
- `intervalo_efetivo` é o que foi aplicado após ajuste-limite · quando `De` < primeiro ponto da base ou `Até` > último ponto, motor ajusta silenciosamente e registra como `AJUSTE_LEVE` no Diagnóstico
- Quando `intervalo_declarado ≠ intervalo_efetivo`, aba Parâmetros lista ambos lado a lado · warnings `W-V{N}-INTERVALO-AJUSTE-INICIO` ou `W-V{N}-INTERVALO-AJUSTE-FIM` disparam

**Validação estrutural** (antes do cálculo analítico):
- `De > Até` em vocabulário ordenado do tipo aplicado é **bloqueio** `B-V{N}-INTERVALO-INVALIDO` · recusa execução · microcopy "Ponto inicial posterior ao ponto final no eixo ordenado"
- Intervalo resulta em menos de 2 pontos efetivos é bloqueio `B-V{N}-INTERVALO-MINIMO-2-PONTOS` (V8 · §4.5 DCV-V8)

**API pública do módulo:**

```python
# /src/transversais/t_eixo.py

def inferir_tipo_eixo(
    valores_unicos: List[str], 
    reconhecedor_cronologico: ReconhecedorCronologico
) -> Tuple[Literal["TEMPORAL", "ORDINAL", "MANUAL"], float]:
    """Retorna (tipo_inferido, confiança_em_0_a_1)."""
    ...

def aplicar_eixo(
    df: pd.DataFrame,
    config: ConfigEixo,
    nome_visao: str    # para prefixar warnings W-V{N}-EIXO-*
) -> Tuple[pd.DataFrame, EixoResult]:
    """
    Aplica tipo declarado + ordem + intervalo.
    Retorna (df enriquecido com coluna auxiliar `_ordem_eixo`, EixoResult com metadados).
    """
    ...
```

**Invocação canônica pelo motor da visão:**

```python
# visao_v3.py e visao_v8.py
df_eixo, eixo_result = t_eixo.aplicar_eixo(df, config.eixo, nome_visao="V3")
# df_eixo tem coluna auxiliar _ordem_eixo usada para ordenação estável downstream
# eixo_result contém todos os warnings para alimentar T-DIAG
```

**Decisão técnica pura resolvida nesta spec (sem necessidade de D-XXX):**

A coluna auxiliar `_ordem_eixo` é int64 posicional (1, 2, 3, ..., N seguindo `pontos_no_intervalo`). Nulos no eixo após aplicação do intervalo recebem `_ordem_eixo = -1` e são excluídos no cálculo sequencial downstream (V3 `Diferença consecutiva` / V8 `Movimentações do intervalo`). Isto é detalhe de implementação · já implícito nos DCVs V3/V8.

---

### E.2 · `T-RANK` · Ranking determinístico com desempate configurável (V1 · V4 · V6 · V7 · V9 · V10 · V11)

**Origem canônica:** D-041 (refino DCV-V4). Estendido em 5 adaptações subsequentes (V7 D-088 · V9 D-096 · V6 D-115 · com consumos secundários em V10 e V11 · V1 consome default sem adaptação).

**Consumidores (8 visões):** V1, V4, V6, V7, V9, V10, V11. Primeira consumidora V4 (estabeleceu contrato default 3 níveis) · demais adaptam via padrão "herança adaptada à natureza analítica" (D-073).

**Contrato de entrada:**

```python
class ConfigRank(BaseModel):
    escopo: Literal["global", "intra_grupo", "cross_elementos_dentro_do_agrupador"] = Field(
        ..., description="global=V4/V10/V11 · intra_grupo=V7 · cross_elementos_dentro_do_agrupador=V9 Modo Segmentado"
    )
    criterio_primario: CriterioOrdenacao = Field(
        ..., description="Regra de ordenação primária · expressa semanticamente pelo consumidor"
    )
    regras_desempate: List[CriterioDesempate] = Field(
        ..., description="3 níveis default (D-041) ou 4 níveis (V6/V7/V9) ou mais · aplicação de D-073"
    )
    coluna_grupo: Optional[str] = Field(
        None, description="Obrigatório quando escopo != global"
    )
    tolerancia_float: float = Field(
        1e-9, description="Tolerância absoluta para empate de floats · herança D-041"
    )
    metodo_rank_para_empate_preservado: Literal["standard", "min", "dense"] = Field(
        "standard", description="V9 usa 'min' em contexto (a) para preservar empate como fato analítico · D-096"
    )

class CriterioOrdenacao(BaseModel):
    coluna_ou_expressao: str
    direcao: Literal["decrescente", "crescente"]
    transformacao: Optional[Literal["abs"]] = Field(
        None, description="V7 usa 'abs' sobre desvio_percentual · D-088"
    )

class CriterioDesempate(BaseModel):
    tipo: Literal[
        "coluna_valor",                    # desempate por outra coluna numérica
        "concatenacao_agrupadores",        # D-041 default nível 2 · concatenação alfabética dos agrupadores
        "coluna_texto_alfabetico",         # V7/V9 nível 3 · nome de elemento alfabético case-insensitive
        "ordem_de_insercao"                # sempre último nível · preserva determinismo C.1
    ]
    parametros: Dict = Field(default_factory=dict)
```

**Contrato de saída (enriquecimento do DataFrame):**

```python
class RankResult(BaseModel):
    coluna_rank_adicionada: str        # nome da coluna rank no df · ex: 'rank_v4' · 'rank_desvio_v7'
    empates_detectados: int            # contagem de registros com valor primário empatado
    regras_desempate_acionadas: Dict[int, int]   # {nivel: contagem_de_usos}
    warnings_gerados: List[WarningEstrutural]
```

**Regra default 3 níveis (D-041 · herança V4):**

1. Valor primário (direção configurada · default decrescente)
2. Concatenação dos agrupadores na ordem declarada pelo usuário · alfabética crescente · case-insensitive · acentos normalizados
3. Ordem de inserção original na base ativa

Visão consumidora sem adaptação específica usa esses 3 níveis direto. **Consumidores com consumo padrão (default 3 níveis):** V1, V4, V10.

**Adaptações específicas por visão (D-073):**

**V11 · consumo padrão mas em contexto probabilístico:** T-RANK ranqueia candidatos de match por score de aderência (Passe 1) ou por valor dentro da tolerância (Passe 2). Desempate alocação gulosa: score decrescente · ordem de inserção. Sem alterações ao contrato (usa default).

**V7 · 4 níveis · ranking intra-grupo por magnitude (D-088):**

```python
ConfigRank(
    escopo="intra_grupo",
    criterio_primario=CriterioOrdenacao(
        coluna_ou_expressao="desvio_percentual",
        direcao="decrescente",
        transformacao="abs"     # magnitude, não sinal
    ),
    regras_desempate=[
        CriterioDesempate(tipo="coluna_valor", parametros={
            "coluna": "desvio_absoluto", "direcao": "decrescente", "transformacao": "abs"
        }),
        CriterioDesempate(tipo="coluna_texto_alfabetico", parametros={
            "coluna": "nome_elemento", "direcao": "crescente"
        }),
        CriterioDesempate(tipo="ordem_de_insercao")
    ],
    coluna_grupo="grupo"
)
```

**V9 · 4 níveis · 2 contextos de uso (D-096):**

Contexto (a) · Atribuição de Posição por Métrica · `metodo_rank_para_empate_preservado="min"` · empate preservado como fato analítico (não desempatado para classificação).

Contexto (b) · Desempate visual determinístico das linhas · 4 níveis:
1. Score Consolidado crescente (menor = melhor)
2. Variação Máxima de Posição crescente
3. Nome do Identificador alfabético case-insensitive
4. Ordem de inserção original

Novo escopo `cross_elementos_dentro_do_agrupador` adicionado ao enum · distinto de `intra_grupo` (V7 tem Grupo como campo dedicado formando unidade Elemento+Grupo · V9 Modo Segmentado · Agrupador apenas segmenta o conjunto · consolidação é Identificador+Agrupador).

**V6 · 4 níveis · ranking global de células (D-115):**

1. Valor da Medida decrescente
2. Valor alfabético de Eixo 1 crescente (case-insensitive)
3. Valor alfabético de Eixo 2 crescente (case-insensitive)
4. Ordem de inserção da primeira ocorrência do par (Eixo1=X ∧ Eixo2=Y) na base ativa crescente

Escopo = `global` no MVP · Modo Segmentado em roadmap P-V6-05-SEGMENTADO-Evo.

**Warnings canônicos gerados:**
- `W-V{N}-RANK-EMPATE` (informativo) · registra casos com resolução por regra secundária ou terciária · inclui contagem por nível
- `W-V{N}-RANK-EMPATE-MASSIVO` (alerta · adicional em V6 · D-115) · dispara quando > 50% das linhas estão empatadas em nível primário

**API pública:**

```python
# /src/transversais/t_rank.py

def aplicar_rank(
    df: pd.DataFrame,
    config: ConfigRank,
    nome_visao: str,
    nome_coluna_rank: str = "rank"
) -> Tuple[pd.DataFrame, RankResult]:
    """
    Aplica ranking determinístico com desempate configurável.
    Retorna df com coluna de rank adicionada + RankResult.
    """
    ...
```

**Decisão técnica pura resolvida (D-137):**

Enum `escopo` de T-RANK na Fundação declara 3 valores: `global`, `intra_grupo`, `cross_elementos_dentro_do_agrupador`. Nenhum escopo adicional antecipado · se V5 (que hoje não consome T-RANK) ou visão futura exigir outro escopo, entra via extensão do enum na Fase 2 sem quebra de contrato.

---

### E.3 · `T-ACUM` · Acumulado progressivo monotônico (V4 · V10)

**Origem canônica:** D-041 contexto (consumida por V4 Modo 2 e V10). Transversal de simplicidade alta sem adaptações documentadas nas 2 consumidoras.

**Consumidores:** V4 (Modo 2 · Modo 3 limitado), V10 (integral).

**Contrato de entrada:**

```python
class ConfigAcum(BaseModel):
    coluna_valor: str = Field(..., description="Coluna numérica a acumular · geralmente Participação após T-RANK")
    coluna_rank: str = Field(..., description="Coluna de rank produzida por T-RANK · garante ordem de acumulação")
    escopo: Literal["global", "intra_grupo"] = Field(
        "global", description="V4/V10 = global · reservado para extensão futura"
    )
    coluna_grupo: Optional[str] = None
```

**Contrato de saída:**

```python
class AcumResult(BaseModel):
    coluna_acumulado_adicionada: str    # ex: 'participacao_acumulada'
    monotonicidade_verificada: bool     # invariante · sempre True se cálculo correto
    warnings_gerados: List[WarningEstrutural]
```

**Regra de cálculo:**

Pré-condição: `coluna_rank` já aplicada (T-RANK aplicado antes · C.1 · determinismo). Acumulado é `cumsum` sobre `coluna_valor` na ordem de `coluna_rank` crescente (rank 1 primeiro).

Monotonicidade: valor acumulado é **crescente monotônico** por construção (todas as visões consumidoras operam sobre valores não-negativos · Participação ∈ [0, 100%]). Se valor negativo entrar no acumulado (caso teórico V4 Modo 1 não-consumidor, ou erro de configuração), warning `W-V{N}-ACUM-NEGATIVO` dispara.

**Regra de corte matemática (consumida por T-ABC · §E.4):** o item que faz o acumulado **atingir ou ultrapassar** o limiar pertence à faixa correspondente. Ordem: ranks 1 → N · acumulado crescente · limiar primeiro atingido determina Classe A · próximo limiar determina Classe B · restante Classe C.

**API pública:**

```python
# /src/transversais/t_acum.py

def aplicar_acumulado(
    df: pd.DataFrame,
    config: ConfigAcum,
    nome_visao: str,
    nome_coluna_acum: str = "acumulado"
) -> Tuple[pd.DataFrame, AcumResult]:
    ...
```

**Simplicidade declarada:** T-ACUM é o transversal mais simples da Fundação. Não tem adaptações por visão no momento. Consumido como caixa-preta por V4/V10. Extensão futura (Família C expandida com nova visão) entra via parâmetros sem alteração de contrato.

---

### E.4 · `T-ABC` · Classificação ABC por limiares de acumulado (V4 · V10)

**Origem canônica:** D-040 (refino DCV-V4). Herdada em V10 como view especializada sobre V4 Modo 2 (D-035 · D-045).

**Consumidores:** V4 (Modo 2 · Modo 3 com limiares globais), V10 (Modo 2 de V4 com apresentação dicotômica · limiar B oculto fixado em 100%).

**Contrato de entrada:**

```python
class ConfigABC(BaseModel):
    coluna_acumulado: str = Field(..., description="Coluna produzida por T-ACUM · geralmente participacao_acumulada")
    limiar_A: float = Field(80.0, description="TED · default declarado 80% · range 50-95%")
    limiar_B: float = Field(95.0, description="TED · default declarado 95% · range limiar_A+1% até 99%")
    modo: Literal["ABC_COMPLETO", "DICOTOMICO_V10"] = Field(
        "ABC_COMPLETO", description="V10 usa DICOTOMICO_V10 · limiar_B fixo 100% oculto"
    )
    coluna_grupo_para_limiares_globais: Optional[str] = Field(
        None, description="V4 Modo 3 · limiares globais aplicados cross-medida · garante comparabilidade"
    )
```

**Contrato de saída:**

```python
class ABCResult(BaseModel):
    coluna_classe_adicionada: str      # ex: 'classe_abc' · valores 'A' | 'B' | 'C' · ou 'VITAL' | 'DEMAIS' em DICOTOMICO_V10
    contagem_por_classe: Dict[str, int]
    limiar_A_aplicado: float
    limiar_B_aplicado: float
    warnings_gerados: List[WarningEstrutural]
```

**Regra de classificação:**

```
Para cada linha (na ordem do rank crescente):
  se acumulado_anterior < limiar_A:
    se acumulado_atual >= limiar_A OR (acumulado_anterior < limiar_A AND acumulado_atual < limiar_A):
      classe = 'A'
  sinão se acumulado_anterior < limiar_B:
    se acumulado_atual >= limiar_B OR (acumulado_anterior < limiar_B AND acumulado_atual < limiar_B):
      classe = 'B'
  sinão:
    classe = 'C'
```

Formulação simplificada · regra de corte "o item que **atinge ou ultrapassa** o limiar pertence à faixa correspondente" (D-040).

**Modo DICOTOMICO_V10 (D-045):**
- `limiar_A` editável pela usuária (default 80%)
- `limiar_B` fixado internamente em 100% · **oculto da UI** · não editável
- Saída: classe ∈ {`VITAL`, `DEMAIS`} em vez de {A, B, C}
- Microcopy de exibição: "Vitais" (Classe A) · "Demais itens" (colapso B+C)
- Redirecionamento declarativo para V4 Modo 2 quando usuária quer ver A/B/C separadamente

**Warnings canônicos:**
- `W-V{N}-ABC-LIMIAR-CUSTOM` (informativo) · limiar_A editado do default
- `W-V{N}-ABC-LIMIAR-B-CUSTOM` (informativo · V4 apenas) · limiar_B editado do default
- `W-V{N}-ABC-CLASSE-VAZIA` (alerta) · quando classe A ou B fica vazia (distribuição pulverizada · V10 microcopy específica "Nenhum item concentra até N% do total isoladamente")

**API pública:**

```python
# /src/transversais/t_abc.py

def aplicar_abc(
    df: pd.DataFrame,
    config: ConfigABC,
    nome_visao: str,
    nome_coluna_classe: str = "classe_abc"
) -> Tuple[pd.DataFrame, ABCResult]:
    ...
```

**Invariante de comparabilidade V4 Modo 3 (D-040):** quando `coluna_grupo_para_limiares_globais` está definida (V4 Modo 3 com múltiplas medidas), os limiares são aplicados **globalmente** · mesmos para todas as medidas · preserva comparabilidade da divergência entre medidas. Limiares por-medida seriam bug analítico neste modo.

---

### E.5 · `T-PIVOT` · Pivot POR_LINHAS → POR_COLUNAS com 3 semânticas (V2 · V3 · V4)

**Origem canônica:** D-026 (refino DCV-V2). Consolidado em 3 semânticas distintas com refinos posteriores.

**Consumidores:** V2 (semântica 1 · Modo 4 · estados empilhados · D-026), V4 (semântica 2 · multi-medida · D-039), V3 (semântica 3 · pontos do eixo empilhados · D-062).

**Contrato de entrada:**

```python
class ConfigPivot(BaseModel):
    semantica: Literal["ESTADOS_EMPILHADOS", "MULTI_MEDIDA", "PONTOS_DO_EIXO"] = Field(
        ..., description="3 semânticas formalizadas · detalhe abaixo"
    )
    coluna_discriminadora: str = Field(
        ..., description="Coluna que contém os valores a pivotar · torna-se cabeçalho de colunas"
    )
    valores_selecionados: Optional[List[str]] = Field(
        None, description="D-026 · usuário escolhe quais valores pivotar · None = todos"
    )
    coluna_valor_a_agregar: str = Field(
        ..., description="Coluna numérica cujo valor vai preencher a matriz pivotada"
    )
    agrupadores: List[str] = Field(
        default_factory=list,
        description="Colunas preservadas como índice da matriz pivotada"
    )
    regra_agregacao_em_colisao: Literal["SUM", "MEAN", "MAX", "MIN", "COUNT"] = Field(
        "SUM", description="Aplicada quando combinação (agrupadores + valor_discriminador) tem múltiplas linhas · zero consumo cruzado com T-AGRUPA nesta etapa"
    )
```

**Contrato de saída:**

```python
class PivotResult(BaseModel):
    df_pivotado: pd.DataFrame                # novo DataFrame em formato wide · colunas = valores pivotados
    colunas_geradas: List[str]               # nomes das novas colunas = valores da coluna_discriminadora
    valores_pivotados: List[str]             # subset aplicado
    valores_nao_pivotados: List[str]         # valores únicos da coluna_discriminadora não selecionados
    linhas_colidas_consolidadas: int         # contagem de casos onde regra_agregacao_em_colisao foi acionada
    warnings_gerados: List[WarningEstrutural]
```

**Diferença entre as 3 semânticas (vocabulário · não contrato):**

| Semântica | Exemplo canônico | Visão | D-XXX |
|---|---|---|---|
| **ESTADOS_EMPILHADOS** | Coluna `Periodo` com valores `Jan/24` e `Jan/25` discriminando a **mesma medida** entre 2 estados | V2 Modo 4 | D-026 |
| **MULTI_MEDIDA** | Coluna `Tipo_Medida` com valores `Receita` · `Custo` · `Margem` discriminando **medidas distintas** | V4 | D-039 |
| **PONTOS_DO_EIXO** | Coluna `Mes` com valores `Jan` · `Fev` · `Mar` discriminando **pontos do eixo sequencial** | V3 | D-062 |

**Motor opera idêntico nas 3 semânticas** · diferença é interpretativa (vocabulário de configuração, microcopy, bloco "Seleção de valores" ativado em condições diferentes). Internamente usa `pandas.pivot_table` com `index=agrupadores`, `columns=coluna_discriminadora`, `values=coluna_valor_a_agregar`, `aggfunc=regra_agregacao_em_colisao`.

**Bloco "Seleção de valores" ativado por regra (vocabulário da UI · detalhe na Spec de cada visão):**

| Semântica | Quando ativa | Threshold (TED) |
|---|---|---|
| ESTADOS_EMPILHADOS | Sempre em Modo 4 V2 | — |
| MULTI_MEDIDA | Sempre em V4 POR_LINHAS | — |
| PONTOS_DO_EIXO | Cardinalidade da coluna_discriminadora ≥ 10 valores únicos | 10 · editável range 5-30 |

**Warnings canônicos:**
- `W-V{N}-PIVOT-COLISAO` (informativo) · registra casos de colisão consolidados pela `regra_agregacao_em_colisao`
- `W-V{N}-PIVOT-VALORES-NAO-SELECIONADOS` (informativo) · lista valores únicos da coluna_discriminadora não incluídos em `valores_selecionados`
- `W-V{N}-PIVOT-CARDINALIDADE-ALTA` (alerta · semântica PONTOS_DO_EIXO) · dispara quando cardinalidade > 50

**API pública:**

```python
# /src/transversais/t_pivot.py

def aplicar_pivot(
    df: pd.DataFrame,
    config: ConfigPivot,
    nome_visao: str
) -> Tuple[pd.DataFrame, PivotResult]:
    ...
```

**Decisão técnica pura resolvida nesta spec:**

T-PIVOT é transversal de **estrutura**, não de **cálculo consolidado**. A consolidação analítica sobre valores pivotados (soma de Receita por cliente, por exemplo) é feita **depois** pelo consumidor via T-AGRUPA. Separação clara · zero confusão de responsabilidade entre T-PIVOT e T-AGRUPA. Isto resolve pergunta implícita dos DCVs V4 e V2 sobre "quem consolida quando há pivot".

---

## Seção F · Transversais de composição

Esta seção especifica 4 transversais de **composição** · transformam a entrada ou produzem estruturas novas que visões consomem. Distinção vs §E: transversais de §E operam sobre DataFrame já consolidado produzindo enriquecimento (ranking, acumulado, classe); transversais de §F operam **antes** do ciclo analítico (T-DUAL, T-CONCAT antes do cálculo · T-FUZZY em paralelo ao cálculo · T-MODELO persistindo a configuração completa).

### F.1 · `T-DUAL` · Entrada em modo dual (V1 · V11)

**Origem canônica:** D-018 (refino DCV-V1). Estendido a V11 em D-047 sem mudança de contrato.

**Consumidores:** V1, V11. Visões da Família A que operam sobre 2 bases lógicas (Origem × Comparado).

**Contrato de entrada (consumido por `motor_upload`):**

```python
class ConfigUploadDual(BaseModel):
    estrutura: Literal["DOIS_ARQUIVOS", "UM_ARQUIVO_DUAS_ABAS"] = Field(
        ..., description="2 estruturas canônicas aceitas · rejeição explícita de RESHAPE (M2 operação futura)"
    )
    arquivo_origem: ArquivoEscolhido = Field(..., description="Identificação da fonte lado Origem")
    arquivo_comparado: ArquivoEscolhido = Field(..., description="Identificação da fonte lado Comparado")
    rotulo_origem: str = Field("Origem", description="Editável pelo usuário · exibição no produto")
    rotulo_comparado: str = Field("Comparado", description="Editável pelo usuário · exibição no produto")

class ArquivoEscolhido(BaseModel):
    indice_arquivo: Literal[0, 1]    # em DOIS_ARQUIVOS: 0 é primeiro arquivo, 1 é segundo · em UM_ARQUIVO_DUAS_ABAS sempre 0
    aba_escolhida: str
```

**Contrato de saída:** produz `UploadResult` em `modo_upload=DUAL` conforme §A.2. Contrato unificado · sem fork de tipo.

**Rejeição estrutural canônica (C.5 · C.3):** RESHAPE (bases empilhadas em única aba com coluna discriminadora) **não é escopo** de T-DUAL. Motor recusa configuração tentando usar coluna discriminadora como "Origem/Comparado" com microcopy "Base parece estar empilhada · operação RESHAPE fica em M2 · suba 2 arquivos ou 1 arquivo com 2 abas". Bloqueio `B-T-DUAL-RESHAPE-DETECTADO` (escapável não) na camada de validação de configuração.

**Padrão de validação cruzada entre lados** (V1 e V11 usam):
- Estrutura de colunas pode diferir entre lados · V1 declara nomes por lado na configuração · V11 idem
- Nomes de aba não precisam casar (UM_ARQUIVO_DUAS_ABAS)
- Encoding/separador CSV detectados independentemente por lado

**API pública:**

```python
# /src/transversais/t_dual.py

def aplicar_upload_dual(
    config: ConfigUploadDual,
    arquivos_bytes: Dict[int, bytes]    # {indice_arquivo: bytes}
) -> UploadResult:
    """
    Compõe UploadResult com 2 ArquivoInfo · caminho_logico origem e comparado.
    Invocado por motor_upload quando modo_upload=DUAL é declarado.
    """
    ...
```

**Simplicidade declarada:** T-DUAL é predominantemente roteamento + composição de `ArquivoInfo`. Sem adaptações por visão. Consumido idêntico por V1 e V11.

---

### F.2 · `T-MODELO` · Persistência de configuração com TED obrigatório (TODAS as 11 visões)

**Origem canônica:** D-015 (promovido a padrão estrutural de produto · CONTEXT §13.3). **D-123 · TED** adicionou requisito de persistência obrigatória de thresholds editáveis.

**Consumidores:** TODAS as 11 visões (V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11). Primeiro padrão estrutural universal da Fundação.

**Contrato de dado serializado:**

```python
class ModeloConfig(BaseModel):
    # Metadados
    nome_modelo: str = Field(..., description="Nome editável pelo usuário · chave para aplicação")
    descricao: Optional[str] = Field(None, description="Opcional · até 500 chars")
    visao_origem: Literal["V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11"]
    modo_da_visao: Optional[str] = Field(None, description="V2 Modo 1-4 · V4 Modo 1-3 · V5 Global/Segmentado · V9 Global/Segmentado · V6 MVP sem modo")
    data_criacao: datetime
    data_ultima_aplicacao: Optional[datetime]
    versao_contrato: str = Field("1.0", description="Controla evolução do contrato do modelo")
    
    # Configuração lógica (não persiste dado fonte · princípio T-MODELO · D-030)
    agrupadores: List[str] = Field(default_factory=list)
    campos_principais: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapeamento nome_analítico -> nome_coluna · ex: {'medida': 'valor_vendas'}"
    )
    
    # Configurações específicas da visão (flexíveis por visão)
    configuracoes_visao: Dict[str, object] = Field(
        default_factory=dict,
        description="Campos específicos da visão · semânticas · tipos de medida · modos · etc"
    )
    
    # Thresholds editáveis (D-123 · TED · persistência OBRIGATÓRIA)
    thresholds_editaveis: Dict[str, ThresholdEditavel] = Field(
        default_factory=dict,
        description="Todos os parâmetros numéricos operacionais da visão · default + edição + contexto"
    )
    
    # Transversais configurados (quando visão customiza)
    config_t_rank: Optional[Dict] = Field(None, description="Quando visão configura T-RANK com parâmetros próprios")
    config_t_agrupa_por_metrica: Optional[Dict] = Field(None, description="V9 · D-096 · multi-regra")
    config_eixo: Optional[Dict] = Field(None, description="V3/V8 · preserva tipo_declarado e ordem")
    
    # Validação de compatibilidade em aplicação cross-base
    campos_declarados_por_lado: Optional[Dict] = Field(
        None, description="V1/V11 · nomes de campos Origem e Comparado separados"
    )

class ThresholdEditavel(BaseModel):
    valor_default: float = Field(..., description="Default declarado original da visão")
    valor_atual: float = Field(..., description="Valor aplicado · igual ao default ou editado")
    range_permitido: Tuple[float, float] = Field(..., description="Limites editáveis · fora do range é bloqueio")
    unidade: Optional[Literal["percentual", "absoluto", "multiplicador"]] = None
    descricao_uso: str = Field(..., description="Microcopy · para auditoria em T-DIAG")
    foi_editado: bool = Field(False, description="True se valor_atual ≠ valor_default")
```

**Regras de persistência:**

1. **Persiste:** configuração lógica (agrupadores, campos, regras, semânticas), thresholds editáveis, configurações de transversais customizadas, metadados de identificação
2. **NÃO persiste:** arquivo bruto, nome do arquivo, dados fonte, filtros pós-execução, resultado da análise, timestamps de execução

**Regras de aplicação em nova base:**

| Cenário | Comportamento | Warning |
|---|---|---|
| Todos os nomes de campo casam com a nova base | Etapas de configuração pré-preenchidas · usuário avança direto para execução | — (sem warning · aplicação limpa) |
| Alguns nomes não casam | Campos que casam são preenchidos · campos que não casam vêm marcados como "ajustar" · usuário completa manualmente | `W-V{N}-MOD-PARCIAL` (informativo) |
| Estrutura incompatível (ex: V1 modelo aplicado em V4) | Recusa aplicação · mensagem "Modelo criado para V1 não pode ser aplicado em V4" | Bloqueio `B-T-MODELO-ESTRUTURA-INCOMPATIVEL` |
| Threshold persistido fora do range da nova visão | Threshold volta ao default · informa alteração | `W-V{N}-MOD-THRESHOLD-FORA-RANGE` (alerta) |

**Cross-visão em view especializada (D-046):** V4 Modo 2 ↔ V10 aceitam modelo mútuo via mapeamento declarado com diálogo de confirmação listando:
- Parâmetros transferidos (comuns)
- Parâmetros com default da visão-destino (específicos da origem sem equivalente)
- Parâmetros descartados (específicos da origem não aplicáveis)

**Contrato especial V5 (D-104):** T-MODELO persiste não apenas o critério de outlier ativo mas também thresholds dos critérios não-ativos · permite troca rápida de critério em re-execução sem reconfigurar.

**Armazenamento:**

Formato: JSON. Local: ambiente do usuário (sessão Streamlit MVP · extensão futura para persistência em banco para colaboração multi-usuário · fora do MVP).

**API pública:**

```python
# /src/transversais/t_modelo.py

def salvar_modelo(config: ModeloConfig) -> str:
    """Retorna ID do modelo salvo."""
    ...

def aplicar_modelo(
    modelo_id: str,
    visao_destino: str,
    upload_atual: UploadResult
) -> Tuple[Dict, List[WarningEstrutural]]:
    """
    Retorna (configuração pré-preenchida, warnings de aplicação).
    Invocado pelo app de cada visão na etapa de configuração.
    """
    ...

def listar_modelos_aplicaveis(
    visao: str,
    upload_atual: UploadResult
) -> List[ModeloConfig]:
    """Retorna lista filtrada · só modelos compatíveis com a visão atual e estrutura do upload."""
    ...
```

**Decisão técnica pura resolvida nesta spec:**

A validação de "nomes casam com nova base" usa comparação **case-sensitive** e **exata** de strings. Matching fuzzy entre nomes de colunas (ex: "Valor_Venda" casa com "valor_vendas") fica em roadmap `P-T-MODELO-FUZZY-NAMES-Evo` · MVP exige match exato e usuário ajusta manualmente divergências. Esta decisão respeita C.5 (usuário decide se nomes diferentes são o mesmo campo · sistema não infere).

---

### F.3 · `T-FUZZY` · Similaridade textual híbrida (V11 MVP · V1 roadmap)

**Origem canônica:** D-050 (candidato · refino DCV-V11 sessão 1) · D-052 (confirmado como transversal da Fundação após refino completo).

**Consumidores:** V11 (MVP), V1 (P-V1-02-Evo · match fuzzy futuro).

**Contrato de entrada:**

```python
class ConfigFuzzy(BaseModel):
    # Nenhum parâmetro exposto ao usuário · transversal encapsulada
    pass   # T-FUZZY é chamada com apenas 2 strings · sem configuração externa
```

**Contrato de saída:**

```python
class FuzzyScore(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0, description="Score de similaridade em [0, 1]")
    texto_a_normalizado: str         # após normalização interna
    texto_b_normalizado: str         # após normalização interna
    tokens_chave_compartilhados: List[str]    # tokens presentes nos dois lados após extração
    trigramas_comuns: int            # contagem de trigramas em comum
    trigramas_total: int             # união de trigramas dos dois lados
```

**Algoritmo híbrido (pesos internos fixos · não expostos · D-138):**

```
score_trigramas = |trigramas_A ∩ trigramas_B| / |trigramas_A ∪ trigramas_B|   (Jaccard)

tokens_chave_A = extrair_tokens(texto_A_normalizado)
tokens_chave_B = extrair_tokens(texto_B_normalizado)
# extrair_tokens retorna:
#   (a) sequências numéricas >= 4 dígitos (ex: "12345", "2024")
#   (b) sequências alfabéticas maiúsculas >= 3 caracteres consecutivos (ex: "CNPJ", "DOC")

score_tokens = |tokens_A ∩ tokens_B| / max(|tokens_A ∪ tokens_B|, 1)    # 0 se nenhum lado tem tokens

# Pesos internos fixos calibrados · não configuráveis
score_final = 0.65 * score_trigramas + 0.35 * score_tokens

# Ajuste de boost quando pelo menos 1 token-chave é compartilhado e score_trigramas >= 0.4
se len(tokens_chave_compartilhados) >= 1 e score_trigramas >= 0.4:
    score_final = min(1.0, score_final * 1.15)    # boost de 15% · calibração interna
```

**Normalização prévia interna** (invisível ao usuário · registrada em linha única informativa no Diagnóstico da V11):

```
1. strip()
2. lower()
3. unidecode (remoção de acentos · mantém ASCII)
4. remoção de caracteres não-alfanuméricos exceto espaço (regex: [^a-z0-9\s])
5. colapso de espaços múltiplos em espaço único
```

**Determinismo absoluto** (C.1): dado o mesmo par de strings, retorno idêntico. Implementação pura em Python sem dependência de LLM ou modelo probabilístico externo. Testes de regressão obrigatórios em F-TRANS.

**API pública:**

```python
# /src/transversais/t_fuzzy.py

def calcular_score(texto_a: str, texto_b: str) -> FuzzyScore:
    """
    Função pura determinística · sem estado · sem side effects.
    API canônica: (texto_A, texto_B) -> score em [0, 1].
    """
    ...

def extrair_tokens_chave(texto_normalizado: str) -> Set[str]:
    """
    Auxiliar exposto para debug e casos extraordinários.
    Retorna sequências numéricas >=4 dígitos + sequências alfabéticas maiúsculas >=3 chars.
    """
    ...
```

**Transformações textuais semânticas fora do escopo:** unificação de abreviações (ex: "PGTO" = "PAGAMENTO"), stop-words, regex custom ficam **fora** de T-FUZZY · são operação declarada do usuário · território de M2.NORMALIZE (futuro). Diagnóstico da V11 registra microcopy quando alta incidência de "Pareamento frágil" sinaliza padronização textual inconsistente · orienta analista a considerar M2.NORMALIZE futuro · não sugere preventivamente (C.5).

**Decisão técnica pura resolvida (D-138):**

Os pesos internos (0.65 trigramas · 0.35 tokens · boost 1.15 condicional) são **calibração fixa da Fundação**. Alteração exige nova decisão D-XXX porque afeta resultados de todos os consumidores. Testes de regressão em F-TRANS incluem casos canônicos do DCV-V11 (cenário Protheus × Safra) com scores esperados documentados.

---

### F.4 · `T-CONCAT` · Composição declarada de campos-fonte (V11 MVP · M2.CONCAT futuro)

**Origem canônica:** D-053 (candidato · refino DCV-V11 sessão 1) · **D-135** (posicionamento confirmado na Fundação · ver §G).

**Consumidores:** V11 MVP (Família A · uso central para compor campo contextual a partir de múltiplas colunas fonte). M2.CONCAT futuro (herdará código sem reescrita · apenas renomeação).

**Contrato de entrada:**

```python
class ConfigConcat(BaseModel):
    campos_fonte: List[str] = Field(
        ..., min_items=1, max_items=3,
        description="Até 3 campos-fonte · D-053/D-135"
    )
    separador: Literal[" "] = Field(
        " ", description="Separador fixo espaço · D-135 · não configurável no MVP"
    )
    normalizar: bool = Field(
        False,
        description="Se True · aplica lowercase + unidecode + alfanum-mantém-espaço · usado quando output alimenta T-FUZZY"
    )
    tratamento_nulos: Literal["PULAR"] = Field(
        "PULAR",
        description="D-135 · nulos são pulados · se todos nulos resultado é string vazia com warning"
    )
```

**Contrato de saída:**

```python
class ConcatResult(BaseModel):
    coluna_concatenada_nome: str                    # nome da coluna gerada · ex: 'contexto_concat_01'
    valores_gerados: int                            # contagem de linhas com string não-vazia
    valores_vazios_todos_nulos: int                 # contagem de linhas onde todos os campos eram nulos
    valores_parcialmente_nulos: int                 # contagem de linhas com pelo menos 1 campo nulo mas não todos
    warnings_gerados: List[WarningEstrutural]
```

**Regra de composição:**

```
Para cada linha do df:
    componentes = []
    para cada campo em campos_fonte:
        valor = df[campo]
        se valor não é nulo e str(valor).strip() != "":
            se normalizar:
                valor = normalizar_texto(valor)    # mesma normalização interna de T-FUZZY
            componentes.append(str(valor).strip())
    
    resultado = separador.join(componentes)    # " " · space-join
    
    se resultado == "":
        gerar warning W-V11-COMP-CAMPOS-NULOS (todas as fontes nulas para esta linha)
    sinão se len(componentes) < len(campos_fonte):
        gerar warning W-V11-COMP-PARCIAL (pelo menos 1 fonte nula)
    
    df[coluna_concatenada] = resultado
```

**Assimetria permitida (D-135):** V11 aceita composição de contextos com quantidades diferentes de campos-fonte em cada lado · ex: Base Investigada compõe 3 campos em `contexto_inv`, Base de Busca compõe 2 campos em `contexto_busca`. Contrato aceita naturalmente · `min_items=1, max_items=3` aplicado por invocação.

**Vocabulário declarativo · dois modos de uso:**

1. **Modo simples (V11 MVP · composição direta para alimentar T-FUZZY)**: `normalizar=True`, resultado passa direto para `t_fuzzy.calcular_score` downstream. Composição + normalização acontecem na mesma passagem · zero duplicação de normalização.

2. **Modo de composição bruta (preservação de formatação original)**: `normalizar=False`, resultado preservado com acentos, maiúsculas, caracteres especiais. Usado quando composição é destinada a exibição na Base Analítica (auditoria) ou quando normalização não é desejada (caso extraordinário).

**Warnings canônicos:**
- `W-V11-COMP-CAMPOS-NULOS` (informativo) · contagem de linhas com todos os campos-fonte nulos · string vazia como resultado
- `W-V11-COMP-PARCIAL` (informativo) · contagem de linhas com pelo menos 1 campo-fonte nulo mas não todos
- `W-V11-SEM-CONTEXTO` (alerta V11-específico) · dispara quando > 30% das linhas resultam em `W-V11-COMP-CAMPOS-NULOS` · base tem padronização textual inconsistente · analista é orientado a considerar M2.NORMALIZE

**API pública:**

```python
# /src/transversais/t_concat.py

def aplicar_concat(
    df: pd.DataFrame,
    config: ConfigConcat,
    nome_visao: str,
    nome_coluna_resultado: Optional[str] = None
) -> Tuple[pd.DataFrame, ConcatResult]:
    """
    Retorna df com coluna concatenada adicionada + ConcatResult.
    Se nome_coluna_resultado não fornecido, gera 'concat_<hash_curto>'.
    """
    ...

def normalizar_texto(texto: str) -> str:
    """Auxiliar · reutilizado por T-FUZZY e T-CONCAT · módulo /src/utils/normalizacao_texto.py."""
    ...
```

**Posicionamento arquitetural estratégico (D-135):** código de T-CONCAT é escrito desde o início em `/src/transversais/t_concat.py` · quando M2 for implementado (pós-MVP), **M2.CONCAT é implementado como thin wrapper** sobre T-CONCAT apenas adicionando UI de operação M2 e metadados de preparação de dados. Zero reescrita do algoritmo · renomeação opcional em fase tardia.

**Roadmap conhecido:**
- `P-T-CONCAT-SEPARADOR-CONFIGURAVEL-Evo` · separador configurável (default espaço · opções: `-` · `|` · `_`)
- `P-T-CONCAT-MAIS-DE-3-CAMPOS-Evo` · limite de campos-fonte expandido · depende de estudo de impacto em T-FUZZY

**Decisão técnica pura resolvida (D-139):**

Módulo `/src/utils/normalizacao_texto.py` centraliza a normalização interna · consumido por T-FUZZY e T-CONCAT (quando `normalizar=True`). Isso elimina duplicação · garante que normalização é idêntica nos 2 pontos de uso · blinda determinismo C.1. Alteração da normalização exige D-XXX nova por afetar ambos.

---

### F.5 · Consolidação dos 12 transversais da Fundação

Fechamento do escopo de transversais da Fundação · **12 transversais totais** (3 em §D · 5 em §E · 4 em §F) confirmados como escopo de F-TRANS:

| # | Transversal | Seção | Consumidores | Status |
|---|---|---|---|---|
| 1 | T-AGRUPA | §D | TODAS exceto V1/V11 | Consolidado |
| 2 | T-DIAG | §D | TODAS | Consolidado |
| 3 | T-SEMA | §D | V2, V3, V7, V9 | Consolidado |
| 4 | T-EIXO | §E | V3, V8 | Consolidado |
| 5 | T-RANK | §E | V1, V4, V6, V7, V9, V10, V11 | Consolidado |
| 6 | T-ACUM | §E | V4, V10 | Consolidado |
| 7 | T-ABC | §E | V4, V10 | Consolidado |
| 8 | T-PIVOT | §E | V2, V3, V4 | Consolidado |
| 9 | T-DUAL | §F | V1, V11 | Consolidado |
| 10 | T-MODELO | §F | TODAS | Consolidado |
| 11 | T-FUZZY | §F | V11 MVP · V1 roadmap | Consolidado |
| 12 | T-CONCAT | §F | V11 MVP · M2.CONCAT futuro | Consolidado (D-135) |

**Escopo F-TRANS definitivo:** 12 transversais. F-BASE consome Dict de configurações por visão · contratos de I/O entre transversais estáveis.

---

## Seção G · Decisão de roadmap · T-CONCAT e M2.STACK (D-135)

**Decisão de negócio fechada em 20/04/2026 · M1 da D-131.**

**Decisão mista:**
- **T-CONCAT entra na Fundação como transversal fundamental** (Posição 1 · código vive em `/src/transversais/t_concat.py`) · V11 consome no MVP · implementação com estrutura apta para renomeação/extração futura para `M2.CONCAT` sem reescrita (zero duplicação arquitetural · coerente com D-053 original).
- **M2.STACK sai do escopo da Fundação** (Posição 2 · fica em M2) · V3 · V6 · V8 mantêm multi-aba como roadmap pós-MVP conforme declarado nos DCVs aprovados (P-V3-01-Evo · P-V8-01-Evo · P-V6-02-MULTIABA-Evo).

**Razão:**
1. **T-CONCAT tem consumidor MVP (V11)** e implementação simples (concatenar 2-3 strings com separador) · implementar na Fundação não atrasa significativamente
2. **M2.STACK tem 3 consumidores em roadmap (V3/V6/V8 · nenhum MVP)** e implementação complexa (detecção de estrutura idêntica entre abas · tratamento de divergência · vocabulário · bloco de confirmação · warnings) · implementar já atrasaria a Fundação em 3-4 semanas sem urgência de entrega
3. **Princípio da fase:** DCVs de V3/V6/V8 declararam explicitamente multi-aba como fora do escopo MVP · Opção B ratifica essa decisão anterior · Opção A/C revisaria sem justificativa de negócio nova
4. **Risco técnico reduzido:** M2.STACK implementado em M2 terá contexto completo do Módulo 2 (onde outras operações de preparação vivem) · decisão de posicionamento mais informada

**Consequências arquiteturais:**
- `/src/transversais/t_concat.py` é especificado em §F.4 como transversal de composição
- M2.STACK **não aparece** na tabela de transversais · GLOSSARIO §4 atualizado para refletir posicionamento M2
- V3/V6/V8 mantêm intacta a declaração de multi-aba como roadmap pós-MVP nos DCVs

**Consequências para F-TRANS:**
- Bloco F-TRANS implementa 12 transversais da Fundação: T-AGRUPA · T-DIAG · T-SEMA · T-EIXO · T-RANK · T-ACUM · T-ABC · T-PIVOT · T-DUAL · T-MODELO · T-FUZZY · **T-CONCAT** (adicionado por D-135)

**Consequências para roadmap posterior:**
- **M2 futuro** herda T-CONCAT da Fundação (renomeação para M2.CONCAT · zero reescrita) · implementa M2.STACK do zero com contexto completo
- **V3/V6/V8 MVP** saem no roadmap da Família B/C/E sem multi-aba · usuário consolida manualmente ou espera M2

### G.1 · Especificação preliminar de T-CONCAT

Dimensões cristalizadas em D-053 + refino T-04 do DCV-V11 · detalhe completo em §F.4:
- Até **3 campos-fonte** por composição
- **Separador fixo: espaço**, visível no preview da configuração
- **Assimetria permitida** — lados compõem com quantidades diferentes de campos-fonte (V11)
- **Tratamento de nulos:** campos nulos são pulados · se todos os componentes são nulos, resultado é string vazia (W-V11-COMP-CAMPOS-NULOS)
- **Normalização opcional:** lowercase · remoção de acentos · remoção de caracteres não-alfanuméricos (usado por V11 via T-FUZZY a jusante)

---

## Seção Exportação · `exportacao.py` consolidado

Esta seção especifica o módulo `exportacao.py` da Fundação que materializa o resultado de qualquer `VNResultBase` em arquivo Excel consumível. Três dimensões cobertas: **estrutura padrão de abas** (alinhamento cross-visão), **capabilities técnicas** (tipos de renderização necessários), **posicionamento arquitetural como bloco único** (D-136).

### EXP.1 · Estrutura padrão de abas por visão

Aplicação direta dos padrões formalizados em CONTEXT §13.5 (Resumo Executivo em 6 Blocos · D-125) · §13.6 (Coração Visual · D-126) · §9 Camada C · C.D3 (BAD · Base Analítica e Diagnóstico · D-124) · D-017 (Diagnóstico sempre última aba).

**Esqueleto padrão de abas** (ordem fixa · consumida por toda visão):

| # | Aba | Obrigatoriedade | Origem do padrão |
|---|---|---|---|
| 1 | **Resumo Executivo** | Toda visão · primeira aba | D-125 · §13.5 · 6 blocos fixos |
| 2 | **Coração Visual** | Toda visão · nome específico por visão | D-126 · §13.6 |
| N | **Abas analíticas específicas** | Variável por visão · entre Coração Visual e Base Analítica | Decisão por DCV |
| N+1 | **Base Analítica** | Toda visão | C.D3 · D-124 · linhas com classificações |
| N+2 | **Parâmetros** | Toda visão · penúltima | Padrão BAD · §9 C.D3 |
| Última | **Diagnóstico** | Toda visão · sempre última | D-017 invariante transversal |

**Aplicação consolidada por visão (do que os 11 DCVs aprovados declararam):**

| Visão | Coração Visual declarado | Abas analíticas específicas | Total |
|---|---|---|---|
| **V2** | Matriz de Confronto (retroação S-V2) | Análise Comparativa · Ranking de Variações | 5-6 |
| **V1** | Mapa de Conciliação (retroação S-V1) | Ponte de Conciliação · Resumo por Agrupador | 5-6 |
| **V11** | Mapa de Aderência (retroação S-V11) | Pareamentos · Sem par · Ponte de Conciliação (opcional) | 5-7 |
| **V4** | Composição Principal | Análise Principal · Comparação de Distribuição (Modo 3) | 5-7 |
| **V10** | Curva Pareto | Vitais · Demais itens | 6 |
| **V3** | (a declarar em S-V3) | Análise Sequencial · Comparação entre Núcleos (Modo Comparativo) | 5-6 |
| **V8** | Matriz de Presença | Movimentações · Ranking de Presença | 6 |
| **V7** | Mapa de Grupos | Detalhe · Desvios Significativos | 6 |
| **V9** | Mapa de Perfil | Detalhe Multi-Métrica · Destaques · Resumo por Agrupador (Segmentado) | 6-7 |
| **V5** | Mapa de Distribuição | Outliers · Resumo por Segmento (Segmentado) | 6-7 |
| **V6** | Matriz de Cruzamento | Ranking de Combinações · Combinações Ausentes | 7 |

**Invariantes cross-visão:**
- Resumo Executivo **sempre** é a primeira aba
- Coração Visual **sempre** é a segunda aba
- Diagnóstico **sempre** é a última aba (D-017)
- Parâmetros **sempre** é a penúltima aba
- Base Analítica **sempre** fica antes de Parâmetros
- Filtros ativos em todas as abas tabulares (default declarado)

### EXP.2 · Contratos de exportação

**API pública do módulo:**

```python
# /src/exportacao.py

def exportar_resultado(
    resultado_visao: VNResultBase,
    caminho_saida: str,
    configuracao_exportacao: Optional[ConfigExportacao] = None
) -> ExportacaoResult:
    """
    Materializa VNResultBase em arquivo .xlsx.
    Invocado pelo app_vN.py quando usuário clica em "Exportar Excel".
    """
    ...

class ConfigExportacao(BaseModel):
    incluir_graficos_nativos: bool = Field(True, description="Default True · desativável para export rápido")
    aplicar_formatacao_condicional: bool = Field(True, description="Cores de classificação")
    paginar_matrizes_grandes: bool = Field(True, description="V6 · V8 · matrizes > 30×30")
    aplicar_filtros_automaticos: bool = Field(True, description="AutoFilter em todas abas tabulares")
    nome_arquivo_saida: Optional[str] = Field(None, description="Nome customizado do arquivo de saída · default None = auto")

class ExportacaoResult(BaseModel):
    caminho_arquivo: str
    tamanho_bytes: int
    numero_abas: int
    tempo_geracao_segundos: float
    warnings_gerados: List[WarningEstrutural]
    capabilities_acionadas: List[str]    # auditoria · quais capabilities foram usadas
```

### EXP.3 · Capabilities consolidadas

As 11 visões exigem um conjunto finito de capabilities técnicas de renderização Excel. Cada capability é um módulo do `exportacao.py` · testável isoladamente · reutilizável entre visões.

**Catálogo de capabilities (11 módulos):**

| # | Capability | Consumidores | Tecnologia | Complexidade |
|---|---|---|---|---|
| 1 | **CAP-TABELA-FORMATADA** | Todas (Base Analítica · Parâmetros · etc) | openpyxl · styles · borders · headers | Baixa |
| 2 | **CAP-RESUMO-EXECUTIVO** | Todas (aba 1 · 6 blocos) | openpyxl · cells + styles + microcopy | Média |
| 3 | **CAP-DIAGNOSTICO** | Todas (aba última) | openpyxl · lista de warnings categorizados | Baixa |
| 4 | **CAP-BARCHART-NATIVO** | V4 · V10 · V5 · V7 | openpyxl.chart.BarChart | Média |
| 5 | **CAP-COLUMNCHART-EMPILHADO-100** | V6 | openpyxl.chart.BarChart type=col stacked=percent | Média-Alta |
| 6 | **CAP-LINECHART-NATIVO** | V10 (acumulado) · V8 (presença ao longo do tempo opcional) · V3 (sequencial) | openpyxl.chart.LineChart | Média |
| 7 | **CAP-COMBO-BAR-LINE** | V10 (Curva Pareto · barras + linha acumulada com 2 eixos Y) | openpyxl.chart com secondary_axis | Alta |
| 8 | **CAP-FORMATACAO-CONDICIONAL-MATRIZ** | V6 (densidade · por célula) · V8 (presença × ausência) · V9 (heatmap) | openpyxl.formatting.rule · ColorScaleRule · FormulaRule | Alta |
| 9 | **CAP-HISTOGRAMA-BINS** | V5 (Mapa de Distribuição) | openpyxl.chart.BarChart com bins pré-calculados | Média |
| 10 | **CAP-PAGINACAO-MATRIZ** | V6 (> 30×30) · V8 (> 30 pontos × 30 entidades) | Geração de abas secundárias com notas de navegação | Alta |
| 11 | **CAP-AUTOFILTER** | Todas (abas tabulares) | openpyxl.Worksheet.auto_filter | Baixa |

**Mapa visão × capabilities:**

| Visão | Capabilities consumidas |
|---|---|
| **V2** | 1, 2, 3, 11 |
| **V1** | 1, 2, 3, 11 |
| **V11** | 1, 2, 3, 11 |
| **V4** | 1, 2, 3, 4, 11 |
| **V10** | 1, 2, 3, 4, 6, 7, 11 |
| **V3** | 1, 2, 3, 6, 11 |
| **V8** | 1, 2, 3, 8, 10, 11 |
| **V7** | 1, 2, 3, 4, 11 |
| **V9** | 1, 2, 3, 8, 11 |
| **V5** | 1, 2, 3, 4, 9, 11 |
| **V6** | 1, 2, 3, 5, 8, 10, 11 |

**Capabilities universais** (consumidas por todas as 11 visões): 1 · 2 · 3 · 11.

**Capabilities especializadas** (consumidas por 1-4 visões): 4 · 5 · 6 · 7 · 8 · 9 · 10.

**Capability de maior complexidade** (requisito exclusivo V10): 7 · CAP-COMBO-BAR-LINE (barras + linha com 2 eixos Y + linhas pontilhadas de referência).

### EXP.4 · Posicionamento arquitetural · F-EXP como bloco único (D-136)

**Decisão de negócio fechada em 20/04/2026 · M2 da D-131.**

**Tradução decisional aplicada:** em que ordem as 11 visões vão ficar "visualmente prontas" · todas juntas após F-EXP inteiro ou priorizando algumas famílias. 3 opções foram apresentadas (A · bloco único · B · 3 sub-blocos por família · C · 2 sub-blocos CORE+VISUAL) com trade-offs de roadmap e recomendação do Arquiteto por B. Usuária escolheu **Opção A · F-EXP bloco único** priorizando simplicidade arquitetural e consistência visual.

**Consequências operacionais:**
- Roadmap linear da Fase 1: **F-MOT → F-TRANS → F-EXP (único) → F-BASE → Fase 2 Família A**
- Consistência visual garantida · todas as 11 visões saem com mesmo nível de polimento
- Simplicidade arquitetural · 1 bloco · 1 revisão · 1 teste integrado · sem risco de divergência entre sub-blocos
- Trade-off aceito: Família A (V2 · V1 · V11) espera F-EXP completo mesmo precisando apenas das 4 capabilities universais (1 · 2 · 3 · 11)
- Bloco IA-Família-A (D-130) acontece após validação visual de V2 · V1 · V11 · como originalmente previsto · timing ajustado mas ordem preservada
- As 11 capabilities (CAP-TABELA-FORMATADA · CAP-RESUMO-EXECUTIVO · CAP-DIAGNOSTICO · CAP-BARCHART-NATIVO · CAP-COLUMNCHART-EMPILHADO-100 · CAP-LINECHART-NATIVO · CAP-COMBO-BAR-LINE · CAP-FORMATACAO-CONDICIONAL-MATRIZ · CAP-HISTOGRAMA-BINS · CAP-PAGINACAO-MATRIZ · CAP-AUTOFILTER) são implementadas em sequência dentro do mesmo bloco F-EXP

### EXP.5 · Warnings canônicos da exportação

Warnings gerados por `exportacao.py` durante materialização:

- `W-EXP-GRAFICO-FALHA` (alerta) · capability de gráfico nativo openpyxl falhou · aba é gerada sem gráfico · dados preservados em tabela
- `W-EXP-MATRIZ-GRANDE-PAGINADA` (informativo) · matriz > 30×30 foi paginada · lista das abas geradas
- `W-EXP-FORMATACAO-TRUNCADA` (alerta) · regras de formatação condicional excederam limite Excel (64000 regras) · parte foi aplicada · aba marcada
- `W-EXP-ARQUIVO-GRANDE` (informativo) · arquivo gerado > 50MB · tempo de geração > 30s · sugere uso de filtros
- `W-EXP-COLUNA-TRUNCADA` (alerta) · coluna excedeu 32767 caracteres (limite Excel) · valor truncado

### EXP.6 · Decisões técnicas puras resolvidas (sem D-XXX)

1. **Biblioteca base:** `openpyxl` 3.1+ · suporte completo a gráficos nativos · formatação condicional · AutoFilter. `xlsxwriter` descartado (desempenho em abas muito grandes com gráficos é inferior · padrão da comunidade Python tab-analítica migrou para openpyxl).
2. **Streaming vs build-in-memory:** `openpyxl` modo `write_only` para abas com > 10000 linhas (Base Analítica de V5/V6/V8 em bases grandes). Abas menores (Resumo · Parâmetros · Diagnóstico) em modo padrão. Decisão fica transparente via capability adequada.
3. **Formatação condicional em matrizes** (CAP-FORMATACAO-CONDICIONAL-MATRIZ): usa `ColorScaleRule` para heatmap-like (V9 Mapa de Perfil) · `FormulaRule` para classificação discreta (V6 densidade · V8 presença/ausência). Limite Excel de 64000 regras observado · paginação de matriz > 30×30 mitiga.
4. **Heatmap real em V6:** não suportado nativamente em openpyxl · alternativa declarada ColumnChart empilhado 100% (D-118 · consumida em CAP-COLUMNCHART-EMPILHADO-100). Roadmap P-V6-06-HEATMAP-NATIVO-Evo preserva gancho.
5. **Gráficos com 2 eixos Y** (V10 Curva Pareto · CAP-COMBO-BAR-LINE): suportado via `secondary_axis` do openpyxl · testes de regressão garantem renderização consistente entre Excel 365 e LibreOffice Calc.

---

## Seção H · Arquitetura do dataset sintético de fundação

### H.1 · Arquitetura · dataset único multi-aba

**Decisão técnica resolvida (D-140):** `base_fundacao.xlsx` é um arquivo Excel único com N abas nomeadas por cenário. **Não múltiplos arquivos temáticos.**

**Rationale:**
- F-BASE definido em CONTEXT §3 como "base sintética de fundação multi-visão" · singular por design
- Alinhado com estrutura de pastas declarada em CONTEXT: `/bases/base_fundacao.xlsx`
- Reprodutibilidade C.1 · um único arquivo com semente fixa é auditável · não há risco de derivação de subconjuntos desincronizados
- motor_upload consome um caminho de arquivo · responsabilidade de escolher qual aba virar `df_base` é do usuário/teste (convenção F-MOT)
- T-DUAL é exceção arquitetural tratada via 2 abas dedicadas (§H.4) · não via 2 arquivos

### H.2 · Dimensões do dataset · linhas · cardinalidades · distribuições

**Decisão técnica resolvida:** dimensionamento calibrado para 3 objetivos simultâneos (volume realista · cobertura de patamares ECP · auditabilidade manual). Parâmetros registrados em `casos_esperados.yaml` como metadados.

**Regras de calibração por aba:**

| Parâmetro | Valor | Justificativa |
|---|---|---|
| Linhas por aba · padrão | 80-120 | Acima de B.3 (≥50) · Usuária consegue inspecionar manualmente |
| Linhas · cenário "volume alto" | 300-500 | Cobre ECP alta cardinalidade · exercita CAP-PAGINACAO-MATRIZ |
| Cardinalidade de agrupador · padrão | 3-8 categorias | Zona saudável ECP |
| Cardinalidade · "muitas categorias" | 25-50 | Zona de warning ECP · exercita W-CARD-ALTA |
| Cardinalidade · "excessiva" | 80+ | Zona de bloqueio ECP (MBO) em 1 aba específica |
| Campo numérico · distribuição padrão | log-normal (μ=6 · σ=1) | Cauda realista · alimenta Pareto (V10) · exercita outliers (V5) |
| Campo numérico · distribuição uniforme | 1 aba específica | Contra-exemplo para T-ABC · V10 deve classificar "sem concentração" |
| % de NULO_MEDIDA | 5-8% distribuído | Exercita warnings de consolidação sem dominar |
| % de Ausente (nulo em agrupador) | 2-4% concentrado | Warning estrutural distinto de NULO_MEDIDA |
| **Semente aleatória** | **`SEED = 42`** | **Determinismo C.1 · D-140 · invariante** |

### H.3 · Domínio simulado de referência

**Decisão técnica resolvida:** vocabulário misto pragmático em pt-BR · não um único domínio fechado.

**Rationale:** forçar um único domínio empobrece cenários · V11 pede descrições de fornecedores com ruído realista · V3 pede períodos claros · V6 pede 2 categóricas ortogonais não-triviais. Abas mapeadas por domínio:

| Domínio | Campos canônicos | Visões que consomem mais |
|---|---|---|
| Vendas varejo | `Mes · Loja · Produto · Categoria · Vendas · Margem · Quantidade` | V2 · V3 · V4 · V8 · V10 |
| Conciliação financeira | `Origem · Comparado · Conta · Centro_Custo · Cliente · Valor · Data` | V1 · V11 (T-DUAL) |
| Operação/logística | `Filial · Transportadora · Região · Status_Entrega · Prazo_Dias · Peso_Kg · Valor_Frete` | V5 · V6 · V7 · V9 |
| Cadastral | `Fornecedor_ID · Nome_Fornecedor · CNPJ · Cidade · UF · Segmento` | V11 (T-FUZZY sobre `Nome_Fornecedor`) |

**Unidades:** monetárias em R$ · datas em formato misto pt-BR/pt-EN (cobrir reconhecedor D-026).

### H.4 · Tratamento do modo DUAL (T-DUAL · V1 · V11)

**Decisão técnica resolvida:** 2 abas dedicadas no `base_fundacao.xlsx` formando **1 par DUAL único compartilhado por V1 e V11**.

**Mecânica:**
- Aba `dual_origem_crm` · ~110 linhas · campos `Conta · Centro_Custo · Cliente · Valor · Data`
- Aba `dual_comparado_erp` · ~105 linhas · mesmos campos com sinônimo controlado (`Cliente` vs `Razao_Social` para exercitar matching de nomes em T-MODELO)

**Divergências controladas embutidas** (declaradas como assertions em §J):
- Match exato (maioria · ~70%)
- Match tolerado (diferença ≤ R$ 0,01 em Valor · 3-5 linhas)
- Divergência significativa (Valor acima de tolerância · 8-10 linhas)
- Só na Origem (sem par · 6-8 linhas)
- Só no Comparado (sem par · 5-7 linhas)
- Nome_Cliente similar-mas-não-idêntico (exercitar T-FUZZY V11 · opcional)
- Mesmo par exato por acaso (ambiguidade potencial P-V1-04 · 2 linhas)

**Por que 1 par único e não 2 pares separados?** V1 e V11 são **Família A · Confronto** e compartilham T-DUAL como contrato de entrada · usar o mesmo par valida que o contrato T-DUAL é idempotente entre as duas visões · `casos_esperados.yaml` em §J declara assertions distintas por visão sobre o mesmo dataset. Reduz linhas duplicadas de base em ~100.

### H.5 · Inventário canônico · 14 abas de `base_fundacao.xlsx`

**Decisão técnica resolvida:** inventário cristalizado em **14 abas** (D-140 · extensão exige D-YYY nova).

| # | Nome da aba | Cenário coberto | Visões principais | Tamanho |
|---|---|---|---|---|
| 1 | `vendas_padrao` | POR_LINHAS · vendas mensais por loja/produto · 2 meses | V2 (Modo 4) · V4 (Modos 1 e 3) | 120 linhas |
| 2 | `vendas_por_colunas` | POR_COLUNAS · meses como colunas · T-PIVOT | V2 alternativo · V3 (semântica 3) | 25 linhas × 14 colunas |
| 3 | `vendas_pre_agregadas` | Dados já agregados · cenário-limite CPCO | V4 · V10 | 50 linhas |
| 4 | `operacao_dispersao` | Univariado numérico · Prazo_Dias · outliers | V5 | 200 linhas |
| 5 | `operacao_cruzamento` | Bivariado · Filial × Transportadora · células ausentes | V6 | 180 linhas |
| 6 | `operacao_perfil_grupo` | Grupos internos + segmentador externo | V7 · V9 | 150 linhas |
| 7 | `dual_origem_crm` | T-DUAL lado Origem | V1 · V11 | 110 linhas |
| 8 | `dual_comparado_erp` | T-DUAL lado Comparado | V1 · V11 | 105 linhas |
| 9 | `cadastral_fuzzy` | Nome_Fornecedor com ruído · CNPJ formato misto | V11 (T-FUZZY foco · T-CONCAT virtual) | 80 linhas |
| 10 | `vendas_volume_alto` | 400 linhas · cardinalidade Produto=45 · Pareto 80/20 | V10 · V8 · V4 | 400 linhas |
| 11 | `cardinalidade_excessiva` | Agrupador com 85 categorias · dispara bloqueio MBO | Teste de BloqueioOperacional | 200 linhas |
| 12 | `boolean_disfarcado` | Coluna Ativo como "Sim/Nao" · exercita D-008 | Teste motor_upload isolado | 60 linhas |
| 13 | `eixo_sequencial_lacunas` | Meses com lacunas intencionais · T-EIXO | V3 · V8 | 80 linhas |
| 14 | `eixo_sequencial_completo` | Meses completos · T-EIXO caso feliz | V3 · V8 | 100 linhas |

**Total:** 14 abas · ~2.063 linhas agregadas.

**Invariantes cristalizados em D-140:**
1. O arquivo é único (`base_fundacao.xlsx`) · nome imutável sem D-YYY
2. O inventário é 14 abas · adição ou remoção exige D-YYY
3. A semente é `SEED = 42` · alteração exige D-YYY e regeneração integral
4. Nomes de abas são canônicos · renomeação exige D-YYY e atualização de `casos_esperados.yaml`

**Tolerância amostral declarada em D-145 (21/04/2026 · retrospectiva F-BASE):** o til literal aplicado ao total ("~2.063") propaga-se aos tamanhos individuais por aba. Valores na coluna "Tamanho" são **alvos com tolerância operacional de ~3%** quando invariantes categóricos (cardinalidades declaradas em §I · ex: Filial=8, Transportadora=6, Regiao=4, Produto=45, agrupador=85) e warnings esperados (ex: `W-V9-SEGMENTO-TAMANHO-INSUFICIENTE` exige segmento com <3 filiais · restringe distribuição amostral possível) tornam o número exato inatingível sem colisões ou violações de contrato. **Contratos fechados** (imutáveis sem D-YYY) permanecem: (a) inventário de 14 abas · (b) nomes canônicos · (c) cardinalidades categóricas declaradas em §H.5/§I · (d) SEED=42. **Sob tolerância** ficam apenas os totais de linhas por aba. Base F-BASE atual (21/04/2026): 1853 linhas agregadas · 12 abas no alvo exato · `operacao_cruzamento` 175 (−5, −2.8%) · `operacao_perfil_grupo` 148 (−2, −1.3%) · todas dentro da tolerância declarada.

---

## Seção I · Cobertura por visão

Mapeamento canônico de quais cenários cada visão consome · quais casos-limite são cobertos · quais warnings são esperados. Consumido por `casos_esperados.yaml` (§J) como base da estrutura de assertions por visão.

### I.1 · V2 · Comparação entre estados (Família A)

**Cenário principal:** `vendas_padrao` · Modo 4 (estados empilhados via T-PIVOT semântica 1 · D-026). Discriminador `Mes` com 2 estados comparáveis (`2025-01` e `2025-02`).

**Casos-limite cobertos:** elemento Ausente em um lado (2-4 ocorrências) · elemento Ausente no lado inverso · NULO_MEDIDA em Vendas (3-4 ocorrências) · variação percentual positiva e negativa (T-SEMA maior-é-melhor sobre Vendas) · cardinalidade saudável de Produto (~12 categorias).

**Warnings esperados:** `W-V2-AUSENTE-EM-UM-LADO` (2-4) · `W-NULO-MEDIDA` (3-4).

**Cenário secundário:** `vendas_por_colunas` · exercita T-PIVOT semântica 1 antes do cálculo.

### I.2 · V1 · Confronto entre bases (Família A · T-DUAL)

**Cenário principal:** `dual_origem_crm` × `dual_comparado_erp`. Campos de match: `Conta · Centro_Custo · Cliente` (3 agrupadores · dentro do limite L-V1-D de 5).

**Casos-limite cobertos:** match exato (~70%) · match aproximado (3-5 linhas · tolerância R$ 0,01) · divergência significativa (8-10 linhas) · só na Origem (6-8) · só no Comparado (5-7) · ambiguidade potencial (2 linhas · exercita P-V1-04) · sinônimo de coluna `Cliente` vs `Razao_Social` (gera warning · T-MODELO exige mapeamento manual conforme §F.2).

**Warnings esperados:** `W-V1-NOME-COLUNA-DIVERGENTE` (1) · `W-V1-AMBIGUIDADE-MATCH` (1) · `W-NULO-MEDIDA` (2-3).

**Observação:** modo DUAL com `1 arquivo com 2 abas` é o cenário dominante. Modo `2 arquivos distintos` fica não-coberto nesta base · é **cobertura suficiente** porque o ponto de entrada do contrato UploadResult é idêntico entre as duas leituras.

### I.3 · V11 · Aderência por pareamento fuzzy (Família A · T-FUZZY)

**Cenário principal:** `cadastral_fuzzy` (80 linhas · 40 "oficiais" + 40 "ruidosas"). Complementado por reuso do par DUAL para contra-prova de baixa necessidade de fuzzy.

**Estrutura do ruído em `cadastral_fuzzy`:**
- Abreviações (`LTDA` → `Ltda.` · `LTDA` removido)
- Erros de digitação (`Vale Verde` → `Valle Verde` · `Valeverd`)
- Ordem de tokens invertida (`Transportes Vale Verde` → `Vale Verde Transportes`)
- Acentos diferentes (`São` vs `Sao`)
- CNPJ com formatações distintas (`12.345.678/0001-90` vs `12345678000190`)

**Casos-limite cobertos:** pareamento claro (score ≥ 0.85) · zona cinza (score entre 0.65 e 0.85 · 5-7 linhas · exercita decisão TED D-123) · pareamento rejeitado (score < 0.65 · 3-4 linhas) · token-chave CNPJ presente em ambos os lados (boost 1.15 ativado · D-138) · token-chave ausente (desempate apenas por trigramas+tokens sem boost) · `tipo_estrutural=ID` detectado automaticamente em CNPJ (D-103 · D-113).

**Warnings esperados:** `W-V11-SCORE-ZONA-CINZA` (5-7) · `W-V11-SEM-PAR-ACIMA-THRESHOLD` (6-8).

**Uso complementar do par DUAL:** V11 consome `dual_origem_crm × dual_comparado_erp` como contra-prova · match por Conta/Centro_Custo diretos · T-FUZZY não ativada indevidamente.

### I.4 · V4 · Composição (Família C)

**Cenário principal:** `vendas_padrao` (filtrado em 1 mês) · `Vendas` agregado por `Produto`. Modos 1 (Composição simples) e 3 (Comparação de Distribuição).

**Casos-limite cobertos:** distribuição Pareto 80/20 clássica (5 produtos concentrando ~78%) · Top-N com corte (exercita P-V4-XX N=10) · T-ABC classificando A/B/C (thresholds TED 80/95 · D-040 · D-123) · T-ACUM monotônico · T-RANK com regra de desempate (2 produtos com Vendas idênticas · exercita D-041).

**Cenário secundário:** `vendas_pre_agregadas` · exercita cenário-limite CPCO onde T-AGRUPA é skipped com warning orientativo `W-AGRUPA-JA-AGREGADO`.

**Contra-exemplo:** distribuição uniforme forçada em uma aba · Classe "sem concentração clara" · `W-ABC-SEM-CONCENTRACAO`.

### I.5 · V10 · Curva Pareto (Família C · view especializada de V4)

**Cenário principal:** `vendas_volume_alto` (400 linhas · cardinalidade Produto=45).

**Casos-limite cobertos:** Curva Pareto clássica · Vitais (Classe A · ~12 produtos concentrando 80%) · Demais itens (~33 produtos) · `tipo_estrutural=NUMERICO` em Vendas · Coração Visual ColumnChart com linha de acumulado (CAP-COMBO-BAR-LINE).

**Contra-exemplo:** `W-V10-SEM-PARETO` quando curva quase linear.

**View especializada V10↔V4:** `casos_esperados.yaml` declara que o mesmo `vendas_volume_alto` processado por V4 produz composição · por V10 produz Pareto · exercita D-035/D-045/D-046.

### I.6 · V3 · Análise sequencial (Família B · T-EIXO)

**Cenário principal:** `eixo_sequencial_completo` (12 valores de `2025-01` a `2025-12` sem lacunas). Modos básico e Comparativo (2 núcleos).

**Casos-limite cobertos:** eixo completo · reconhecedor pt-BR/pt-EN (D-026) · datas em formato `YYYY-MM`.

**Cenário secundário:** `eixo_sequencial_lacunas` (faltam `2025-03` e `2025-07`) · exercita detecção de lacunas sem preenchimento (D-061) · `W-V3-EIXO-LACUNA` (2 ocorrências) · `W-V3-EIXO-DESORDENADO` (reservado para linhas fora de ordem · motor reordena e sinaliza · princípio C.2).

**Cenário terciário:** `vendas_por_colunas` · exercita T-PIVOT semântica 3 (D-062) antes de T-EIXO.

### I.7 · V8 · Matriz de Presença (Família B · herança integral de T-EIXO)

**Cenário principal:** matriz conceitual `Produto × Mes` derivada de `eixo_sequencial_completo` + `vendas_volume_alto`. Cada célula indica presença/ausência de Vendas.

**Casos-limite cobertos:** presença contínua · intermitente · entrada tardia (produto aparece só a partir do 4º mês) · saída antecipada (produto some após o 8º mês) · matriz densa (~70% ocupação) · alta cardinalidade (540 células · exercita CAP-PAGINACAO-MATRIZ) · **ausência como conteúdo principal** (não warning · padrão D-076 · 4 aplicações).

**Warnings esperados:** `W-CARD-ALTA` (aviso de paginação) · `W-V8-MATRIZ-DENSIDADE-BAIXA` (se densidade < 20%).

**T-RANK V8:** ranking de presença · escopo `global` (D-137).

### I.8 · V7 · Grupos internos (Família D · T-SEMA global)

**Cenário principal:** `operacao_perfil_grupo` · Filiais agrupadas por Região · métrica Prazo_Dias com T-SEMA **menor-é-melhor** global (D-087).

**Casos-limite cobertos:** grupos de 3-5 filiais por região (4 regiões) · Desvio Significativo dentro de grupo (3-4 filiais acima da média regional) · Desvio significativo abaixo da média (2 filiais melhor que grupo) · 1 região uniforme (`W-V7-GRUPO-UNIFORME`) · T-RANK `intra_grupo` (D-088 · D-137 · 4 níveis de desempate).

**Cenário limite:** 1 região construída com 2 filiais · `W-V7-GRUPO-TAMANHO-INSUFICIENTE`.

### I.9 · V9 · Perfil multi-métrica segmentado (Família D · par de V7)

**Cenário principal:** `operacao_perfil_grupo` (reuso · semântica distinta). Perfil de cada filial em múltiplas métricas (`Prazo_Dias · Peso_Kg`) agrupado por `Transportadora` (segmentador externo).

**Casos-limite cobertos:** perfil multi-métrica · segmentação por agrupador externo · T-RANK escopo `cross_elementos_dentro_do_agrupador` (D-096 · D-137) · destaque por concentração de desempenho (2-3 filiais) · Resumo por Agrupador Segmentado · NULO_MEDIDA em métrica secundária (1-2 filiais sem Peso_Kg).

**Warnings esperados:** `W-V9-SEGMENTO-TAMANHO-INSUFICIENTE` · `W-NULO-MEDIDA-METRICA-SECUNDARIA`.

**View especializada V7↔V9:** mesmo dataset · V7 expõe como "grupos internos" · V9 como "perfil multi-métrica segmentado" · exercita D-081/D-091.

### I.10 · V5 · Dispersão e outliers (Família E · univariado)

**Cenário principal:** `operacao_dispersao` · campo numérico único `Prazo_Dias`.

**Distribuição desenhada:**
- Núcleo (~180 linhas) · normal em torno da mediana (μ=18 · σ=4)
- Outliers à direita (~15 linhas · valores 45-120)
- Outliers à esquerda (~5 linhas · valores 1-3)
- Valor extremo isolado (1 linha · Prazo_Dias=350)

**Casos-limite cobertos:** histograma com bins determinísticos (CAP-HISTOGRAMA-BINS) · quartis estáveis (tolerância 1e-9) · classificação de outlier por IQR×1.5 default (TED editável) · `subtipo_id_detectado=false` (heurística D-103) · Modo Segmentado em roadmap declarado.

**Warnings esperados:** `W-V5-OUTLIERS-DETECTADOS` · `W-V5-DISTRIBUICAO-ASSIMETRICA`.

### I.11 · V6 · Cruzamento de duas categóricas (Família E · bivariado)

**Cenário principal:** `operacao_cruzamento` · matriz Filial × Transportadora com Valor_Frete como conteúdo · cardinalidade Filial=8 · Transportadora=6 · 48 células teóricas.

**Casos-limite cobertos:** células densas (~70%) · células ausentes (~14 · aba "Combinações Ausentes" dedicada · D-119 · sub-bloco 4b do Resumo Executivo) · célula dominante (1-2 combinações > 20% · verde-intenso) · célula relevante (5-20% · verde-médio) · célula marginal (< 1% · cinza) · Total linha/coluna (CPCO sobre matriz) · T-RANK de combinações top-N (D-115 · 4 níveis) · CAP-FORMATACAO-CONDICIONAL-MATRIZ · CAP-COLUMNCHART-EMPILHADO-100 (D-118).

**Warnings esperados:** `W-V6-CELULAS-AUSENTES-ALTO-TOTAL` (3-4) · `W-V6-MATRIZ-ESPARSA` (se densidade < 40%).

### I.12 · Cobertura adicional · abas de motor puro

**`boolean_disfarcado` (60 linhas):** coluna `Ativo` com valores `Sim/Não/Ativo/Inativo` mistos · exercita D-008 · `tipo_estrutural` esperado: CATEGORICO. Não consumida por visão diretamente.

**`cardinalidade_excessiva` (200 linhas):** agrupador com 85 categorias · exercita bloqueio MBO (C.D4 · D-127 · D-134) · qualquer visão encontra `BloqueioOperacional` antes do cálculo.

**`vendas_pre_agregadas` (50 linhas):** cenário-limite CPCO · consolidação pré-cálculo skipped com warning orientativo.

### I.13 · Mapa consolidado cenário × aba × visões

| Aba | Cenário analítico central | Visões primárias | Visões secundárias |
|---|---|---|---|
| `vendas_padrao` | POR_LINHAS · 2 meses | V2 (Modo 4) · V4 (Modos 1 e 3) | V10 |
| `vendas_por_colunas` | POR_COLUNAS · T-PIVOT | V2 alternativo · V3 (semântica 3) | — |
| `vendas_pre_agregadas` | CPCO skip · warning | V4 · V10 | — |
| `operacao_dispersao` | Univariado numérico · outliers | V5 | — |
| `operacao_cruzamento` | Bivariado categórico · matriz | V6 | — |
| `operacao_perfil_grupo` | Grupos e segmentação | V7 · V9 | V5 (Modo Segmentado roadmap) |
| `dual_origem_crm` + `dual_comparado_erp` | T-DUAL · confronto | V1 · V11 | — |
| `cadastral_fuzzy` | T-FUZZY · ruído textual | V11 | — |
| `vendas_volume_alto` | Cardinalidade alta · Pareto | V10 | V4 · V8 |
| `cardinalidade_excessiva` | Bloqueio MBO | Teste transversal | — |
| `boolean_disfarcado` | Motor upload D-008 | Teste motor_upload | — |
| `eixo_sequencial_lacunas` | T-EIXO com lacunas | V3 · V8 | — |
| `eixo_sequencial_completo` | T-EIXO completo | V3 · V8 | — |

### I.14 · Ratificação de cobertura dos 12 transversais

| Transversal | Onde é exercitado |
|---|---|
| T-AGRUPA | Todas as abas com agregação (CPCO) |
| T-DIAG | Todas as abas (diagnóstico universal) |
| T-SEMA | `vendas_padrao` (V2 maior-é-melhor) · `operacao_perfil_grupo` (V7 menor-é-melhor) |
| T-EIXO | `eixo_sequencial_completo` + `eixo_sequencial_lacunas` |
| T-RANK | V4/V10 (global) · V7 (intra_grupo) · V9 (cross_elementos) · V6 (4 níveis) |
| T-ACUM | `vendas_volume_alto` (V10 Pareto) · `vendas_padrao` (V4) |
| T-ABC | `vendas_volume_alto` (V10) · `vendas_padrao` (V4) |
| T-PIVOT | `vendas_por_colunas` (3 semânticas exercitadas via V2/V3/V4) |
| T-DUAL | `dual_origem_crm` + `dual_comparado_erp` |
| T-MODELO | Exercitado em F-MOT/F-TRANS com persistência de config (transversal) |
| T-FUZZY | `cadastral_fuzzy` |
| T-CONCAT | `cadastral_fuzzy` (campos CNPJ+Nome concatenados em campo virtual V11 MVP) |

---

## Seção J · `casos_esperados.yaml` · artefato canônico de validação

### J.1 · Formato · YAML

**Decisão técnica resolvida (D-141):** arquivo único `casos_esperados.yaml` em formato YAML.

**Rationale (princípio 5):**
- YAML é legível por humano (Usuária inspeciona · derivação de checklist é auditável)
- Parsing nativo Python (`pyyaml`) · zero dependência nova
- Suporta comentários (essencial para rastreabilidade com DCVs)
- Blocos multi-linha naturais (`|`) para descrições ricas
- JSON excluído (sem comentários · aspas/vírgulas ruidosas) · MD estruturado excluído (exige parser customizado · inviável para testes de regressão)

**Caminho canônico:** `/bases/casos_esperados.yaml`.

### J.2 · Estrutura canônica · 3 níveis

**Decisão técnica resolvida (D-141):** hierarquia `metadata` → `visoes:{V1..V11}` → `transversais`. Assertions em cada nível com 5 tipos canônicos fechados.

**Esqueleto completo:**

```yaml
# casos_esperados.yaml
# Artefato canônico de validação da base de fundação (D-141)
# Consumido em 3 pontos:
#   (1) F-BASE · auto-validação da base gerada
#   (2) F-MOT/F-TRANS · testes de regressão automatizados
#   (3) Fase 2 · checklist de Validação Visual derivado por visão
# Referência canônica: spec_fundacao.md §J · D-141

metadata:
  versao_base: "1.0"
  seed: 42                               # D-140 · invariante
  total_abas: 14                         # D-140 · invariante
  total_linhas_agregado: 2063
  data_geracao_esperada: "gerada em F-BASE"

visoes:

  V2:
    descricao: "Comparação entre estados · Família A · Modo 4"
    aba_principal: "vendas_padrao"
    assertions:
      - id: "V2-A01"
        tipo: "contagem_categoria"
        descricao: "Entre os 2 meses deve haver 2-4 elementos na categoria Ausente em um lado"
        esperado: {min: 2, max: 4}
        warning_associado: "W-V2-AUSENTE-EM-UM-LADO"
      - id: "V2-A02"
        tipo: "warning_presente"
        descricao: "W-NULO-MEDIDA emitido com 3-4 ocorrências"
        esperado: {warning_code: "W-NULO-MEDIDA", min: 3, max: 4}
      - id: "V2-A03"
        tipo: "estrutura_saida"
        descricao: "Resumo Executivo tem 6 blocos · Coração Visual é Matriz de Confronto"
        esperado: {resumo_blocos: 6, coracao_visual: "Matriz de Confronto"}
    aba_secundaria:
      nome: "vendas_por_colunas"
      nota: "Exercita T-PIVOT semântica 1 · POR_COLUNAS → POR_LINHAS antes do cálculo"

  V1:
    descricao: "Confronto entre bases · Família A · T-DUAL"
    abas_consumidas: ["dual_origem_crm", "dual_comparado_erp"]
    assertions:
      - id: "V1-A01"
        tipo: "contagem_categoria"
        descricao: "Match exato em ~70% das linhas"
        esperado: {min_pct: 65, max_pct: 75}
      - id: "V1-A02"
        tipo: "contagem_exata"
        descricao: "Divergências significativas (acima de tolerância R$ 0.01) · 8-10 linhas"
        esperado: {min: 8, max: 10}
      - id: "V1-A06"
        tipo: "warning_presente"
        descricao: "W-V1-NOME-COLUNA-DIVERGENTE · 1 ocorrência (Cliente vs Razao_Social)"
        esperado: {warning_code: "W-V1-NOME-COLUNA-DIVERGENTE", exato: 1}

  V11:
    descricao: "Aderência por pareamento fuzzy · Família A · T-FUZZY · T-CONCAT"
    aba_principal: "cadastral_fuzzy"
    assertions:
      - id: "V11-A01"
        tipo: "contagem_categoria"
        descricao: "Pareamentos em zona cinza (0.65 ≤ score < 0.85)"
        esperado: {min: 5, max: 7}
        warning_associado: "W-V11-SCORE-ZONA-CINZA"
      - id: "V11-A02"
        tipo: "inferencia_subtipo_id"
        descricao: "Coluna CNPJ detectada como categórica com subtipo ID (D-103 · D-146)"
        esperado: {tipo_estrutural: "CATEGORICO_ELEGIVEL", subtipo_id_detectado: true}

  # ... V4, V10, V3, V8, V7, V9, V5, V6 seguem mesmo padrão
  # Arquivo completo com 60-80 assertions é gerado em F-BASE pelo Claude Code

transversais:

  motor_upload:
    - id: "MU-A01"
      tipo: "inferencia_boolean"
      descricao: "Coluna Ativo em boolean_disfarcado detectada como CATEGORICO_ELEGIVEL · não NUMERICO · D-008"
      aba: "boolean_disfarcado"
      esperado: {tipo_estrutural: "CATEGORICO_ELEGIVEL", subtipo_id_detectado: false}
    - id: "MU-A02"
      tipo: "inferencia_subtipo_id"
      descricao: "Coluna CNPJ em cadastral_fuzzy detectada como categórica com subtipo ID (D-103 · D-146)"
      aba: "cadastral_fuzzy"
      esperado: {tipo_estrutural: "CATEGORICO_ELEGIVEL", subtipo_id_detectado: true}

  bloqueio_operacional:
    - id: "BO-A01"
      tipo: "bloqueio_emitido"
      descricao: "Aba cardinalidade_excessiva dispara BloqueioOperacional antes do cálculo"
      aba: "cardinalidade_excessiva"
      esperado: {bloqueio_codigo: "B-CARD-EXCESSIVA", contrato: "BloqueioOperacional"}

  determinismo:
    - id: "DET-A01"
      tipo: "determinismo_seed"
      descricao: "Execução duas vezes com SEED=42 produz mesmo DataFrame (hash estável)"
      esperado: {hash_estavel: true}
```

**Enum canônico de `tipo_estrutural` (D-146 · formalizado em 21/04/2026 · retrospectiva F-BASE):** o valor de `tipo_estrutural` em qualquer assertion é sempre um dos 5 valores declarados em §A linha 126 — `CATEGORICO_ELEGIVEL` · `NUMERICO_CONTINUO` · `TEMPORAL` · `BOOLEANO` · `VAZIO_OU_AMBIGUO`. **IDs são representados como `CATEGORICO_ELEGIVEL` + `subtipo_id_detectado: true`** (regra canônica de §C linha 409-410 · "ID é categórico apesar de int"). Formulações anteriores deste esqueleto que usavam `tipo_estrutural: "ID"` ficam obsoletas · o esqueleto acima é a referência canônica. Extensão do enum (novo valor) exige D-YYY · esse ponto do esqueleto reflete D-146.

### J.3 · 5 tipos canônicos de assertion · lista fechada

| Tipo | Semântica | Consumo principal |
|---|---|---|
| `contagem_exata` | Número exato de linhas/elementos/ocorrências | F-MOT · F-TRANS testes |
| `contagem_categoria` | Quantidade em categoria declarada (com min/max ou pct) | Validação de classificação |
| `warning_presente` | Warning de código específico foi emitido (com contagem) | Validação C.2 nada silencioso |
| `estrutura_saida` | Forma da saída (nº abas · nome Coração Visual · blocos Resumo) | Validação camada exportação |
| `bloqueio_emitido` | BloqueioOperacional de código específico emitido | Validação MBO · C.D4 |

**Tipos adicionais parametrizados** (instâncias dos 5 canônicos aplicadas a metadados): `inferencia_boolean` · `inferencia_subtipo_id` · `determinismo_seed`. Extensão do conjunto canônico (novo tipo) exige D-YYY nova.

### J.4 · 3 pontos de consumo do `casos_esperados.yaml`

**Ponto 1 · F-BASE · Claude Code gera a base.** Prompt de F-BASE consome `casos_esperados.yaml` como contrato de saída. Claude Code gera `base_fundacao.xlsx` com as 14 abas · roda script de auto-validação carregando a base e verificando assertions de natureza estrutural (contagens de linhas · cardinalidades · presença de NULOs · ruído em `cadastral_fuzzy`) · não prossegue para entrega se assertion estrutural falhar. Subconjunto consumido: `contagem_exata` e `contagem_categoria` sobre a base bruta.

**Ponto 2 · F-MOT e F-TRANS · testes de regressão.** Testes automatizados consomem `casos_esperados.yaml` como gabarito de comportamento. Para cada assertion de tipo `warning_presente` · `bloqueio_emitido` · `inferencia_*` · `determinismo_seed` · roda cenário correspondente sobre a base de fundação e compara com esperado. Testes quebram se assertions divergirem. Subconjunto consumido: bloco `transversais` completo + assertions de warning em `visoes`.

**Ponto 3 · Fase 2 · Validação Visual por visão.** Na Fase 2, quando a Usuária abre `app_vN.py` com a base de fundação carregada · o checklist de Validação Visual é **derivado mecanicamente** das assertions de cada visão em `casos_esperados.yaml`. Assertions de tipo `contagem_categoria` viram itens de checklist ("há 2-4 elementos Ausentes?") · `warning_presente` viram itens ("o warning X apareceu?") · `estrutura_saida` viram itens ("a aba Coração Visual está presente e com o nome correto?"). Spec da visão (Fase 2) documenta o mapeamento de derivação.

**Princípio 4 de D-131 preservado:** na Fase 2 a Usuária **não lê código** · apenas marca checklist derivado. Na Fase 1 a validação é inspeção manual da base processada em F-BASE.

### J.5 · Escopo desta spec vs. artefato completo

Esta seção (§J) declara **estrutura · regras · esqueleto** de `casos_esperados.yaml`. O **arquivo completo** com todas as assertions (~60-80 estimadas) é **gerado em F-BASE** pelo Claude Code a partir do prompt consolidado · respeitando os cenários declarados em §I e o esqueleto declarado aqui. Profundidade A (decidida em §H) · spec operacional · Claude Code tem autonomia para derivar assertions concretas respeitando os contratos declarados.

---

## Seção K · Fechamento da Fundação · transição para F-MOT

### K.1 · Checklist de coerência final · 8/8 verificações

Varredura sistemática cross-seções desta spec:

**✅ 1 · Contratos de §A consumidos corretamente em §B/§C/§D/§E/§F (transversais) e §H/§I (base).**
- `UploadResult` consumido por `motor_base` · exercitado em `dual_origem_crm + dual_comparado_erp` e `boolean_disfarcado`
- `MotorResult` consumido por todas as visões · exercitado indiretamente em todas as 11 visões
- `VNResultBase` consumido por `exportacao.py` · estrutura de aba específica declarada em §I
- `DiagnosticoVN` emitido por T-DIAG · todos os warnings listados em §I fluem por esse contrato
- `BloqueioOperacional` (D-134) exercitado em `cardinalidade_excessiva` com assertion `BO-A01`

**✅ 2 · 12 transversais consolidados em §D/§E/§F são exercitados em §I.** Ratificado na tabela §I.14. Zero transversal órfão.

**✅ 3 · 7 padrões consolidados (D-122 a D-128) aparecem na base.**
- CPCO · C.D1 · T-AGRUPA sempre aplicado · cenário-limite em `vendas_pre_agregadas`
- TED · C.D2 · thresholds editáveis em T-ABC · T-FUZZY · IQR V5
- BAD · C.D3 · Base Analítica e Diagnóstico como aba padrão em todas as 11 visões
- MBO · C.D4 · exercitado em `cardinalidade_excessiva`
- ECP · C.D5 · 3 zonas exercitadas (saudável · warning · bloqueio)
- Resumo Executivo em 6 Blocos · §13.5 · assertion `estrutura_saida` em cada visão
- Coração Visual · §13.6 · assertion `estrutura_saida` nomeia o Coração de cada visão

**✅ 4 · 4 contratos com receptividade a IA (D-130) não são violados pelas seções §H/§I/§J.** Base de fundação é fonte de dados · não toca camada de IA. `Field(..., description=...)` · enums string · `.para_contexto_ia()` preservados.

**✅ 5 · Decisão D-135 (T-CONCAT na Fundação · M2.STACK em M2) respeitada.** T-CONCAT exercitado em `cadastral_fuzzy` (V11 MVP · CNPJ+Nome virtual). M2.STACK ausente da base · correto.

**✅ 6 · Decisão D-136 (F-EXP bloco único) não ameaçada.** Base exercita todas as 11 capabilities através dos cenários das 11 visões. Nenhuma capability fica sem teste de base.

**✅ 7 · Determinismo C.1 preservado.** SEED=42 declarado em §H.2 · assertion `DET-A01` em `casos_esperados.yaml` exige hash estável. Tolerância 1e-9 em floats respeitada.

**✅ 8 · Nada silencioso C.2 preservado.** Todo fenômeno estrutural da base tem warning declarado em §I · ordenação automática sinalizada · bloqueios emitidos.

**Resultado:** 8/8 · nenhuma contradição entre as seções desta spec.

### K.2 · Prompt de abertura de F-MOT (para Claude Code)

Prompt consolidado · pronto para copiar em sessão dedicada de Claude Code após aplicação do kit desta sessão.

```
# Bloco F-MOT · Implementação dos motores da Fundação
# Sessão dedicada Claude Code · primeiro bloco de implementação da Fase 1

## Contexto

Implementar motor_upload.py (v2) e motor_base.py (v2) conforme especificação 
consolidada em spec_fundacao.md e contratos declarados em contratos.py.

Este é o primeiro bloco de implementação da Fase 1 · antecede F-TRANS · F-EXP · F-BASE.

## Artefatos a produzir

1. /src/contratos.py · Pydantic BaseModel para UploadResult · MotorResult · 
   VNResultBase · DiagnosticoVN · MotorConfig · BloqueioOperacional · 
   ConfigExportacao · ColumnMeta (+ enums de tipo_estrutural e subtipo ID).
   Requisitos D-130: model_config para enums como string · Field(..., 
   description=...) em todo campo · método .para_contexto_ia() em 
   VNResultBase e MotorResult.

2. /src/motor_upload.py · leitura de arquivos Excel (xlsx) · inferência 
   semântica de tipos (D-008 · boolean disfarçado) · reconhecedor pt-BR/pt-EN 
   (D-026) · deteção de subtipo ID (D-103) · inferência de tipo_estrutural 
   com 5 valores enum (D-113) deferida para motor_base (D-133) · preview de 
   5 linhas · preservação de arquivo_bytes (D-007) · suporte a modo T-DUAL 
   (2 arquivos OU 1 arquivo 2 abas · D-018).

3. /src/motor_base.py · consolidação pré-cálculo via T-AGRUPA (CPCO · C.D1) · 
   inferência de tipo_estrutural sempre computada sobre coluna completa (D-133) 
   · matriz column_meta por coluna · emissão de BloqueioOperacional quando 
   cardinalidade excessiva detectada (MBO · C.D4) · emissão de WarningEstrutural 
   via coletor T-DIAG.

4. /src/utils/normalizacao_texto.py · módulo centralizado (D-139) consumido 
   por T-FUZZY e T-CONCAT em F-TRANS. Neste bloco F-MOT apenas declarar 
   interface · implementação completa fica em F-TRANS.

5. /src/testes/test_motor_upload.py e /src/testes/test_motor_base.py · 
   testes automatizados cobrindo: (a) inferência de tipos incluindo boolean 
   disfarçado · (b) reconhecedor pt-BR/pt-EN de cronológicos · (c) detecção 
   de subtipo ID · (d) tipo_estrutural com 5 enums · (e) bloqueio MBO.

## Restrições invioláveis

- Determinismo C.1 · nenhuma operação dependente de ordem de iteração não-estável.
- Nada silencioso C.2 · toda inferência que não seja perfeita emite warning.
- Receptividade a IA D-130 · 4 contratos serializáveis JSON-compatível.
- Biblioteca: pandas · openpyxl 3.1+ · pydantic v2 · pyyaml para consumir 
  casos_esperados.yaml em testes.
- Não implementar T-* · isso fica em F-TRANS.
- Não implementar exportacao.py · isso fica em F-EXP.
- Não gerar base sintética · isso vem pronto de F-BASE (executado depois de 
  F-MOT e F-TRANS).

## Validação

Ao final do bloco · rodar os testes automatizados. Zero testes falhando 
antes de entregar.

## Anexos necessários no painel desta sessão

- spec_fundacao.md · spec consolidada da Fundação (fonte autoritativa única)
- CONTEXT.md · princípios invioláveis
- DECISIONS.md · rationale das decisões críticas (D-007 · D-008 · D-018 · 
  D-026 · D-103 · D-113 · D-130 · D-133 · D-134 · D-135 · D-139)
- contratos.py v2 será produzido neste bloco (ainda não existe · é parte 
  do deliverable)
```

**Observação didática para a Usuária:** este prompt é copiado · colado em uma nova sessão de Claude Code (terminal dedicado · não o chat do Projects) · Claude Code executa com autonomia · validação ao final via **teste automatizado rodando com 100% de sucesso** (princípio 4 de D-131 respeitado · Usuária não precisa ler código).

### K.3 · Marco · Fundação-Design CONCLUÍDA

Com o fechamento de K.1 (checklist 8/8) e K.2 (prompt F-MOT pronto), consolida-se marco operacional:

**Fundação-Design · CONCLUÍDA (20/04/2026).**

Artefato único de design da Fundação: `spec_fundacao.md` consolidado (este documento) · produzido em 3 blocos sequenciais (G-FUND 1 · 2 · 3 · todos em 20/04/2026) e unificado em sessão ALINHA-Fundação-Design→F-MOT (20/04/2026).

**O que o marco significa:**
- 12 transversais cristalizados (lista fechada · extensão exige D-XXX nova)
- 14 abas canônicas na base de fundação (inventário cristalizado · D-140)
- 5 tipos de assertion canônicos em `casos_esperados.yaml` (D-141)
- 3 momentos de consumo do `casos_esperados.yaml` (F-BASE · F-MOT/F-TRANS · Fase 2)
- Prompt de F-MOT pronto para Claude Code

**Próximo passo operacional:** F-MOT · sessão dedicada de Claude Code · primeiro bloco de implementação da Fase 1.

**Roadmap remanescente da Fase 1:**
1. F-MOT → produz `motor_upload.py` v2 · `motor_base.py` v2 · `contratos.py` · interface de `normalizacao_texto.py` · testes
2. F-TRANS → produz 12 transversais em `/src/transversais/` · `normalizacao_texto.py` completo · testes
3. F-EXP → produz `exportacao.py` com 11 capabilities · bloco único (D-136) · testes
4. F-BASE → produz `base_fundacao.xlsx` (14 abas · SEED=42) + `casos_esperados.yaml` completo · auto-validação
5. **Fase 1 CONCLUÍDA** · abre Fase 2 com S-V2 (Família A)

---

## Referências canônicas

- **CONTEXT.md** §1 (princípio 3 · IA sugere · D-130) · §3 (Fase 1 Fundação · ordem dos blocos) · §6 (12 transversais · lista fechada) · §9 Camada C (5 princípios derivados) · §13 (6 padrões estruturais de produto) · §14 (condução Fase 1 · estabilizado após 3 aplicações)
- **DECISIONS.md** D-007 (arquivo_bytes) · D-008 (boolean disfarçado) · D-015 (T-MODELO origem) · D-017 (Diagnóstico última aba) · D-018 (T-DUAL) · D-026 (reconhecedor pt-BR/pt-EN · T-PIVOT estados) · D-030 (T-MODELO V2 persistência lógica) · D-035/D-045/D-046 (V4↔V10 view especializada) · D-039 (T-PIVOT multi-medida) · D-040 (T-ABC limiares) · D-041 (T-RANK default 3 níveis) · D-052 (T-FUZZY confirmado) · D-053 (T-CONCAT origem) · D-061 (T-EIXO formalizado) · D-062 (T-PIVOT pontos do eixo) · D-067 (T-SEMA contrato 1) · D-071-D-080 (DCV-V8 · T-EIXO herança · D-076 warning×conteúdo) · D-081/D-091 (retroação V7↔V9) · D-087 (T-SEMA contrato 2 · V7) · D-088 (T-RANK V7 4 níveis) · D-093-D-096 (DCV-V9 · T-SEMA efeito cálculo · T-RANK escopo novo · multi-regra) · D-102 (V5 adaptação T-AGRUPA) · D-103 (subtipo ID) · D-104 (TED origem) · D-113 (tipo_estrutural 5 enums) · D-115 (T-RANK V6 4 níveis) · D-118 (ColumnChart empilhado V6) · D-119 (Combinações Ausentes V6) · D-122 a D-129 (7 padrões formalizados) · D-130 (receptividade IA) · D-131 (condução Fase 1) · D-132 (dashboard visual) · D-133 (tipo_estrutural sempre computado) · D-134 (BloqueioOperacional contrato único) · D-135 (T-CONCAT Fundação · M2.STACK em M2) · D-136 (F-EXP bloco único) · D-137 (enum escopo T-RANK) · D-138 (pesos T-FUZZY) · D-139 (normalização centralizada) · **D-140 (base_fundacao 14 abas SEED=42)** · **D-141 (casos_esperados.yaml canônico)**
- **GLOSSARIO.md** §4 (12 transversais · T-CONCAT Fundação pós-D-135) · §10 (padrões consolidados formalizados)
- **DCVs aprovados** 11 de 11 (V2 · V1 · V11 · V4 · V10 · V3 · V8 · V7 · V9 · V5 · V6)

---

*Fim de `spec_fundacao.md`. Marco **Fundação-Design CONCLUÍDA (20/04/2026)**. Próximo bloco: F-MOT (implementação Claude Code · prompt em §K.2).*
