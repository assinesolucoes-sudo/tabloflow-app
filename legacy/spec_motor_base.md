# spec_motor_base.md # TabloFlow — Especificação Técnica: Motor Base + Contrato MotorResult ## 1. Papel do Motor Base na Arquitetura O Motor Base é a segunda camada da pipeline do TabloFlow. Ele recebe o UploadResult produzido pelo Motor de Upload e transforma os dados brutos em uma estrutura analítica normalizada: o MotorResult. Nenhuma visão (V1–V10) acessa arquivo bruto diretamente. Toda visão recebe exclusivamente um MotorResult. Pipeline: Arquivo bruto → motor_upload.py → UploadResult → motor_base.py → MotorResult → Visão Vx → Excel exportado --- ## 2. Responsabilidades do Motor Base - Receber um UploadResult válido (success=True) - Selecionar a aba/base correta conforme instrução da visão - Normalizar tipos de coluna (numérico, texto, data, booleano) - Detectar e tratar valores nulos (NaN, None, string vazia, "N/A", "-") - Inferir tipos quando não declarados explicitamente - Produzir o MotorResult com metadados completos das colunas - Nunca modificar os dados originais — apenas ler e descrever - Registrar warnings para anomalias não-fatais - Registrar errors para falhas que impedem o processamento --- ## 3. Contrato MotorResult (Pydantic) ```python from pydantic import BaseModel from typing import Optional import pandas as pd class ColumnMeta(BaseModel): name: str # Nome original da coluna inferred_type: str # "numeric" | "text" | "date" | "boolean" | "mixed" | "empty" null_count: int # Quantidade de valores nulos null_pct: float # Percentual de nulos (0.0 a 1.0) unique_count: int # Quantidade de valores únicos sample_values: list[str] # Até 5 valores de exemplo (como string) is_candidate_key: bool # True se unique_count == total de linhas não-nulas is_candidate_numeric: bool # True se inferred_type == "numeric" is_candidate_date: bool # True se inferred_type == "date" is_candidate_categorical: bool # True se inferred_type == "text" e unique_count <= 50 class MotorResult(BaseModel): success: bool source_file: str # Nome do arquivo original selected_sheet: Optional[str] # Nome da aba selecionada (None se CSV) total_rows: int # Total de linhas (excluindo cabeçalho) total_cols: int # Total de colunas columns: list[ColumnMeta] # Metadados por coluna warnings: list[str] # Avisos não-fatais errors: list[str] # Erros fatais (se success=False) df: Optional[object] # DataFrame pandas normalizado (não serializado no JSON)
4. Regras de Inferência de Tipo

4.1 Numérico (numeric)

Coluna é numérica se ≥ 80% dos valores não-nulos forem convertíveis para float
Separador decimal: aceitar ponto e vírgula (tentar ambos)
Separador de milhar: remover ponto/vírgula antes de converter
Prefixos monetários (R$, $, €) devem ser removidos antes da conversão
Se conversão falhar em > 20% dos valores → tipo = "mixed"
4.2 Data (date)

Tentar os formatos: %d/%m/%Y, %Y-%m-%d, %d-%m-%Y, %m/%d/%Y, %Y%m%d
Coluna é date se ≥ 80% dos valores não-nulos forem convertíveis
Armazenar como datetime no DataFrame normalizado
4.3 Booleano (boolean)

Valores aceitos: True/False, Sim/Não, S/N, 1/0, Yes/No (case-insensitive)
Coluna é boolean se todos os valores não-nulos forem desse conjunto
4.4 Texto (text)

Fallback para qualquer coluna que não se encaixe nos tipos acima
Strip de espaços em branco aplicado
4.5 Misto (mixed)

Coluna com tipos inconsistentes que não atingem 80% de nenhum tipo
Registrar warning: "Coluna '{nome}' tem tipos mistos — tratada como texto"
4.6 Vazia (empty)

Coluna com 100% de valores nulos
Registrar warning: "Coluna '{nome}' está completamente vazia"
5. Tratamento de Nulos

Valores considerados nulos (além de NaN/None do pandas):

String vazia: ""
Strings: "N/A", "n/a", "NA", "null", "NULL", "None", "-", "--", "?"
Comportamento:

Substituir todos por NaN no DataFrame normalizado
Registrar null_count e null_pct no ColumnMeta
Se null_pct > 0.5 → registrar warning: "Coluna '{nome}' tem {pct}% de nulos"
Nunca remover linhas automaticamente — manter todas as linhas originais
6. Seleção de Aba

O Motor Base recebe como parâmetro opcional sheet_name:

Se sheet_name=None e arquivo tem 1 aba → selecionar automaticamente
Se sheet_name=None e arquivo tem múltiplas abas → selecionar a primeira, registrar warning
Se sheet_name fornecido → selecionar a aba especificada
Se aba não encontrada → success=False, error: "Aba '{nome}' não encontrada"
Para CSV: selected_sheet = None (não aplicável)

7. Candidatos para Sugestão de IA

O MotorResult expõe flags nos metadados de coluna para facilitar
as sugestões automáticas da IA nas visões:

is_candidate_key: colunas com valores únicos por linha → candidatas a agrupadores/chaves
is_candidate_numeric: colunas numéricas → candidatas a campos de medida
is_candidate_date: colunas de data → candidatas a eixo sequencial (V3, V8)
is_candidate_categorical: texto com baixa cardinalidade → candidatas a agrupadores/dimensões
Limite de cardinalidade para categórico: unique_count ≤ 50
(configurável via constante CATEGORICAL_THRESHOLD = 50)

8. Warnings e Errors

Warnings (não impedem o processamento):

Coluna com > 50% de nulos
Coluna com tipos mistos
Coluna completamente vazia
Múltiplas abas detectadas, primeira selecionada automaticamente
Cabeçalho com nomes duplicados (renomear com sufixo _2, _3...)
Cabeçalho com células vazias (renomear como "Coluna_1", "Coluna_2"...)
Errors (success=False):

Arquivo não é um UploadResult válido
UploadResult.success = False
Aba especificada não encontrada
DataFrame resultante tem 0 linhas
DataFrame resultante tem 0 colunas
Falha inesperada na leitura do DataFrame
9. Interface da Função Principal

def processar_motor_base( upload_result: UploadResult, sheet_name: Optional[str] = None ) -> MotorResult: """ Recebe um UploadResult e retorna um MotorResult normalizado. Parâmetros: upload_result: resultado do motor_upload.py (deve ter success=True) sheet_name: nome da aba a selecionar (None = automático) Retorna: MotorResult com df normalizado, metadados de colunas, warnings e errors. """
10. Exemplo de Uso

from motor_upload import processar_upload from motor_base import processar_motor_base # Bloco 1 — já implementado upload_result = processar_upload("vendas_2024.xlsx") # Bloco 2 — a implementar motor_result = processar_motor_base(upload_result, sheet_name="Base") if motor_result.success: print(f"Linhas: {motor_result.total_rows}") print(f"Colunas: {motor_result.total_cols}") for col in motor_result.columns: print(f" {col.name}: {col.inferred_type} | nulos: {col.null_pct:.0%}") else: print("Erros:", motor_result.errors)
11. Restrições de Implementação

NÃO modificar dados originais — apenas ler e descrever
NÃO remover linhas com nulos automaticamente
NÃO fazer análise analítica (isso é responsabilidade da Visão)
NÃO acessar arquivos diretamente — sempre via UploadResult
O campo df do MotorResult é um objeto pandas — não serializar em JSON
Usar apenas: pandas, pydantic, datetime, re, typing
Sem dependências externas além das listadas acima
12. Arquivo a Implementar

Nome: motor_base.py
Localização: C:\Users\ecbme\tabloflow\motor_base.py
Depende de: motor_upload.py (já implementado — 405 linhas)
Importa: UploadResult de motor_upload.py

13. Prompt de Abertura para o Claude Code (Bloco 2)

Cole este prompt ao abrir o Claude Code na pasta /tabloflow/:

Leia CONTEXT.md e spec_motor_base.md antes de começar.
Não leia outros arquivos além desses dois e motor_upload.py.

Implemente motor_base.py conforme a spec.

Requisitos:

Função principal: processar_motor_base(upload_result, sheet_name=None) → MotorResult
Modelos Pydantic: ColumnMeta e MotorResult conforme spec seção 3
Inferência de tipos conforme seção 4 (numeric, date, boolean, text, mixed, empty)
Tratamento de nulos conforme seção 5
Seleção de aba conforme seção 6
Flags de candidatos conforme seção 7
Warnings e errors conforme seção 8
Sem dependências externas além de pandas, pydantic, datetime, re, typing
Ao final, mostre as primeiras 30 linhas do arquivo implementado.

```