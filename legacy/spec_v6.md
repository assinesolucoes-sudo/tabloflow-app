pecs/spec_v6.md — Bloco 6

# spec_v6.md — Visão V6: Análise de Relacionamento entre Dimensões ## Contexto Leia CONTEXT.md antes de continuar. Esta spec define o contrato e a lógica da Visão V6 do TabloFlow. Implemente: src/visao_v6.py Não leia outros arquivos além de CONTEXT.md e este. --- ## O que é a V6 A V6 responde à pergunta: dentro de uma base de dados, como dois campos categóricos se relacionam? O motor lê uma única base, identifica todos os pares possíveis entre dois campos (produto cartesiano) e calcula a densidade de cada combinação. O resultado é uma matriz de cruzamento classificada, ranqueada e com lacunas explicitadas. Não compara estados no tempo. Não confronta bases externas. Não analisa distribuição estatística. Analisa estrutura de cruzamento. --- ## Contrato de Entrada ```python from pydantic import BaseModel from typing import Optional, List from enum import Enum class TipoMedida(str, Enum): CONTAGEM = "CONTAGEM" SOMA = "SOMA" MEDIA = "MEDIA" class ConfigV6(BaseModel): eixo1: str # nome da coluna — Dimensão Linha eixo2: str # nome da coluna — Dimensão Coluna tipo_medida: TipoMedida # CONTAGEM, SOMA ou MEDIA campo_medida: Optional[str] # obrigatório se tipo_medida != CONTAGEM nome_analitico_medida: str # nome editável — aparece na análise e exportação limiar_dominante: float = 0.20 # top X% acumulado do total = Dominante limiar_residual: float = 0.02 # abaixo de X% do total = Residual
Contrato de Saída — V6Result (Pydantic)

from pydantic import BaseModel from typing import List, Optional from enum import Enum class ClassificacaoDensidade(str, Enum): DOMINANTE = "DOMINANTE" RELEVANTE = "RELEVANTE" RESIDUAL = "RESIDUAL" AUSENTE = "AUSENTE" class CombinacaoCruzamento(BaseModel): eixo1_valor: str eixo2_valor: str valor_medida: Optional[float] # None se AUSENTE participacao_percentual: Optional[float] # None se AUSENTE ranking: Optional[int] # posição no ranking (1 = maior) classificacao: ClassificacaoDensidade class ResumoV6(BaseModel): total_combinacoes_possiveis: int # produto cartesiano completo total_combinacoes_presentes: int # combinações com dados total_combinacoes_ausentes: int # gaps estruturais total_dominantes: int total_relevantes: int total_residuais: int valor_total_medida: float # soma de todas as medidas presentes top5_dominantes: List[CombinacaoCruzamento] combinacoes_ausentes: List[CombinacaoCruzamento] class V6Result(BaseModel): config: ConfigV6 combinacoes: List[CombinacaoCruzamento] # todas as presentes, ordenadas por ranking resumo: ResumoV6 warnings: List[str] errors: List[str] success: bool
Lógica de Processamento

Passo a passo do motor:

Recebe o DataFrame já processado pelo Motor Base (MotorResult)
Valida os campos de entrada (eixo1, eixo2, campo_medida)
Calcula o produto cartesiano: todos os pares possíveis entre
valores únicos de eixo1 × valores únicos de eixo2
Para cada combinação PRESENTE na base, calcula a medida:
CONTAGEM: COUNT(linhas onde eixo1=X e eixo2=Y)
SOMA: SUM(campo_medida onde eixo1=X e eixo2=Y)
MEDIA: AVG(campo_medida onde eixo1=X e eixo2=Y)
Identifica combinações AUSENTES (no cartesiano mas não na base)
Calcula participação percentual de cada combinação presente
sobre o total das combinações presentes (ausentes não entram no denominador)
Ordena por valor_medida DESC para gerar ranking
Classifica cada combinação:
DOMINANTE: combinações que acumulam até limiar_dominante do total
(ex: as combinações que juntas somam os primeiros 20% do total)
RESIDUAL: combinações com participacao_percentual < limiar_residual
RELEVANTE: todas as demais presentes
AUSENTE: combinações do cartesiano sem dados
Desempate no ranking:

Mesmo valor de medida → desempatar por eixo1_valor ASC, depois eixo2_valor ASC
Participação percentual:

Calculada sobre o total das combinações PRESENTES
Combinações AUSENTES têm participacao_percentual = None
Classificação de Dominante — Detalhe

O limiar_dominante (padrão 0.20) define o percentual ACUMULADO do total.
Exemplo com limiar_dominante=0.20 e total=1000:

Ordenar combinações por valor DESC
Acumular valores até atingir 200 (20% de 1000)
Todas as combinações dentro desse acumulado = DOMINANTE
Atenção: se uma única combinação já representa 80%+ do total,
emitir warning W04
Erros e Warnings

Errors (bloqueiam execução):

E01: eixo1 não encontrado no MotorResult
E02: eixo2 não encontrado no MotorResult
E03: eixo1 == eixo2 — mesmo campo nos dois eixos (bloqueado)
E04: campo_medida não encontrado quando tipo_medida != CONTAGEM
E05: campo_medida não é numérico quando tipo_medida == SOMA ou MEDIA
E06: base vazia após filtros
Warnings (não bloqueiam, registrados em warnings[]):

W01: cardinalidade excessiva — eixo1 ou eixo2 com mais de 200 valores
distintos → "Campo '{campo}' tem {n} valores distintos. Matrizes muito
grandes podem prejudicar a leitura."
W02: base trivial — produto cartesiano com menos de 10 combinações possíveis
→ "Apenas {n} combinações possíveis. A análise pode ter valor limitado."
W03: base pequena — menos de 50 registros → "Base com {n} registros.
A classificação de densidade pode ser instável."
W04: concentração extrema — mais de 80% do valor em menos de 3 combinações
→ "Alta concentração: {n} combinações representam mais de 80% do total.
O limiar padrão de Dominante pode não ser adequado."
W05: medida não aditiva — tipo_medida == SOMA em campo que parece ser
percentual ou índice (valores entre 0 e 1 ou entre 0 e 100 com nome
sugestivo) → "Campo '{campo}' pode ser percentual ou índice. Soma pode
não fazer sentido analítico."
Assinatura da Função Principal

def analisar_v6( df: pd.DataFrame, config: ConfigV6 ) -> V6Result: """ Executa a análise de relacionamento entre dimensões (V6). Args: df: DataFrame já processado pelo Motor Base config: configuração da análise (eixos, medida, limiares) Returns: V6Result com combinações classificadas, resumo e warnings/errors """
Decisões de Pendências em Aberto

As seguintes pendências do Blueprint foram resolvidas para esta implementação:

Mesmo campo nos dois eixos → bloquear com E03. Mensagem:
"Eixo 1 e Eixo 2 não podem ser o mesmo campo."

Base pré-agregada com duplicatas na mesma combinação → somar.
O motor trata como base transacional e agrega normalmente.
Emitir W06 se detectar que a base parece pré-agregada mas tem duplicatas:
"Base parece pré-agregada mas contém combinações duplicadas. Os valores
foram somados."

Limite de combinações na visualização → não é responsabilidade do
motor Python. O motor retorna todas as combinações. A interface limita
a exibição. O motor apenas emite W01 quando cardinalidade > 200.

Reordenação da matriz → não é responsabilidade do motor Python.
O motor retorna os dados ordenados por ranking (valor DESC).
A interface gerencia a reordenação visual.

Estrutura de Saída para Excel (referência — não implementar aqui)

Aba 1 — Matriz de Cruzamento: eixo1 nas linhas × eixo2 nas colunas,
valor da medida em cada célula, formatação condicional por classificação
Aba 2 — Ranking de Combinações: lista ordenada de combinações presentes
com valor, participação % e classificação
Aba 3 — Combinações Ausentes: todos os pares do cartesiano sem dados
Aba 4 — Dados Brutos Processados: base original com coluna de classificação
Regras de Sessão

Leia CONTEXT.md e specs/spec_v6.md
Implemente src/visao_v6.py
Não leia outros arquivos
Não implemente exportação Excel — apenas o motor analítico
Entregue o arquivo completo, sem truncar
Use pandas + pydantic (já disponíveis no ambiente)

