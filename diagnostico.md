# Diagnóstico de Problemas - Classificação Taxonômica

Analisei o output do classificador (classificador\_output.tsv) e os
erros encontrados confirmam que o banco de dados original estava
com inconsistências, o que comprometeu a confiança das atribuições.
Abaixo, detalho os principais gargalos identificados:

### Por que tivemos sequências "Unassigned"?

O caso mais crítico foi a seq004. Ela não foi classificada porque
o banco de treino original não seguia o padrão de prefixos (k\_\_, p\_\_).
Como o algoritmo Naive Bayes trabalha com reconhecimento de padrões
de texto associados a k-mers, a falta dessa estrutura impede a
correta identificação, mesmo que a sequência de DNA fosse de alta
qualidade. Outro ponto foi o comprimento: sequências muito curtas
não oferecem informação genética suficiente para um score de
confiança aceitável, gerando ruído estatístico no modelo.

### Problemas de Resolução e Nomenclatura

Notei que gêneros importantes, como Pseudomonas, ficaram travados
em níveis taxonômicos superiores. Isso acontece por dois motivos:
a alta similaridade da região 16S entre espécies próximas e a
presença de duplicatas exatas no banco de referência. Quando o
classificador encontra a mesma sequência para duas espécies
diferentes no treino, a confiança cai e ele trunca a classificação
no nível de Gênero para não cometer um falso-positivo. Além disso,
identifiquei nomes desatualizados (Propionibacterium) que devem
ser corrigidos para manter a consistência com as bases globais.

### 

