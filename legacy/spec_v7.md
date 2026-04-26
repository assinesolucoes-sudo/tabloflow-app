# spec_v7.md — Visão V7: Desvio em Relação à Média do Grupo ## Identificação - **Visão:** V7 — Desvio em Relação à Média do Grupo - **Bloco:** 5 - **Arquivo de saída:** src/visao_v7.py - **Dependências:** motor_base.py (MotorResult, ColumnMeta) --- ## Propósito Posicionar cada elemento dentro do seu grupo de referência. O motor calcula a média do grupo a partir dos próprios dados e classifica cada registro como Acima, Na Média ou Abaixo. Não exige referência externa — o grupo é a referência. --- ## Contrato de Entrada ```python from pydantic import BaseModel from typing import Optional class ConfigV7(BaseModel): campo_grupo: str # coluna categórica que define o grupo campo_medida: str # coluna numérica analisada nome_analitico: str # nome exibido na análise e exportação tolerancia_pct: float = 5.0 # % de tolerância para "Na Média" (padrão: 5%)
Contrato de Saída (V7Result)

from pydantic import BaseModel from typing import Optional, List class ElementoDesvio(BaseModel): grupo: str elemento: str # valor da linha (identificador do registro) valor: float media_grupo: float desvio_absoluto: float # valor - media_grupo (pode ser negativo) desvio_percentual: Optional[float] # (desvio_absoluto / media_grupo) * 100 classificacao: str # "ACIMA" | "NA_MEDIA" | "ABAIXO" class ResumoGrupo(BaseModel): grupo: str media: float total_registros: int acima: int na_media: int abaixo: int maior_desvio_positivo: Optional[float] maior_desvio_negativo: Optional[float] class V7Result(BaseModel): registros: List[ElementoDesvio] resumo_por_grupo: List[ResumoGrupo] total_registros: int grupos_processados: int warnings: List[str] errors: List[str] success: bool
Lógica de Cálculo

Média do grupo

media_grupo = mean(campo_medida) para todos os registros do grupo
Desvio absoluto

desvio_absoluto = valor - media_grupo
Desvio percentual

se media_grupo != 0: desvio_percentual = (desvio_absoluto / abs(media_grupo)) * 100 else: desvio_percentual = None
Classificação

se abs(desvio_percentual) <= tolerancia_pct → "NA_MEDIA" se desvio_absoluto > 0 e fora da tolerância → "ACIMA" se desvio_absoluto < 0 e fora da tolerância → "ABAIXO" Caso especial: se media_grupo == 0 e valor == 0 → "NA_MEDIA" Caso especial: se media_grupo == 0 e valor != 0 → "ACIMA" ou "ABAIXO" por sinal
Arredondamento

Todos os floats: 4 casas decimais
Erros Bloqueantes

E01 campo_grupo não encontrado no MotorResult E02 campo_medida não encontrado no MotorResult E03 campo_medida não é numérico (type != "numeric") E04 campo_grupo é numérico (deve ser categórico) E05 base vazia após remoção de nulos E06 tolerancia_pct < 0 ou > 100
Warnings

W01 Registros com valor nulo em campo_medida removidos (informar quantidade) W02 Registros com valor nulo em campo_grupo removidos (informar quantidade) W03 Grupo com apenas 1 registro — média = próprio valor, desvio = 0 W04 Grupo com média = 0 — desvio_percentual não calculável W05 tolerancia_pct = 0 — nenhum registro será classificado como NA_MEDIA
Assinatura da Função Principal

def executar_v7( motor_result: MotorResult, config: ConfigV7 ) -> V7Result: ...
Estrutura de Exportação Excel (3 abas)

Aba 1 — Detalhe

Todos os registros com: grupo, elemento (índice da linha ou valor identificador),
valor, media_grupo, desvio_absoluto, desvio_percentual, classificacao

Aba 2 — Resumo por Grupo

Uma linha por grupo: grupo, media, total, acima, na_media, abaixo,
maior_desvio_positivo, maior_desvio_negativo

Aba 3 — Configuração

Parâmetros usados: campo_grupo, campo_medida, nome_analitico, tolerancia_pct

Decisões de Pendências

Identificador do elemento: usar o índice da linha (int) como elemento
se não houver campo identificador explícito na config.
O campo_grupo + índice garante unicidade.
Grupos com 1 registro: processar normalmente, emitir W03.
Valores negativos na medida: suportados — desvio funciona normalmente.
Tolerância padrão: 5% (configurável via ConfigV7.tolerancia_pct).